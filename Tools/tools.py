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
        "description": "When asked what the date is use this tool ",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    
    {
        "type": "function",
        "name": "get_activities",
        "description": "When asked for recent running activiteis use this tool",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    
     {
        "type": "function",
        "name": "get_nyc_weather",
        "description": "When asked about the weather use this tool",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]

def run_tools(tool_name):
    if tool_name == "get_date":
        return get_date()
    elif tool_name == "get_activities":
        return get_activities()
    elif tool_name =="get_nyc_weather":
        return get_nyc_weather()