import streamlit as st
import requests
from datetime import datetime
import time

class ArchaeologyChat:
    def __init__(self):
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        # Get URL from config
        from config import config
        self.qa_service_url = config.cloud_function_url
        
        if not self.qa_service_url:
            st.error("Cloud Function URL not configured. Please set CLOUD_FUNCTION_URL environment variable.")
            st.stop()

    def get_answer(self, question: str) -> dict:
        try:
            response = requests.post(
                self.qa_service_url,
                json={"question": question},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            st.error(f"Error getting answer: {str(e)}")
            return None

    def stream_response(self, response_text, sources):
        words = response_text.split()
        for i, word in enumerate(words):
            yield word + " "
            if i % 3 == 0:
                time.sleep(0.05)
        
        if sources:
            yield "\n\n*Sources available below ↓*"

    def render(self):
        # Container for the entire chat interface
        main_container = st.container()
        
        # Create a container for the input field that will stay at the bottom
        input_container = st.container()
        
        with main_container:
            st.title("Archaeological News Chatbot")

            # Only show examples if no messages yet
            if not st.session_state.messages:
                st.caption("Welcome to the Chatbot, this LLM is currently programmed to strictly answer questions about archaeological discoveries ONLY. Example: What are news lately about Egypt?")
            
            # Display chat messages from history
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
                    if message["role"] == "assistant" and "sources" in message:
                        with st.expander("Sources", expanded=False):
                            for source in message["sources"]:
                                st.markdown(f"""
                                **{source['title']}**  
                                {source['source']} • {source['date']}  
                                [Article]({source['url']})
                                """)

        # Chat input at the bottom
        with input_container:
            if prompt := st.chat_input("Ask about archaeological discoveries..."):
                # Add user message to chat history and display
                st.session_state.messages.append({"role": "user", "content": prompt})
                with main_container:
                    with st.chat_message("user"):
                        st.markdown(prompt)

                    # Get and display assistant response
                    with st.chat_message("assistant"):
                        response_data = self.get_answer(prompt)
                        
                        if response_data and "results" in response_data:
                            # Prepare sources
                            sources = [{
                                "title": result["title"],
                                "source": result["source"],
                                "date": datetime.fromisoformat(result["publish_date"]).strftime("%Y-%m-%d"),
                                "url": result["url"]
                            } for result in response_data["results"]]
                            
                            # Stream the response
                            formatted_response = response_data.get("formatted_response", "I apologize, but I couldn't generate a response.")
                            response = st.write_stream(self.stream_response(formatted_response, sources))
                            
                            # Show sources in expander
                            with st.expander("Sources", expanded=False):
                                for source in sources:
                                    st.markdown(f"""
                                    **{source['title']}**  
                                    {source['source']} • {source['date']}  
                                    [Article]({source['url']})
                                    """)
                            
                            # Add to chat history
                            st.session_state.messages.append({
                                "role": "assistant", 
                                "content": response,
                                "sources": sources
                            })
                        else:
                            error_msg = "I apologize, but I encountered an error. Please try again."
                            st.markdown(error_msg)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": error_msg
                            })
        
        # Clear chat button - in sidebar to avoid layout shifts
        if st.session_state.messages:
            with st.sidebar:
                if st.button("Clear Chat", type="primary"):
                    st.session_state.messages = []
                    st.rerun()