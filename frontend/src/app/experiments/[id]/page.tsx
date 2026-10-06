import { notFound } from "next/navigation";
import { ExperimentForm } from "@/components/ExperimentForm";
import { api } from "@/lib/api";
import { deleteExperiment, updateExperiment } from "../actions";

export default async function ExperimentPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  let pub;
  try {
    pub = await api.get(Number(id));
  } catch {
    notFound();
  }
  if (!pub) notFound();
  return (
    <article className="space-y-6">
      <header>
        <h1 className="text-2xl font-bold">{pub.name}</h1>
        <p className="text-gray-600">
          {pub.model_name} · {pub.dataset} · {pub.status}
        </p>
        <p className="text-gray-600">
          Accuracy: {pub.accuracy ?? "—"} · Длительность: {pub.duration_sec ?? "—"} сек
        </p>
      </header>
      {pub.notes && <p className="whitespace-pre-line">{pub.notes}</p>}
      <details className="rounded border bg-white p-4">
        <summary className="cursor-pointer font-semibold">Редактировать</summary>
        <div className="mt-4">
          <ExperimentForm action={updateExperiment.bind(null, pub.id)} initial={pub} />
        </div>
      </details>
      <form action={deleteExperiment.bind(null, pub.id)}>
        <button className="rounded border border-red-700 px-4 py-2 text-red-700">Удалить</button>
      </form>
    </article>
  );
}
