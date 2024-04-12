""" This file contains functions for helping our LLM provide structured outputs.
As a guide, start here: https://python.langchain.com/docs/use_cases/query_analysis/quickstart/
"""

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from typing import Optional, List, Dict
import api_utils
import requests

GPT_MODEL = "gpt-3.5-turbo-0613"

class ThingsSearchModel(BaseModel):
    """
    Search over USGS SensorThings Things.
    """

    state: Optional[str] = Field(None, description="The state to search in." \
                                 "These should always be written out fully, no abbreviations." \
                                 "For example, North Carolina.")
    county: Optional[str] = Field(None, description="The county to search in. It should always end with 'County'.")
    active: Optional[bool] = Field(None, description="Whether the thing is active.")
    monitoring_location_type: Optional[str] = Field(None,
                                        description="The type of the thing." \
                                        "It could be 'Well', 'Stream', etc." \
                                        "It always starts with a capital letter.")
    observed_property: Optional[str] = Field(None, description="The observed property required by the filter.")

class ThingsSearchUrl:

    def __init__(self, search_params: ThingsSearchModel):

        self.search_params = search_params
        self.url: str = "https://labs.waterdata.usgs.gov/sta/v1.1/Things"

    def construct_url(self) -> None:
        """
        Construct the final URL.
        """

        and_filters = self.get_and_filter_str()
        observed_property_filters = self.get_observed_property_filter_str()

        if and_filters and observed_property_filters:
            self.url += "?$filter=" + and_filters + " and " + observed_property_filters
        elif and_filters:
            self.url += "?$filter=" + and_filters
        elif observed_property_filters:
            self.url += "?$filter=" + observed_property_filters

        self.add_count()
    
    def get_and_filter_str(self) -> str:
        """
        Retrieve USGS SensorThings Things based on the state, county, active, and monitoring location type search criteria.
        :param search: the search criteria
        :return: a string expressing the mandatory search criteria
        """
        filter_str = ""
        filters = []
        if self.search_params.state:
            filters.append(f"properties/state eq '{self.search_params.state}'")
        if self.search_params.county:
            filters.append(f"properties/county eq '{self.search_params.county}'")
        if self.search_params.active:
            filters.append(f"properties/active eq {self.search_params.active}")
        if self.search_params.monitoring_location_type:
            filters.append(f"properties/monitoringLocationType eq '{self.search_params.monitoring_location_type}'")
        
        if filters:
            filter_str += "(" + " and ".join(filters) + ")"

        return filter_str if filter_str else None
    

    def get_observed_property_id(self) -> Dict[str, str]:
        """
        Get the observed property IDs based on the search parameters.
        :return: a dict of acceptable observed property IDs with their names as values
        """
        if self.search_params.observed_property:
            url = "https://labs.waterdata.usgs.gov/sta/v1.1/ObservedProperties" \
                    f"?$filter=substringof('{self.search_params.observed_property}',name)" \
                    "&$select=@iot.id,name"
            
            id_dict = {}
            response = requests.get(url)
            data = response.json()
            for item in data["value"]:
                id_dict[item["@iot.id"]] = item["name"]
            return id_dict
        return None
    
    def get_observed_property_filter_str(self) -> str:
        """
        Add observed property-based filter to the URL based on the search parameters.
        :return: the filter string
        """
        filter_str = ""
        id_dict = self.get_observed_property_id()
        if not id_dict:
            return None
        
        filters = []
        for id in id_dict.keys():
            filters.append(f"Datastreams/ObservedProperty/@iot.id eq {id}")

        if filters:
            filter_str += "(" + " or ".join(filters) + ")"

        return filter_str if filter_str else None
            
    def add_count(self) -> None:
        """
        Add a count to the URL.
        """
        self.url += "&$count=true"

def query_analysis(query: str) -> ThingsSearchModel:
    """
    Analyze a query to search over USGS SensorThings Things.
    :param query: the query to analyze
    :return: a ThingsSearch object
    """

    system = """You are an expert at converting user questions into USGS SensorThings API queries. \
        Given a question or request, return a list of API queries optimized to retrieve the most relevant data. \
        
        If there are acronyms or words you are not familiar with, do not try to rephrase them.
        """
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}")
        ]
    )

    llm = ChatOpenAI(
        api_key=api_utils.get_openai_key_from_file("openai_key.txt"),
        model=GPT_MODEL,
        temperature=0)

    structured_llm = llm.with_structured_output(ThingsSearchModel)
    query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm
    
    return query_analyzer.invoke(query) 

def generate_url(query: str) -> dict:
    """
    Generate URL to retrieve USGS SensorThings Things based on the query.
    :param query: the query to analyze
    :return: a dictionary with the search results
    """
    system = """You are an expert at converting user questions into USGS SensorThings API queries. \
        Given a question or request, return a list of API queries optimized to retrieve the most relevant data. \
        
        If there are acronyms or words you are not familiar with, do not try to rephrase them.
        """
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "{question}")
        ]
    )

    llm = ChatOpenAI(
        api_key=api_utils.get_openai_key_from_file("openai_key.txt"),
        model=GPT_MODEL,
        temperature=0)

    structured_llm = llm.with_structured_output(ThingsSearchModel)
    query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm
    retrieval_chain = query_analyzer | things_retrieval
    return retrieval_chain.invoke(query)

def generate_summary_from_json(data: dict) -> str:
    """
    Generate a summary from the JSON data using ChatOpenAI.
    :param data: the JSON data
    :return: a summary of the data
    """
    system = """You are an expert at converting USGS SensorThings API responses into summaries. \
        Given a JSON response from the API, return a summary of the data. \
        
        If there are acronyms or words you are not familiar with, do not try to rephrase them.
        """
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("user", "{data}")
        ]
    )

    llm = ChatOpenAI(
        api_key=api_utils.get_openai_key_from_file("openai_key.txt"),
        model=GPT_MODEL,
        temperature=0)
    output_parser = StrOutputParser()

    summary_chain = {"data": RunnablePassthrough()} | prompt | llm | output_parser
    return summary_chain.invoke(data)