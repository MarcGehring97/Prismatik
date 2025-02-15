get_entity_logo_schema = {
    "type": "function",
    "function": {
        "name": "get_entity_logo",
        "description": "Retrieve the logo of a given company, political party, or entity.",
        "parameters": {
            "type": "object",
            "properties": {
                "entity_name": {
                    "type": "string",
                    "description": "The name of the company, political party, or entity (e.g., 'Google', 'Democratic Party')."
                },
                "entity_type": {
                    "type": "string",
                    "description": "The type of entity (e.g., 'company', 'political party')."
                }
            },
            "required": ["entity_name", "entity_type"],
            "additionalProperties": False
        },
        "strict": True
    }
}

def get_entity_logo():
    pass