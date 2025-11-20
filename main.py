# main.py
import json

from openai import OpenAI
from Tools import get_date, get_activities,get_nyc_weather, tools

# Prompts: What is the weather?
# What is my mileage of the last 7 days 

client = OpenAI()


# First call: Ask the model to use the tool 
prompt = input("Please input your prompt: ")

context = [
    {
        "role": "user",
        "content":f"Pleasse call {prompt} and tell me the result"
        
    }
]

response = client.responses.create(
    model="o4-mini",
    input=context, 
    tools=tools
    
)

#print("first response output (Should include a function calll): ")
#print(response.output)

#find the Function call in response.output 
function_call = None 
for item in response.output:
    # Look for the first item whose type is "function_call"
    if item.type == "function_call":
        function_call = item
        break


if function_call is None:
    raise RuntimeError("Model did not call any function")


#Run the local function and add output to tool_result
print(f"Tool Called name is: {item.name}")

if item.name == "get_date":
    tool_result = get_date()
    
elif item.name == "get_activities":
    tool_result = get_activities()
elif item.name =="get_nyc_weather":
    tool_result= get_nyc_weather()

#Adding the llm response to the context  (this could happen above right?)
context += response.output 

#Add the functon_call_output with the results 
context.append ({
        "type":"function_call_output",
        "call_id": function_call.call_id, 
        "output": str(tool_result)
    })

response2 = client.responses.create(
    model="o4-mini",
    input=context, 
    tools=tools,
)

print("\n Final Answer from the model: ")
print(response2.output_text)



