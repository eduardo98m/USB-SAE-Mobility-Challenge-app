import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from get_dataframes import get_crash_data_df, get_gridwise_data_df


st.set_page_config(
     page_title='USB-SAE Mobility Team',
     page_icon="🚲",
     layout="centered", # Puede cambiarse a "wide"
     initial_sidebar_state="collapsed",
     menu_items={
         'Report a bug': "https://github.com/eduardo98m",
         'About': "https://www.sae.org",

     }
 )

px.set_mapbox_access_token(st.secrets["map_box_key"])


# Reading the datasets files

df = get_crash_data_df()

df_gw = get_gridwise_data_df()


# App layout #
st.title('USB-SAE Mobility Team')



st.text("[Párrafo introductorio]")




with st.expander("🚦 The intersection problem"):
    plot_data = pd.DataFrame(df['INTERSECTION'].value_counts())
    print(plot_data)
    st.plotly_chart(px.bar(plot_data), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)

with st.expander("🚗🛵🥡 Delivery data insights"):
   
    #st.plotly_chart(px.pie(df, values='tip', names='day'), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)

    

with st.expander("📈 Economics"):
    plot_data = pd.DataFrame(df['CRASH_YEAR'].value_counts())
    st.plotly_chart(px.pie(plot_data), use_container_width=True)
    st.write("""
    [Párrafo Explicando la data]
    """)

with st.expander("📊 Datasets"):

    st.write("""
    The data used for this study is the Allegheny County Crash Data, it is a dataset 
    containing information about the different car crashes and accidents that occurred 
    in the County between the years 2004 and 2020.  
    The data set is well structured and contains lots of details abouteach accident. 
    A data set provided by Gridwise was also employed to find some complementary insights 
    for our proposal.
    """)
