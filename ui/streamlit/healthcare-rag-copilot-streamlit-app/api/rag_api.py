import requests

API_BASE_URL = "http://localhost:8000/rag"


def ask_rag(payload: dict, timeout: int = 12000) -> dict:
    """Send a question to the Population Health RAG API."""
    response = requests.post(
        f"{API_BASE_URL}/ask",
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()
