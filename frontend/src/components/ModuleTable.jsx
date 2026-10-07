import { useState } from "react";

const RISK_STYLE = {
  HIGH: "text-signal-high bg-signal-high/10 border-signal-high/30",
  MEDIUM: "text-signal-medium bg-signal-medium/10 border-signal-medium/30",
  LOW: "text-signal-low bg-signal-low/10 border-signal-low/30",
};

const RISK_ORDER = { HIGH: 0, MEDIUM: 1, LOW: 2 };

export default function ModuleTable({ modules }) {
  const [sortBy, setSortBy] = useState("risk");
  const [selected, setSelected] = useState(null);

  const sorted = [...modules].sort((a, b) => {
    if (sortBy === "risk") return RISK_ORDER[a.risk_level] - RISK_ORDER[b.risk_level];
    if (sortBy === "prob") return b.defect_probability - a.defect_probability;
    if (sortBy === "loc") return b.loc - a.loc;
    return 0;
  });

  return (
    <div className="bg-panel border border-line rounded-lg overflow-hidden">
      <div className="flex items-center justify-between px-5 py-4 border-b border-line">
        <div className="text-xs uppercase tracking-widest text-mist font-display">Modules</div>
        <select
          value={sortBy}
          onChange={(e) => setSortBy(e.target.value)}
          className="bg-ink border border-line rounded px-2 py-1 text-xs text-mist font-display"
        >
          <option value="risk">Sort: Risk</option>
          <option value="prob">Sort: Probability</option>
          <option value="loc">Sort: LOC</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-mist text-xs uppercase tracking-wider font-display border-b border-line">
              <th className="px-5 py-3">Module</th>
              <th className="px-5 py-3">LOC</th>
              <th className="px-5 py-3">Complexity</th>
              <th className="px-5 py-3">Probability</th>
              <th className="px-5 py-3">Risk</th>
              <th className="px-5 py-3">Reason</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((m) => (
              <tr
                key={m.file_path}
                onClick={() => setSelected(selected === m.file_path ? null : m.file_path)}
                className="border-b border-line/50 hover:bg-white/[0.02] cursor-pointer transition"
              >
                <td className="px-5 py-3 font-mono text-xs text-white/90">{m.file_path}</td>
                <td className="px-5 py-3 text-mist">{m.loc}</td>
                <td className="px-5 py-3 text-mist">{m.complexity}</td>
                <td className="px-5 py-3 text-mist">{(m.defect_probability * 100).toFixed(0)}%</td>
                <td className="px-5 py-3">
                  <span className={`inline-block px-2 py-0.5 rounded border text-xs font-medium ${RISK_STYLE[m.risk_level]}`}>
                    {m.risk_level}
                  </span>
                </td>
                <td className="px-5 py-3 text-mist text-xs truncate max-w-xs" title={m.flag_reason}>
                  {m.flag_reason || "-"}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && (
        <ModuleDetail module={modules.find((m) => m.file_path === selected)} />
      )}
    </div>
  );
}

function ModuleDetail({ module }) {
  if (!module) return null;
  return (
    <div className="px-5 py-4 border-t border-line bg-ink/50 text-sm">
      <div className="font-mono text-xs text-accent mb-2">{module.file_path}</div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs text-mist">
        <div>Functions: <span className="text-white">{module.num_functions}</span></div>
        <div>Classes: <span className="text-white">{module.num_classes}</span></div>
        <div>Imports: <span className="text-white">{module.num_imports}</span></div>
        <div>Comment ratio: <span className="text-white">{(module.comment_ratio * 100).toFixed(1)}%</span></div>
      </div>
    </div>
  );
}
