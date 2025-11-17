
name ="bob"

def handle_tool_call(name:str, arguments: dict) -> str: 
    "Route tool calls from the model to python functions"
    if name =="add_numbers": 
        return add_numbers(arguments)
    
      # If you add more tools later, extend this if/elif block:
    # elif name == "other_tool":
    #     return other_tool(arguments)

    raise ValueError(f"Unkown tool: {name}")

handle_tool_call(name)