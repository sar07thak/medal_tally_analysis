import pandas as pd 
import numpy as np 
import streamlit as st

@st.cache_data
def preprocess(df , region_df) :
    df = df[df['Season'] == 'Summer']
    df = df.merge( region_df , on='NOC' , how='left')
    df = df.drop_duplicates()
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)

    return df 