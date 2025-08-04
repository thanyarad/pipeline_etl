# Stardog Knowledge Graph Agentic AI

## What is this project?

This is an **Agentic AI system** that autonomously interacts with your **knowledge graph** (a database that stores information in a connected way). Unlike a simple chatbot, this AI agent can:

-   **Make autonomous decisions** about how to process your requests
-   **Orchestrate complex workflows** with multiple steps and decision points
-   **Learn and adapt** from previous interactions
-   **Self-correct** when things go wrong
-   **Plan and execute** multi-step reasoning processes

Think of it as an intelligent assistant that doesn't just answer questions, but actively thinks through problems and takes actions to solve them.

## How does it work?

1. **You ask a question** in normal English (like "Get name of all students")
2. **The agent autonomously decides** the best approach to handle your request
3. **It orchestrates a workflow** that may include caching, relevance checking, query generation, and execution
4. **It makes intelligent decisions** at each step based on context and previous interactions
5. **It adapts and learns** from each interaction to improve future responses
6. **It provides you** with a clear, human-readable answer

## Key Features

-   **Agentic AI**: Autonomous decision-making and workflow orchestration
-   **Memory System**: Remembers conversations and builds context over time
-   **Query Caching**: Intelligently reuses similar queries for efficiency
-   **Knowledge Graph Integration**: Seamlessly works with Stardog databases
-   **Relevance Checking**: Autonomous filtering of relevant vs irrelevant queries
-   **Error Recovery**: Self-correcting with retry mechanisms and fallback strategies
-   **Workflow Orchestration**: Complex multi-step processing with conditional logic
-   **Learning & Adaptation**: Improves responses based on interaction history

## Project Structure

```
src/
├── core/           # Core agent components (agent, client, memory)
├── config/         # Settings and configuration
├── workflow/       # Agentic workflow orchestration
├── utils/          # Helper functions
└── test/           # Tests to ensure agent reliability
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Environment Variables

Create a `.env` file in the project root:

```env
# Stardog Database Settings
STARDOG_ENDPOINT=http://localhost:5820
STARDOG_DATABASE=your_database_name
STARDOG_USERNAME=admin
STARDOG_PASSWORD=admin

# OpenAI Settings
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
DEFAULT_LLM_PROVIDER=openai
```

### 3. Run the Application

**Option 1: Using the batch file (Windows)**

```bash
run_main.bat
```

**Option 2: Using Python directly**

```bash
python src/main.py
```

## How the Agentic AI Processes Questions

The agent follows an intelligent workflow with autonomous decision-making:

1. **Cache Check**: Agent decides whether to use cached results (uses same sparql query) or generate new ones
2. **Relevance Check**: Autonomous filtering to determine if the question is relevant
3. **Query Generation**: Intelligent conversion of natural language to database queries (sparql)
4. **Execution**: Autonomous execution with error handling
5. **Answer Generation**: Context-aware response generation
6. **Memory Update**: Learning from the interaction for future improvements
7. **Error Recovery**: Self-correcting mechanisms when things go wrong

## Requirements

-   Python 3.8+
-   Stardog database server running
-   OpenAI API key
-   Internet connection (for AI model access)

## Testing

Run the tests to ensure the agent works reliably:

```bash
# Windows
run_tests.bat

# Or directly
python -m pytest src/test/
```

## What You Need to Know

-   **Agentic AI**: This system makes autonomous decisions and orchestrates complex workflows
-   **Stardog**: The knowledge graph database that the agent interacts with
-   **OpenAI API**: Powers the agent's reasoning and decision-making capabilities
-   **Memory**: The agent learns and adapts from conversations over time
-   **Workflow Orchestration**: Complex multi-step processing with intelligent routing

## Troubleshooting

-   **"Stardog connection failed"**: Make sure your Stardog server is running and the connection details are correct
-   **"OpenAI API error"**: Check your API key and internet connection
-   **"No relevant data found"**: Make sure your question is related to the data in your knowledge graph

## Project Files Explained

-   `main.py`: Entry point that initializes and runs the agentic AI system
-   `agent.py`: The core agent with autonomous decision-making capabilities
-   `client.py`: Connects the agent to your Stardog database
-   `memory.py`: Enables the agent to learn and remember interactions
-   `graph.py`: Defines the agentic workflow with autonomous routing
-   `settings.py`: Configuration for the agent's behavior

This project demonstrates how AI agents can autonomously interact with knowledge graphs, making intelligent decisions and learning from each interaction to provide increasingly better assistance!
