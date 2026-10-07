import axios from "axios";

const API_BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";

export const api = axios.create({ baseURL: API_BASE });

export function analyzeRepo(repoUrl, token) {
  return api.post(
    "/analyze",
    { repo_url: repoUrl },
    token ? { headers: { Authorization: `Bearer ${token}` } } : undefined
  );
}

export function getAnalysis(id) {
  return api.get(`/analyze/${id}`);
}

export function listAnalyses(token) {
  return api.get(
    "/analyses",
    token ? { headers: { Authorization: `Bearer ${token}` } } : undefined
  );
}
