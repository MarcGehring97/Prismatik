from openai import OpenAI
import plotly.graph_objects as go
import pandas as pd
import requests
import json

from tools.get_entity_logo import get_entity_logo_schema, get_entity_logo
from tools.get_person_image import get_person_image_schema, get_person_image 
from tools.create_bar_chart import create_bar_chart_schema, create_bar_chart
from tools.create_line_chart import create_line_chart_schema, create_line_chart
from tools.create_scatter_chart import create_scatter_chart_schema, create_scatter_chart

# Functions dictionary
functions = {
    "get_entity_logo": get_entity_logo,
    "get_person_image": get_person_image,
    "create_bar_chart": create_bar_chart,
    "create_line_chart": create_line_chart,
    "create_scatter_chart": create_scatter_chart
}

# Load the dataset
file_path = "/Users/marc/Desktop/Applications/Accenture/Churn.csv"
df = pd.read_csv(file_path)
columns = df.columns.tolist()
# summary = df.describe().to_dict()

# Initialize the OpenAI client
client = OpenAI()

# Define the tools to be used
tools = [
    # get_entity_logo_schema,
    # get_person_image_schema, 
    create_bar_chart_schema, 
    create_line_chart_schema, 
    create_scatter_chart_schema
]

"""
stream = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a data analysis assistant."},
        {"role": "user", "content": f"Here is a dataset with columns {columns}. Suggest useful plots."}
    ],
    tools=tools,
    stream=True
)

final_tool_calls = {}

for chunk in stream:
    for tool_call in chunk.choices[0].delta.tool_calls or []:
        index = tool_call.index

        print(tool_call)

        if index not in final_tool_calls:
            final_tool_calls[index] = tool_call

        final_tool_calls[index].function.arguments += tool_call.function.arguments

print(final_tool_calls)

for tool_call in final_tool_calls.values():
    args = json.loads(tool_call.function.arguments)
"""

messages=[
    {"role": "system", "content": "You are a data analysis assistant."},
    {"role": "user", "content": f"Here is a dataset with columns {columns}. Pick any of the available tools to make insightful plots. We don't need a background image or color palette for this task. Use the tools at your disposal to generate the plot(s) and explain your reasoning."}
]

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

choice = completion.choices[0]

if choice.finish_reason == "tool_calls":
    # Print the message
    print("Message:", choice.message.content)
    for call in choice.message.tool_calls:
        function_name = call.function.name
        function_args = json.loads(call.function.arguments)

        fig = functions[function_name](df, **function_args)

        fig.show()

        print("Function output:", fig)