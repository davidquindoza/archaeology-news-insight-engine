import streamlit as st
from services.bigquery_service import LocationService
from services.news_service import NewsService
from components.map import DiscoveryMap
from components.news import NewsSection
from components.qa import ArchaeologyChat

def main():
    # Page config
    st.set_page_config(
        page_title="Archaeological News Hub",
        page_icon="📜",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    st.title("Archaeological News Hub")
    
    # Initialize services
    location_service = LocationService()
    news_service = NewsService()
    chat = ArchaeologyChat()
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Discovery Map", "Chat Assistant", "Recent News"])
    
    try:
        with tab1:
            # Map Section
            locations = location_service.get_discovery_locations(limit=15)
            if locations:
                discovery_map = DiscoveryMap()
                discovery_map.render(locations)
            else:
                st.warning("No location data available.")
        
        with tab2:
            # Chat Interface
            chat.render()
        
        with tab3:
            # News Section
            news_items = news_service.get_recent_news()
            if news_items:
                news_section = NewsSection()
                news_section.render(news_items)
            else:
                st.warning("No recent news available.")
                
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

if __name__ == "__main__":
    main()