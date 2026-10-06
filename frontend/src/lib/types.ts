export type ExperimentStatus = "planned" | "running" | "completed" | "failed";

export type Experiment = {
  id: number;
  name: string;
  dataset: string;
  model_name: string;
  status: ExperimentStatus;
  accuracy: number | null;
  duration_sec: number | null;
  notes: string | null;
  created_at: string;
};

export type ExperimentInput = Omit<Experiment, "id" | "created_at">;

export type ExperimentStats = {
  total: number;
  by_status: Record<string, number>;
  avg_accuracy: number | null;
  best_id: number | null;
  best_accuracy: number | null;
};

export type FormState = { error?: string };
