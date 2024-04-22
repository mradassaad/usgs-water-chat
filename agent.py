# Defines the LLM agent

from query_analysis import ThingsSearchModel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

GPT_MODEL = "gpt-3.5-turbo-0613"


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