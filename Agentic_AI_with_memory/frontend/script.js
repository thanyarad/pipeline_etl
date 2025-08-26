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

    // Add user message to chat (no data object for user messages)
    addMessage(message, "user", null);

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
            // Add bot response with the complete data object
            addMessage(null, "bot", data);

            // Store SPARQL query for sidebar
            if (data.sparql_query) {
                currentSparqlQuery = data.sparql_query;
                showSparqlQuery(data.sparql_query);
            }

            // Show memory info with enhanced details
            if (data.memory_info) {
                const memoryMessage = data.cached_response 
                    ? `Cached response (${Math.round(data.cache_similarity * 100)}% match)`
                    : `Conversation ${data.memory_info.conversation_count}`;
                showToast(memoryMessage, "info");
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

function createMessageContent(data, sender) {
    // For user messages, just return the text
    if (sender === "user") {
        return data;
    }

    console.log("Creating message content for bot:", data);

    // For bot messages, handle different response types
    const container = document.createElement("div");

    // Add cache indicator if response was cached
    if (data.cached_response) {
        const cacheInfo = document.createElement("div");
        cacheInfo.className = "message-cached";
        cacheInfo.textContent = `Cached Response (${Math.round(data.cache_similarity * 100)}% match)`;
        container.appendChild(cacheInfo);
    }

    // Handle large response (table format)
    if (data.response_large) {
        const tableInfo = document.createElement("div");
        tableInfo.className = "table-info";
        tableInfo.textContent = `Showing ${data.response_large.length} results:`;
        container.appendChild(tableInfo);

        const tableContainer = document.createElement("div");
        tableContainer.className = "table-container";

        const table = document.createElement("table");
        table.className = "message-table";

        // Create header
        if (data.response_large.length > 0) {
            const thead = document.createElement("thead");
            const headerRow = document.createElement("tr");
            Object.keys(data.response_large[0]).forEach(key => {
                const th = document.createElement("th");
                th.textContent = key;
                headerRow.appendChild(th);
            });
            thead.appendChild(headerRow);
            table.appendChild(thead);

            // Create body
            const tbody = document.createElement("tbody");
            data.response_large.forEach(row => {
                const tr = document.createElement("tr");
                Object.values(row).forEach(value => {
                    const td = document.createElement("td");
                    td.textContent = value;
                    tr.appendChild(td);
                });
                tbody.appendChild(tr);
            });
            table.appendChild(tbody);
        }

        tableContainer.appendChild(table);
        container.appendChild(tableContainer);
    } 
    // Handle small response (text format)
    else if (data.response_small || data.response) {
        const text = document.createElement("div");
        text.textContent = data.response_small || data.response;
        container.appendChild(text);
    }

    return container;
}

function addMessage(text, sender, data = null) {
    const messageDiv = document.createElement("div");
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement("div");
    avatar.className = "message-avatar";

    const icon = document.createElement("i");
    icon.className = sender === "user" ? "fas fa-user" : "fas fa-robot";
    avatar.appendChild(icon);

    const contentDiv = document.createElement("div");
    contentDiv.className = "message-content";

    const messageText = document.createElement("div");
    messageText.className = "message-text";

    if (sender === "bot" && data) {
        // Create formatted content using the helper function
        const formattedContent = createMessageContent(data, sender);
        if (formattedContent instanceof HTMLElement) {
            messageText.appendChild(formattedContent);
        } else {
            messageText.textContent = formattedContent;
        }
    } else {
        messageText.textContent = text;
    }

    const timestamp = document.createElement("div");
    timestamp.className = "message-timestamp";
    timestamp.textContent = new Date().toLocaleTimeString();

    contentDiv.appendChild(messageText);
    contentDiv.appendChild(timestamp);

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(contentDiv);

    chatMessages.appendChild(messageDiv);

    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
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
