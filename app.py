import streamlit as st
import pandas as pd
from src import read_data, top_10_tracks, top_10_year, top_5_artists, top_5_artists_year, summary_plots, data_year, \
    create_spider_plot, create_stacked_bar_plot, create_scatter_plot, \
    create_bubble_plot, create_genre_plot, \
    generate_pdf_report, generate_excel_report, download_excel_report

SELECT_YEAR_PROMPT = 'Select a year:'

# Custom CSS for better styling
def add_custom_css():
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #1DB954, #191414);
        color: white;
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1DB954;
        margin: 0.5rem 0;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        color: #1DB954;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #666;
        text-transform: uppercase;
    }
    
    .sidebar-info {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #e9ecef;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding-left: 20px;
        padding-right: 20px;
        border-radius: 10px 10px 0 0;
        background-color: #f0f2f6;
        border: 1px solid #e0e0e0;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1DB954;
        color: white;
    }
    
    .chart-container {
        background-color: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Cache data loading for better performance
@st.cache_data
def load_spotify_data():
    """Load and cache the Spotify dataset"""
    return read_data()

def show_dataset_summary():
    """Display key metrics about the dataset"""
    data = load_spotify_data()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(data):,}</div>
            <div class="metric-label">Total Tracks</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{data['artist'].nunique():,}</div>
            <div class="metric-label">Unique Artists</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        year_range = f"{data['year'].min()}-{data['year'].max()}"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{year_range}</div>
            <div class="metric-label">Year Range</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        genres_count = data['genre'].str.split(',').explode().nunique()
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{genres_count:,}</div>
            <div class="metric-label">Unique Genres</div>
        </div>
        """, unsafe_allow_html=True)

def run():
    st.set_page_config(
        page_title='Spotify Dashboard', 
        page_icon='🎵', 
        layout='wide',  # Changed to wide for better use of space
        initial_sidebar_state='expanded'  # Show sidebar by default
    )
    
    # Add custom CSS
    add_custom_css()
    
    # Create main header
    st.markdown("""
    <div class="main-header">
        <h1>🎵 Spotify Music Analytics Dashboard</h1>
        <p>Explore and analyze Spotify tracks from 2000-2019</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Show dataset summary
    show_dataset_summary()
    
    st.divider()

    menu_data = st.tabs(['Home',
                        'Top 10 Tracks',
                        'Top 5 Artists',
                        'Genres',
                        'Analysis',
                        'Reports'])

    with menu_data[0]:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📊 Welcome to the Spotify Dashboard!")
            st.markdown("""
            This comprehensive dashboard analyzes **Top Hits Spotify tracks from 2000-2019**, providing insights into:
            
            - 🎵 **Track Analysis**: Explore the most popular songs and their audio features
            - 🎤 **Artist Insights**: Discover top-performing artists across different years  
            - 🎭 **Genre Trends**: Understand genre popularity over time
            - 📈 **Interactive Visualizations**: Dive deep with customizable charts and filters
            - 📄 **Export Reports**: Download data in CSV, Excel, and PDF formats
            
            **Navigate through the tabs above to start exploring!**
            """)
            
            # Interactive data preview
            with st.expander("📋 Dataset Preview", expanded=False):
                data_sample = load_spotify_data().head(10)
                st.dataframe(
                    data_sample, 
                    use_container_width=True,
                    hide_index=True
                )
        
        with col2:
            st.markdown("### 📈 Quick Stats")
            data = load_spotify_data()
            
            # Most popular song
            most_popular = data.loc[data['popularity'].idxmax()]
            st.markdown(f"""
            <div class="sidebar-info">
                <h4>🔥 Most Popular Track</h4>
                <p><strong>{most_popular['song']}</strong><br>
                by {most_popular['artist']}<br>
                Popularity: {most_popular['popularity']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Year with most tracks
            year_counts = data['year'].value_counts()
            top_year = year_counts.idxmax()
            st.markdown(f"""
            <div class="sidebar-info">
                <h4>📅 Peak Year</h4>
                <p><strong>{top_year}</strong><br>
                {year_counts[top_year]:,} tracks</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Most prolific artist
            top_artist = data['artist'].value_counts().idxmax()
            artist_count = data['artist'].value_counts().iloc[0]
            st.markdown(f"""
            <div class="sidebar-info">
                <h4>🎤 Most Prolific Artist</h4>
                <p><strong>{top_artist}</strong><br>
                {artist_count} tracks in dataset</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Charts section
        st.markdown("### 📊 Tracks Per Year Analysis")
        
        # Chart options in columns
        chart_col1, chart_col2 = st.columns([3, 1])
        
        with chart_col2:
            st.markdown("**Chart Options:**")
            explicit_filter = st.checkbox('🚫 Show Explicit Content Analysis', value=False)
            show_trend = st.checkbox('📈 Show Trend Line', value=True)
        
        with chart_col1:
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            if explicit_filter:
                summary_plots(explicit=True)
            else:
                summary_plots(explicit=False)
            st.markdown('</div>', unsafe_allow_html=True)

    with menu_data[1]:
        st.markdown("### 🎵 Top 10 Tracks Analysis")
        
        # Controls in sidebar-style layout
        control_col, content_col = st.columns([1, 3])
        
        with control_col:
            st.markdown("#### 🎛️ Controls")
            year = st.selectbox(
                SELECT_YEAR_PROMPT, 
                ['All Time'] + list(range(1999, 2020)), 
                key='top_10_tracks',
                help="Select a specific year or 'All Time' for overall rankings"
            )
            
            show_table = st.checkbox("📊 Show Data Table", value=True)
            show_charts = st.checkbox("📈 Show Radar Charts", value=True)
            
            if year != 'All Time':
                st.markdown(f"**Analyzing year: {year}**")
            else:
                st.markdown("**Analyzing all-time favorites**")
        
        with content_col:
            if year == 'All Time':
                tracks_data = top_10_tracks()
                st.markdown("#### 🏆 All-Time Top 10 Tracks")
                
                if show_table:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    # Enhanced dataframe display
                    df_display = tracks_data.copy()
                    df_display['popularity'] = df_display['popularity'].astype(int)
                    df_display = df_display.round(3)
                    st.dataframe(
                        df_display, 
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "song": st.column_config.TextColumn("🎵 Song", width="medium"),
                            "artist": st.column_config.TextColumn("🎤 Artist", width="medium"),
                            "popularity": st.column_config.NumberColumn("⭐ Popularity", format="%d"),
                            "danceability": st.column_config.NumberColumn("💃 Danceability", format="%.3f"),
                            "energy": st.column_config.NumberColumn("⚡ Energy", format="%.3f"),
                            "loudness": st.column_config.NumberColumn("🔊 Loudness", format="%.1f"),
                            "liveness": st.column_config.NumberColumn("🎪 Liveness", format="%.3f"),
                            "tempo": st.column_config.NumberColumn("🎶 Tempo", format="%.1f")
                        }
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if show_charts:
                    st.divider()
                    st.markdown("#### 🕸️ Audio Features Comparison")
                    create_spider_plot(year, all_tracks=True)
            
            elif year:
                tracks_data = top_10_year(year)
                st.markdown(f"#### 🏆 Top 10 Tracks of {year}")
                
                if show_table:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    # Enhanced dataframe display
                    df_display = tracks_data.copy()
                    df_display['popularity'] = df_display['popularity'].astype(int)
                    df_display = df_display.round(3)
                    st.dataframe(
                        df_display, 
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "song": st.column_config.TextColumn("🎵 Song", width="medium"),
                            "artist": st.column_config.TextColumn("🎤 Artist", width="medium"),
                            "popularity": st.column_config.NumberColumn("⭐ Popularity", format="%d"),
                            "danceability": st.column_config.NumberColumn("💃 Danceability", format="%.3f"),
                            "energy": st.column_config.NumberColumn("⚡ Energy", format="%.3f"),
                            "loudness": st.column_config.NumberColumn("🔊 Loudness", format="%.1f"),
                            "liveness": st.column_config.NumberColumn("🎪 Liveness", format="%.3f"),
                            "tempo": st.column_config.NumberColumn("🎶 Tempo", format="%.1f")
                        }
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if show_charts:
                    st.divider()
                    st.markdown("#### 🕸️ Audio Features Comparison")
                    create_spider_plot(year)

    with menu_data[2]:
        st.markdown("### 🎤 Top 5 Artists Analysis")
        
        # Controls and content layout
        control_col, content_col = st.columns([1, 3])
        
        with control_col:
            st.markdown("#### 🎛️ Controls")
            year = st.selectbox(
                SELECT_YEAR_PROMPT, 
                ['All Time'] + list(range(1999, 2020)), 
                key='top_5_artists',
                help="Select a specific year or 'All Time' for overall rankings"
            )
            
            show_details = st.checkbox("📊 Show Artist Details", value=True)
            show_comparison = st.checkbox("📊 Show Feature Comparison", value=True)
        
        with content_col:
            if year == 'All Time':
                artists_data = top_5_artists()
                st.markdown("#### 🏆 All-Time Top 5 Artists")
                
                if show_details:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    df_display = artists_data.copy()
                    df_display['popularity'] = df_display['popularity'].astype(int)
                    df_display = df_display.round(3)
                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "artist": st.column_config.TextColumn("🎤 Artist", width="medium"),
                            "popularity": st.column_config.NumberColumn("⭐ Popularity", format="%d"),
                            "danceability": st.column_config.NumberColumn("💃 Danceability", format="%.3f"),
                            "energy": st.column_config.NumberColumn("⚡ Energy", format="%.3f"),
                            "loudness": st.column_config.NumberColumn("🔊 Loudness", format="%.1f"),
                            "liveness": st.column_config.NumberColumn("🎪 Liveness", format="%.3f"),
                            "tempo": st.column_config.NumberColumn("🎶 Tempo", format="%.1f")
                        }
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if show_comparison:
                    st.divider()
                    st.markdown("#### 📊 Artist Feature Comparison")
                    create_stacked_bar_plot(None, all_time=True)
            
            elif year:
                artists_data = top_5_artists_year(year)
                st.markdown(f"#### 🏆 Top 5 Artists of {year}")
                
                if show_details:
                    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                    df_display = artists_data.copy()
                    df_display['popularity'] = df_display['popularity'].astype(int)
                    df_display = df_display.round(3)
                    st.dataframe(
                        df_display,
                        use_container_width=True,
                        hide_index=True,
                        column_config={
                            "artist": st.column_config.TextColumn("🎤 Artist", width="medium"),
                            "popularity": st.column_config.NumberColumn("⭐ Popularity", format="%d"),
                            "danceability": st.column_config.NumberColumn("💃 Danceability", format="%.3f"),
                            "energy": st.column_config.NumberColumn("⚡ Energy", format="%.3f"),
                            "loudness": st.column_config.NumberColumn("🔊 Loudness", format="%.1f"),
                            "liveness": st.column_config.NumberColumn("🎪 Liveness", format="%.3f"),
                            "tempo": st.column_config.NumberColumn("🎶 Tempo", format="%.1f")
                        }
                    )
                    st.markdown('</div>', unsafe_allow_html=True)
                
                if show_comparison:
                    st.divider()
                    st.markdown("#### 📊 Artist Feature Comparison")
                    create_stacked_bar_plot(year)

    with menu_data[3]:
        st.markdown("### 🎭 Genre Analysis & Interactive Filters")
        
        # Genre overview
        st.markdown("#### 📊 Genre Distribution")
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        create_genre_plot()
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # Interactive filtering section
        st.markdown("#### 🎛️ Interactive Audio Features Explorer")
        st.markdown("*Explore how different audio features correlate by year and genre*")
        
        # Filter controls in a nice layout
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            year = st.selectbox(
                SELECT_YEAR_PROMPT, 
                list(range(1998, 2021)), 
                index=None, 
                key='genres',
                help="Select a year to filter the bubble chart"
            )
        
        with filter_col2:
            x_axis_options = ["danceability", "energy", "loudness", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo"]
            x = st.selectbox(
                '📊 X-axis Feature', 
                x_axis_options, 
                index=0,
                help="Choose the audio feature for the X-axis"
            )
        
        with filter_col3:
            y = st.selectbox(
                '📊 Y-axis Feature', 
                x_axis_options, 
                index=2,
                help="Choose the audio feature for the Y-axis"
            )
        
        # Feature descriptions
        feature_descriptions = {
            "danceability": "💃 How suitable a track is for dancing (0.0 to 1.0)",
            "energy": "⚡ Intensity and activity measure (0.0 to 1.0)",
            "loudness": "🔊 Overall loudness in decibels (dB)",
            "speechiness": "🗣️ Presence of spoken words (0.0 to 1.0)",
            "acousticness": "🎸 Whether the track is acoustic (0.0 to 1.0)",
            "instrumentalness": "🎼 Whether a track contains no vocals (0.0 to 1.0)",
            "liveness": "🎪 Presence of live audience (0.0 to 1.0)",
            "valence": "😊 Musical positiveness (0.0 to 1.0)",
            "tempo": "🎶 Speed of the track (BPM)"
        }
        
        # Show selected feature descriptions
        desc_col1, desc_col2 = st.columns(2)
        with desc_col1:
            st.info(f"**X-axis**: {feature_descriptions.get(x, x)}")
        with desc_col2:
            st.info(f"**Y-axis**: {feature_descriptions.get(y, y)}")
        
        # Validation and chart display
        if x == y:
            st.error("⚠️ Please select different features for X-axis and Y-axis to create a meaningful comparison.")
        elif year:
            st.markdown(f"#### 🎯 Audio Features Analysis for {year}")
            st.markdown(f"*Comparing **{x}** vs **{y}** - bubble size represents popularity, colors represent genres*")
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            create_bubble_plot(year, x, y)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("🎯 Select a year above to explore the interactive audio features chart!")

    with menu_data[4]:
        st.markdown("### 📈 Advanced Analysis")
        
        # Analysis options
        analysis_col1, analysis_col2 = st.columns([1, 3])
        
        with analysis_col1:
            st.markdown("#### 🎛️ Analysis Options")
            
            analysis_type = st.radio(
                "Select Analysis Type:",
                ["📊 Feature Correlation", "📈 Trend Analysis", "🎯 Detailed Scatter Plot"],
                help="Choose the type of analysis to perform"
            )
            
            if analysis_type == "📈 Trend Analysis":
                feature_to_analyze = st.selectbox(
                    "Feature to Analyze:",
                    ["danceability", "energy", "loudness", "valence", "tempo", "popularity"],
                    help="Select which audio feature to analyze over time"
                )
        
        with analysis_col2:
            if analysis_type == "📊 Feature Correlation":
                st.markdown("#### 🔗 Audio Feature Correlation Analysis")
                st.markdown("*Explore relationships between danceability, loudness, year, and popularity*")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                create_scatter_plot()
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Add correlation insights
                st.markdown("##### 💡 Insights")
                data = load_spotify_data()
                correlation = data[['danceability', 'loudness', 'popularity']].corr()
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Danceability ↔ Popularity", 
                        f"{correlation.loc['danceability', 'popularity']:.3f}",
                        help="Correlation between danceability and popularity"
                    )
                with col2:
                    st.metric(
                        "Loudness ↔ Popularity", 
                        f"{correlation.loc['loudness', 'popularity']:.3f}",
                        help="Correlation between loudness and popularity"
                    )
            
            elif analysis_type == "📈 Trend Analysis":
                st.markdown(f"#### 📈 {feature_to_analyze.title()} Trend Over Time")
                
                # Create trend analysis
                data = load_spotify_data()
                yearly_avg = data.groupby('year')[feature_to_analyze].mean().reset_index()
                
                import altair as alt
                
                trend_chart = alt.Chart(yearly_avg).mark_line(
                    point=True, 
                    strokeWidth=3,
                    color='#1DB954'
                ).encode(
                    x=alt.X('year:O', title='Year'),
                    y=alt.Y(f'{feature_to_analyze}:Q', title=feature_to_analyze.title()),
                    tooltip=['year', f'{feature_to_analyze}:Q']
                ).properties(
                    width=600,
                    height=400,
                    title=f'Average {feature_to_analyze.title()} by Year'
                )
                
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                st.altair_chart(trend_chart, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show trend insights
                trend_direction = "increasing" if yearly_avg[feature_to_analyze].iloc[-1] > yearly_avg[feature_to_analyze].iloc[0] else "decreasing"
                st.info(f"📊 **Trend**: {feature_to_analyze.title()} shows an overall {trend_direction} trend from 2000 to 2019.")
            
            else:  # Detailed Scatter Plot
                st.markdown("#### 🎯 Detailed Audio Features Scatter Plot")
                st.markdown("*Interactive visualization showing relationships between multiple audio features*")
                st.markdown('<div class="chart-container">', unsafe_allow_html=True)
                create_scatter_plot()
                st.markdown('</div>', unsafe_allow_html=True)

    with menu_data[5]:
        st.markdown("### 📄 Export Reports & Data")
        
        # Report options layout
        report_col1, report_col2 = st.columns([1, 2])
        
        with report_col1:
            st.markdown("#### 🎛️ Export Options")
            
            year = st.selectbox(
                SELECT_YEAR_PROMPT, 
                ['All Data'] + list(range(1998, 2021)), 
                index=None, 
                key='reports',
                help="Select 'All Data' for complete dataset or specific year"
            )
            
            if year:
                st.markdown("**Available Formats:**")
                export_csv = st.checkbox("📊 CSV Data Export", value=True)
                export_excel = st.checkbox("📈 Excel Report with Charts", value=True)
                export_pdf = st.checkbox("📄 PDF Analytical Report", value=True)
        
        with report_col2:
            if year == 'All Data':
                st.markdown("#### 📦 Complete Dataset Export")
                st.markdown("*Export the entire Spotify dataset (2000-2019)*")
                
                data = load_spotify_data()
                st.markdown(f"**Dataset Overview:**")
                st.markdown(f"- 📊 **{len(data):,}** total tracks")
                st.markdown(f"- 🎤 **{data['artist'].nunique():,}** unique artists")
                st.markdown(f"- 📅 **{data['year'].nunique()}** years of data")
                st.markdown(f"- 🎭 **{data['genre'].str.split(',').explode().nunique()}** unique genres")
                
                st.divider()
                
                # Download buttons with better styling
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if export_csv:
                        st.download_button(
                            '📊 Download CSV',
                            data.to_csv(index=False),
                            'SpotifyData_Complete.csv',
                            mime='text/csv',
                            help="Download complete dataset as CSV"
                        )
                
                with col2:
                    if export_excel:
                        st.info("💡 Excel export for complete dataset coming soon!")
                
                with col3:
                    if export_pdf:
                        try:
                            pdf_data = generate_pdf_report()
                            st.download_button(
                                '📄 Download PDF Report',
                                pdf_data,
                                'Spotify_Complete_Report_2000-2019.pdf',
                                mime='application/pdf',
                                help="Download comprehensive PDF report"
                            )
                        except Exception as e:
                            st.error(f"PDF generation error: {str(e)}")
            
            elif year is not None:
                st.markdown(f"#### 📋 Year {year} Report")
                st.markdown(f"*Export data and analysis for year {year}*")
                
                # Show year statistics
                year_data = load_spotify_data()[load_spotify_data()['year'] == year]
                
                if len(year_data) > 0:
                    st.markdown(f"**Year {year} Overview:**")
                    st.markdown(f"- 📊 **{len(year_data):,}** tracks")
                    st.markdown(f"- 🎤 **{year_data['artist'].nunique():,}** unique artists")
                    st.markdown(f"- ⭐ **{year_data['popularity'].mean():.1f}** average popularity")
                    st.markdown(f"- 🎵 Most popular: **{year_data.loc[year_data['popularity'].idxmax(), 'song']}**")
                    
                    st.divider()
                    
                    # Download buttons
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if export_csv:
                            st.download_button(
                                '📊 Download CSV',
                                data_year(year),
                                f'SpotifyData_{year}.csv',
                                mime='text/csv',
                                help=f"Download {year} data as CSV"
                            )
                    
                    with col2:
                        if export_excel:
                            try:
                                wb = generate_excel_report(year)
                                excel_file = download_excel_report(wb)
                                st.download_button(
                                    '📈 Download Excel',
                                    excel_file,
                                    f'Spotify_Report_{year}.xlsx',
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    help=f"Download {year} Excel report with charts"
                                )
                            except Exception as e:
                                st.error(f"Excel generation error: {str(e)}")
                    
                    with col3:
                        if export_pdf:
                            try:
                                pdf_file = generate_pdf_report(str(year))
                                st.download_button(
                                    '📄 Download PDF',
                                    pdf_file,
                                    f'Spotify_Report_{year}.pdf',
                                    mime='application/pdf',
                                    help=f"Download {year} PDF report"
                                )
                            except Exception as e:
                                st.error(f"PDF generation error: {str(e)}")
                else:
                    st.warning(f"⚠️ No data found for year {year}")
            
            else:
                st.info("👆 Select a year or 'All Data' above to see export options")
                
                # Show general information
                st.markdown("#### ℹ️ About Reports")
                st.markdown("""
                **Available Export Formats:**
                
                - **📊 CSV**: Raw data in spreadsheet format
                - **📈 Excel**: Formatted reports with charts and analysis
                - **📄 PDF**: Comprehensive analytical reports with visualizations
                
                **Report Contents:**
                - Top tracks and artists analysis
                - Audio features breakdown
                - Genre distribution
                - Popularity trends
                - Statistical summaries
                """)

if __name__ == "__main__":
    run()
