from src.utils.data import read_data
import os
import altair as alt
import pandas as pd
import random
import plotly.express as px

base = read_data()

years = base['year'].unique()
years.sort()

df_count = pd.DataFrame(base['year'].value_counts()).reset_index()
df_count.columns = ['year', 'count']

alt.Chart(df_count).mark_bar().encode(
    x='year:O',
    y='count:Q'
)

def top_10_year(year):
    base = read_data()
    base['Ranking'] = base['popularity'].astype(int)

    base_year = base[base['year']==year]

    return base_year.sort_values(by='Ranking', ascending=False)[:10][['song', 'artist', 'popularity', 'loudness', 'liveness', 'tempo']].reset_index(drop=True)

def plot_radar(year):
    data_10 = top_10_year(year)

    df_top_10 = pd.DataFrame(data_10)
    df_top_10.columns = ['song', 'artist', 'popularity', 'loudness', 'liveness', 'tempo']

    df_top_10['liveness'] = df_top_10['liveness'] * 100
    df_top_10['loudness'] = df_top_10['loudness'] * -5
    df_top_10['tempo'] = df_top_10['tempo'] / 2.1

    for index, track in df_top_10.iterrows():
        attributes = ['popularity', 'loudness', 'liveness', 'tempo']
        values = track[attributes].tolist()
        color = f"rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.3)"
        fig = px.line_polar(df_top_10, r=values, theta=attributes, line_close=True)
        fig.update_traces(fill='toself', fillcolor=color)
        fig.update_layout(title=f"{track['song']} by {track['artist']}")
        fig.update_polars(radialaxis=dict(range=[0, 100]))
        fig.update_layout(plot_bgcolor='rgba(14, 17, 23, 1)', paper_bgcolor='rgba(14, 17, 23, 1)', font_color='white')
        
        index += 1
        filename = f"images/Radar_{year}_{index}.svg"
        fig.write_image(filename)

for year in years:
    plot_radar(year)