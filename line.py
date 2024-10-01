import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)

app = Dash(__name__)

# -- Import and clean data (importing csv into pandas)
#df = pd.read_csv("Dataset/intro_bees.csv")
df = pd.read_csv("C:/Users/user/Desktop/BIG DATA/Data Science/Classwork projects/intro_bees.csv")

df = df.groupby(['State', 'ANSI', 'Affected by', 'Year', 'state_code'])[['Pct of Colonies Impacted']].mean()
df.reset_index(inplace=True)
print(df[:5])

bee_killers = ["Disease", "Other", "Pesticides", "Pests_excl_Varroa", "Unknown", "Varroa_mites"]



# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([

    html.H1("Web application Dashboard with Dash", style={'text-align': 'center'}),

    dcc.Dropdown(id="slct_impact",
                 options=[
                     {"label": x,"value":x} for x in bee_killers],
                 multi=False,
                 value="Pesticides",
                 style={'width': "40%"}
                 ),

    html.Div(id='output_container', children=[]),
    html.Br(),

    dcc.Graph(id='my_bee_map', figure={})

])


# ------------------------------------------------------------------------------

# Connect the Plotly graphs with Dash Components
@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_bee_map', component_property='figure')],
    [Input(component_id='slct_impact', component_property='value')]
)
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = "The year chosen by user was: {}".format(option_slctd)

    dff = df.copy()
    dff = dff[dff["Affected by"] == option_slctd]
    dff = dff[(dff["State"] == "Idaho") | (dff["State"]== "New York") | (dff["State"]== "New Mexico")]

    # Plotly Express
    fig = px.line(
        data_frame=dff,
        x='Year', y='Pct of Colonies Impacted',
        color='State',
        template='plotly_dark'
    )

    # Plotly Graph Objects (GO)
    # fig = go.Figure(
    #     data=[go.Choropleth(
    #         locationmode='USA-states',
    #         locations=dff['state_code'],
    #         z=dff["Pct of Colonies Impacted"].astype(float),
    #         colorscale='Reds',
    #     )]
    # )
    #
    # fig.update_layout(
    #     title_text="Bees Affected by Mites in the USA",
    #     title_xanchor="center",
    #     title_font=dict(size=24),
    #     title_x=0.5,
    #     geo=dict(scope='usa'),
    # )

    return container, fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True)
    