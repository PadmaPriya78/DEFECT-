const CONFIG = [
  { key: "high_risk_count", label: "High Risk", color: "bg-signal-high", text: "text-signal-high" },
  { key: "medium_risk_count", label: "Medium Risk", color: "bg-signal-medium", text: "text-signal-medium" },
  { key: "low_risk_count", label: "Low Risk", color: "bg-signal-low", text: "text-signal-low" },
];

export default function SummaryCards({ analysis }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
      <div className="col-span-2 md:col-span-2 bg-panel border border-line rounded-lg p-5">
        <div className="text-xs uppercase tracking-widest text-mist font-display">Files Analyzed</div>
        <div className="text-3xl font-display text-white mt-2">{analysis.files_analyzed}</div>
      </div>

      {CONFIG.map((c) => (
        <div key={c.key} className="bg-panel border border-line rounded-lg p-5 relative overflow-hidden">
          <div className={`absolute left-0 top-0 h-full w-1 ${c.color}`} />
          <div className="text-xs uppercase tracking-widest text-mist font-display">{c.label}</div>
          <div className={`text-3xl font-display mt-2 ${c.text}`}>{analysis[c.key]}</div>
        </div>
      ))}
    </div>
  );
}
