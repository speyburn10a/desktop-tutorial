import dash
from dash import dcc, html, dash_table,State
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from datetime import datetime
import webbrowser
import os



# Load data from local file path
file_path = 'C:\\Users\\francisco.deleon\\downtinerecords.csv'
df = pd.read_csv(file_path)

# Sort DataFrame by descending Duration
df = df.dropna(subset=['Duration'])
df = df.sort_values(by='Duration', ascending=False)

# Get unique shifts
all_shifts = df['Shift'].unique()

# Get the current year
current_year = datetime.now().year
current_month = datetime.now().strftime('%b')

# Get unique values for dropdown options
operation_options = [{'label': op, 'value': op} for op in df['Operation'].unique()]
machine_options = [{'label': machine, 'value': machine} for machine in df['Machines'].unique()]
year_options = [{'label': year, 'value': year} for year in df['Year'].unique()]
month_options = [{'label': month, 'value': month} for month in df['Month'].unique()]


# Initialize the app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([

    html.Div([
            html.H1("Duration by Machines and Cause"),
            html.Div([
                html.Div([
                html.Label('Operation(s)'),
                dcc.Dropdown(
                    id='operation-filter',
                    options=operation_options,
                    multi=True,
                    value=['Welders'],
                    style={'width': '100%'}
                ),
                ],style={'width': '100%','display': 'block'}),
                html.Div([
                html.Label('Year'),
                dcc.Dropdown(
                    id='year-dropdown-2',
                    options=year_options,
                    value=current_year,  # Set default value to current year
                    style={'width': '100%'}
                ),
                ],style={'width': '100%','display': 'block'}),
                html.Div([
                html.Label('Month'),
                dcc.Dropdown(
                    id='month-dropdown-2',
                    options=month_options,
                    value=current_month if current_month in df['Month'].unique() else 'January',  # Set default value to a specific month if desired
                    style={'width': '100%'}
                ),
                ],style={'width': '100%','display': 'block'}),
            ],style={'width': '50%','display': 'flex'}),
            html.Hr(),
            dcc.Graph(id='machines-duration-chart')
        ], style={'width': '50%', 'float': 'left'}),
    
])
   
   
   #>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.callback(
    Output('machines-duration-chart', 'figure'),
   
    [Input('operation-filter', 'value'),
     Input('year-dropdown-2', 'value'),
     Input('month-dropdown-2', 'value')]
)
def update_machines_duration_chart(selected_operations, selected_year, selected_month):
    try:
            df['Duration'] = df['Duration'].astype(float)
    except ValueError:
            fig = px.bar(title='Invalid Duration Data Type')
    else:
        filtered_df = df[(df['Operation'].isin(selected_operations)) & (df['Year'] == selected_year) & (df['Month'] == selected_month)]
        filtered_df = filtered_df.sort_values(by='Duration', ascending=False)  # Sort by Duration

        if filtered_df.empty:
            fig = px.bar(title='No Data Available'),
        else:
           fig = px.bar(filtered_df, y='Duration', x='Machines', color='Cause', title='Duration vs Machines')

        fig.update_xaxes(categoryorder='total descending')  # Set x-axis order
        
        fig.update_layout(
            #plot_bgcolor='white',
            xaxis_title='Machines',  # Set x-axis title
            yaxis_title='Duration (Minutes)',  # Set y-axis title
            showlegend=True  # Hide legend
            ),
    
    return fig



@app.callback(
    Output('month-dropdown-2', 'options'),
    [Input('year-dropdown-2', 'value')]
)
def update_month_dropdown_2(selected_year):
    months = df[df['Year'] == selected_year]['Month'].unique()
    return [{'label': month, 'value': month} for month in months]


if __name__ == '__main__':
    # Open the default web browser with the Dash app URL
    webbrowser.open('http://127.0.0.1:8050/')
    
    # Run the Dash app
    app.run_server(debug=True)