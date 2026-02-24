from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY id ASC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]
    
@mcp.tool()
def delete_expense(expense_id: int) -> str:
    """
    Delete an expense by its ID.
    """
    import sqlite3

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Check if expense exists
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return f"No expense found with ID {expense_id}"

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    conn.close()

    return f"Expense with ID {expense_id} deleted successfully."


@mcp.tool()
def edit_expense(expense_id: int, field: str, new_value: str) -> str:
    """
    Edit a specific field of an expense.
    Allowed fields: date, amount, category, title, description
    """
    import sqlite3

    allowed_fields = ["date", "amount", "category", "title", "description"]

    if field not in allowed_fields:
        return f"Invalid field. Allowed fields: {allowed_fields}"

    conn = sqlite3.connect("expenses.db")
    cursor = conn.cursor()

    # Check existence
    cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
    record = cursor.fetchone()

    if not record:
        conn.close()
        return f"No expense found with ID {expense_id}"

    # Update dynamically but safely
    query = f"UPDATE expenses SET {field} = ? WHERE id = ?"
    cursor.execute(query, (new_value, expense_id))

    conn.commit()
    conn.close()

    return f"Expense ID {expense_id} updated successfully."

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

### for local server
# if __name__ == "__main__":
#     mcp.run()

### for remote server
if __name__ == "__main__":
    mcp.run(transport="http", host="0.0.0.0", port=8000)