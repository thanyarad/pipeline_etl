#!/usr/bin/env python3
"""
Development server that serves both the Flask API and static frontend files.
This is useful for development and testing.
"""

from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
import sys
import os
import json
from datetime import datetime

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.core.client import StardogClient
from src.core.agent import StardogAgent
from src.core.memory import SessionMemory
from src.workflow.graph import build_workflow
from src.config.settings import STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD

app = Flask(__name__, static_folder='frontend')
CORS(app)

# Global variables to store the agent and workflow
stardog_client = None
agent = None
workflow = None

def initialize_agent():
    """Initialize the Stardog agent and workflow"""
    global stardog_client, agent, workflow
    
    try:
        # Initialize Stardog client
        stardog_client = StardogClient(STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD)
        print("Stardog KG client initialized successfully!")
        
        # Initialize agent first to get LLM instance
        agent = StardogAgent(stardog_client)
        
        # Initialize memory with the agent's LLM for semantic similarity
        memory = SessionMemory(max_history=10, llm=agent.llm)
        agent.memory = memory
        
        # Compile workflow
        workflow = build_workflow(agent)
        print("Stardog KG Agent workflow compiled successfully!")
        
        return True
    except Exception as e:
        print(f"Error initializing agent: {e}")
        return False

# Serve frontend files
@app.route('/')
def serve_frontend():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('frontend', path)

# API endpoints
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'agent_initialized': agent is not None
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat requests"""
    try:
        data = request.get_json()
        question = data.get('message', '').strip()
        
        if not question:
            return jsonify({'error': 'Message is required'}), 400
        
        if agent is None or workflow is None:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        # Process the question through the workflow
        result = workflow.invoke({"question": question, "attempts": 1})
        
        # Get memory info
        memory_info = agent.get_memory_info()
        
        response = {
            'response': result.get('query_result', 'No response generated'),
            'sparql_query': result.get('sparql_query', ''),
            'timestamp': datetime.now().isoformat(),
            'memory_info': {
                'session_id': memory_info.get('session_id'),
                'conversation_count': memory_info.get('conversation_count', 0)
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing chat request: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/clear-memory', methods=['POST'])
def clear_memory():
    """Clear the agent's memory"""
    try:
        if agent is None:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        agent.clear_memory()
        memory_info = agent.get_memory_info()
        
        return jsonify({
            'message': 'Memory cleared successfully',
            'memory_info': {
                'session_id': memory_info.get('session_id'),
                'conversation_count': memory_info.get('conversation_count', 0)
            }
        })
        
    except Exception as e:
        print(f"Error clearing memory: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh-schema', methods=['POST'])
def refresh_schema():
    """Refresh the knowledge graph schema"""
    try:
        if agent is None:
            return jsonify({'error': 'Agent not initialized'}), 500
        
        success = agent.refresh_schema()
        
        if success:
            return jsonify({'message': 'Schema refreshed successfully'})
        else:
            return jsonify({'error': 'Failed to refresh schema'}), 500
        
    except Exception as e:
        print(f"Error refreshing schema: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get the current status of the system"""
    try:
        if agent is None or stardog_client is None:
            return jsonify({
                'status': 'disconnected',
                'message': 'Agent not initialized'
            })
        
        # Test connection to Stardog
        try:
            # Simple connection test
            schema = stardog_client.get_formatted_schema()
            connected = schema is not None
        except:
            connected = False
        
        memory_info = agent.get_memory_info()
        
        return jsonify({
            'status': 'connected' if connected else 'disconnected',
            'message': 'Connected to Stardog' if connected else 'Disconnected from Stardog',
            'memory_info': {
                'session_id': memory_info.get('session_id'),
                'conversation_count': memory_info.get('conversation_count', 0)
            }
        })
        
    except Exception as e:
        print(f"Error getting status: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Initialize the agent when starting the server
    if initialize_agent():
        print("Development server initialized successfully!")
    else:
        print("Warning: Development server initialized with errors!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)