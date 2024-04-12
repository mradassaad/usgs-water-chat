"""
Defines the Flask application instance.
"""

from flask import Flask
import query_analysis

app = Flask(__name__)

@app.route('/')
def landing():
    return "Welcome to the USGS SensorThings ChatBot!"

@app.route('/generate_url/<string:query>')
def generate_url(query):
    return query_analysis.generate_url(query)