import streamlit as st
from streamlit_navigation_bar import st_navbar
from src import read_data, top_10_year, count_tracks, radar_charts

st.set_page_config(page_title='Spotify Dashboard', page_icon='./public/icon.png', layout='centered', initial_sidebar_state='collapsed')

HOME = 'Home'
TOP_10_TRACKS = 'Top 10 Tracks'
TOP_5_ARTISTS = 'Top 5 Artists'
GENRES = 'Genres'
ANALYSIS = 'Analysis'
REPORTS = 'Reports'

menu_data = [HOME, TOP_10_TRACKS, TOP_5_ARTISTS, GENRES, ANALYSIS, REPORTS]

# Sidebar Settings
# st.sidebar.title('Menu')
# page = st.sidebar.radio('Select a page:', menu_data, index=0)

page = st_navbar(menu_data)

if page == HOME:
    st.title('Spotify Dashboard')
    st.divider()
    st.write('Welcome to the Spotify Dashboard!')
    st.write('This is a complete dataset of Spotify tracks from 2000 to 2019.')
    st.write('This app is a Streamlit dashboard that can be used to analyze the Spotify tracks dataset.')
    st.write('You can select different pages from the sidebar to explore the dataset.')
    st.write(read_data())
    st.divider()
    st.markdown("<h2 style='text-align: center;'>Number of songs per year on Spotify</h2>", unsafe_allow_html=True)
    explicit_filter = st.checkbox('Show Explicits', value=False)
    if explicit_filter:
        count_tracks(explicit=True)
    else:
        count_tracks(explicit=False)
    
elif page == TOP_10_TRACKS:
    st.title(TOP_10_TRACKS)
    st.write('This page shows the top 10 tracks for each year from 2000 to 2019.')
    st.write('You can use the sidebar to select a year and view the top 10 tracks for that year.')
    year = st.selectbox('Select a year:', list(range(1999, 2020)))
    st.write(top_10_year(year))
    st.markdown("<h2 style='text-align: center;'>Features</h2>", unsafe_allow_html=True)
    st.divider()
    st.write(radar_charts(year))
    # st.bar_chart(top_10_year(year))
elif page == TOP_5_ARTISTS:
    st.title(TOP_5_ARTISTS)
    st.write('This page shows the top 5 artists for each year from 2000 to 2019.')
elif page == GENRES:
    st.title(GENRES)
    st.write('This page shows the genres of the top 10 tracks for each year from 2000 to 2019.')
elif page == ANALYSIS:
    st.title(ANALYSIS)
    st.write('This page shows the analysis of the Spotify dataset.')
elif page == REPORTS:
    st.title(REPORTS)
    st.write('This page shows the reports of the Spotify dataset.')
    year = st.selectbox('Select a year:', list(range(1998, 2021)))
    st.download_button('Download CSV', 'data/spotify-charts.csv', 'Click here to download the Spotify dataset as a CSV file.')
    st.download_button('Download Excel', 'data/spotify-charts.xlxs', 'Click here to download the Spotify dataset as an Excel file.')
    st.download_button('Download PDF', 'data/spotify-charts.pdf', 'Click here to download the Spotify dataset as a PDF file.')