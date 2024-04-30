import streamlit as st
import pandas as pd
import random
import altair as alt
import plotly.graph_objects as go
from .data import read_data, top_10_year

def summary_plots(explicit: bool):
    base = read_data()

    years = base['year'].unique()
    years.sort()

    if explicit:
        df_explicit = base.groupby(['year', 'explicit']).size().reset_index(name='count')

        fig = alt.Chart(df_explicit).mark_bar().encode(
            x='year:O',
            y='count:Q',
            color='explicit:N',
        )

        st.altair_chart(fig, use_container_width=True)    
    else:
        df_count = pd.DataFrame(base['year'].value_counts()).reset_index()
        df_count.columns = ['year', 'count']

        fig = alt.Chart(df_count).mark_bar().encode(
            x='year:O',
            y='count:Q'
        )

        st.altair_chart(fig, use_container_width=True)

def create_spider_plot(year: int):
    data_10 = top_10_year(year)

    df_top_10 = pd.DataFrame(data_10)
    df_top_10.columns = ['song', 'artist', 'popularity', 'loudness', 'liveness', 'tempo']

    df_top_10['liveness'] = df_top_10['liveness'] * 100
    df_top_10['loudness'] = df_top_10['loudness'] * -5
    df_top_10['tempo'] = df_top_10['tempo'] / 2.1
    
    for index, track in df_top_10.iterrows():
        attributes = ['popularity', 'loudness', 'liveness', 'tempo']
        track_features = track[attributes]
        color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)"

        fig = go.Figure(data=go.Scatterpolar(
            r=track_features,
            theta=attributes,
            fill='toself',
            fillcolor=color
            ))
        
        st.markdown(f"{track['song']} by {track['artist']}")
        
        st.plotly_chart(fig, use_container_width=True)
