import streamlit as st
from typing import List, Dict, Any

class NewsSection:
    def __init__(self):
        # Style for the read more button
        st.markdown("""
            <style>
            .stButton > button {
                background: none;
                border: none;
                color: #1e88e5;
                font-weight: 500;
                padding: 0;
            }
            .stButton > button:hover {
                color: #1565c0;
                text-decoration: underline;
            }
            </style>
        """, unsafe_allow_html=True)

    def render(self, news_items: List[Dict[str, Any]]) -> None:
        """Render news items in a single column with dialog functionality"""
        # Define the dialog function
        @st.dialog("Article")
        def show_article(article):
            st.header(article['title'])
            st.caption(f"📰 {article['source']} • 📅 {article['date']}")
            st.markdown("---")
            
            # Display full content
            st.write(article.get('full_content', 
                              article.get('summary', 'Content not available.')))
            
            # Link to original article
            st.link_button("Read Original Article", article['url'], 
                         use_container_width=True)

        # Container for all news items
        with st.container():
            # Generate HTML for all cards
            for idx, item in enumerate(news_items):
                # Create a container for card and button
                with st.container():
                    # Create HTML card
                    card_html = f"""
                    <div style="
                        background: white;
                        border-radius: 10px;
                        padding: 1.5rem;
                        margin-bottom: 0.5rem;
                        border: 1px solid #e0e0e0;
                        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                    ">
                        <h3 style="
                            margin: 0 0 0.75rem 0;
                            font-size: 1.2rem;
                            color: #1e88e5;
                            font-weight: 600;
                        ">{item['title']}</h3>
                        
                        <div style="
                            color: #666;
                            font-size: 0.9rem;
                            margin-bottom: 0.75rem;
                        ">
                            <span>📰 {item['source']}</span> • 
                            <span>📅 {item['date']}</span>
                        </div>
                        
                        <div style="
                            color: #444;
                            font-size: 0.95rem;
                            line-height: 1.5;
                        ">
                            {item.get('summary', '')[:150]}...
                        </div>
                    </div>
                    """
                    
                    # Display the card using st.html
                    st.html(card_html)
                    
                    # Add the Read More button
                    if st.button("Read More →", key=f"news_{idx}"):
                        show_article(item)
                    
                    # Add some spacing after each card
                    st.markdown("<div style='margin-bottom: 1.5rem;'></div>", unsafe_allow_html=True)