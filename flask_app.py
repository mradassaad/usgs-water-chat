"""
Defines the Flask application instance.
"""

from flask import Flask
import agent
import os


app = Flask(__name__)

agent_executor = agent.create_agent_executor()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_URL"] = "https://api.smith.langcahin.com"
os.environ["LANGCHAIN_PROJECT"] = "usgs-water-chat"
os.environ["LANGCHAIN_API_KEY"] = input("Please enter your LANGCHAIN_API_KEY: ")

@app.route('/')
def landing():
    return "Welcome to the USGS SensorThings ChatBot!"

@app.route('/invoke/generate_url/<string:query>')
def generate_url(query):
    return agent_executor.invoke({"input": query})
