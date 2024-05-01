import pandas as pd

def read_data():
    database = pd.read_csv('data/spotify-charts.csv')
    return database

def top_10_year(year):
    base = read_data()
    base['Ranking'] = base['popularity'].astype(int)

    base_year = base[base['year']==year].drop_duplicates()

    return base_year.sort_values(by='Ranking', ascending=False)[:10][['song', 'artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']].reset_index(drop=True)

def top_5_artists(year):
    base = read_data()
    base['Ranking'] = base['popularity'].astype(int)

    base_year = base[base['year']==year]

    top_artists = base_year.sort_values(by='Ranking', ascending=False)['artist'].unique()[:5]

    artist_data = base_year[base_year['artist'].isin(top_artists)].drop_duplicates(subset='artist')[['artist', 'popularity', 'danceability', 'energy', 'loudness', 'liveness', 'tempo']].reset_index(drop=True)

    return artist_data

def genres():
    base = read_data()
    base['genre'] = base['genre'].str.split(', ')
    base = base.explode('genre')

    return base['genre'].value_counts()
