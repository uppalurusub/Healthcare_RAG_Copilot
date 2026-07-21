import requests
import streamlit as st

from api.rag_api import ask_rag
from components.request_form import (
    build_payload,
    render_chat_history,
    render_question_input,
)
from components.response_view import render_response
from components.sidebar import render_sidebar


st.set_page_config(
    page_title="Population Health RAG Copilot",
    page_icon="🩺",
    layout="wide",
)


def initialize_session_state() -> None:
    if "history" not in st.session_state:
        st.session_state.history = []

    if "messages" not in st.session_state:
        st.session_state.messages = []


def main() -> None:
    initialize_session_state()
    config = render_sidebar()

    st.title("🩺 Population Health RAG Copilot")
    st.markdown(
        """
        Ask clinical questions against the Population Health
        knowledge base.
        """
    )

    render_chat_history(st.session_state.messages)
    question = render_question_input()

    if not question:
        return

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)

    payload = build_payload(
        question=question,
        config=config,
        conversation_history=st.session_state.history,
    )

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            try:
                result = ask_rag(payload)
                answer = render_response(
                    result=result,
                    include_sources=config["include_sources"],
                )

                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
                st.session_state.history.append(
                    {"question": question, "answer": answer}
                )

            except requests.HTTPError as ex:
                response_text = (
                    ex.response.text
                    if ex.response is not None
                    else str(ex)
                )
                st.error(response_text)

            except requests.RequestException as ex:
                st.error(
                    "Unable to connect to the Population Health RAG API. "
                    f"Error details: {ex}"
                )

            except Exception as ex:
                st.error(f"Unexpected error: {ex}")


if __name__ == "__main__":
    main()
