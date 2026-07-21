import { FormEvent, useState } from "react";
import { Search } from "lucide-react";
import type { RAGRequest } from "../types/rag";

interface Props { loading: boolean; onSubmit: (request: RAGRequest) => void; }
const split = (v: string) => v.split(",").map(x => x.trim()).filter(Boolean);

export default function RequestForm({ loading, onSubmit }: Props) {
  const [question, setQuestion] = useState("What is the process for reporting an adverse event?");
  const [topK, setTopK] = useState(3);
  const [types, setTypes] = useState("sop");
  const [departments, setDepartments] = useState("clinical_operations");
  const [documents, setDocuments] = useState("adverse_event_reporting_sop.pdf");
  const [includeSources, setIncludeSources] = useState(true);

  const submit = (e: FormEvent) => {
    e.preventDefault();
    onSubmit({ question: question.trim(), top_k: topK, document_types: split(types), departments: split(departments), document_names: split(documents), include_sources: includeSources, conversation_history: [] });
  };

  return <form className="card form" onSubmit={submit}>
    <div className="section-title"><Search size={20}/> Ask Healthcare RAG</div>
    <label>Question<textarea rows={4} value={question} onChange={e=>setQuestion(e.target.value)} required /></label>
    <div className="grid two">
      <label>Top K<input type="number" min={1} max={50} value={topK} onChange={e=>setTopK(Number(e.target.value))}/></label>
      <label className="check"><input type="checkbox" checked={includeSources} onChange={e=>setIncludeSources(e.target.checked)}/> Include sources</label>
    </div>
    <label>Document Types <small>comma separated</small><input value={types} onChange={e=>setTypes(e.target.value)}/></label>
    <label>Departments <small>comma separated</small><input value={departments} onChange={e=>setDepartments(e.target.value)}/></label>
    <label>Document Names <small>comma separated</small><input value={documents} onChange={e=>setDocuments(e.target.value)}/></label>
    <button disabled={loading || !question.trim()}>{loading ? "Running RAG workflow..." : "Ask Question"}</button>
  </form>;
}