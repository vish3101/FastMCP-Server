# 🚀 FastMCP Expense Tracker Server

A Python-based **MCP (Model Context Protocol) server** built using
**FastMCP** that provides a complete Expense Tracker system with full
CRUD support.

This server can:

-   Run locally via STDIO\
-   Be deployed remotely (e.g., FastMCP Cloud)\
-   Connect to MCP clients like Claude Desktop

------------------------------------------------------------------------

## 📌 Features

This MCP server provides the following tools:

### 🟢 Create

-   `add_expense` → Add a new expense record

### 🔵 Read

-   `list_expenses` → View expenses within a date range

### 🟣 Aggregate

-   `summarize` → Get total expense grouped by category

### 🟠 Update

-   `edit_expense` → Update any field of an existing expense

### 🔴 Delete

-   `delete_expense` → Delete an expense by ID

------------------------------------------------------------------------

## 🗂 Project Structure

``` text
FastMCP-Server/
├── main.py                # MCP server implementation
├── categories.json        # Static categories resource
├── expenses.db            # SQLite database (auto-created)
├── pyproject.toml         # Project configuration
└── README.md              # Documentation
```

------------------------------------------------------------------------

## 🧠 Prerequisites

Make sure you have:

-   Python 3.11+\
-   pip installed\
-   (Optional) uv for running FastMCP\
-   An MCP-compatible client (e.g., Claude Desktop)

------------------------------------------------------------------------

## ⚙️ Installation

### 1️⃣ Clone Repository

``` bash
git clone https://github.com/vish3101/FastMCP-Server.git
cd FastMCP-Server
```

### 2️⃣ Create Virtual Environment

**macOS / Linux:**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows:**

``` bash
python -m venv .venv
.venv\Scripts\activate
```

### 3️⃣ Install Dependencies

``` bash
pip install .
```

------------------------------------------------------------------------

## 🗄 Database Schema

The server uses SQLite (`expenses.db`). The table is automatically
created when the server runs.

``` sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    amount REAL,
    category TEXT,
    title TEXT,
    description TEXT
);
```

------------------------------------------------------------------------

## 🚀 Running the Server

### 💻 Option 1: Run with Python

``` bash
python main.py
```

### ⚡ Option 2: Run with FastMCP CLI

``` bash
fastmcp run main.py
```

------------------------------------------------------------------------

## 🌐 Deploying to FastMCP Cloud

1.  Push your repo to GitHub.\
2.  Connect your repo on FastMCP Cloud.\
3.  Deploy using the default entrypoint (`main.py`).

Your server will be available via an HTTPS endpoint:

    https://your-server.fastmcp.cloud

------------------------------------------------------------------------

## 🔌 Connecting to Claude Desktop

Edit your `claude_desktop_config.json` file:

``` json
{
  "mcpServers": {
    "ExpenseTracker": {
      "url": "http://localhost:8000"
    }
  }
}
```

Restart Claude Desktop after saving.

------------------------------------------------------------------------

## 🛠 Tool Usage Examples

### Add Expense

``` json
{
  "tool": "add_expense",
  "args": ["2026-02-01", 500, "Food", "Lunch", "Cafe meal"]
}
```

### List Expenses

``` json
{
  "tool": "list_expenses",
  "args": ["2026-02-01", "2026-02-28"]
}
```

------------------------------------------------------------------------

## 👨‍💻 Author

**Vishva Chaudhary**

GitHub: https://github.com/vish3101
