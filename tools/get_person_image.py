get_person_image_schema = {
    "type": "function",
    "function": {
        "name": "get_person_image",
        "description": "Retrieve an image of a person of interest, such as a politician or public figure.",
        "parameters": {
            "type": "object",
            "properties": {
                "person_name": {
                    "type": "string",
                    "description": "The name of the person of interest (e.g., 'Angela Merkel', 'Barack Obama')."
                },
                "person_type": {
                    "type": "string",
                    "description": "The type of person (e.g., 'politician', 'celebrity')."
                }
            },
            "required": ["person_name", "person_type"],
            "additionalProperties": False
        },
        "strict": True
    }
}

def get_person_image():
    pass