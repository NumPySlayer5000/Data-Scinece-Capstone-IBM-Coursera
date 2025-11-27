# Import required libraries
import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Precompute dropdown options
launch_sites = spacex_df['Launch Site'].unique().tolist()
site_options = [{'label': 'All Sites', 'value': 'ALL'}] + [
    {'label': site, 'value': site} for site in launch_sites
]

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=site_options,
        value='ALL',                 # default value
        placeholder='Select a Launch Site here',
        searchable=True
    ),

    html.Br(),

    # TASK 2: Pie chart
    html.Div(
        dcc.Graph(id='success-pie-chart')
    ),

    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: Add RangeSlider
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 2000)},
        value=[min_payload, max_payload]
    ),

    html.Br(),

    # TASK 4: Scatter chart
    html.Div(
        dcc.Graph(id='success-payload-scatter-chart')
    ),
])

# TASK 2:
# Callback for pie chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):

    filtered_df = spacex_df

    # If ALL sites selected: show total success launches by site
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',
            names='Launch Site',
            title='Total Success Launches by Site'
        )
        return fig

    # If specific site selected: show success vs failed counts
    else:
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(
            site_df,
            names='class',
            title=f'Total Success vs Failure for site {entered_site}'
        )
        return fig


# TASK 4:
# Callback for scatter plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_scatter_plot(entered_site, slider_range):

    low, high = slider_range
    df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) &
                   (spacex_df['Payload Mass (kg)'] <= high)]

    # If ALL sites chosen: use all filtered data
    if entered_site == 'ALL':
        fig = px.scatter(
            df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title='Correlation between Payload and Success for All Sites'
        )
        return fig

    # If specific site chosen: filter then plot
    else:
        site_df = df[df['Launch Site'] == entered_site]
        fig = px.scatter(
            site_df,
            x='Payload Mass (kg)',
            y='class',
            color='Booster Version Category',
            title=f'Correlation between Payload and Success for site {entered_site}'
        )
        return fig


# Run the app
if __name__ == '__main__':
    app.run(port=8050)