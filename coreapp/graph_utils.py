import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot


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
                      yaxis_title='Land Size (Acres)',
                      title_x=0.5)

    # Convert the figure to HTML
    trends_html = plot(fig, output_type='div')
    return trends_html


def plot_species():
    df = pd.read_csv('..\loews\Datasets\data.csv')

  # Create a Bar chart
    bar_fig = go.Figure()

    species_counts = df['Species'].value_counts()
    bar_fig.add_trace(go.Bar(x=species_counts.index, y=species_counts.values, marker_color='cornflowerblue'))
    bar_fig.update_layout(title='Distribution of Locust Species - Bar Chart', title_x=0.5, showlegend=False)

    # Create a Table
    table_fig = go.Figure()

    table_fig.add_trace(go.Table(
        header=dict(values=['Species', 'Count']),
        cells=dict(values=[species_counts.index, species_counts.values])
    ))
    table_fig.update_layout(title='Distribution of Locust Species - Table', title_x=0.5)

    # Layout customization for the table
    table_fig.update_layout(height=300, width=400)  # Adjust height and width as needed

    distribution_html = table_fig.to_html(full_html=False)

    # Show the table
    return distribution_html