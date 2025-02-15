import plotly.graph_objects as go

create_line_chart_schema = {
    "type": "function",
    "function": {
        "name": "create_line_chart",
        "description": "Create a line chart with optional background and color palette.",
        "parameters": {
            "type": "object",
            "properties": {
                "data": {
                    "type": "object",
                    "description": "Data for the chart.",
                    "additionalProperties": False
                },
                "x_column": {
                    "type": "string",
                    "description": "Column name for the x-variable."
                },
                "y_column": {
                    "type": "string",
                    "description": "Column name for the y-variable."
                },
                "background_image": {
                    "type": "string",
                    "description": "URL or file path of the background image.",
                    "nullable": True
                },
                "palette": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of colors for the lines.",
                    "nullable": True
                }
            },
            "required": ["x_column", "y_column", "background_image", "palette"],
            "additionalProperties": False
        },
        "strict": True
    }
}

def create_line_chart(data, x_column, y_column, background_image=None, palette=None):
    """
    Create a line chart with optional background and color palette.
    
    Parameters:
    - data: DataFrame with columns for x and y values
    - x_column: Column name for the x-variable
    - y_column: Column name for the y-variable
    - background_image: URL or file path of the background image
    - palette: List of colors for the lines
    """
    fig = go.Figure()
    
    # Assign colors
    colors = palette if palette else ['blue', 'red', 'green', 'purple']
    
    # Add lines
    for i, (label, y_values) in enumerate(data[y_column].items()):
        fig.add_trace(go.Scatter(x=data[x_column], y=y_values, mode='lines+markers', name=label, line=dict(color=colors[i % len(colors)])))
    
    # Add background image
    if background_image:
        fig.update_layout(images=[dict(source=background_image, x=0, y=1, xref='paper', yref='paper', sizex=1, sizey=1, xanchor='left', yanchor='top', layer='below')])
    
    return fig