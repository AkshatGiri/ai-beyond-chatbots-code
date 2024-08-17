from openai import OpenAI
import os
from typing import Literal, Union

client = OpenAI(api_key="<your-api-key>")

def add(a: float, b: float) -> float:
    return a + b

def subtract(a: float, b: float) -> float:
    return a - b

def multiply(a: float, b: float) -> float:
    return a * b

def divide(a: float, b: float) -> Union[float, str]:
    if b == 0:
        return "Error: Division by zero"
    return a / b

# Define the functions
functions = [
    {
        "name": "add",
        "description": "Add two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number"},
                "b": {"type": "number", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
    {
        "name": "subtract",
        "description": "Subtract the second number from the first",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number"},
                "b": {"type": "number", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
    {
        "name": "multiply",
        "description": "Multiply two numbers",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number"},
                "b": {"type": "number", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
    {
        "name": "divide",
        "description": "Divide the first number by the second",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {"type": "number", "description": "The first number"},
                "b": {"type": "number", "description": "The second number"},
            },
            "required": ["a", "b"],
        },
    },
]

def process_calculation(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": user_input}],
        functions=functions,
        function_call="auto",
    )

    message = response.choices[0].message

    if message.function_call:
        function_name = message.function_call.name
        function_args = eval(message.function_call.arguments)
        
        result = globals()[function_name](**function_args)
        
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_input},
                message,
                {
                    "role": "function",
                    "name": function_name,
                    "content": str(result),
                },
            ],
        )
        return final_response.choices[0].message.content
    else:
        return message.content

# Example usage
user_queries = [
  input("Enter a calculation:")
]
# user_queries = [
#     "What's 15 plus 27?",
#     "Can you subtract 8 from 23?",
#     "Multiply 6 by 4 please.",
#     "Divide 15 by 3 for me.",
#     "What's 10 divided by 0?",
# ]

for query in user_queries:
    print(f"Query: {query}")
    print(f"Response: {process_calculation(query)}\n")