import { RAG_ASK_ENDPOINT } from "../config/api";
import type { RAGRequest, RAGResponse } from "../types/rag";

export async function askRagQuestion(payload: RAGRequest): Promise<RAGResponse> {
  let response: Response;
  try {
    response = await fetch(RAG_ASK_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json", Accept: "application/json" },
      body: JSON.stringify(payload),
    });
  } catch {
    throw new Error(`Unable to connect to ${RAG_ASK_ENDPOINT}. Verify FastAPI and CORS configuration.`);
  }
  if (!response.ok) {
    let detail = `Request failed with HTTP ${response.status}`;
    try { const body = await response.json(); detail = body.detail ?? body.message ?? detail; } catch {}
    throw new Error(detail);
  }
  return response.json() as Promise<RAGResponse>;
}