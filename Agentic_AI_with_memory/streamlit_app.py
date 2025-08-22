import streamlit as st
import sys
import os
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.client import StardogClient
from src.core.agent import StardogAgent
from src.core.memory import SessionMemory
from src.workflow.graph import build_workflow
from src.config.settings import STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD, OPENAI_API_KEY

# Page configuration
st.set_page_config(
    page_title="Knowledge Graph Chatbot",
    page_icon="🤖",
    layout="centered"
)

# Enhanced CSS for better styling
st.markdown("""
<style>
    /* Main container styling */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        margin-bottom: 30px;
        color: white;
    }
    
    /* Status indicator styling */
    .status-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
        padding: 10px 15px;
        border-radius: 10px;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
    }
    
    .status-indicator {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 10px;
        animation: pulse 2s infinite;
    }
    
    .status-connected {
        background-color: #10b981;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
    }
    
    .status-disconnected {
        background-color: #ef4444;
        box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
    }
    
    @keyframes pulse {
        0% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        }
        70% {
            box-shadow: 0 0 0 10px rgba(16, 185, 129, 0);
        }
        100% {
            box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
        }
    }
    
    /* Message styling */
    .message {
        margin-bottom: 20px;
        display: flex;
        align-items: flex-start;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        justify-content: flex-end;
    }
    
    .bot-message {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 75%;
        padding: 15px 20px;
        border-radius: 20px;
        word-wrap: break-word;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: all 0.2s ease;
    }
    
    .message-bubble:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 5px;
    }
    
    .bot-bubble {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-bottom-left-radius: 5px;
    }
    
    /* Input area styling */
    .input-container {
        position: relative;
        padding: 15px;
        border-radius: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 1px solid #e5e7eb;
        margin-top: 20px;
    }
    
    .stTextInput > div > div > input {
        border-radius: 20px;
        border: 2px solid #e5e7eb;
        padding: 12px 20px;
        padding-right: 160px;
        font-size: 16px;
        transition: all 0.3s ease;
        width: 100%;
        box-sizing: border-box;
        height: 48px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stButton > button {
        position: absolute;
        right: 20px;
        top: 6px;
        border-radius: 15px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
        min-width: 60px;
        z-index: 10;
        height: 36px;
        line-height: 1;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0;
    }
    
    /* Clear button styling */
    .stButton > button[data-testid="baseButton-secondary"] {
        right: -260px;
        background-color: #6c757d;
        color: white;
    }
    
    .stButton > button[data-testid="baseButton-secondary"]:hover {
        background-color: #5a6268;
    }
        
    /* Hide input label */
    .stTextInput > label {
        display: none;
    }
    
    /* Dataframe styling */
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 15px 0;
    }
    
    /* Welcome message styling */
    .welcome-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
    }
    
    /* Error message styling */
    .error-message {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    /* Success message styling */
    .success-message {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

def render_chat_message(message, is_user=True, data=None):
    """Render a chat message with proper styling"""
    if is_user:
        st.markdown(f"""
        <div class="message user-message">
            <div class="message-bubble user-bubble">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message bot-message">
            <div class="message-bubble bot-bubble">
                {message}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # If there's data to display as a table
        if data is not None:
            try:
                import pandas as pd
                if isinstance(data, pd.DataFrame):
                    st.dataframe(data, use_container_width=True, height=300)
                elif isinstance(data, list):
                    df = pd.DataFrame(data)
                    st.dataframe(df, use_container_width=True, height=300)
            except Exception as e:
                st.error(f"Error displaying data: {str(e)}")

def initialize_agent():
    """Initialize the Stardog agent with memory"""
    try:
        # Check if environment variables are set
        missing_vars = []
        if not STARDOG_ENDPOINT:
            missing_vars.append("STARDOG_ENDPOINT")
        if not STARDOG_DATABASE:
            missing_vars.append("STARDOG_DATABASE")
        if not STARDOG_USERNAME:
            missing_vars.append("STARDOG_USERNAME")
        if not STARDOG_PASSWORD:
            missing_vars.append("STARDOG_PASSWORD")
        if not OPENAI_API_KEY:
            missing_vars.append("OPENAI_API_KEY")
        
        if missing_vars:
            return None, None, f"Missing environment variables: {', '.join(missing_vars)}"
        
        # Initialize Stardog client
        stardog_client = StardogClient(STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD)
        
        # Test connection
        test_result = stardog_client.query("SELECT ?s WHERE { ?s ?p ?o } LIMIT 1")
        if test_result is None:
            return None, None, "Failed to connect to Stardog. Please check your connection settings."
        
        # Initialize agent
        agent = StardogAgent(stardog_client)
        
        # Initialize memory with the agent's LLM for semantic similarity
        memory = SessionMemory(max_history=10, llm=agent.llm)
        agent.memory = memory
        
        # Compile workflow
        app = build_workflow(agent)
        
        return agent, app, None
    except Exception as e:
        return None, None, f"Failed to initialize agent: {str(e)}"

def main():

    data_path = "https://product.org/product_catalog/apparel#"
    # Main container
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Knowledge Graph Chatbot</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'app' not in st.session_state:
        st.session_state.app = None
    if 'chat_messages' not in st.session_state:
        st.session_state.chat_messages = []
    if 'initialized' not in st.session_state:
        st.session_state.initialized = False
    if 'error_message' not in st.session_state:
        st.session_state.error_message = None
    
    # Auto-initialize agent if not already done
    if not st.session_state.initialized:
        with st.spinner("Initializing agent..."):
            agent, app, error = initialize_agent()
            if agent and app:
                st.session_state.agent = agent
                st.session_state.app = app
                st.session_state.initialized = True
                st.session_state.error_message = None
            else:
                st.session_state.error_message = error

    # Show error if initialization failed
    if st.session_state.error_message:
        st.markdown(f"""
        <div class="error-message">
            <h4>❌ Initialization Error</h4>
            <p>{st.session_state.error_message}</p>
            <p><strong>Please check your environment variables and Stardog connection.</strong></p>
        </div>
        """, unsafe_allow_html=True)
        st.stop()
    
    # Chat interface
    if st.session_state.agent:
        # Welcome message if no chat history
        if not st.session_state.chat_messages:
            st.markdown("""
            <div class="welcome-message">
                <h3>🎉 Welcome to Knowledge Graph Assistant!</h3>
                <p>I can help you explore the product database. Try asking me questions like:</p>
                <ul style="text-align: left; margin: 10px 0;">
                    <li>Find all products with 'protein' in their keywords</li>
                    <li>What are the top-rated products?</li>
                    <li>Show me products under $50</li>
                    <li>List all products with their prices and ratings</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            st.session_state.chat_messages.append({
                'type': 'bot',
                'message': "Hello! I'm your Knowledge Graph Assistant. Ask me anything about the product database!",
                'timestamp': datetime.now()
            })
        
        # Display chat messages
        for msg in st.session_state.chat_messages:
            render_chat_message(
                msg['message'], 
                is_user=(msg['type'] == 'user'),
                data=msg.get('data', None)
            )
                
        # Initialize clear input flag
        if 'clear_input' not in st.session_state:
            st.session_state.clear_input = False
        
        # Clear input if flag is set
        if st.session_state.clear_input:
            st.session_state.clear_input = False
            user_input = st.text_input(
                "",
                key="chat_input_clear",
                placeholder="Ask me about products, ratings, prices..."
            )
        else:
            user_input = st.text_input(
                "",
                key="chat_input",
                placeholder="Ask me about products, ratings, prices..."
            )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            clear_button = st.button("Clear", type="secondary")
        
        with col2:
            send_button = st.button("Send", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Handle clear button
        if clear_button:
            # Clear the input by using a different key
            st.session_state.clear_input = True
            st.rerun()
        
        # Process chat input
        if send_button and user_input and user_input.strip():
            # Add user message to chat
            st.session_state.chat_messages.append({
                'type': 'user',
                'message': user_input,
                'timestamp': datetime.now()
            })
            
            # Process the query immediately
            with st.spinner("Processing your query..."):
                try:
                    # Process query
                    result = st.session_state.app.invoke({
                        "question": user_input, 
                        "attempts": 1
                    })
                    
                    # Add bot response
                    if result and "query_result" in result:
                        response = result["query_result"]
                        
                        # Check if we have raw SPARQL results in the agent state
                        if "query_results" in result and result["query_results"]:
                            raw_results = result["query_results"]
                            
                            # Only show table for large datasets (more than 15 results)
                            if isinstance(raw_results, list) and len(raw_results) > 15:
                                # Extract raw SPARQL results and convert to DataFrame for large datasets
                                import pandas as pd
                                try:
                                    # Convert SPARQL bindings to DataFrame
                                    if len(raw_results) > 0:
                                        # Extract column names from the first result
                                        first_result = raw_results[0]
                                        columns = list(first_result.keys())
                                        
                                        # Convert bindings to DataFrame
                                        data = []
                                        for binding in raw_results:
                                            row = {}
                                            for col in columns:
                                                value_obj = binding.get(col, {})
                                                if isinstance(value_obj, dict):
                                                    # Extract the actual value from the SPARQL binding
                                                    value = value_obj.get('value', str(value_obj))
                                                    # Remove the data prefix if it exists
                                                    if isinstance(value, str) and value.startswith(data_path):
                                                        value = value.replace(data_path, '')
                                                    row[col] = value
                                                else:
                                                    value = str(value_obj)
                                                    # Remove the data prefix if it exists
                                                    if value.startswith(data_path):
                                                        value = value.replace(data_path, '')
                                                    row[col] = value
                                            data.append(row)
                                        
                                        df = pd.DataFrame(data)
                                        
                                        if not df.empty:
                                            st.session_state.chat_messages.append({
                                                'type': 'bot',
                                                'message': f"Found {len(raw_results)} results from the SPARQL query:",
                                                'timestamp': datetime.now(),
                                                'data': df
                                            })
                                        else:
                                            st.session_state.chat_messages.append({
                                                'type': 'bot',
                                                'message': "The query returned no results.",
                                                'timestamp': datetime.now()
                                            })
                                    else:
                                        # No results, show as text
                                        st.session_state.chat_messages.append({
                                            'type': 'bot',
                                            'message': response,
                                            'timestamp': datetime.now()
                                        })
                                except Exception as e:
                                    # Fallback to text response if DataFrame conversion fails
                                    st.session_state.chat_messages.append({
                                        'type': 'bot',
                                        'message': f"Error processing results: {str(e)}\n\nResponse: {response}",
                                        'timestamp': datetime.now()
                                    })
                            else:
                                # For small datasets, show the human-readable response
                                st.session_state.chat_messages.append({
                                    'type': 'bot',
                                    'message': response,
                                    'timestamp': datetime.now()
                                })
                        else:
                            # No raw results available, show the processed response as text
                            st.session_state.chat_messages.append({
                                'type': 'bot',
                                'message': response,
                                'timestamp': datetime.now()
                            })
                    else:
                        response = "I'm sorry, I couldn't process that query. Please try rephrasing your question."
                        st.session_state.chat_messages.append({
                            'type': 'bot',
                            'message': response,
                            'timestamp': datetime.now()
                        })
                    
                except Exception as e:
                    # Add error message
                    st.session_state.chat_messages.append({
                        'type': 'bot',
                        'message': f"❌ Error: {str(e)}",
                        'timestamp': datetime.now()
                    })
            
            st.rerun()
    
    # Close main container
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
