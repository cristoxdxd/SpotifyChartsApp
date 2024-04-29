import streamlit as st

def count_tracks(explicit: bool):
    if explicit:
        st.image('images/visualization_e.svg',  use_column_width=True)
    else:
        st.image('images/visualization.svg', use_column_width=True)

def radar_charts(year: int):
    if year < 1998 or year > 2020:
        st.error("Invalid year. Please choose a year between 1999 and 2020.")
        return

    for index in range(1, 11):
        st.image(f'images/Radar_{year}_{index}.svg')
        st.divider()