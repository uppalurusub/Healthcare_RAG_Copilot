from typing import List, Dict, Any
from chromadb import PersistentClient
from sentence_transformers import SentenceTransformer
from app.config.settings import settings
logger = settings.get_logger()

import uuid
import time
from pathlib import Path
backend_dir = Path(__file__).resolve().parents[3]
chromadb_dir = backend_dir / "chroma_db"
class VectorStore:

    def __init__(
        self,
        db_path: str = chromadb_dir,
        collection_name: str = "healthcare_knowledge_base"
    ):
        """
        Initialize ChromaDB Vector Store
        """

        try:
            logger.info(
                f"Initializing ChromaDB Collection: {collection_name}"
            )

            self.client = PersistentClient(path=db_path)

            self.collection = self.client.get_or_create_collection(
                name=collection_name
            )

            self.embedding_model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            logger.success(
                "Vector Store Initialized Successfully"
            )

        except Exception as ex:
            logger.exception(
                f"Vector Store Initialization Failed: {str(ex)}"
            )
            raise

    def add_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> Dict:

        """
        documents = [
            {
                "content": "...",
                "document_name": "...",
                "document_type": "...",
                "department": "...",
                "version": "..."
            }
        ]
        """

        start_time = time.time()

        try:

            logger.info(
                f"Adding {len(documents)} documents"
            )

            ids = []
            texts = []
            metadatas = []

            for doc in documents:

                ids.append(str(uuid.uuid4()))

                texts.append(
                    doc["content"]
                )

                metadatas.append({
                    "document_name":
                        doc.get("document_name"),

                    "document_type":
                        doc.get("document_type"),

                    "department":
                        doc.get("department"),

                    "version":
                        doc.get("version", "1.0")
                })

            embeddings = self.embedding_model.encode(
                texts
            ).tolist()

            self.collection.add(
                ids=ids,
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas
            )

            elapsed = round(
                time.time() - start_time,
                2
            )

            logger.success(
                f"{len(documents)} documents added"
            )

            return {
                "success": True,
                "documents_added": len(documents),
                "time_seconds": elapsed
            }

        except Exception as ex:

            logger.exception(
                f"Document ingestion failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }

    def search(
        self,
        query: str,
        top_k: int = 5,
        document_type: str = None,
        department: str = None
    ) -> Dict:

        """
        Semantic Search
        """

        start_time = time.time()

        try:

            logger.info(
                f"Searching KB: {query}"
            )

            embedding = self.embedding_model.encode(
                query
            ).tolist()

            where_clause = {}

            if document_type:
                where_clause["document_type"] = (
                    document_type
                )

            if department:
                where_clause["department"] = (
                    department
                )

            result = self.collection.query(
                query_embeddings=[embedding],
                n_results=top_k,
                where=where_clause if where_clause else None
            )

            elapsed = round(
                time.time() - start_time,
                2
            )

            logger.success(
                f"Retrieved {len(result['ids'][0])} documents"
            )

            return {
                "success": True,
                "query": query,
                "documents":
                    result.get("documents", [[]])[0],
                "metadatas":
                    result.get("metadatas", [[]])[0],
                "distances":
                    result.get("distances", [[]])[0],
                "ids":
                    result.get("ids", [[]])[0],
                "retrieval_time_seconds":
                    elapsed
            }

        except Exception as ex:

            logger.exception(
                f"Search failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }

    def get_collection_stats(self) -> Dict:

        try:

            count = self.collection.count()

            logger.info(
                f"Collection Count: {count}"
            )

            return {
                "success": True,
                "collection_name":
                    self.collection.name,
                "document_count":
                    count
            }

        except Exception as ex:

            logger.exception(
                f"Stats failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }

    def delete_collection(self) -> Dict:

        try:

            collection_name = self.collection.name

            self.client.delete_collection(
                name=collection_name
            )

            logger.warning(
                f"Deleted collection: {collection_name}"
            )

            return {
                "success": True,
                "message":
                    f"{collection_name} deleted"
            }

        except Exception as ex:

            logger.exception(
                f"Delete failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }

    def reset_collection(self) -> Dict:

        try:

            count = self.collection.count()

            ids = self.collection.get()["ids"]

            if ids:
                self.collection.delete(ids=ids)

            logger.warning(
                f"Removed {count} documents"
            )

            return {
                "success": True,
                "deleted_documents": count
            }

        except Exception as ex:

            logger.exception(
                f"Reset failed: {str(ex)}"
            )

            return {
                "success": False,
                "message": str(ex)
            }