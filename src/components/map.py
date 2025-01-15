# src/components/map.py

import streamlit as st
import folium
from streamlit_folium import st_folium
from typing import List, Dict, Any

class DiscoveryMap:
    def __init__(self):
        self.default_location = [20, 0]  # Center of the map
        self.default_zoom = 2

    def create_popup_html(self, location: Dict[str, Any]) -> str:
        """Creates HTML content for marker popups"""
        return f"""
            <div style='width: 200px'>
                <h4 style='margin-bottom: 8px;'>{location['title']}</h4>
                <p style='margin-bottom: 4px;'><strong>Location:</strong> {location['location']}</p>
                <p style='margin-bottom: 4px;'><strong>Date:</strong> {location['date']}</p>
                <p style='margin-bottom: 4px;'><strong>Source:</strong> {location['source']}</p>
                <a href='{location['url']}' target='_blank'>Read More</a>
            </div>
        """

    def render(self, locations: List[Dict[str, Any]]) -> None:
        """Creates and displays the map with discoveries"""
        st.subheader("Map of New Discoveries")
        
        # Create base map
        m = folium.Map(
            location=self.default_location,
            zoom_start=self.default_zoom,
            tiles='cartodb positron'  # Clean, modern style
        )

        # Add markers for each location
        for loc in locations:
            popup_html = self.create_popup_html(loc)
            
            folium.Marker(
                location=loc['coordinates'],
                popup=folium.Popup(popup_html, max_width=300),
                tooltip=loc['title'],
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)

        # Display the map
        st_folium(
            m,
            height=500,  # Adjusted height for better viewing
            width="100%",
            returned_objects=["last_active_drawing"],
            key="discovery_map"
        )

# Only for testing the component directly
if __name__ == "__main__":
    st.set_page_config(layout="wide")
    
    # Sample data for testing
    sample_locations = [
        {
            "title": "Test Discovery",
            "location": "Test Location",
            "coordinates": [0, 0],
            "date": "2024-01-01",
            "source": "Test Source",
            "url": "http://example.com"
        }
    ]
    
    map_component = DiscoveryMap()
    map_component.render(sample_locations)