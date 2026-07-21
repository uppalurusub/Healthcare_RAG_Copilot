import type { ReactNode } from "react";
export default function MetricCard({ label, value, icon }: {label:string; value:string|number; icon:ReactNode}) {
  return <div className="metric"><span className="metric-icon">{icon}</span><div><div className="muted">{label}</div><strong>{value}</strong></div></div>;
}