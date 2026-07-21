def extract_answer(result: dict) -> str:
    return (
        result.get("answer")
        or result.get("response")
        or result.get("result")
        or "No answer returned."
    )


def extract_sources(result: dict) -> list:
    return (
        result.get("sources")
        or result.get("source_documents")
        or result.get("references")
        or []
    )


def format_label(value: str) -> str:
    return str(value).replace("_", " ").strip().title()
