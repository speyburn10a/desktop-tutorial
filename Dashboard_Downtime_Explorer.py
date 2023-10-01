import dash
from dash import dcc, html, dash_table,State
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.express as px
from datetime import datetime
import webbrowser
import os
#import dash_bootstrap_components as dbc


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

colors = {
    'background': '#111111',
    'text': '#7FDBFF'}



# Initialize the app
app = dash.Dash(__name__)

# Define layout of the app
app.layout = html.Div([
    
    html.Div([
        html.H1("Duration by Operation"),
            html.Div([
                html.Div([
                    html.Label('Year'),
                    dcc.Dropdown(
                        id='year-dropdown',
                        options=year_options,
                        value=current_year,  # Set default value to current year
                        style={'width': '100%','border': '1px solid #ccc', 'border-radius': '4px'},
                        placeholder="Select a Year"
                    )
                ],style={'width': '100%','display': 'block'}),
                html.Div([    
                    html.Label('Month'),
                    dcc.Dropdown(
                        id='month-dropdown',
                        options=month_options,
                        value=current_month if current_month in df['Month'].unique() else 'January',  # Set default value to a specific month if desired
                        style={'width': '100%','border': '1px solid #ccc', 'border-radius': '4px'}
                    )
                ],style={'width': '100%','display': 'block'}),
                html.Div([     
                    html.Label('Cause(s)'),
                    dcc.Dropdown(
                        id='cause-dropdown',
                        #options=[{'label': cause, 'value': cause} for cause in df['Cause'].unique()],
                        multi=True,
                        value=['MFX'] if ['MFX'] in df['Cause'].unique() else ['TM'],
                        style={'width': '100%','border': '1px solid #ccc', 'border-radius': '4px'}
                    )
                ],style={'width': '100%','display': 'block'}),

            ],style={'width': '100%','display': 'flex'}),
            
        html.Hr(),
    dcc.Graph(id='bar-chart')
    ], style={'width': '48%', 'float': 'left'}),
    
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
        ],style={'width': '100%','display': 'flex'}),
        html.Hr(),
        dcc.Graph(id='machines-duration-chart')
    ], style={'width': '48%', 'float': 'right'}),
    
    # Divider between top and bottom sections
    html.Hr(style={'width': '90%', 'border': '5px solid #0A227E'}),


    html.Div([
        html.H1("Duration by Machine and Shift (Table)",style={'font-size': '24px'}),
        html.Div([
            html.Label('Year'),
            dcc.Dropdown(
                id='year-dropdown-3',
                options=year_options,
                value=current_year,
                style={'width': '50%'}
            ),
            html.Label('Month'),
            dcc.Dropdown(
                id='month-dropdown-3',
                options=month_options,
                value=current_month if current_month in df['Month'].unique() else 'January',
                style={'width': '50%'}
            ),
            html.Label('Shift'), 
            dcc.Dropdown(
                    id='shift-dropdown',  # New dropdown for Shift
                    multi=True,
                    options=[1,2,3], #[{'label': shift, 'value': shift} for shift in all_shifts],
                    value=all_shifts,  # Default value to include all shifts
                    style={'width': '50%'}
                ),    
        ],style={}),

                html.Div([
                html.Label('Operation(s)'),
                dcc.Dropdown(
                    id='operation-dropdown',  # New dropdown for Operation
                    multi=True,
                    options=operation_options,
                    value=['Welders'],
                    clearable=False,  # Default value to include all operations
                    style={'width': '100%'}
                ),        
                html.Label('Machine(s)'),
                dcc.Dropdown(
                    id='machines-dropdown',
                    multi=True,
                    options=machine_options,
                    value=df['Machines'].unique(),
                    style={'width': '100%'}
                ),
                
                ],style={'width': '48%', 'float': 'left'}),

    ],style={'width': '30%', 'float': 'left'}),  

         

        html.Br(),
        
    
    html.Div([
        html.H1("Filtered Data (Table)"),
        dash_table.DataTable(
            id='filtered-table',
            columns=[{'name': col, 'id': col} for col in df.columns],
            style_table={'overflowY': 'scroll','maxHeight': '600px'},
            page_size=60,
            sort_action="native",
            style_cell={'textAlign': 'left'},
            style_data={
        'color': 'black',
        'backgroundColor': 'white'
            },
            style_data_conditional=[
                {
                    'if': {'row_index': 'odd'},
                    'backgroundColor': 'rgb(204,255,204)',
                }
            ],
            style_header={
                'backgroundColor': 'rgb(93, 213, 211)',
                'color': 'black',
                'fontWeight': 'bold',
                'fontsize':12}
        ),
        
    ],style={'width': '68%', 'float': 'left'}),
    
     
    
    
    
    # Close button
    html.Button('Close App', id='close-button', n_clicks=0, style={'position': 'absolute', 'top': '10px', 'right': '10px'}),

])
    
   

    
    


@app.callback(
    Output('month-dropdown', 'options'),
    [Input('year-dropdown', 'value')]
)
def update_month_dropdown(selected_year):
    months = df[df['Year'] == selected_year]['Month'].unique()
    return [{'label': month, 'value': month} for month in months]

@app.callback(
    Output('cause-dropdown', 'options'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_cause_dropdown(selected_year, selected_month):
    filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]
    unique_causes = filtered_df['Cause'].unique()
    cause_options =[{'label': cause, 'value': cause} for cause in unique_causes]
    return cause_options



@app.callback(
    Output('bar-chart', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value'),
     Input('cause-dropdown', 'value')]
)
def update_bar_chart(selected_year, selected_month, selected_causes):
    global fig

    try:
            df['Duration'] = df['Duration'].astype(float)
    except ValueError:
            fig = px.bar(title='Invalid Duration Data Type')
    else:

        filtered_df = df[(df['Year'] == selected_year) & (df['Month'] == selected_month)]
        if selected_causes:
            filtered_df = filtered_df[filtered_df['Cause'].isin(selected_causes)]

        if filtered_df.empty:
            fig = px.bar(title='No Data Available')
        else:
            fig = px.bar(filtered_df, y='Duration', x='Operation', color='Operation', title=f'Duration vs Operation for Year {selected_year}')
        fig.update_xaxes(categoryorder='total descending'),  # Set x-axis order
        fig.update_layout(
            #plot_bgcolor='white',
            xaxis_title='Operation',  # Set x-axis title
            yaxis_title='Duration (Minutes)',  # Set y-axis title
            showlegend=True  # Hide legend
            ),


    return fig


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
    fig.show()
    
    return fig
   

   

@app.callback(
    Output('month-dropdown-2', 'options'),
    [Input('year-dropdown-2', 'value')]
)
def update_month_dropdown_2(selected_year):
    months = df[df['Year'] == selected_year]['Month'].unique()
    return [{'label': month, 'value': month} for month in months]



#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
@app.callback(
    Output('month-dropdown-3', 'options'),
    [Input('year-dropdown-3', 'value')]
)
def update_month_dropdown_3(selected_year):
    months = df[df['Year'] == selected_year]['Month'].unique()
    return [{'label': month, 'value': month} for month in months]




@app.callback(
    Output('machines-dropdown', 'value'),  # Update the value property of machines-dropdown
    [Input('operation-dropdown', 'value')]  # Listen to changes in operation-dropdown
)

def update_default_selected_machines(selected_operations):
    if not selected_operations:
        return df['Machines'].unique()  # If no operations selected, return all machines
    else:
        filtered_df = df[df['Operation'].isin(selected_operations)]
        return filtered_df['Machines'].unique().tolist()


@app.callback(
    Output('filtered-table', 'data'),
    [Input('year-dropdown-3', 'value'),
     Input('month-dropdown-3', 'value'),
     Input('machines-dropdown', 'value'),
     Input('operation-dropdown', 'value'),
     Input('shift-dropdown', 'value')]  # Add Input for shift dropdown
)
def update_filtered_table(selected_year, selected_month, selected_machines, selected_operations, selected_shifts):
    filtered_df = df[(df['Year'] == selected_year) & 
                     (df['Month'] == selected_month) & 
                     (df['Machines'].isin(selected_machines)) & 
                     (df['Operation'].isin(selected_operations)) & 
                     (df['Shift'].isin(selected_shifts))]  # Filter by selected shifts
    return filtered_df.to_dict('records')





## Callback to close the app
@app.callback(
    Output('close-button', 'disabled'),
    Output('close-button', 'n_clicks'),
    Input('close-button', 'n_clicks'),
    State('close-button', 'n_clicks'),
    prevent_initial_call=True  # Prevents callback from running on app startup
)
def close_app(n_clicks, current_clicks):
    if n_clicks > current_clicks:
        # Close the app by setting the disabled state of the close button
        return True, n_clicks
    return False, n_clicks





if __name__ == '__main__':
    # Open the default web browser with the Dash app URL
    webbrowser.open('http://127.0.0.1:8050/')
    
    # Run the Dash app
    app.run_server(debug=True)

    fig.show()

