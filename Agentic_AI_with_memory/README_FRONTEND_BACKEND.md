# Knowledge Graph Chatbot - Frontend/Backend Setup

This document describes how to run the Knowledge Graph Chatbot using the new Flask backend and HTML/CSS/JavaScript frontend instead of Streamlit.

## Architecture

The new setup consists of:

-   **Backend**: Flask API server (`backend/app.py`)
-   **Frontend**: HTML/CSS/JavaScript interface (`frontend/`)
-   **Communication**: RESTful API calls between frontend and backend

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
-   CORS support for cross-origin requests
-   Health check and status monitoring
-   Chat processing with SPARQL generation
-   Memory management
-   Schema refresh functionality
-   Error handling and logging

## Quick Start

### 1. Start the Backend Server

Run the backend server using the provided batch file:

```bash
run_backend.bat
```

Or manually:

```bash
# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Start the server
python backend/app.py
```

The backend will start on `http://localhost:5000`

### 2. Open the Frontend

Open the frontend in your browser using the provided batch file:

```bash
open_frontend.bat
```

Or manually open `frontend/index.html` in your web browser.

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
│   └── app.py                 # Flask backend server
├── frontend/
│   ├── index.html            # Main HTML file
│   ├── styles.css            # CSS styling
│   └── script.js             # JavaScript functionality
├── src/                      # Core chatbot logic (unchanged)
├── requirements.txt          # Python dependencies
├── run_backend.bat          # Backend startup script
├── open_frontend.bat        # Frontend launcher
└── README_FRONTEND_BACKEND.md # This file
```

## Configuration

### Backend Configuration

The backend uses the same configuration as the original Streamlit app:

-   Stardog connection settings in `src/config/settings.py`
-   OpenAI API key for LLM functionality
-   Database and authentication credentials

### Frontend Configuration

The frontend connects to the backend via the `API_BASE_URL` constant in `script.js`:

```javascript
const API_BASE_URL = "http://localhost:5000/api";
```

Change this if your backend runs on a different port or host.

## Usage

1. **Start the backend server** - This initializes the Stardog connection and agent
2. **Open the frontend** - The interface will automatically check connection status
3. **Ask questions** - Type your questions in natural language
4. **View SPARQL queries** - Generated queries appear in the sidebar
5. **Manage memory** - Use the action buttons to clear memory or refresh schema

## Troubleshooting

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

## Development

### Adding New Features

-   **Backend**: Add new routes in `backend/app.py`
-   **Frontend**: Update `script.js` for new API calls and `styles.css` for styling
-   **API**: Follow RESTful conventions for new endpoints

### Customization

-   **Styling**: Modify `frontend/styles.css` for visual changes
-   **Functionality**: Update `frontend/script.js` for behavior changes
-   **API**: Extend `backend/app.py` for new backend features

## Comparison with Streamlit

| Feature           | Streamlit | Frontend/Backend |
| ----------------- | --------- | ---------------- |
| Setup Complexity  | Simple    | Moderate         |
| Customization     | Limited   | High             |
| Performance       | Good      | Better           |
| Mobile Support    | Limited   | Full             |
| Deployment        | Easy      | More flexible    |
| Development Speed | Fast      | Moderate         |

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
2. Review the original Streamlit implementation for reference
3. Check browser console and backend logs for error details
