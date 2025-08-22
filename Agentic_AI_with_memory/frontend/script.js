// Configuration
const API_BASE_URL = "http://localhost:5000/api";

// DOM elements
const chatMessages = document.getElementById("chatMessages");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const charCount = document.getElementById("charCount");
const statusIndicator = document.getElementById("statusIndicator");
const statusText = document.getElementById("statusText");
const loadingOverlay = document.getElementById("loadingOverlay");
const sidebar = document.getElementById("sidebar");
const sparqlQuery = document.getElementById("sparqlQuery");
const closeSidebar = document.getElementById("closeSidebar");
const copyQueryBtn = document.getElementById("copyQueryBtn");
const clearMemoryBtn = document.getElementById("clearMemoryBtn");
const refreshSchemaBtn = document.getElementById("refreshSchemaBtn");
const toastContainer = document.getElementById("toastContainer");

// State
let isConnected = false;
let currentSparqlQuery = "";

// Initialize the application
document.addEventListener("DOMContentLoaded", function () {
    initializeApp();
    setupEventListeners();
    setWelcomeTimestamp();
});

function initializeApp() {
    // Check connection status
    checkConnectionStatus();

    // Set up auto-resize for textarea
    setupTextareaAutoResize();

    // Set up character count
    updateCharCount();
}

function setupEventListeners() {
    // Send message
    sendButton.addEventListener("click", sendMessage);
    messageInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Input events
    messageInput.addEventListener("input", function () {
        updateCharCount();
        updateSendButton();
    });

    // Sidebar events
    closeSidebar.addEventListener("click", closeSidebarPanel);
    copyQueryBtn.addEventListener("click", copySparqlQuery);

    // Action buttons
    clearMemoryBtn.addEventListener("click", clearMemory);
    refreshSchemaBtn.addEventListener("click", refreshSchema);
}

function setupTextareaAutoResize() {
    messageInput.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = Math.min(this.scrollHeight, 120) + "px";
    });
}

function updateCharCount() {
    const count = messageInput.value.length;
    charCount.textContent = `${count}/1000`;

    if (count > 900) {
        charCount.style.color = "#e74c3c";
    } else if (count > 800) {
        charCount.style.color = "#f39c12";
    } else {
        charCount.style.color = "#6c757d";
    }
}

function updateSendButton() {
    const hasText = messageInput.value.trim().length > 0;
    sendButton.disabled = !hasText || !isConnected;
}

function setWelcomeTimestamp() {
    const welcomeTimestamp = document.getElementById("welcomeTimestamp");
    welcomeTimestamp.textContent = new Date().toLocaleTimeString();
}

async function checkConnectionStatus() {
    try {
        setStatus("connecting");

        const response = await fetch(`${API_BASE_URL}/status`);
        const data = await response.json();

        if (response.ok) {
            isConnected = data.status === "connected";
            setStatus(isConnected ? "connected" : "disconnected", data.message);
        } else {
            setStatus("disconnected", "Failed to connect to server");
        }
    } catch (error) {
        console.error("Error checking connection status:", error);
        setStatus("disconnected", "Cannot connect to server");
    }

    updateSendButton();
}

function setStatus(status, message = "") {
    statusIndicator.className = `status-indicator ${status}`;
    statusText.textContent = message || getStatusMessage(status);
    isConnected = status === "connected";
}

function getStatusMessage(status) {
    const messages = {
        connected: "Connected to Stardog",
        disconnected: "Disconnected from Stardog",
        connecting: "Connecting...",
    };
    return messages[status] || "Unknown status";
}

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || !isConnected) return;

    // Add user message to chat
    addMessage(message, "user");

    // Clear input
    messageInput.value = "";
    messageInput.style.height = "auto";
    updateCharCount();
    updateSendButton();

    // Show loading
    showLoading(true);

    try {
        const response = await fetch(`${API_BASE_URL}/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        if (response.ok) {
            // Add bot response
            addMessage(data.response, "bot");

            // Store SPARQL query for sidebar
            if (data.sparql_query) {
                currentSparqlQuery = data.sparql_query;
                showSparqlQuery(data.sparql_query);
            }

            // Show memory info
            if (data.memory_info) {
                showToast(
                    `Conversation ${data.memory_info.conversation_count}`,
                    "info"
                );
            }
        } else {
            addMessage(`Error: ${data.error}`, "bot");
            showToast(data.error, "error");
        }
    } catch (error) {
        console.error("Error sending message:", error);
        addMessage(
            "Sorry, I encountered an error while processing your request. Please try again.",
            "bot"
        );
        showToast("Network error occurred", "error");
    } finally {
        showLoading(false);
    }
}

function addMessage(text, sender) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";

    const icon = document.createElement("i");
    icon.className = sender === "user" ? "fas fa-user" : "fas fa-robot";
    avatar.appendChild(icon);

    const content = document.createElement("div");
    content.className = "message-content";

    const messageText = document.createElement("div");
    messageText.className = "message-text";

    // Check if the text contains a table (ASCII art table)
    if (sender === "bot" && isTableResult(text)) {
        messageText.innerHTML = formatTableResult(text);
    } else {
        messageText.textContent = text;
    }

    const timestamp = document.createElement("div");
    timestamp.className = "message-timestamp";
    timestamp.textContent = new Date().toLocaleTimeString();

    content.appendChild(messageText);
    content.appendChild(timestamp);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function isTableResult(text) {
    // Check if text contains ASCII table patterns
    const tablePatterns = [
        /\|.*\|.*\|/, // Contains pipe-separated columns
        /\+.*\+.*\+/, // Contains plus-separated borders
        /-.*\|.*-/, // Contains dash-separated rows
        /product_name/i, // Contains common table headers
        /customer_name/i,
        /order_id/i,
        /price/i,
        /quantity/i,
    ];

    return tablePatterns.some((pattern) => pattern.test(text));
}

function formatTableResult(text) {
    // Split text into lines
    const lines = text.split("\n").filter((line) => line.trim());

    // Find the table content (between borders or with pipe separators)
    const tableLines = lines.filter(
        (line) =>
            line.includes("|") ||
            line.includes("+") ||
            line.includes("-") ||
            line.trim().startsWith("|") ||
            line.trim().endsWith("|")
    );

    if (tableLines.length === 0) {
        return text; // Return original text if no table found
    }

    // Extract headers and data
    const headers = [];
    const data = [];
    let inTable = false;

    for (const line of tableLines) {
        const cleanLine = line.trim();

        // Skip border lines (lines with only +, -, or |)
        if (/^[+\-|]+$/.test(cleanLine.replace(/\s/g, ""))) {
            continue;
        }

        // Extract columns from pipe-separated line
        if (cleanLine.includes("|")) {
            const columns = cleanLine
                .split("|")
                .map((col) => col.trim())
                .filter((col) => col.length > 0);

            if (columns.length > 0) {
                if (headers.length === 0) {
                    headers.push(...columns);
                } else {
                    data.push(columns);
                }
            }
        }
    }

    // Create HTML table
    if (headers.length > 0) {
        let tableHTML =
            '<div class="table-container"><table class="result-table">';

        // Add header row
        tableHTML += "<thead><tr>";
        headers.forEach((header) => {
            tableHTML += `<th>${header}</th>`;
        });
        tableHTML += "</tr></thead>";

        // Add data rows
        if (data.length > 0) {
            tableHTML += "<tbody>";
            data.forEach((row) => {
                tableHTML += "<tr>";
                row.forEach((cell) => {
                    tableHTML += `<td>${cell}</td>`;
                });
                tableHTML += "</tr>";
            });
            tableHTML += "</tbody>";
        }

        tableHTML += "</table></div>";
        return tableHTML;
    }

    // Fallback: return original text if table parsing fails
    return text;
}

function showLoading(show) {
    if (show) {
        loadingOverlay.classList.add("show");
    } else {
        loadingOverlay.classList.remove("show");
    }
}

function showSparqlQuery(query) {
    sparqlQuery.textContent = query;
    sidebar.classList.add("open");
}

function closeSidebarPanel() {
    sidebar.classList.remove("open");
}

async function copySparqlQuery() {
    try {
        await navigator.clipboard.writeText(currentSparqlQuery);
        showToast("SPARQL query copied to clipboard", "success");
    } catch (error) {
        console.error("Failed to copy query:", error);
        showToast("Failed to copy query", "error");
    }
}

async function clearMemory() {
    try {
        const response = await fetch(`${API_BASE_URL}/clear-memory`, {
            method: "POST",
        });

        const data = await response.json();

        if (response.ok) {
            showToast("Memory cleared successfully", "success");
            addMessage(
                "Memory has been cleared. I'll start fresh with our conversation.",
                "bot"
            );
        } else {
            showToast(data.error, "error");
        }
    } catch (error) {
        console.error("Error clearing memory:", error);
        showToast("Failed to clear memory", "error");
    }
}

async function refreshSchema() {
    try {
        const response = await fetch(`${API_BASE_URL}/refresh-schema`, {
            method: "POST",
        });

        const data = await response.json();

        if (response.ok) {
            showToast("Schema refreshed successfully", "success");
        } else {
            showToast(data.error, "error");
        }
    } catch (error) {
        console.error("Error refreshing schema:", error);
        showToast("Failed to refresh schema", "error");
    }
}

function showToast(message, type = "info") {
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;

    const icon = document.createElement("i");
    icon.className = getToastIcon(type);

    const messageSpan = document.createElement("span");
    messageSpan.className = "toast-message";
    messageSpan.textContent = message;

    toast.appendChild(icon);
    toast.appendChild(messageSpan);

    toastContainer.appendChild(toast);

    // Auto remove after 5 seconds
    setTimeout(() => {
        toast.remove();
    }, 5000);
}

function getToastIcon(type) {
    const icons = {
        success: "fas fa-check-circle",
        error: "fas fa-exclamation-circle",
        info: "fas fa-info-circle",
    };
    return icons[type] || icons.info;
}

// Periodic status check
setInterval(checkConnectionStatus, 30000); // Check every 30 seconds
