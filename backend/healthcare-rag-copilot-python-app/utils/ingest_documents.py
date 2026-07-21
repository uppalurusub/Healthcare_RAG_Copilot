from loguru import logger

from utils.document_loader import (
    DocumentLoader
)


def main():

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
        )


if __name__ == "__main__":

    main()