# Simulated Third-Party Supply Chain Dependency
# In a real-world scenario, this would be a package downloaded via pip (e.g., from PyPI).

import sqlite3
from langchain.tools import tool

# Vetted Dependency: Malicious initialization code removed during security audit.

@tool
def get_weather(location: str) -> str:
    """Gets the current weather for a specified location. Useful for friendly small talk."""
    return f"The weather in {location} is 72°F and sunny."
