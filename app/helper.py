import pandas as pd
import numpy as np
import plotly.express as px
import plotly.figure_factory as ff
import seaborn as sns
import matplotlib.pyplot as plt
   
def medal_tally( df , country , year ) :
    # update the problem and make sure it count as 1 medal
    medal_df = df.drop_duplicates(subset=['NOC','Games','Year','Season','City','Sport','Event','Medal','region','notes','Bronze','Gold','Silver'])
    flag = 0 
    # Filter before grouping
    if country == 'overall' and year == 'overall':
        filtered = medal_df
    elif country == 'overall' and year != 'overall':
        filtered = medal_df[medal_df['Year'] == year]
    elif country != 'overall' and year == 'overall':
        flag = 1
        filtered = medal_df[medal_df['region'] == country]
    else:
        filtered = medal_df[(medal_df['region'] == country) & (medal_df['Year'] == year)]

    # Group and sum
    if flag : 
        result = filtered.groupby('Year')[['Gold','Silver','Bronze']].sum().sort_values(by='Gold', ascending=False).reset_index()
    else :
        result = filtered.groupby('region')[['Gold','Silver','Bronze']].sum().sort_values(by='Gold', ascending=False).reset_index()

    result['total'] = result['Gold'] + result['Silver'] + result['Bronze']

    return result

def country_year_list( df ) :
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')

    regions = np.unique( df['region'].dropna().values).tolist()
    regions.sort()
    regions.insert(0,'overall')

    return years , regions 

def participating_data_over_time( df , value ):
    # Step 1: Remove duplicates
    new_df = df.drop_duplicates(['Year', value ])

    # Step 2: Count countries per year
    year_wise_data = new_df.groupby('Year')[value].size().reset_index()

    # Rename column for clarity
    year_wise_data.rename(columns={value: f'num of {value}'}, inplace=True)

    # Step 3: Plot using Plotly
    if value == 'region' :
        fig = px.line(
            year_wise_data,
            x='Year',
            y=f'num of {value}',
            title='Number of Countries Participating in Olympics Over Years'
        )
    elif value == 'Event' :
        fig = px.bar(
            year_wise_data,
            x='Year',
            y=f'num of {value}',
            color=f'num of {value}',
            title='Number of Countries Participating in Olympics Over Years'
        )
    elif value == 'Name' :
        fig = px.area(
            year_wise_data,
            x='Year',
            y=f'num of {value}',
            title='Number of Countries Participating in Olympics Over Years'
        )
    

    return fig

def heatmap_event( df ) :
    # Step 1: Remove duplicate events (important)
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])

    # Step 2: Create pivot table
    pivot_table = x.pivot_table(
        index='Sport',
        columns='Year',
        values='Event',
        aggfunc='count'
    ).fillna(0).astype(int)

    fig, ax = plt.subplots(figsize=(20, 20))

    sns.heatmap(
        pivot_table,
        annot=True,        # show numbers
        fmt="d",           # integer format
        cmap="viridis",    # color style
        ax=ax
    )

    ax.set_title("Number of Events per Sport over Years")
    ax.set_xlabel("Year")
    ax.set_ylabel("Sport")

    plt.tight_layout()
    
    return fig

def most_successfull_athelte(df, sport):
    # Step 1: Keep only medal winners
    df_medal = df[df['Medal'].notnull()]

    # Step 2: Group by Name + Sport + Region
    medal_sport_df = df_medal.groupby(
        ['Name', 'Sport', 'region']
    )[['Gold', 'Silver', 'Bronze']].sum().reset_index()

    # Step 3: Add total medals
    medal_sport_df['Total'] = (
        medal_sport_df['Gold'] +
        medal_sport_df['Silver'] +
        medal_sport_df['Bronze']
    )

    # Step 4: Sort and get top 15
    medal_sport_df = medal_sport_df.sort_values(by='Total', ascending=False)
    table = medal_sport_df[['Name', 'Sport', 'region', 'Gold', 'Silver', 'Bronze', 'Total']]
    table = table.reset_index(drop=True)

    if sport == 'overall':
        return table.head(15)
    else:
        sport_filter = table[table['Sport'] == sport].reset_index(drop=True).head(15)
        return sport_filter


def country_medal_tally_per_year(df, country):
    """Get medal tally for a country across all years (line plot data)"""
    # Remove duplicates based on unique event participation
    medal_df = df.drop_duplicates(subset=['NOC','Games','Year','Season','City','Sport','Event','Medal'])
    
    if country == 'overall':
        filtered = medal_df
        grouped = filtered.groupby(['Year', 'region'])[['Gold','Silver','Bronze']].sum().reset_index()
        # Get top 10 countries by total medals
        country_totals = grouped.groupby('region')[['Gold','Silver','Bronze']].sum()
        country_totals['Total'] = country_totals['Gold'] + country_totals['Silver'] + country_totals['Bronze']
        top_countries = country_totals.nlargest(10, 'Total').index.tolist()
        grouped = grouped[grouped['region'].isin(top_countries)]
    else:
        filtered = medal_df[medal_df['region'] == country]
        grouped = filtered.groupby('Year')[['Gold','Silver','Bronze']].sum().reset_index()
    
    grouped['Total'] = grouped['Gold'] + grouped['Silver'] + grouped['Bronze']
    
    return grouped


def plot_country_medal_tally_per_year(df, country):
    """Create line plot for country medal tally per year - showing only total medals"""
    grouped = country_medal_tally_per_year(df, country)
    
    if country == 'overall':
        # For overall, show top 10 countries by total medals
        country_totals = grouped.groupby('region')[['Gold','Silver','Bronze']].sum()
        country_totals['Total'] = country_totals['Gold'] + country_totals['Silver'] + country_totals['Bronze']
        top_countries = country_totals.nlargest(10, 'Total').index.tolist()
        
        # Get yearly totals for top countries
        grouped = grouped[grouped['region'].isin(top_countries)]
        grouped['Total'] = grouped['Gold'] + grouped['Silver'] + grouped['Bronze']
        
        fig = px.line(
            grouped,
            x='Year',
            y='Total',
            color='region',
            title='Total Medals Per Year by Country (Top 10)',
            labels={'Year': 'Year', 'Total': 'Total Medals', 'region': 'Country'}
        )
    else:
        # For specific country, show only total medals trend
        grouped['Total'] = grouped['Gold'] + grouped['Silver'] + grouped['Bronze']
        fig = px.line(
            grouped,
            x='Year',
            y='Total',
            title=f'{country} - Total Medals Per Year',
            labels={'Year': 'Year', 'Total': 'Total Medals'}
        )
    
    return fig


def country_sport_heatmap(df, year, country):
    """
    Create bar chart showing medal distribution by sport for a country.
    
    Use cases:
    - Specific country: Shows which sports the country excels at
    - Overall: Shows top sports across all countries
    """
    # Get medal-winning performances only
    medal_df = df[df['Medal'].notnull()].drop_duplicates(['NOC', 'Games', 'Sport', 'Event', 'Medal', 'region'])
    
    # Apply filters
    if year != 'overall':
        medal_df = medal_df[medal_df['Year'] == year]
    if country != 'overall':
        medal_df = medal_df[medal_df['region'] == country]
    
    if medal_df.empty:
        return None
    
    # Group by sport and count medals
    sport_medals = medal_df.groupby('Sport').size().reset_index(name='Medal_Count')
    sport_medals = sport_medals.sort_values('Medal_Count', ascending=True)
    
    # Get top 15 sports
    sport_medals = sport_medals.tail(15)
    
    fig = px.bar(
        sport_medals,
        x='Medal_Count',
        y='Sport',
        orientation='h',
        title=f"Top Sports by Medal Count - {country}" if country != 'overall' else "Top Sports by Medal Count (All Countries)",
        labels={'Medal_Count': 'Number of Medals', 'Sport': 'Sport'},
        color='Medal_Count',
        color_continuous_scale='YlOrRd'
    )
    
    fig.update_layout(height=600, yaxis={'categoryorder': 'total ascending'})
    
    return fig


def top_athletes_by_country(df, country):
    """Get top 10 most successful athletes for a country"""
    # Keep only medal winners
    df_medal = df[df['Medal'].notnull()].drop_duplicates(['NOC', 'Games', 'Event', 'Medal', 'Name'])

    if country == 'overall':
        filtered = df_medal
    else:
        filtered = df_medal[df_medal['region'] == country]

    # Group by athlete
    athlete_medals = filtered.groupby(['Name', 'Sport', 'region'])[['Gold', 'Silver', 'Bronze']].sum().reset_index()
    athlete_medals['Total'] = athlete_medals['Gold'] + athlete_medals['Silver'] + athlete_medals['Bronze']

    # Sort and get top 10
    athlete_medals = athlete_medals.sort_values(by='Total', ascending=False).head(10)

    return athlete_medals[['Name', 'Sport', 'region', 'Gold', 'Silver', 'Bronze', 'Total']].reset_index(drop=True)

import plotly.graph_objects as go
import numpy as np
from scipy.stats import gaussian_kde

def distribution_graph_plotly(df, selected):
    df = df.drop_duplicates(subset=['Name','region'])

    fig = go.Figure()

    def add_kde(data, label):
        data = data.dropna()

        if len(data) > 0:
            kde = gaussian_kde(data)
            x_vals = np.linspace(data.min(), data.max(), 200)
            y_vals = kde(x_vals)

            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                name=label
            ))

    if 'All Athletes' in selected:
        add_kde(df['Age'], 'All Athletes')

    if 'Gold' in selected:
        add_kde(df[df['Medal']=='Gold']['Age'], 'Gold')

    if 'Silver' in selected:
        add_kde(df[df['Medal']=='Silver']['Age'], 'Silver')

    if 'Bronze' in selected:
        add_kde(df[df['Medal']=='Bronze']['Age'], 'Bronze')

    fig.update_layout(
        title="Age Distribution Comparison (KDE)",
        xaxis_title="Age",
        yaxis_title="Density"
    )

    return fig


def age_sport_distribution_plotly(df, selected_sports):
    """Create age distribution graph for multiple sports using distplot"""
    df_filtered = df.drop_duplicates(subset=['Name', 'Sport'])
    
    # Filter by selected sports
    df_filtered = df_filtered[df_filtered['Sport'].isin(selected_sports)]
    
    # Prepare data for each sport
    data = []
    valid_sports = []
    for sport in selected_sports:
        sport_data = df_filtered[df_filtered['Sport'] == sport]['Age'].dropna()
        # Need at least 2 data points and variance in ages (not all same age)
        if len(sport_data) > 1 and sport_data.nunique() > 1:
            data.append(sport_data.values)
            valid_sports.append(sport)
    
    if not data:
        return go.Figure().update_layout(title="No data available")
    
    # Create distplot
    fig = ff.create_distplot(
        data,
        group_labels=valid_sports,
        show_hist=False,
        show_rug=False
    )
    
    fig.update_layout(
        title='Age Distribution by Sport (Comparison)',
        xaxis_title="Age",
        yaxis_title="Density",
        showlegend=True
    )
    
    return fig