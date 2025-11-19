from openai import OpenAI
import json
from tools import tools, get_lucky_number, get_weather # My Tools package 

client = OpenAI()


# First call: Ask the model to use the tool 

context = [
    {
        "role": "user",
        "content":"Plese call get_weather and tell me the result"
        
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

#there are not arugments on this one, this is probably not needed but normally would be? 

#args = json.loads(function_call.arguments)

#Run the local function 
print(item.name)

if item.name == "get_lucky_number":
    tool_result = get_lucky_number()
    
elif item.name == "get_weather":
    tool_result = get_weather()

#So, adding the llm response to the context  (this could happen above right?)
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




