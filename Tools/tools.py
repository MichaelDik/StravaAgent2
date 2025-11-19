from datetime import date

from .Weather.nyc_weather import get_nyc_weather


def get_date():
    return date.today()

def get_activities():
    return "Activities"

tools = [
    {
        "type": "function",
        "name": "get_date",
        "description": "get_date",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    
    {
        "type": "function",
        "name": "get_activities",
        "description": "get_activities",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    
     {
        "type": "function",
        "name": "get_nyc_weather",
        "description": "get_nyc_weather",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]
