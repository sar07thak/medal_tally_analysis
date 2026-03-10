import pandas as pd
import numpy as np


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

