# src/app.py

import streamlit as st
from services.bigquery_service import LocationService
from services.news_service import NewsService
from components.map import DiscoveryMap
from components.news import NewsSection

def main():
    # Page config
    st.set_page_config(
        page_title="Archaeological News Hub",
        page_icon="📜",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Archaeological News Hub by David")
    
    # Initialize services
    location_service = LocationService()
    news_service = NewsService()
    
    try:
        # Map Section - Full Width
        locations = location_service.get_discovery_locations(limit=15)
        if locations:
            discovery_map = DiscoveryMap()
            discovery_map.render(locations)
        else:
            st.warning("No location data available.")
        
        # Add some spacing
        st.markdown("<div style='margin: 30px 0;'></div>", unsafe_allow_html=True)
        
        # News Section - Below Map
        st.subheader("Recent Archaeological News")
        news_items = news_service.get_recent_news()  # Show 6 articles (2x3 grid)
        if news_items:
            news_section = NewsSection()
            news_section.render(news_items)
        else:
            st.warning("No recent news available.")
                
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    main()