from openai import OpenAI 
import os
from dotenv import load_dotenv
import json

load_dotenv()

client = OpenAI()

def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with 25°C."

# Step 1: Ask the model
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's the weather in Paris?"}
    ],
    tools=[
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get weather info for a city",
                "parameters": {
                    "type": "object",
                    "properties": {"city": {"type": "string"}},
                    "required": ["city"]
                }
            }
        }
    ]
)

tool_call = response.choices[0].message.tool_calls
if tool_call:
    # Step 2: Extract the tool call details
    fn_name = tool_call[0].function.name
    args = json.loads(tool_call[0].function.arguments)

    # Step 3: Execute the function in Python
    if fn_name == "get_weather":
        result = get_weather(**args)
        print("Function Result:", result)

        # Step 4: Send the result back to the model (optional, for natural language output)
        followup = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's the weather in Paris?"},
                response.choices[0].message,  # model's tool call
                {"role": "tool", "tool_call_id": tool_call[0].id, "content": result}
            ]
        )
        print("AI:", followup.choices[0].message.content)
