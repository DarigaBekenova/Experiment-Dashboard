import type { Experiment, ExperimentInput, ExperimentStats } from "./types";

const API_URL = process.env.API_URL ?? "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    cache: "no-store",
    ...init,
    headers: { "Content-Type": "application/json", ...init?.headers },
  });
  if (!res.ok) {
    throw new Error(`API ${res.status}: ${await res.text()}`);
  }
  return (res.status === 204 ? undefined : await res.json()) as T;
}

export const api = {
  list(q?: string, page = 1, pageSize = 20, status?: string, sort_by = "created_at", sort_order = "desc") {
    const params = new URLSearchParams({
      limit: String(pageSize),
      offset: String((page - 1) * pageSize),
      sort_by,
      sort_order,
    });
    if (q) params.set("q", q);
    if (status) params.set("status", status);
    return request<Experiment[]>(`/experiments?${params}`);
  },
  stats() {
    return request<ExperimentStats>("/experiments/stats");
  },
  async get(id: number): Promise<Experiment | null> {
    const res = await fetch(`${API_URL}/experiments/${id}`, { cache: "no-store" });
    if (res.status === 404) return null;
    if (!res.ok) throw new Error(`API ${res.status}`);
    return res.json();
  },
  create(data: ExperimentInput) {
    return request<Experiment>("/experiments", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },
  update(id: number, data: Partial<ExperimentInput>) {
    return request<Experiment>(`/experiments/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },
  remove(id: number) {
    return request<void>(`/experiments/${id}`, { method: "DELETE" });
  },
};
