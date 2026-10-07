import { useState } from "react";

export default function RepoForm({ onAnalyze, loading }) {
  const [url, setUrl] = useState("");

  function handleSubmit(e) {
    e.preventDefault();
    if (!url.trim()) return;
    onAnalyze(url.trim());
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <label className="block text-xs uppercase tracking-widest text-mist mb-2 font-display">
        Repository URL
      </label>
      <div className="flex gap-3">
        <input
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://github.com/org/repo"
          className="flex-1 bg-panel border border-line rounded-md px-4 py-3 font-display text-sm
                     text-white placeholder-mist/50 focus:outline-none focus:ring-2 focus:ring-accent
                     focus:border-accent transition"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 rounded-md bg-accent hover:bg-accent/85 disabled:opacity-40
                     disabled:cursor-not-allowed text-white font-medium text-sm transition
                     whitespace-nowrap"
        >
          {loading ? "Scanning…" : "Analyze"}
        </button>
      </div>
    </form>
  );
}
