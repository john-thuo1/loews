import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
from tqdm import tqdm


def plot_trend():
    df = pd.read_csv('..\loews\Datasets\data.csv', parse_dates=['Report_Date'])

    # Plot the trend
    df['Report_Date'] = pd.to_datetime(df['Report_Date'])

    monthly_tally = df.resample('M', on='Report_Date')['Land_Size(Acres)'].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=monthly_tally['Report_Date'], y=monthly_tally['Land_Size(Acres)'], mode='lines+markers', marker=dict(size=10),
                             name='Affected Monthly Land Size in Acres For both Infestation and Breeding Grounds'))
    fig.update_layout(title='Land Size Affected',
                      xaxis_title='Month, Year',
                      yaxis_title='Land Size (Acres)',
                      title_x=0.5)

    # Convert the figure to HTML
    trends_html = plot(fig, output_type='div')
    return trends_html


def plot_regions():
    df = pd.read_csv('..\loews\Datasets\data.csv')

    df['Stage'] = df['Stage'].astype(str)

    df['Category'] = pd.NA
    df.loc[df['Stage'].isin(['Hoppers/Nymph(Breeding Ground)', 'Eggs(Breeding Ground)']), 'Category'] = 'Breeding Ground'
    df.loc[df['Stage'].isin(['Fledglings(Young Adults)', 'Adults']), 'Category'] = 'Infestation'
    df.loc[df['Stage'] == 'Unknown', 'Category'] = 'Unconfirmed'

    grouped_df = df.groupby(['Location', 'Category']).size().reset_index(name='Count')

    pivot_df = grouped_df.pivot(index='Location', columns='Category', values='Count').reset_index()

    sorted_df = pivot_df.sort_values(by='Infestation', ascending=False).head(100)

  # Table

    table_html = """
    <div class="table-responsive">
        <table class="table table-hover">
            <thead class="thead-dark">
                <tr>
                    <th scope="col">Index(Descending Order)</th>
                    <th scope="col">Region</th>
                    <th scope="col">Infestation</th>
                    <th scope="col">Breeding Ground</th>
                    <th scope="col">Unconfirmed</th>
                </tr>
            </thead>
            <tbody>
    """
    for idx, (_, row) in enumerate(sorted_df.iterrows(), start=1):
        table_html += f"""
            <tr>
                <td>{idx}</td>
                <td>{row['Location']}</td>
                <td>{row['Infestation']}</td>
                <td>{row['Breeding Ground']}</td>
                <td>{row['Unconfirmed']}</td>
            </tr>
        """

    table_html += """
            </tbody>
        </table>
    </div>
    """

    return table_html, df


def plot_seasonality():
    # df = pd.read_csv('..\loews\Datasets\data.csv')
    _, df = plot_regions()

    infestation_df = df[df['Category'] == 'Infestation']
    breeding_ground_df = df[df['Category'] == 'Breeding Ground']

    # Group by Season and calculate counts
    infestation_counts = infestation_df.groupby('Season').size().reset_index(name='Infestation Count')
    breeding_ground_counts = breeding_ground_df.groupby('Season').size().reset_index(name='Breeding Ground Count')

    fig2 = go.Figure()

    fig2.add_trace(go.Bar(x=infestation_counts['Season'], y=infestation_counts['Infestation Count'],
                        name='Infestations', marker_color='skyblue', width=0.2)) 

    fig2.add_trace(go.Bar(x=breeding_ground_counts['Season'], y=breeding_ground_counts['Breeding Ground Count'],
                        name='Breeding Grounds', marker_color='salmon', width=0.2)) 

    fig2.update_layout(title='',
                    xaxis_title='',
                    yaxis_title='Count',
                    barmode='stack',  
                    legend=dict(x=0.01, y=0.99),
                    margin=dict(l=0, r=0, t=30, b=0))
    fig2.update_xaxes(tickvals=[], ticktext=[])
    fig2.update_yaxes(range=[0, 900]) 


    season_html = plot(fig2,  output_type='div')


    return season_html

    
