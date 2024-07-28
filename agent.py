# Defines the LLM agent

from api_utils import get_openai_key_from_file
from query_analysis import ThingsSearchModel, generate_url
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.output_parsers import StrOutputParser
from langchain.agents.format_scratchpad.openai_tools import (
    format_to_openai_tool_messages,
)
from langchain.agents.output_parsers.openai_tools import OpenAIToolsAgentOutputParser
import os

GPT_MODEL = "gpt-3.5-turbo-0613"

def create_agent_executor():
    """Initializes langchain OpenAI agent executor with llm bound to tools defined in query_analysis:
    - generate_url
    """

    llm = ChatOpenAI(
        api_key=get_openai_key_from_file("openai_key.txt"),
        model=GPT_MODEL,
        temperature=0
        )
    
    tools = [generate_url]

    prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an expert at converting user questions into USGS SensorThings API queries." \
            "Given a question or request, return a list of API queries optimized to retrieve the most relevant data." \
            "If there are acronyms or words you are not familiar with, do not try to rephrase them."
        ),
        ("user", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
    )

    llm_with_tools = llm.bind_tools(tools)

    agent = (
    {
        "input": lambda x: x["input"],
        "agent_scratchpad": lambda x: format_to_openai_tool_messages(
            x["intermediate_steps"]
        ),
    }
    | prompt
    | llm_with_tools
    | OpenAIToolsAgentOutputParser()
    )


    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

    return agent_executor


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
        api_key=get_openai_key_from_file("openai_key.txt"),
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
        api_key=get_openai_key_from_file("openai_key.txt"),
        model=GPT_MODEL,
        temperature=0)
    output_parser = StrOutputParser()

    summary_chain = {"data": RunnablePassthrough()} | prompt | llm | output_parser
    return summary_chain.invoke(data)