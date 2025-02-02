import requests
import streamlit as st
from dotenv import load_dotenv
import os
from requests.exceptions import Timeout, RequestException

load_dotenv()

# Load configuration from environment variables
BASE_API_URL = os.getenv("BASE_API_URL")
LANGFLOW_ID = os.getenv("LANGFLOW_ID")
FLOW_ID = os.getenv("FLOW_ID")
APPLICATION_TOKEN = os.getenv("APPLICATION_TOKEN")

def run_flow(message: str) -> dict:
    """
    Send a message to the Langflow API and get the response.
    
    Args:
        message (str): The input message to process
        
    Returns:
        dict: The API response
        
    Raises:
        RuntimeError: If the API request fails
    """
    if not all([BASE_API_URL, LANGFLOW_ID, FLOW_ID, APPLICATION_TOKEN]):
        raise ValueError("Missing required environment variables")

    api_url = f"{BASE_API_URL}/lf/{LANGFLOW_ID}/api/v1/run/{FLOW_ID}"

    payload = {
        "input_value": message,
        "output_type": "chat",
        "input_type": "chat",
    }

    headers = {
        "Authorization": f"Bearer {APPLICATION_TOKEN}", 
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            api_url, 
            json=payload, 
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the message text from the nested structure
        if (response_data 
            and 'outputs' in response_data 
            and len(response_data['outputs']) > 0 
            and 'outputs' in response_data['outputs'][0] 
            and len(response_data['outputs'][0]['outputs']) > 0 
            and 'results' in response_data['outputs'][0]['outputs'][0] 
            and 'message' in response_data['outputs'][0]['outputs'][0]['results']):
            
            message_data = response_data['outputs'][0]['outputs'][0]['results']['message']
            
            # First try to get text directly if it's not an agent message
            if 'text' in message_data:
                text = message_data['text']
                if not text.startswith('Agent') and not text.startswith('{'):
                    return text
            
            # If that fails, try to get the response from content blocks
            if 'content_blocks' in message_data:
                for block in message_data['content_blocks']:
                    if 'contents' in block:
                        for content in block['contents']:
                            if (content.get('type') == 'text' 
                                and content.get('header', {}).get('title') == 'Output' 
                                and 'text' in content):
                                return content['text']
            
            # If we still haven't found a response, try artifacts
            if ('artifacts' in response_data['outputs'][0]['outputs'][0] 
                and 'message' in response_data['outputs'][0]['outputs'][0]['artifacts']):
                return response_data['outputs'][0]['outputs'][0]['artifacts']['message']
            
        return "Sorry, I couldn't process that request."
        
    except Timeout:
        raise RuntimeError("Request timed out. The API took too long to respond.")
    except RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            if e.response.status_code == 401:
                raise RuntimeError("Authentication failed. Please check your APPLICATION_TOKEN.")
            elif e.response.status_code == 404:
                raise RuntimeError("Flow not found. Please check your FLOW_ID and LANGFLOW_ID.")
            elif e.response.status_code == 403:
                raise RuntimeError("Access forbidden. Please check your permissions.")
            else:
                error_message = e.response.text if e.response.text else str(e)
                raise RuntimeError(f"API request failed: {error_message}")
        else:
            raise RuntimeError(f"API request failed: {str(e)}")

def main():
    st.title("Chat Interface")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask something..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        try:
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = run_flow(prompt)
                    st.markdown(response)
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Error: {str(e)}")

if __name__ == "__main__":
    main()