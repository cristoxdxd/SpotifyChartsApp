import streamlit as st
from src import read_data, top_10_tracks, top_10_year, top_5_artists, top_5_artists_year, summary_plots, data_year, \
    create_spider_plot, create_stacked_bar_plot, create_scatter_plot, \
    create_bubble_plot, create_genre_plot, \
    generate_pdf_report, generate_excel_report, download_excel_report

SELECT_YEAR_PROMPT = 'Select a year:'

def run():
    st.set_page_config(page_title='Spotify Dashboard', 
                    page_icon='./public/icon.png', 
                    layout='centered', 
                    initial_sidebar_state='collapsed')

    st.title('Spotify Dashboard')
    st.divider()

    menu_data = st.tabs(['Home',
                        'Top 10 Tracks',
                        'Top 5 Artists',
                        'Genres',
                        'Analysis',
                        'Reports'])

    with menu_data[0]:
        st.write('Welcome to the Spotify Dashboard!')
        st.write('This is a complete dataset of Spotify tracks from 2000 to 2019.')
        st.write('This app is a Streamlit dashboard that can be used to analyze the Spotify tracks dataset.')
        st.write('You can select different pages from the sidebar to explore the dataset.')
        with st.expander("Data Preview"):
            st.write(read_data())
        st.divider()
        st.markdown("<h2 style='text-align: center;'>Number of songs per year on Spotify</h2>", unsafe_allow_html=True)
        explicit_filter = st.checkbox('Show Explicits', value=False)
        if explicit_filter:
            summary_plots(explicit=True)
        else:
            summary_plots(explicit=False)

    with menu_data[1]:
        st.title('Top 10 Tracks')
        year = st.selectbox(SELECT_YEAR_PROMPT, ['All'] + list(range(1999, 2020)), key='top_10_tracks')
        if year == 'All':
            st.write(top_10_tracks())
            st.divider()
            st.write(create_spider_plot(year, all_tracks=True))
        elif year:
            st.write(top_10_year(year))
            st.divider()
            st.write(create_spider_plot(year))

    with menu_data[2]:
        st.title('Top 5 Artists')
        st.write('This page shows the top 5 artists for each year from 2000 to 2019.')
        year = st.selectbox(SELECT_YEAR_PROMPT, ['All'] + list(range(1999, 2020)), key='top_5_artists')
        if year == 'All':
            st.write(top_5_artists())
            st.divider()
            st.write(create_stacked_bar_plot(None, all_time=True))
        elif year:
            st.write(top_5_artists_year(year))
            st.divider()
            st.write(create_stacked_bar_plot(year))

    with menu_data[3]:
        st.title('Genres')
        create_genre_plot()
        st.markdown("<h2 style='text-align: center;'>Play with Filters</h2>", unsafe_allow_html=True)
        year = st.selectbox(SELECT_YEAR_PROMPT, list(range(1998, 2021)), index=None, key='genres')
        x = st.selectbox('X-axis', ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"], index=0)
        y = st.selectbox('Y-axis', ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"], index=2)
        if x == y:
            st.error("Please select different values for X-axis and Y-axis.")
            st.stop()
        if year:
            create_bubble_plot(year, x, y)

    with menu_data[4]:
        st.title('Analysis')
        st.write('This page shows the analysis of the Spotify dataset.')
        create_scatter_plot()

    with menu_data[5]:
        st.title('Reports')
        st.write('This page shows the reports of the Spotify dataset.')
        year = st.selectbox(SELECT_YEAR_PROMPT, ['All'] + list(range(1998, 2021)), index=None, key='reports')
        if year == 'All':
            st.download_button('Download CSV', read_data().to_csv(index=False), 'SpotifyData_CSV.csv')
            # st.download_button('Download Excel', generate_excel_report(), 'Spotify_Report_EXCEL.xlsx')
            st.download_button('Download PDF', generate_pdf_report(), 'Spotify_Full_Report_2000_2019.pdf')
        if year is not None and year != 'All':
            st.download_button('Download CSV', data_year(year), f'SpotifyData_{year}_CSV.csv')
            wb = generate_excel_report(year)
            excel_file = download_excel_report(wb)
            st.download_button('Download Excel', excel_file, f'Spotify_Report_{year}_EXCEL.xlsx', mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            
            st.download_button('Download PDF', generate_pdf_report(str(year)), f'Spotify_Report_{year}_PDF.pdf')

if __name__ == "__main__":
    run()