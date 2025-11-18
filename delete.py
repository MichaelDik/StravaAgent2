from openai import OpenAI
import json

client = OpenAI()


def get_lucky_number():
    return 42


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
    }
]


# First call: Ask the model to use the tool 

context = [
    {
        "role": "user",
        "content":"Plese call get_lucky_number and tell me the result"
        
    }
]

response = client.responses.create(
    model="o4-mini",
    input=context, 
    tools=tools
    
)

print("first response output (Should include a function calll): ")
print(response.output)

#find the Function call in response.output 
function_call = None 
for item in response.output: 
    #look for the first item whose type is "function_call"
    if item.type == "function_call":
        function_call = item 
        break 

if function_call is None: 
    raise RuntimeError("Model did not call a function")

#there are not arugments on this one, this is probably not needed but normally would be? 
args = json.loads(function_call.arguments)

#Run the local function 
tool_result = get_lucky_number()

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




