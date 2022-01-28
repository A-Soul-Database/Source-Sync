import requests
import os
import json
from PhotoSearch.oped import main as oped

Config = {
    "Sources":["Jiabu","Naifen","Ofiicial"]
}

# Detect Sources 
if requests.get("http://localhost:4399/ping").status_code != 200 and requests.get("http://localhost:4400/ping").status_code != 200:
    os._exit(128)

# AnalySis