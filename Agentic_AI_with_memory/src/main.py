import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.client import StardogClient
from src.core.agent import StardogAgent
from src.core.memory import SessionMemory
from src.workflow.graph import build_workflow
from src.config.settings import STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD

def main():
    # Initialize Stardog client
    stardog_client = StardogClient(STARDOG_ENDPOINT, STARDOG_DATABASE, STARDOG_USERNAME, STARDOG_PASSWORD)
    print("Stardog KG client initialized successfully!")
    
    # Initialize agent first to get LLM instance
    agent = StardogAgent(stardog_client)
    
    # Initialize memory with the agent's LLM for semantic similarity
    memory = SessionMemory(max_history=10, llm=agent.llm)
    agent.memory = memory
    
    # Compile workflow
    app = build_workflow(agent)
    print("Stardog KG Agent workflow compiled successfully!")
        
    # Example queries to demonstrate memory
    queries = [
        "Get name of all students",
        "Get city of all students who have mark greater than 80",
        "Get name of all students"
    ]
    
    for i, user_question in enumerate(queries, 1):
        print(f"\n=== Query {i}: {user_question} ===")
        try:
            result = app.invoke({"question": user_question, "attempts": 1})
            print("Result:", result["query_result"])
            
            # Show memory info
            memory_info = agent.get_memory_info()
            print(f"Memory Info - Session: {memory_info['session_id']}, Conversations: {memory_info['conversation_count']}")
            if memory_info['user_preferences']:
                print(f"User Preferences: {memory_info['user_preferences']}")
            
        except Exception as e:
            print(f"Error running query: {e}")
            print("Note: This requires a running Stardog instance with the appropriate data loaded.")
    
    # Demonstrate memory clearing
    print("\n=== Clearing Memory ===")
    agent.clear_memory()
    memory_info = agent.get_memory_info()
    print(f"Memory cleared. Conversations: {memory_info['conversation_count']}")

if __name__ == "__main__":
    main()