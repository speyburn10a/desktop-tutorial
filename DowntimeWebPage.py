import plotly.express as px
import pandas as pd
import streamlit as st
import plotly
import sqlite3
from plotly.offline import plot
from plotly.subplots import make_subplots
import plotly.graph_objects as go

# Read Data From Excel and store in a variable df [dataframe]


def get_data():
    file_path = 'C:\\Users\\francisco.deleon\\downtinerecords.csv'
    df = pd.read_csv(file_path)

    return df


df1 = get_data()
df1.dropna(inplace=True)


# Store each column in a seperate varibale.
operations = df1["Operation"].unique()
date = df1["Date"]


time_by_operation = (df1.groupby(by=["Operation"]).sum(numeric_only=True)[
    ["Duration"]].sort_values(by="Duration", ascending=False))





fig = px.bar(
    time_by_operation,
    x=time_by_operation.index,
    y="Duration",
    title="<b>Downtime by Operation (%)</b>",
    text_auto=True,
    color=time_by_operation.index,
    animation_group=time_by_operation.index,
    template="plotly_white",
)
fig.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

#print(time_by_operation.index)
Dh = pd.DataFrame(time_by_operation.index)

# DOWNIME BY MACHINE [BAR CHART]
df_selection = df1[df1["Operation"].isin(Dh['Operation'][0:])]

time_by_machine = (
    df_selection.groupby(by=["Machines"]).sum(numeric_only=True)[
        ["Duration"]].sort_values(by="Duration", ascending=False))
    


fig1 = px.bar(
    time_by_machine,
    x=time_by_machine.index,
    y="Duration",
    title="<b>Downtime by Operation (%)</b>",
    text_auto=True,
    color=time_by_machine.index,
    animation_group=time_by_machine.index,
    template="plotly_white",
)
fig1.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)

# DOWNTIME BY CAUSE[BAR CHART]
time_by_cause = (df_selection.groupby(by=["Cause"]).sum(numeric_only=True)[
    ["Duration"]].sort_values(by="Duration", ascending=False))/60
fig_cause_time = px.bar(
    time_by_cause,
    x=time_by_cause.index,
    y="Duration",
    title="<b>From Selected Machines: Downtime by Cause (Hrs)</b>",
    color_discrete_sequence=["#0083B8"] * len(time_by_cause),
    template="plotly_white",
)
fig_cause_time.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)



# Create Bar Chart and store figure as fig
def figures_to_html(figs, filename="dashboard.html"):
    with open(filename, 'w') as dashboard:
        dashboard.write("<html><head></head><body>" + "\n")
        for fig in figs:
            inner_html = fig.to_html().split('<body>')[1].split('</body>')[0]
            dashboard.write(inner_html)
        dashboard.write("</body></html>" + "\n")

'''# Add dropdown
fig.update_layout(
    updatemenus=[
        dict(
            buttons=list([
                dict(
                    args=["type", "surface"],
                    label="3D Surface",
                    method="restyle"
                ),
                dict(
                    args=["type", "heatmap"],
                    label="Heatmap",
                    method="restyle"
                )
            ]),
            direction="down",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.1,
            xanchor="left",
            y=1.1,
            yanchor="top"
        ),
    ]
)

# Add annotation
fig.update_layout(
    annotations=[
        dict(text="Trace type:", showarrow=False,
        x=0, y=1.085, yref="paper", align="left")
    ]
)'''


# Save Chart and export to HTML
figures_to_html([fig, fig1])
#plotly.offline.plot(, filename="DowntimeWeb.html")
fig.show()