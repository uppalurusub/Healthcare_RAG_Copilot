from pathlib import Path
from typing import List, Dict

from pypdf import PdfReader
from app.config.settings import settings
logger = settings.get_logger()

from app.memory.vector_store import VectorStore


class DocumentLoader:

    def __init__(self):

        self.vector_store = VectorStore()

    def extract_text_from_pdf(
        self,
        pdf_path: Path
    ) -> str:

        try:

            text = ""

            reader = PdfReader(str(pdf_path))

            for page in reader.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

            return text

        except Exception as ex:

            logger.exception(
                f"Failed reading PDF: {pdf_path}"
            )

            return ""

    def chunk_text(
        self,
        text: str,
        chunk_size: int = 1000,
        overlap: int = 200
    ) -> List[str]:

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunks.append(
                text[start:end]
            )

            start += chunk_size - overlap

        return chunks

    def determine_metadata(
        self,
        file_path: Path
    ) -> Dict:

        parent_folder = file_path.parent.name

        if parent_folder == "clinical_guidelines":
            doc_type = "guideline"

        elif parent_folder == "sops":
            doc_type = "sop"

        elif parent_folder == "protocols":
            doc_type = "protocol"

        else:
            doc_type = "unknown"

        department = self.get_department(
            file_path.name
        )

        return {
            "document_name": file_path.name,
            "document_type": doc_type,
            "department": department,
            "version": "1.0"
        }

    def get_department(
        self,
        filename: str
    ) -> str:

        filename = filename.lower()

        if "diabetes" in filename:
            return "endocrinology"

        elif "hypertension" in filename:
            return "cardiology"

        elif "heart_failure" in filename:
            return "cardiology"

        elif "stroke" in filename:
            return "neurology"

        elif "asthma" in filename:
            return "pulmonology"

        elif "copd" in filename:
            return "pulmonology"

        elif "oncology" in filename:
            return "oncology"

        elif "kidney" in filename:
            return "nephrology"

        elif "depression" in filename:
            return "psychiatry"

        elif "sepsis" in filename:
            return "critical_care"

        return "general"

    def load_documents(
        self,
        knowledge_base_path: str = "knowledge_base"
    ):

        try:

            logger.info(
                f"Loading documents from "
                f"{knowledge_base_path}"
            )

            documents = []

            pdf_files = list(
                Path(
                    knowledge_base_path
                ).rglob("*.pdf")
            )

            logger.info(
                f"Found {len(pdf_files)} PDFs"
            )

            for pdf_file in pdf_files:

                logger.info(
                    f"Processing {pdf_file.name}"
                )

                text = self.extract_text_from_pdf(
                    pdf_file
                )

                if not text.strip():

                    logger.warning(
                        f"No text found in "
                        f"{pdf_file.name}"
                    )

                    continue

                metadata = (
                    self.determine_metadata(
                        pdf_file
                    )
                )

                chunks = self.chunk_text(
                    text
                )

                logger.info(
                    f"Created {len(chunks)} chunks"
                )

                for idx, chunk in enumerate(
                    chunks
                ):

                    documents.append({

                        "content": chunk,

                        "document_name":
                        metadata[
                            "document_name"
                        ],

                        "document_type":
                        metadata[
                            "document_type"
                        ],

                        "department":
                        metadata[
                            "department"
                        ],

                        "version":
                        metadata[
                            "version"
                        ]
                    })

            logger.info(
                f"Total chunks created: "
                f"{len(documents)}"
            )

            result = (
                self.vector_store.add_documents(
                    documents
                )
            )

            logger.success(
                "Knowledge Base Loaded Successfully"
            )

            return result

        except Exception as ex:

            logger.exception(
                f"Document Loading Failed: "
                f"{str(ex)}"
            )

            raise