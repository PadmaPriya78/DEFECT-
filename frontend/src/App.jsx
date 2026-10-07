import { useState } from "react";
import RepoForm from "./components/RepoForm.jsx";
import SummaryCards from "./components/SummaryCards.jsx";
import RiskChart from "./components/RiskChart.jsx";
import ModuleTable from "./components/ModuleTable.jsx";
import { analyzeRepo } from "./api.js";

export default function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  async function handleAnalyze(repoUrl) {
    setLoading(true);
    setError(null);
    setAnalysis(null);
    try {
      const res = await analyzeRepo(repoUrl);
      if (res.data.status === "failed") {
        setError(res.data.error_message || "Analysis failed.");
      } else {
        setAnalysis(res.data);
      }
    } catch (e) {
      setError(e?.response?.data?.detail || "Could not reach the analysis service.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen scanline">
      <header className="border-b border-line">
        <div className="max-w-5xl mx-auto px-6 py-6 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded bg-accent/15 border border-accent/30 flex items-center justify-center">
              <span className="text-accent font-display text-sm">DG</span>
            </div>
            <div>
              <div className="font-display text-white text-sm tracking-wide">DefectGuard AI</div>
              <div className="text-xs text-mist">Repository defect & risk analyzer</div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-10 space-y-8">
        <div className="bg-panel border border-line rounded-lg p-6">
          <RepoForm onAnalyze={handleAnalyze} loading={loading} />
          {error && (
            <div className="mt-4 text-sm text-signal-high bg-signal-high/10 border border-signal-high/30 rounded-md px-4 py-3">
              {error}
            </div>
          )}
        </div>

        {loading && <ScanningState />}

        {analysis && !loading && (
          <div className="space-y-8">
            <SummaryCards analysis={analysis} />
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="md:col-span-1">
                <RiskChart analysis={analysis} />
              </div>
              <div className="md:col-span-2">
                <ModuleTable modules={analysis.modules} />
              </div>
            </div>
          </div>
        )}

        {!analysis && !loading && !error && (
          <div className="text-center py-16 text-mist text-sm">
            Paste a public GitHub repository URL above to scan it for defect risk.
          </div>
        )}
      </main>
    </div>
  );
}

function ScanningState() {
  return (
    <div className="bg-panel border border-line rounded-lg p-10 flex flex-col items-center gap-4">
      <div className="relative w-48 h-1 bg-line rounded-full overflow-hidden">
        <div className="absolute inset-y-0 left-0 w-1/3 bg-accent rounded-full animate-[scan_1.2s_ease-in-out_infinite]" />
      </div>
      <div className="text-xs text-mist font-display tracking-widest uppercase">
        Cloning, extracting, scoring…
      </div>
      <style>{`
        @keyframes scan {
          0% { transform: translateX(-100%); }
          100% { transform: translateX(300%); }
        }
      `}</style>
    </div>
  );
}
