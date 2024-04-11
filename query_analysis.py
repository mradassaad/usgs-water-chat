""" This file contains functions for helping our LLM provide structured outputs.
As a guide, start here: https://python.langchain.com/docs/use_cases/query_analysis/quickstart/
"""

from langchain.pydantic_v1 import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from typing import Optional
import api_utils
import requests

GPT_MODEL = "gpt-3.5-turbo-0613"

class ThingsSearch(BaseModel):
    """
    Search over USGS SensorThings Things.
    """

    state: Optional[str] = Field(None, description="The state to search in.")
    county: Optional[str] = Field(None, description="The county to search in. It should always end with 'County'.")
    active: Optional[bool] = Field(None, description="Whether the thing is active.")
    monitoring_location_type: Optional[str] = Field(None,
                                        description="The type of the thing. It could be 'Well', 'Stream', etc. It always starts with a capital letter.")
    
def things_retrieval(search: ThingsSearch) -> dict:
    """
    Retrieve USGS SensorThings Things based on the search criteria.
    :param search: the search criteria
    :return: a dictionary with the search results
    """
    url = "https://labs.waterdata.usgs.gov/sta/v1.1/Things"
    filters = []
    if search.state:
        filters.append(f"properties/state eq '{search.state}'")
    if search.county:
        filters.append(f"properties/county eq '{search.county}'")
    if search.active:
        filters.append(f"properties/active eq {search.active}")
    if search.monitoring_location_type:
        filters.append(f"properties/monitoringLocationType eq '{search.monitoring_location_type}'")
    
    if filters:
        url += "?$filter=" + " and ".join(filters)

    response = requests.get(url)
    print(url)
    return response.json()


def retrieval(query: str) -> dict:
    """
    Retrieve USGS SensorThings Things based on the query.
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

    structured_llm = llm.with_structured_output(ThingsSearch)
    query_analyzer = {"question": RunnablePassthrough()} | prompt | structured_llm
    retrieval_chain = query_analyzer | things_retrieval
    return retrieval_chain.invoke(query)