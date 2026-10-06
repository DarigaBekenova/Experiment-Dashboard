"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { api } from "@/lib/api";
import type { ExperimentInput, FormState } from "@/lib/types";

function parseForm(formData: FormData): ExperimentInput | null {
  const text = (name: string) => String(formData.get(name) ?? "").trim();
  const name = text("name");
  const dataset = text("dataset");
  const model_name = text("model_name");
  const statusRaw = text("status") || "planned";
  const allowed = ["planned", "running", "completed", "failed"];
  if (name.length < 3 || dataset.length < 2 || model_name.length < 2) return null;
  if (!allowed.includes(statusRaw)) return null;
  const accRaw = text("accuracy");
  const durRaw = text("duration_sec");
  const accuracy = accRaw === "" ? null : Number(accRaw);
  const duration_sec = durRaw === "" ? null : Number(durRaw);
  if (accuracy !== null && !(accuracy >= 0 && accuracy <= 1)) return null;
  if (duration_sec !== null && !(duration_sec >= 0)) return null;
  return {
    name,
    dataset,
    model_name,
    status: statusRaw as ExperimentInput["status"],
    accuracy,
    duration_sec,
    notes: text("notes") || null,
  };
}

export async function createExperiment(_prev: FormState, formData: FormData): Promise<FormState> {
  const data = parseForm(formData);
  if (!data) return { error: "Проверьте поля: название, датасет, модель обязательны; accuracy 0–1." };
  let id: number;
  try {
    id = (await api.create(data)).id;
  } catch {
    return { error: "Не удалось сохранить эксперимент." };
  }
  revalidatePath("/experiments");
  redirect(`/experiments/${id}`);
}

export async function updateExperiment(
  id: number,
  _prev: FormState,
  formData: FormData,
): Promise<FormState> {
  const data = parseForm(formData);
  if (!data) return { error: "Проверьте поля: название, датасет, модель обязательны." };
  try {
    await api.update(id, data);
  } catch {
    return { error: "Не удалось сохранить изменения." };
  }
  revalidatePath("/experiments");
  redirect(`/experiments/${id}`);
}

export async function deleteExperiment(id: number) {
  await api.remove(id);
  revalidatePath("/experiments");
  redirect("/experiments");
}
