import io
import streamlit as st
import pandas as pd
import random
import altair as alt
import plotly.graph_objects as go
import plotly.express as px
from .data import read_data, top_10_tracks, top_10_year, top_5_artists, top_5_artists_year, genres

def summary_plots(explicit: bool):
    base = read_data()

    years = base['year'].unique()
    years.sort()

    YEAR_AXIS = 'year:O'
    COUNT_AXIS = 'count:Q'

    if explicit:
        df_explicit = base.groupby(['year', 'explicit']).size().reset_index(name='count')

        fig = alt.Chart(df_explicit).mark_bar().encode(
            x=YEAR_AXIS,
            y=COUNT_AXIS,
            color='explicit:N'
        )

        st.altair_chart(fig, use_container_width=True)    
    else:
        df_count = pd.DataFrame(base['year'].value_counts()).reset_index()
        df_count.columns = ['year', 'count']

        fig = alt.Chart(df_count).mark_bar().encode(
            x=YEAR_AXIS,
            y=COUNT_AXIS
        )

        st.altair_chart(fig, use_container_width=True)

def create_spider_plot(year: int, all_tracks: bool = False):
    if all_tracks:
        data = top_10_tracks()
    else:
        data = top_10_year(year)

    df_top = pd.DataFrame(data)
    df_top.columns = ['song', 'artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']

    df_top['danceability'] = df_top['danceability'] * 100
    df_top['energy'] = df_top['energy'] * 100
    df_top['liveness'] = df_top['liveness'] * 100
    df_top['loudness'] = df_top['loudness'] * -5
    df_top['tempo'] = df_top['tempo'] / 2.1
    
    for index, track in df_top.iterrows():
        attributes = ['popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']
        track_features = track[attributes]
        color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)"

        fig = go.Figure(data=go.Scatterpolar(
            r=track_features,
            theta=attributes,
            fill='toself',
            fillcolor=color
            ))
        
        st.markdown(f"<h2 style='text-align: center;'>{track['song']} by <i>{track['artist']}<i></h2>", unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.divider()

def create_stacked_bar_plot(year: int, all_time: bool = False):
    if all_time:
        data_5 = top_5_artists()
    else:
        data_5 = top_5_artists_year(year)

    df_top_5 = pd.DataFrame(data_5)
    df_top_5.columns = ['artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']

    df_top_5['danceability'] = df_top_5['danceability'] * 100
    df_top_5['energy'] = df_top_5['energy'] * 100
    df_top_5['liveness'] = df_top_5['liveness'] * 100
    df_top_5['loudness'] = df_top_5['loudness'] * -5
    df_top_5['tempo'] = df_top_5['tempo'] / 2.1

    df_top_5 = df_top_5.melt(id_vars=['artist'], var_name='attribute', value_name='count')

    fig = alt.Chart(df_top_5).mark_bar().encode(
        x='artist:O',
        y=alt.Y('count:Q', axis=alt.Axis(title='', values=[])),
        color='attribute:N'
    )

    st.altair_chart(fig, use_container_width=True)

def create_scatter_plot():
    base = read_data()

    fig = alt.Chart(base).mark_circle().encode(
        x='danceability',
        y='loudness',
        color='year',
        size='popularity'
    )

    st.altair_chart(fig, use_container_width=True)

def create_genre_plot():
    base = genres()

    fig = px.bar(base, x=base.index, y='count', labels={'x': 'Genre', 'y': 'Count'})

    st.plotly_chart(fig, use_container_width=True)

def create_bubble_plot(year: int, x: str, y: str):
    base = read_data()
    base['genre'] = base['genre'].str.split(',')
    base = base.explode('genre')
    
    fig = px.scatter(base.query(f"year=={year}"), x=x, y=y,
                     size="popularity", color="genre",
                     hover_name="song", log_x=True, size_max=60)
    
    st.plotly_chart(fig, use_container_width=True)

def create_spider_plots_pdf(year: int = 0, all_tracks: bool = False):
    if all_tracks:
        data = top_10_tracks()
    else:
        data = top_10_year(year)

    df_top = pd.DataFrame(data)
    df_top.columns = ['song', 'artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']

    df_top['danceability'] = df_top['danceability'] * 100
    df_top['energy'] = df_top['energy'] * 100
    df_top['liveness'] = df_top['liveness'] * 100
    df_top['loudness'] = df_top['loudness'] * -5
    df_top['tempo'] = df_top['tempo'] / 2.1

    images = []
    
    for index, track in df_top.iterrows():
        attributes = ['popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']
        track_features = track[attributes]
        color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)"

        fig = go.Figure(data=go.Scatterpolar(
            r=track_features,
            theta=attributes,
            fill='toself',
            fillcolor=color
            ))
        
        image_data = fig.to_image(format="png", engine="kaleido")
        image = io.BytesIO(image_data)
        images.append(image)
    
    return images