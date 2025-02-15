import plotly.graph_objects as go

create_scatter_chart_schema = {
    "type": "function",
    "function": {
        "name": "create_scatter_chart",
        "description": "Create a scatter chart with optional background and color palette.",
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
                    "description": "List of colors for the points.",
                    "nullable": True
                }
            },
            "required": ["x_column", "y_column", "background_image", "palette"],
            "additionalProperties": False
        },
        "strict": True
    }
}

def create_scatter_chart(data, x_column, y_column, background_image=None, palette=None):
    """
    Create a scatter chart with optional background and color palette.
    
    Parameters:
    - data: DataFrame with columns for x and y values
    - x_column: Column name for the x-variable
    - y_column: Column name for the y-variable
    - background_image: URL or file path of the background image
    - palette: List of colors for the points
    """
    fig = go.Figure()
    
    # Assign colors
    colors = palette if palette else ['blue'] * len(data[x_column])
    
    # Add scatter points
    fig.add_trace(go.Scatter(x=data[x_column], y=data[y_column], mode='markers', marker=dict(color=colors, size=10)))
    
    # Add background image
    if background_image:
        fig.update_layout(images=[dict(source=background_image, x=0, y=1, xref='paper', yref='paper', sizex=1, sizey=1, xanchor='left', yanchor='top', layer='below')])
    
    return fig