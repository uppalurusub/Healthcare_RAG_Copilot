import ReactMarkdown from "react-markdown";
import { Bot, CheckCircle2, Clock3, Database, FileText, ShieldCheck } from "lucide-react";
import type { RAGResponse } from "../types/rag";
import { percent, seconds, titleCase } from "../utils/formatters";
import MetricCard from "./MetricCard";

export default function ResponseView({ data }: { data: RAGResponse }) {
  return <div className="results">
    <div className="metrics">
      <MetricCard label="Validation" value={data.validation.is_valid ? "Valid" : "Invalid"} icon={<ShieldCheck/>}/>
      <MetricCard label="Confidence" value={percent(data.validation.confidence_score)} icon={<CheckCircle2/>}/>
      <MetricCard label="Documents" value={data.retrieval_metadata.retrieved_documents} icon={<Database/>}/>
      <MetricCard label="Execution Time" value={seconds(data.execution_time_seconds)} icon={<Clock3/>}/>
    </div>

    <section className="card">
      <div className="section-title"><Bot size={20}/> Validated Answer</div>
      <div className="markdown"><ReactMarkdown>{data.answer}</ReactMarkdown></div>
    </section>

    <section className="card">
      <div className="section-title"><ShieldCheck size={20}/> Validation Summary</div>
      <div className="validation-row"><span className={data.validation.is_valid ? "badge success" : "badge danger"}>{data.validation.is_valid ? "VALID" : "INVALID"}</span><strong>{percent(data.validation.confidence_score)} confidence</strong></div>
      <p>{data.validation.validation_notes}</p>
    </section>

    {data.sources?.length > 0 && <section className="card">
      <div className="section-title"><FileText size={20}/> Sources</div>
      <div className="stack">{data.sources.map((s,i)=><article className="source" key={`${s.document_name}-${i}`}>
        <div className="source-head"><strong>{s.document_name}</strong><span className="score">{percent(s.relevance_score)}</span></div>
        <div className="chips"><span>{titleCase(s.document_type)}</span><span>{titleCase(s.department)}</span><span>v{s.version}</span></div>
        <p>{s.excerpt}</p>
      </article>)}</div>
    </section>}

    {data.agent_outputs?.length > 0 && <section className="card">
      <div className="section-title"><Bot size={20}/> Agent Outputs</div>
      <div className="stack">{data.agent_outputs.map((a,i)=><details className="agent" key={`${a.agent_name}-${i}`} open={i===data.agent_outputs.length-1}>
        <summary>{a.agent_name}</summary><div className="markdown"><ReactMarkdown>{a.output}</ReactMarkdown></div>
      </details>)}</div>
    </section>}
  </div>;
}