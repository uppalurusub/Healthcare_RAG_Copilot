import streamlit as st

from utils.formatters import extract_answer, extract_sources, format_label


def render_sources(sources: list) -> None:
    st.divider()
    st.subheader("📚 Sources")

    for index, source in enumerate(sources, start=1):
        with st.expander(f"Source {index}"):
            if isinstance(source, dict):
                for key, value in source.items():
                    st.markdown(f"**{format_label(key)}:**")
                    if isinstance(value, (dict, list)):
                        st.json(value)
                    else:
                        st.write(value)
            else:
                st.write(source)


def render_response(result: dict, include_sources: bool) -> str:
    answer = extract_answer(result)
    st.markdown(answer)

    sources = extract_sources(result)
    if include_sources and sources:
        render_sources(sources)

    with st.expander("Complete Response JSON"):
        st.json(result)

    return answer
