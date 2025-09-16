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
            x=alt.X(YEAR_AXIS, title='Year'),
            y=alt.Y(COUNT_AXIS, title='Number of Tracks'),
            color=alt.Color('explicit:N', 
                          scale=alt.Scale(domain=[True, False], range=['#ff6b6b', '#4ecdc4']),
                          legend=alt.Legend(title="Explicit Content"))
        ).properties(
            width=600,
            height=400,
            title='Number of Tracks per Year (by Explicit Content)'
        )

        st.altair_chart(fig, use_container_width=True)    
    else:
        df_count = pd.DataFrame(base['year'].value_counts()).reset_index()
        df_count.columns = ['year', 'count']

        fig = alt.Chart(df_count).mark_bar(color='#1DB954').encode(
            x=alt.X(YEAR_AXIS, title='Year'),
            y=alt.Y(COUNT_AXIS, title='Number of Tracks'),
            tooltip=['year:O', 'count:Q']
        ).properties(
            width=600,
            height=400,
            title='Number of Tracks per Year'
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

    fig = alt.Chart(base).mark_circle(
        size=60,
        opacity=0.7
    ).encode(
        x=alt.X('danceability:Q', title='Danceability', scale=alt.Scale(domain=[0, 1])),
        y=alt.Y('loudness:Q', title='Loudness (dB)'),
        color=alt.Color('year:O', 
                       scale=alt.Scale(scheme='viridis'),
                       legend=alt.Legend(title="Year")),
        size=alt.Size('popularity:Q', 
                     scale=alt.Scale(range=[20, 200]),
                     legend=alt.Legend(title="Popularity")),
        tooltip=['song:N', 'artist:N', 'year:O', 'danceability:Q', 'loudness:Q', 'popularity:Q']
    ).properties(
        width=700,
        height=450,
        title='Audio Features Correlation: Danceability vs Loudness (sized by Popularity, colored by Year)'
    ).interactive()

    st.altair_chart(fig, use_container_width=True)

def create_genre_plot():
    base = genres()

    # Create a more informative bar chart
    genre_df = pd.DataFrame({'genre': base.index, 'count': base.values})
    
    # Take top 15 genres for better readability
    genre_df = genre_df.head(15)

    fig = px.bar(
        genre_df, 
        x='genre', 
        y='count', 
        labels={'genre': 'Genre', 'count': 'Number of Tracks'},
        title='Top 15 Most Popular Genres',
        color='count',
        color_continuous_scale='viridis'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=False
    )
    
    fig.update_traces(
        texttemplate='%{y}',
        textposition='outside'
    )

    st.plotly_chart(fig, use_container_width=True)

def create_bubble_plot(year: int, x: str, y: str):
    base = read_data()
    base['genre'] = base['genre'].str.split(',')
    base = base.explode('genre')
    
    # Filter by year and clean data
    year_data = base.query(f"year=={year}").copy()
    year_data['genre'] = year_data['genre'].str.strip()
    
    # Take top 10 genres for better readability
    top_genres = year_data['genre'].value_counts().head(10).index
    year_data = year_data[year_data['genre'].isin(top_genres)]
    
    fig = px.scatter(
        year_data, 
        x=x, 
        y=y,
        size="popularity", 
        color="genre",
        hover_name="song",
        hover_data={
            'artist': True,
            'popularity': True,
            x: ':.3f',
            y: ':.3f'
        },
        size_max=60,
        title=f'Audio Features Analysis for {year}: {x.title()} vs {y.title()}'
    )
    
    fig.update_layout(
        height=500,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.01
        )
    )
    
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