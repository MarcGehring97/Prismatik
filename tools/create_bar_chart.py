import plotly.graph_objects as go

create_bar_chart_schema = {
    "type": "function",
    "function": {
        "name": "create_bar_chart",
        "description": "Create a bar chart for specified categories and values column with optional background and color palette.",
        "strict": True,
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "description": "Data for the chart.",
                    "additionalProperties": False
                },
                "categories_column": {
                    "type": "string",
                    "description": "Column name for the categories."
                },
                "values_column": {
                    "type": "string",
                    "description": "Column name for the values."
                },
                "background_image": {
                    "type": "string",
                    "description": "URL or file path of the background image.",
                    "nullable": True
                },
                "palette": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of colors for the bars.",
                    "nullable": True
                }
            },
            "required": ["categories_column", "values_column", "background_image", "palette"],
            "additionalProperties": False
        }
    }
}

def create_bar_chart(data, categories_column, values_column, background_image=None, palette=None):
    """
    Create a bar chart with optional background and color palette.
    
    Parameters:
    - data: DataFrame with columns for categories and values
    - categories_column: Column name for the categories
    - values_column: Column name for the values
    - background_image: URL or file path of the background image
    - palette: List of colors for the bars
    """
    fig = go.Figure()
    
    # Assign colors
    colors = palette if palette else ['blue'] * len(data[values_column])
    
    # Add bars
    fig.add_trace(go.Bar(x=data[categories_column], y=data[values_column], marker_color=colors))
    
    # Add background image
    if background_image:
        fig.update_layout(images=[dict(source=background_image, x=0, y=1, xref='paper', yref='paper', sizex=1, sizey=1, xanchor='left', yanchor='top', layer='below')])
    
    return fig