# Knowledge Graph Chatbot - Frontend/Backend Setup

This document describes how to run the Knowledge Graph Chatbot using the Flask backend and HTML/CSS/JavaScript frontend with a unified startup process.

## Architecture

The setup consists of:

-   **Backend**: Flask API server (`backend/app.py`) that serves both API endpoints and frontend files
-   **Frontend**: HTML/CSS/JavaScript interface (`frontend/`)
-   **Communication**: RESTful API calls between frontend and backend
-   **Unified Startup**: Single command to start both frontend and backend (`run_app.bat`)

## Features

### Frontend Features

-   Modern, responsive chat interface
-   Real-time connection status indicator
-   Auto-resizing text input
-   Character count and validation
-   SPARQL query sidebar with copy functionality
-   Toast notifications for user feedback
-   Memory management controls
-   Schema refresh capability
-   Mobile-responsive design

### Backend Features

-   RESTful API endpoints
-   Frontend file serving (HTML, CSS, JS)
-   CORS support for cross-origin requests
-   Health check and status monitoring
-   Chat processing with SPARQL generation
-   Memory management
-   Schema refresh functionality
-   Error handling and logging

## Quick Start

### Single Command Setup

Run the entire application (both frontend and backend) using the unified batch file:

```bash
run_app.bat
```

This will:

1. Start the Flask backend server on `http://localhost:5000`
2. Automatically open the frontend in your default browser
3. Serve both API endpoints and frontend files from the same server

### Manual Setup (Alternative)

If you prefer to run components separately:

#### 1. Start the Backend Server

```bash
# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Start the server
python backend/app.py
```

The backend will start on `http://localhost:5000` and serve both API endpoints and frontend files.

#### 2. Access the Frontend

Open your browser and navigate to:

```
http://localhost:5000
```

The backend server will serve the frontend files directly.

## API Endpoints

### Health Check

-   **GET** `/api/health`
-   Returns server health status

### Chat

-   **POST** `/api/chat`
-   Body: `{"message": "your question here"}`
-   Returns: `{"response": "bot response", "sparql_query": "generated query", "memory_info": {...}}`

### Status

-   **GET** `/api/status`
-   Returns connection status and memory information

### Clear Memory

-   **POST** `/api/clear-memory`
-   Clears the agent's conversation memory

### Refresh Schema

-   **POST** `/api/refresh-schema`
-   Refreshes the knowledge graph schema cache

## File Structure

```
Agentic_AI_with_memory/
├── backend/
│   └── app.py                 # Flask backend server (serves API + frontend)
├── frontend/
│   ├── index.html             # Main HTML file
│   ├── styles.css             # CSS styling
│   └── script.js              # JavaScript functionality
├── src/                       # Core chatbot logic
├── requirements.txt           # Python dependencies
├── run_app.bat                # Unified startup script
├── run_backend.bat            # Backend-only startup script (optional)
├── run_tests.bat              # Test runner script (optional)
└── README_FRONTEND_BACKEND.md # This file
└── README_AGENTIC_AI.md       # Read me for agentic AI usage
```

## Configuration

### Backend Configuration

The backend uses the same configuration as:

-   Stardog connection settings in `src/config/settings.py` using the env in root folder.
-   OpenAI API key for LLM functionality
-   Database and authentication credentials

### Frontend Configuration

The frontend connects to the backend via the `API_BASE_URL` constant in `script.js`:

```javascript
const API_BASE_URL = "http://localhost:5000/api";
```

Change this if your backend runs on a different port or host.

## Usage

1. **Run the application** - Execute `run_app.bat` to start everything
2. **Wait for initialization** - The backend will initialize the Stardog connection and agent
3. **Browser opens automatically** - The frontend will open in your default browser
4. **Ask questions** - Type your questions in natural language
5. **View SPARQL queries** - Generated queries appear in the sidebar
6. **Manage memory** - Use the action buttons to clear memory or refresh schema

## Troubleshooting

### Application Startup Issues

-   **Virtual environment not found**: Run `python -m venv .venv` to create it
-   **Python not found**: Ensure Python is installed and in your PATH
-   **Port 5000 in use**: The backend will show an error if the port is occupied

### Backend Issues

-   **Connection failed**: Check Stardog server is running and credentials are correct
-   **Import errors**: Ensure all dependencies are installed (`pip install -r requirements.txt`)
-   **Port conflicts**: Change the port in `backend/app.py` if 5000 is in use

### Frontend Issues

-   **Cannot connect to backend**: Ensure backend is running on `http://localhost:5000`
-   **CORS errors**: Backend includes CORS support, but check browser console for details
-   **Styling issues**: Ensure all CSS and JavaScript files are in the correct location

### Common Issues

1. **"Agent not initialized"**: Backend failed to connect to Stardog
2. **"Network error"**: Backend server is not running
3. **"Failed to copy query"**: Browser clipboard permissions may be required
4. **"404 Not Found"**: Ensure you're accessing `http://localhost:5000` (not `file://` URLs)

## Development

### Adding New Features

-   **Backend**: Add new routes in `backend/app.py`
-   **Frontend**: Update `script.js` for new API calls and `styles.css` for styling
-   **API**: Follow RESTful conventions for new endpoints

### Customization

-   **Styling**: Modify `frontend/styles.css` for visual changes
-   **Functionality**: Update `frontend/script.js` for behavior changes
-   **API**: Extend `backend/app.py` for new backend features

### Running Individual Components

-   **Backend only**: Use `run_backend.bat` or `python backend/app.py`
-   **Tests**: Use `run_tests.bat` to run test suites

## Security Considerations

-   The current setup is for development use
-   For production, consider:
    -   HTTPS for all communications
    -   Authentication and authorization
    -   Rate limiting
    -   Input validation and sanitization
    -   Environment variable management for secrets

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Check browser console and backend logs for error details
3. Ensure you're using the unified `run_app.bat` for the simplest setup
