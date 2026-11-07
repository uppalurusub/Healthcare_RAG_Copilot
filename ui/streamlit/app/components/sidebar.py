import streamlit as st


DOCUMENT_TYPES = [
    "guideline",
    "policy",
    "clinical_protocol",
    "research",
    "patient_education",
]

DEPARTMENTS = [
    "endocrinology",
    "cardiology",
    "neurology",
    "oncology",
    "pulmonology",
    "nephrology",
    "general_medicine",
]


def render_sidebar() -> dict:
    st.sidebar.title("⚙️ RAG Configuration")

    top_k = st.sidebar.slider("Top K Documents", 1, 20, 5)
    include_sources = st.sidebar.checkbox("Include Sources", True)

    document_types = st.sidebar.multiselect(
        "Document Types",
        DOCUMENT_TYPES,
        default=["guideline"],
    )

    departments = st.sidebar.multiselect(
        "Departments",
        DEPARTMENTS,
        default=["endocrinology"],
    )

    document_names_text = st.sidebar.text_area(
        "Document Names (one per line)",
        "diabetes_management_guideline.pdf",
    )

    document_names = [
        value.strip()
        for value in document_names_text.splitlines()
        if value.strip()
    ]

    st.sidebar.divider()

    return {
        "top_k": top_k,
        "include_sources": include_sources,
        "document_types": document_types,
        "departments": departments,
        "document_names": document_names,
    }
