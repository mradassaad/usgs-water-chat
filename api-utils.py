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



