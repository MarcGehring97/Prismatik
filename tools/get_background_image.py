import os
import requests

get_background_image_schema = {
    "type": "function",
    "function": {
        "name": "get_background_image",
        "description": "Fetch images from the Unsplash API using a search query.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search keyword for finding relevant images."
                },
                "per_page": {
                    "type": "integer",
                    "description": "The number of images to fetch (maximum 30).",
                },
                "api_key": {
                    "type": "string",
                    "description": "Unsplash API key. If not provided, the function will look for an environment variable UNSPLASH_API_KEY.",
                    "nullable": True
                }
            },
            "required": ["query", "per_page", "api_key"],
            "additionalProperties": False
        }
    }
}

def get_background_image(query, per_page=1, api_key=None):
    """
    Fetch images from the Unsplash API using a search query.

    Parameters:
    - query (str): The search keyword.
    - per_page (int): Number of images to fetch (max 30).
    - api_key (str): Unsplash API key (if not set as an environment variable).

    Returns:
    - list: A list of image URLs.
    """

    # Use the API key from environment variables if not provided
    if api_key is None:
        api_key = os.getenv("UNSPLASH_API_KEY")

    if not api_key:
        raise ValueError("Unsplash API key is required. Set it as an env variable or pass it as an argument.")

    url = "https://api.unsplash.com/search/photos"
    headers = {"Authorization": f"Client-ID {api_key}"}
    params = {
        "query": query,
        "per_page": per_page,
        "orientation": "landscape"  # You can change this to 'portrait' or 'squarish'
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if per_page == 1:
            return data["results"][0]["urls"]["regular"]
        else:
            return [photo["urls"]["regular"] for photo in data["results"]]
    else:
        raise Exception(f"Error {response.status_code}: {response.json()}")
