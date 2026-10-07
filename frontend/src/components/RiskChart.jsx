import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from "recharts";

const COLORS = { HIGH: "#E5484D", MEDIUM: "#F5A524", LOW: "#3DD68C" };

export default function RiskChart({ analysis }) {
  const data = [
    { name: "High", value: analysis.high_risk_count, key: "HIGH" },
    { name: "Medium", value: analysis.medium_risk_count, key: "MEDIUM" },
    { name: "Low", value: analysis.low_risk_count, key: "LOW" },
  ].filter((d) => d.value > 0);

  if (data.length === 0) return null;

  return (
    <div className="bg-panel border border-line rounded-lg p-5">
      <div className="text-xs uppercase tracking-widest text-mist font-display mb-3">
        Risk Distribution
      </div>
      <ResponsiveContainer width="100%" height={220}>
        <PieChart>
          <Pie
            data={data}
            dataKey="value"
            nameKey="name"
            innerRadius={55}
            outerRadius={85}
            paddingAngle={3}
          >
            {data.map((d) => (
              <Cell key={d.key} fill={COLORS[d.key]} stroke="#0B0F14" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip
            contentStyle={{ background: "#121821", border: "1px solid #232C38", borderRadius: 8 }}
            itemStyle={{ color: "#E6EBF2" }}
          />
          <Legend wrapperStyle={{ fontSize: 12, color: "#8A97A6" }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
