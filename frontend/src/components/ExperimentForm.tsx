"use client";

import { useActionState } from "react";
import type { Experiment, FormState } from "@/lib/types";

type Props = {
  action: (prev: FormState, formData: FormData) => Promise<FormState>;
  initial?: Experiment;
};

const field = "w-full rounded border px-3 py-2";

export function ExperimentForm({ action, initial }: Props) {
  const [state, formAction, pending] = useActionState(action, {});
  return (
    <form action={formAction} className="space-y-4">
      <label className="block">
        Название *
        <input name="name" required minLength={3} defaultValue={initial?.name} className={field} />
      </label>
      <label className="block">
        Датасет *
        <input name="dataset" required defaultValue={initial?.dataset} className={field} />
      </label>
      <label className="block">
        Модель *
        <input name="model_name" required defaultValue={initial?.model_name} className={field} />
      </label>
      <label className="block">
        Статус *
        <select name="status" defaultValue={initial?.status ?? "planned"} className={field}>
          <option value="planned">planned</option>
          <option value="running">running</option>
          <option value="completed">completed</option>
          <option value="failed">failed</option>
        </select>
      </label>
      <label className="block">
        Accuracy (0–1)
        <input
          name="accuracy"
          type="number"
          step="0.001"
          min={0}
          max={1}
          defaultValue={initial?.accuracy ?? ""}
          className={field}
        />
      </label>
      <label className="block">
        Длительность (сек)
        <input
          name="duration_sec"
          type="number"
          step="1"
          min={0}
          defaultValue={initial?.duration_sec ?? ""}
          className={field}
        />
      </label>
      <label className="block">
        Заметки
        <textarea name="notes" rows={4} defaultValue={initial?.notes ?? ""} className={field} />
      </label>
      {state.error && <p className="text-red-700">{state.error}</p>}
      <button
        disabled={pending}
        className="rounded bg-blue-700 px-4 py-2 text-white disabled:opacity-50"
      >
        {pending ? "Сохранение…" : "Сохранить"}
      </button>
    </form>
  );
}
