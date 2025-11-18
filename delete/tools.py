def get_lucky_number():
    return 42
def get_weather():
    return "Weather is fantastic!"

tools = [
    {
        "type": "function",
        "name": "get_lucky_number",
        "description": "Return a hardcoded lucky number",
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
