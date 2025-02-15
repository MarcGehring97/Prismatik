from openai import OpenAI
import json

# OpenAI client setup (replace with your API key)
client = OpenAI()

# Define available functions
def get_weather(city):
    return {"city": city, "temperature": "15°C", "condition": "Cloudy"}

def get_time(city):
    return {"city": city, "time": "14:30"}

# Define function descriptions
functions = [
    {
        "name": "get_weather",
        "description": "Get the current weather for a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The name of the city"},
            },
            "required": ["city"],
        },
    },
    {
        "name": "get_time",
        "description": "Get the current time in a city.",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string", "description": "The name of the city"},
            },
            "required": ["city"],
        },
    },
]

# User query
user_message = "What's the weather like in Berlin?"

# Call OpenAI API
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": user_message}],
    tools=functions,
    tool_choice="auto"
)

# Check if the model wants to call a function
if response.choices[0].message.tool_calls:
    tool_call = response.choices[0].message.tool_calls[0]
    function_name = tool_call.function.name
    function_args = json.loads(tool_call.function.arguments)

    # Call the appropriate function
    if function_name == "get_weather":
        result = get_weather(**function_args)
    elif function_name == "get_time":
        result = get_time(**function_args)

    print("Function output:", result)
