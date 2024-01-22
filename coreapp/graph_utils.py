import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot

df = pd.read_csv('..\loews\Datasets\data.csv')

def plot_trend():
    df = pd.read_csv('..\loews\Datasets\data.csv', parse_dates=['Report_Date'])

    # Plot the trend
    df['Report_Date'] = pd.to_datetime(df['Report_Date'])

    monthly_tally = df.resample('M', on='Report_Date')['Land_Size(Acres)'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_tally['Report_Date'], y=monthly_tally['Land_Size(Acres)'], mode='lines+markers', marker=dict(size=10),
                             name='Affected Monthly Land Size in Acres For both Infestation and Breeding Grounds'))
    fig.update_layout(title='Affected Monthly Land Size in Acres For both Infestation and Breeding Grounds',
                      xaxis_title='Month',
                      yaxis_title='Land Size (Acres)')

    # Convert the figure to HTML
    trends_html = plot(fig, output_type='div')
    return trends_html