from openai import OpenAI
import pandas as pd
import json
 
# Import the schemas and functions
from tools.get_entity_logo import get_entity_logo_schema, get_entity_logo
from tools.get_person_image import get_person_image_schema, get_person_image 
from tools.get_background_image import get_background_image_schema, get_background_image
from tools.create_bar_chart import create_bar_chart_schema, create_bar_chart
from tools.create_line_chart import create_line_chart_schema, create_line_chart
from tools.create_scatter_chart import create_scatter_chart_schema, create_scatter_chart
from tools.image_validation import is_image_suitable

# Functions mapping
functions_mapping = {
    "get_entity_logo": get_entity_logo,
    "get_person_image": get_person_image,
    "get_background_image": get_background_image,
    "create_bar_chart": create_bar_chart,
    "create_line_chart": create_line_chart,
    "create_scatter_chart": create_scatter_chart
}

# Load the dataset
file_path = "/Users/marc/Desktop/Applications/Accenture/Churn.csv"
df = pd.read_csv(file_path, sep=";")
columns = df.columns.tolist()

# Calculate summary statistics
summary = df.describe().to_dict()

# Define the context description of the dataset
context_description = """
The dataset used in the case study pertains to customer churn prediction for a large German insurance company. 
It includes various customer attributes to help build a predictive model. The target variable, churn, indicates 
whether a customer has left the insurance (1=churn). The dataset contains demographic and financial features 
such as credit_score, country, sex, birthdate, tenure, account_balance, number_of_products, has_health_insurance, 
has_life_insurance, salary_estimated, and monthly_fees. These features provide insights into customer behavior and 
financial standing, aiding in churn prediction.
"""

# Initialize the OpenAI client
client = OpenAI()

# Define the tools to be used
tools = [
    # get_entity_logo_schema,
    # get_person_image_schema, 
    get_background_image_schema,
    create_bar_chart_schema, 
    create_line_chart_schema, 
    create_scatter_chart_schema
]

# Define the messages
messages = [
    {"role": "system", "content": "You are a data analysis assistant."},
    {"role": "user", "content": f"""
     Here is a dataset with columns {columns}. The context description of the dataset is: {context_description}.
     The summary statistics of the dataset are: {json.dumps(summary, indent=2)}.
     Pick any of the available tools to make one insightful plot. Also fetch an image from Unsplash API using a suitably detailed query.
     We don't need a color palette for this task. Use the tools at your disposal to generate the plot and explain your reasoning.
     """
     }
]

# Define the function to check if the image is suitable
def is_image_suitable(image_url):
    # Implement your logic to check if the image is suitable
    # For example, you can use image recognition or metadata analysis
    # Here, we will just return True for simplicity
    return True

# Call the completions endpoint
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages,
    tools=tools
)

# Select the choice
choice = completion.choices[0]

# Initialize the background image URL
background_image_url = None

if choice.finish_reason == "tool_calls":
    # Print the message
    print("Message:", choice.message.content)
    for call in choice.message.tool_calls:
        function_name = call.function.name
        function_args = json.loads(call.function.arguments)

        # Check if the function is get_background_image and fetch the image
        if function_name == "get_background_image":
            print("Query:", function_args["query"])
            background_image_url = functions_mapping[function_name](**function_args)
            
            # Validate the background image
            if not is_image_suitable(background_image_url):
                print("The background image is not suitable.")
                continue
            
            continue

        # Add the background image URL to the function arguments
        function_args["background_image"] = background_image_url

        # Call the function with the arguments and get the plot
        fig = functions_mapping[function_name](df, **function_args)

        fig.show()