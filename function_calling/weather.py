from openai import OpenAI
import os
from typing import Literal

client = OpenAI(api_key="<your-api-key>")

def get_current_weather(location: str, unit: Literal["celsius", "fahrenheit"] = "celsius") -> str:
    """Get the current weather in a given location"""
    # In a real scenario, you would call a weather API here
    return f"The current weather in {location} is 22 degrees {unit}"

# Define the function
functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather in a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
            },
            "required": ["location"],
        },
    }
]

city = input("Enter the city to fetch weather info : ")

# Make the API call
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": f"What's the weather like in {city}. Give it to me in f?"}],
    functions=functions,
    function_call="auto",
)

# Check if the model wants to call a function
message = response.choices[0].message

if message.function_call:
    function_name = message.function_call.name
    function_args = message.function_call.arguments

    # Call the function
    if function_name == "get_current_weather":
        weather = get_current_weather(**eval(function_args))
        # print(weather)

        # You can then send this result back to the model if needed
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": f"What's the weather like in {city}?"},
                message,
                {
                    "role": "function",
                    "name": "get_current_weather",
                    "content": weather,
                },
            ],
        )
        print(final_response.choices[0].message.content)
else:
    print(message.content)