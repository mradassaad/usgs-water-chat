"""
    This file contains utility functions for accessing the USGS water data web APIs: https://waterdata.usgs.gov/blog/api_catalog/.
    Speficially, we will be using the following APIs:
    - https://labs.waterdata.usgs.gov/sta/v1.1/
"""
import requests
import json
import pandas as pd
import numpy as np
from datetime import datetime
from tenacity import retry, wait_random_exponential, stop_after_attempt
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool, StructuredTool, tool
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI

GPT_MODEL = "gpt-3.5-turbo-0613"

@retry(wait=wait_random_exponential(multiplier=1, max=40), stop=stop_after_attempt(3))
def chat_completion_request(client, messages, tools=None, tool_choice=None, model=GPT_MODEL):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice=tool_choice,
        )
        return response
    except Exception as e:
        print("Unable to generate ChatCompletion response")
        print(f"Exception: {e}")
        return e

@tool
def query_usgs_sensorthings_api(url: str):
    """
    Query the USGS SensorThings API. 
    :param url: the URL to query
    :return: the response from the API
    """
    print(f"[INFO] Querying USGS SensorThings API at {url}")
    response = requests.get(url)
    return response

@tool
def get_thing_data(thing_id: str) -> dict:
    """
    Get the data for a specific USGS thing using the `thing_id`.
    :param thing_id: the thing id
    :return: a pandas dataframe with the data
    """
    url = f"https://labs.waterdata.usgs.gov/sta/v1.1/Things('{thing_id}')"
    print(f"[INFO] Getting data for thing {thing_id} from {url}")
    response = requests.get(url)
    data = response.json()
    # df = pd.DataFrame(data['value']['timeSeries'][0]['values'][0]['value'])
    # df['dateTime'] = pd.to_datetime(df['dateTime'])
    # df['value'] = pd.to_numeric(df['value'])
    return data

def get_openai_key_from_file(file: str) -> str:
    """
    Get the OpenAI API key from the file.
    :return: the OpenAI API key
    """
    with open(file, 'r') as f:
        key = f.read()
    return key