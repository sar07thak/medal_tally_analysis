import pandas as pd
import numpy as np
import plotly.express as px

   
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

def participating_nations_over_time( df ):
    # Step 1: Remove duplicates
    new_df = df.drop_duplicates(['Year', 'region'])

    # Step 2: Count countries per year
    year_region = new_df.groupby('Year')['region'].size().reset_index()

    # Rename column for clarity
    year_region.rename(columns={'region': 'num_countries'}, inplace=True)

    # Step 3: Plot using Plotly
    fig = px.line(
        year_region,
        x='Year',
        y='num_countries',
        title='Number of Countries Participating in Olympics Over Years'
    )

    return fig


def events_over_time( df ):
    new_df = df.drop_duplicates(['Year', 'Event'])

    new_df = new_df.groupby('Year')['Event'].count().reset_index()

    new_df.rename(columns={'Event': 'num_of_events'}, inplace=True)

    fig = px.bar(
    new_df,
    x='Year',
    y='num_of_events',
    color='num_of_events',
    title='Number of Events held in Olympics Over Years'
    )   

    return fig 
