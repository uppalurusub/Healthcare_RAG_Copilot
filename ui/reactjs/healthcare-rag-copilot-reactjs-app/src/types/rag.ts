export type ConversationRole = "user" | "assistant";
export interface ConversationMessage { role: ConversationRole; content: string; }
export interface RAGRequest {
  question: string;
  top_k: number;
  document_types: string[];
  departments: string[];
  document_names: string[];
  include_sources: boolean;
  conversation_history: ConversationMessage[];
}
export interface Validation { is_valid: boolean; confidence_score: number; validation_notes: string; }
export interface RetrievalMetadata { retrieved_documents: number; top_k: number; retrieval_time_seconds: number; }
export interface Source { document_name: string; document_type: string; department: string; version: string; relevance_score: number; excerpt: string; }
export interface AgentOutput { agent_name: string; output: string; }
export interface RAGResponse {
  success: boolean; question: string; answer: string; validation: Validation;
  retrieval_metadata: RetrievalMetadata; sources: Source[]; agent_outputs: AgentOutput[];
  session_id: string | null; execution_time_seconds: number; message: string;
}