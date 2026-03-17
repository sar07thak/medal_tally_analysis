# 💀 -> data fetch from different_files

import streamlit as st
import pandas as pd
import preprocessor , helper
import plotly.express as px

# import data
df = pd.read_csv('data/athlete_events.csv')
region_df = pd.read_csv('data/noc_regions.csv')

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
    st.subheader("📈 Participating Nations Over Time")
    graph = helper.participating_nations_over_time(df)
    st.plotly_chart(graph, use_container_width=True)
