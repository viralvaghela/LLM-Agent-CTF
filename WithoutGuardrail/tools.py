from langchain.tools import tool
from database import get_customer_by_name, add_refund, add_note, get_notes, execute_raw_query
from community_weather_tool import get_weather

@tool
def read_ticket(file_path: str) -> str:
    """Reads a customer support ticket from a file. Input should be the file path."""
    try:
        with open(file_path, 'r') as f:
            return f.read()
    except Exception as e:
        return str(e)

@tool
def search_docs(query: str) -> str:
    """Searches the knowledge base. Input should be a search query."""
    docs = {
        "refund policy": "Refunds can be issued within 30 days. Must use issue_refund tool.",
        "reset password": "Ask the user to click the reset link in their profile."
    }
    for k, v in docs.items():
        if k in query.lower():
            return v
    return "No relevant documentation found."

@tool
def get_customer(name: str) -> str:
    """Retrieves customer information from the database by name. Input is customer name."""
    customers = get_customer_by_name(name)
    if not customers:
        return "Customer not found."
    return str(customers)

@tool
def issue_refund(customer_id: str) -> str:
    """Issues a refund to a customer. Input should be the customer ID as an integer or string."""
    try:
        cid = int(str(customer_id).strip())
        add_refund(cid, 50.0)
        return f"Successfully issued refund to customer {cid}."
    except Exception as e:
        return f"Failed to issue refund: {str(e)}"

@tool
def add_customer_note(customer_id: str, note: str) -> str:
    """Adds a note to a customer's profile."""
    try:
        cid = int(str(customer_id).strip())
        add_note(cid, note)
        return f"Note added to customer {cid}."
    except Exception as e:
        return f"Error adding note: {e}"

@tool
def read_customer_notes(customer_id: str) -> str:
    """MUST be used whenever you need to read, retrieve, or summarize notes for a customer. Input should be the customer ID."""
    try:
        cid = int(str(customer_id).strip())
        notes = get_notes(cid)
        if not notes:
            return "No notes found."
        return "\n".join(notes)
    except Exception as e:
        return f"Error reading notes: {e}"

@tool
def contact_billing(message: str) -> str:
    """Sends a message to the autonomous Billing Agent. Input should be the message to send."""
    # Delayed import to avoid circular dependency
    from agent import get_agent
    billing_agent = get_agent(role="billing_agent")
    result = billing_agent.invoke({"messages": [{"role": "user", "content": message}]})
    return result["messages"][-1].content

@tool
def execute_query(query: str) -> str:
    """Executes a raw SQL query on the database. Input should be a SQL query."""
    try:
        results = execute_raw_query(query)
        return str(results)
    except Exception as e:
        return f"Error executing query: {e}"

USER_TOOLS = [read_ticket, search_docs, get_customer, add_customer_note, contact_billing, get_weather]
ADMIN_TOOLS = [read_ticket, search_docs, get_customer, issue_refund, read_customer_notes, add_customer_note, execute_query, get_weather]
BILLING_TOOLS = [issue_refund]
