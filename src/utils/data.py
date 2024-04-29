import pandas as pd

def read_data():
    database = pd.read_csv('data/spotify-charts.csv')
    return database

def top_10_year(year):
    base = read_data()
    base['Ranking'] = base['popularity'].astype(int)

    base_year = base[base['year']==year]

    return base_year.sort_values(by='Ranking', ascending=False)[:10][['song', 'artist', 'popularity', 'loudness', 'liveness', 'tempo']].reset_index(drop=True)