# main.py
import json

from openai import OpenAI
from Tools import get_date, get_activities,get_nyc_weather, run_tools, tools

# Prompts: What is the weather?
# What is my mileage of the last 7 days 

client = OpenAI()


#Loop to prompt the user for tool calls, will loop until a tool is selected  
function_call = None 
while function_call == None:
    
    # Set Prompt from User
    prompt = input("Please input your prompt: ")    
    
    #Set Context
    
    context = [
    {
        "role": "user",
        "content":f"Please call {prompt} and tell me the result"
        
    }
    ]
    
    # Call LLM
    response = client.responses.create(
    model="o4-mini",
    input=context, 
    tools=tools
    )
    
    for item in response.output:
        # Look for the first item whose type is "function_call"
        if item.type == "function_call":
            function_call = item
            break

    # No Tool was selected 
    if function_call is None:
        print ("Im sorry, I can only call three tools right now: please tell mew if you want Weather, Activites or Date: ")
        


conversationEnded = None


#Print name of Tool
print(f"Tool Called name is: {item.name}")

#Call the function to run the tools
tool_result = run_tools(item.name)

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

while conversationEnded != 'q':

    conversationEnded = input("\n Is there anything else you would like me to do? (hit q to exit) ") 
    
    




