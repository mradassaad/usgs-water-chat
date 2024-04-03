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

def get_thing_data(thing_id: str):
    """
    Get the data for a specific station between the start and end dates.
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