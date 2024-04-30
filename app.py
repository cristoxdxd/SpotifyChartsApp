import streamlit as st
from src import read_data, top_10_year, create_spider_plot, summary_plots

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
        st.write('This page shows the top 10 tracks for each year from 2000 to 2019.')
        st.write('You can use the sidebar to select a year and view the top 10 tracks for that year.')
        year = st.selectbox('Select a year:', list(range(1999, 2020)))
        st.write(top_10_year(year))
        st.divider()
        st.write(create_spider_plot(year))

    with menu_data[2]:
        st.title('Top 5 Artists')
        st.write('This page shows the top 5 artists for each year from 2000 to 2019.')

    with menu_data[3]:
        st.title('Genres')
        st.write('This page shows the genres of the top 10 tracks for each year from 2000 to 2019.')

    with menu_data[4]:
        st.title('Analysis')
        st.write('This page shows the analysis of the Spotify dataset.')

    with menu_data[5]:
        st.title('Reports')
        st.write('This page shows the reports of the Spotify dataset.')
        # year = st.selectbox('Select a year:', list(range(1998, 2021)))
        st.download_button('Download CSV', 'data/spotify-charts.csv', 'Click here to download the Spotify dataset as a CSV file.')
        st.download_button('Download Excel', 'data/spotify-charts.xlxs', 'Click here to download the Spotify dataset as an Excel file.')
        st.download_button('Download PDF', 'data/spotify-charts.pdf', 'Click here to download the Spotify dataset as a PDF file.')

if __name__ == "__main__":
    run()