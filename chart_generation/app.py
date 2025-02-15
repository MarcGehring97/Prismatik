import vizro.plotly.express as px
from vizro_ai import VizroAI

df = px.data.gapminder()

vizro_ai = VizroAI(model="gpt-4o-mini")
fig = vizro_ai.plot(
    df,
    """create a line graph for GDP per capita since 1950 for each continent.
    Mark the x axis as Year, y axis as GDP Per Cap and don't include a title.
    Make sure to take average over continent."""
)

fig.show()

"""
print(res)

print("Blank line\n\n\n")

print(res.code)
print(res.chart_insights)
print(res.code_explanation)
"""

# Render the plot
# res.show()