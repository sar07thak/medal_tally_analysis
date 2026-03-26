# 💀 -> data fetch from different_files

import os
import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px

# import data
base_path = os.path.dirname(os.path.dirname(__file__))
df = pd.read_csv(os.path.join(base_path, 'data/athlete_events.csv'))
region_df = pd.read_csv(os.path.join(base_path, 'data/noc_regions.csv'))

# 💀 this is the completed Filtered data on the basis of summer season
df = preprocessor.preprocess(df , region_df)

# Configure page layout for better UI
st.set_page_config(page_title="Olympics Analysis", page_icon="🏅", layout="wide")


# Sidebar navigation with better styling
st.sidebar.header("📊 Navigation")
user_menu = st.sidebar.radio(
    'Select an option',
    ('Medal Tally', 'Overall Analysis', 'Country Wise Analysis', 'Athlete Wise Analysis')
)

# 🧒 if user can select Medal Tally 
if user_menu == 'Medal Tally':
    # Main header with emoji
    st.title("🏅 Olympics Analysis Dashboard")
    st.markdown("---")
    st.sidebar.subheader("🏅 Medal Tally Filters")
    # 💀 number of unique country and years are fetched
    years, regions = helper.country_year_list(df)
    
    # Create two columns for side-by-side dropdowns
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        # Year selection with icon
        selected_year = st.selectbox("📅 Year", years)
    
    with col2:
        # Country selection with icon
        selected_country = st.selectbox("🌍 Country", regions)
    # Display section header with dynamic title
    if selected_year == 'overall' and selected_country == 'overall':
        st.subheader("🏆 Overall Medal Tally (All Years, All Countries)")
    elif selected_year == 'overall':
        st.subheader(f"🏆 Medal Tally for {selected_country} (All Years)")
    elif selected_country == 'overall':
        st.subheader(f"🏆 Medal Tally for {selected_year} (All Countries)")
    else:
        st.subheader(f"🏆 Medal Tally for {selected_country} in {selected_year}")
    
    # 💀 Get medal tally data fetched 
    medal_tally = helper.medal_tally(df, selected_country, selected_year)
    
    # Check if data exists before displaying
    if medal_tally.empty:
        st.warning("⚠️ No data available for the selected filters.")
    else:
        # 💀 Display summary metrics in columns
        total_gold = medal_tally['Gold'].sum()
        total_silver = medal_tally['Silver'].sum()
        total_bronze = medal_tally['Bronze'].sum()
        total_medals = medal_tally['total'].sum()
        
        # Create metric cards for quick overview
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            st.metric(label="🥇 Gold", value=total_gold)
        
        with metric_col2:
            st.metric(label="🥈 Silver", value=total_silver)
        
        with metric_col3:
            st.metric(label="🥉 Bronze", value=total_bronze)
        
        with metric_col4:
            st.metric(label="📊 Total", value=total_medals)
        
        st.markdown("---")
        
        # Style the dataframe with custom formatting
        # Apply color gradient to medal columns for better visualization
        styled_df = medal_tally.style.background_gradient(
            subset=['Gold', 'Silver', 'Bronze', 'total'], 
            cmap='YlOrBr'
        ).format({
            'Gold': '{:.0f}',
            'Silver': '{:.0f}',
            'Bronze': '{:.0f}',
            'total': '{:.0f}'
        })
        
        # Display the styled dataframe
        st.dataframe(
            styled_df,
            use_container_width=True,  # Make table span full width
            hide_index=True  # Hide row indices for cleaner look
        )
      
# 🧒 if user can select Overall Analysis 
if user_menu == 'Overall Analysis':
    # 💀 overall analysis fetched
    unique_country = df['region'].unique().shape[0]
    edition = df['Year'].unique().shape[0]
    unique_cities = df['City'].unique().shape[0]
    unique_games = df['Sport'].unique().shape[0]
    unique_athlete = df['Name'].unique().shape[0]
    unique_events = df['Event'].unique().shape[0]

    st.title("🏅 Overall Analysis Dashboard")
    st.markdown("---")
    
    # Key Statistics Section
    st.subheader("📊 Key Statistics")
    
    # First row of metrics with icons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏛️ Editions",
            value=edition,
            help="Total number of Olympic editions held"
        )
    
    with col2:
        st.metric(
            label="🏙️ Host Cities",
            value=unique_cities,
            help="Total number of unique host cities"
        )
    
    with col3:
        st.metric(
            label="🎯 Sports",
            value=unique_games,
            help="Total number of unique sports categories"
        )
    
    # Second row of metrics with icons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="🏃 Events",
            value=unique_events,
            help="Total number of unique events"
        )
    
    with col2:
        st.metric(
            label="👥 Athletes",
            value=unique_athlete,
            help="Total number of unique athletes participated"
        )
    
    with col3:
        st.metric(
            label="🌍 Nations",
            value=unique_country,
            help="Total number of participating nations"
        )
    
    st.markdown("---")
    
    # 💀 Graph data fetch from the helper for Visualizations Section
    st.subheader("📈Participating Nations Over Time")
    nation_over_time_graph = helper.participating_data_over_time(df , 'region')
    st.plotly_chart( nation_over_time_graph , use_container_width=True)

    st.subheader("🎮Event held Over Time")
    event_over_time_graph = helper.participating_data_over_time( df , 'Event' )
    st.plotly_chart( event_over_time_graph , use_container_width=True )

    st.subheader("🧑Atheletes participate Over Time")
    athelete_over_time_graph = helper.participating_data_over_time( df , 'Name' )
    st.plotly_chart( athelete_over_time_graph , use_container_width=True )

    st.subheader("🔥 Events per Sport over Years (Heatmap)")
    heatmap_fig = helper.heatmap_event(df)
    st.pyplot(heatmap_fig)

    st.subheader("🏆 Most Successful Athletes")
    st.markdown("Top 15 athletes by total medal count")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'overall')
    selected_sport = st.selectbox('select a sport ' , sport_list )
    successful_athlete = helper.most_successfull_athelte(df,  selected_sport )

    if successful_athlete.empty:
        st.warning("⚠️ No data available")
    else:
        # Style the dataframe with medal color gradients
        styled_df = successful_athlete.style.background_gradient(
            subset=['Gold', 'Silver', 'Bronze', 'Total'],
            cmap='YlOrBr'
        ).format({
            'Gold': '{:.0f}',
            'Silver': '{:.0f}',
            'Bronze': '{:.0f}',
            'Total': '{:.0f}'
        })

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

# 🧒 if user can select Country Wise Analysis
if user_menu == 'Country Wise Analysis':
    st.title("🌍 Country Wise Analysis Dashboard")
    st.markdown("---")
    
    # Country selection
    st.sidebar.subheader("🌍 Country Filter")
    years, regions = helper.country_year_list(df)
    selected_country = st.sidebar.selectbox("Select Country", regions)
    
    # 1. Country-wise medal tally per year (line plot)
    st.subheader("📈 Medal Tally Per Year")
    if selected_country == 'overall':
        st.markdown("Top 10 countries by total medals")
    else:
        st.markdown(f"Medal breakdown for **{selected_country}**")
    
    medal_tally_fig = helper.plot_country_medal_tally_per_year(df, selected_country)
    st.plotly_chart(medal_tally_fig, use_container_width=True)
    
    # 2. Top Sports by Medal Count
    st.subheader("🏅 Top Sports by Medal Count")
    st.markdown("Sports where the country has won the most medals")
    
    sports_fig = helper.country_sport_heatmap(df, 'overall', selected_country)
    if sports_fig:
        st.plotly_chart(sports_fig, use_container_width=True)
    else:
        st.warning("⚠️ No data available")
    
    # 3. Most successful athletes (Top 10)
    st.subheader("🏆 Top 10 Most Successful Athletes")
    if selected_country == 'overall':
        st.markdown("Top athletes across all countries")
    else:
        st.markdown(f"Top athletes from **{selected_country}**")
    
    top_athletes = helper.top_athletes_by_country(df, selected_country)
    
    if top_athletes.empty:
        st.warning("⚠️ No data available")
    else:
        styled_athletes = top_athletes.style.background_gradient(
            subset=['Gold', 'Silver', 'Bronze', 'Total'],
            cmap='YlOrBr'
        ).format({
            'Gold': '{:.0f}',
            'Silver': '{:.0f}',
            'Bronze': '{:.0f}',
            'Total': '{:.0f}'
        })

        st.dataframe(
            styled_athletes,
            use_container_width=True,
            hide_index=True
        )


if user_menu == 'Athlete Wise Analysis':

    options = ['All Athletes', 'Gold', 'Silver', 'Bronze']

    selected = st.multiselect(
        "Select categories to compare",
        options,
        default=['All Athletes']
    )


    st.title("Distribution of Age")
    fig = helper.distribution_graph_plotly(df, selected)
    st.plotly_chart(fig, use_container_width=True)


    st.title("🏃 Age Distribution by Sport")
    st.markdown("---")
    
    # Get unique sports list
    sports_list = df['Sport'].unique().tolist()
    sports_list.sort()
    sports_list.insert(0, 'overall')
    
    selected_sports = st.multiselect(
        "Select Sports to Compare",
        sports_list,
        default=['overall']
    )
    
    # If 'overall' is selected or no selection, show top 10 sports
    if not selected_sports or 'overall' in selected_sports:
        # Get top 10 sports by athlete count
        df_temp = df.drop_duplicates(subset=['Name', 'Sport'])
        sport_counts = df_temp.groupby('Sport').size().nlargest(10).reset_index(name='count')
        selected_sports = sport_counts['Sport'].tolist()
    
    if selected_sports:
        age_sport_fig = helper.age_sport_distribution_plotly(df, selected_sports)
        st.plotly_chart(age_sport_fig, use_container_width=True)
    else:
        st.warning("⚠️ Please select at least one sport")


