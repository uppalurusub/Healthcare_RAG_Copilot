from app.config.settings import settings
logger = settings.get_logger()

from app.utils.document_loader import (
    DocumentLoader
)
from pathlib import Path


""" def main():

    try:

        logger.info(
            "Starting Document Ingestion"
        )

        loader = DocumentLoader()

        result = loader.load_documents(
            "knowledge_base"
        )

        logger.success(result)

    except Exception as ex:

        logger.exception(
            str(ex)
        ) """


def main():

    try:
        logger.info("Starting Document Ingestion")

        # Resolve knowledge_base relative to backend directory
        backend_dir = Path(__file__).resolve().parents[3]
        knowledge_base = backend_dir / "knowledge_base"

        logger.info(f"Knowledge Base Path: {knowledge_base}")

        if not knowledge_base.exists():
            raise FileNotFoundError(
                f"Knowledge base directory not found: {knowledge_base}"
            )

        pdf_files = list(knowledge_base.rglob("*.pdf"))

        logger.info(f"PDF files discovered: {len(pdf_files)}")

        if not pdf_files:
            raise FileNotFoundError(
                f"No PDF documents found in {knowledge_base}"
            )

        for pdf in pdf_files:
            logger.info(f"Discovered PDF: {pdf.name}")

        loader = DocumentLoader()

        result = loader.load_documents(
            str(knowledge_base)
        )

        if not isinstance(result, dict) or not result.get("success"):
            raise RuntimeError(
                f"Document ingestion failed: {result}"
            )

        logger.success(
            f"Document ingestion completed: {result}"
        )

    except Exception as ex:
        logger.exception(f"Document ingestion failed: {ex}")
        raise


if __name__ == "__main__":

    main()