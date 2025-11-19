def get_activities():
    return 42
def get_weather():
    return "Weather is fantastic!"

tools = [
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
        "name": "get_weather",
        "description": "Return a hardcoded weather temperature",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
   
   
]
