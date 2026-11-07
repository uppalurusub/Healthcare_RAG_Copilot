import streamlit as st


def render_chat_history(messages: list[dict]) -> None:
    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def render_question_input() -> str | None:
    return st.chat_input("Ask your clinical question...")


def build_payload(
    question: str,
    config: dict,
    conversation_history: list[dict],
) -> dict:
    return {
        "question": question,
        "top_k": config["top_k"],
        "document_types": config["document_types"],
        "departments": config["departments"],
        "document_names": config["document_names"],
        "include_sources": config["include_sources"],
        "conversation_history": conversation_history,
    }
