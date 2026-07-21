import { useState } from "react";
import { Activity } from "lucide-react";
import { askRagQuestion } from "./api/ragApi";
import RequestForm from "./components/RequestForm";
import ResponseView from "./components/ResponseView";
import type { RAGRequest, RAGResponse } from "./types/rag";

export default function App() {
  const [data, setData] = useState<RAGResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function submit(request: RAGRequest) {
    setLoading(true); setError(""); setData(null);
    try { setData(await askRagQuestion(request)); }
    catch (e) { setError(e instanceof Error ? e.message : "Unexpected error"); }
    finally { setLoading(false); }
  }

  return <main>
    <header><div className="brand"><Activity size={30}/><div><h1>Healthcare RAG Copilot</h1><p>Clinical knowledge retrieval and multi-agent validation</p></div></div><span className="endpoint">POST /rag/ask</span></header>
    <div className="layout">
      <aside><RequestForm loading={loading} onSubmit={submit}/></aside>
      <section>{error && <div className="error">{error}</div>}{!data && !error && <div className="empty"><Activity size={48}/><h2>Ask a healthcare knowledge question</h2><p>The response will show the validated answer, retrieval metadata, sources, and agent findings.</p></div>}{data && <ResponseView data={data}/>}</section>
    </div>
  </main>;
}