import streamlit as st
from src import read_data, count_tracks

st.set_page_config(page_title='My Spotify App', page_icon=':musical_note:')

st.title('Spotify Tracks App')
st.divider()

st.write('This is a complete dataset of Spotify tracks from 2000 to 2019.')

st.write(read_data())

count_tracks()
st.divider()