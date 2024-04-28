import pandas as pd

def read_data():
    database = pd.read_csv('data/spotify-charts.csv')
    return database
