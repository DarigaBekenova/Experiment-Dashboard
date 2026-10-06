import Link from "next/link";
import { api } from "@/lib/api";

const PAGE_SIZE = 20;

export default async function ExperimentsPage({
  searchParams,
}: {
  searchParams: Promise<{ q?: string; page?: string; status?: string; sort_by?: string; sort_order?: string }>;
}) {
  const { q, page, status, sort_by, sort_order } = await searchParams;
  const current = Math.max(1, Number(page) || 1);
  const sortBy = sort_by || "created_at";
  const sortOrder = sort_order === "asc" ? "asc" : "desc";

  let items = [];
  let stats = null;
  try {
    [items, stats] = await Promise.all([
      api.list(q, current, PAGE_SIZE, status, sortBy, sortOrder),
      api.stats(),
    ]);
  } catch {
    return <p className="text-red-700">Бэкенд недоступен. Запустите docker compose up --build.</p>;
  }

  const link = (p: number) =>
    `/experiments?${new URLSearchParams({
      ...(q ? { q } : {}),
      ...(status ? { status } : {}),
      sort_by: sortBy,
      sort_order: sortOrder,
      page: String(p),
    })}`;

  const withSort = (sb: string, so: string) =>
    `/experiments?${new URLSearchParams({
      ...(q ? { q } : {}),
      ...(status ? { status } : {}),
      page: "1",
      sort_by: sb,
      sort_order: so,
    })}`;

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Эксперименты</h1>
        <Link href="/experiments/new" className="rounded bg-blue-700 px-4 py-2 text-white">
          Добавить
        </Link>
      </div>

      {stats && (
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <div className="rounded border bg-white p-3">
            <p className="text-sm text-gray-500">Всего</p>
            <p className="text-xl font-bold">{stats.total}</p>
          </div>
          <div className="rounded border bg-white p-3">
            <p className="text-sm text-gray-500">Средняя accuracy</p>
            <p className="text-xl font-bold">{stats.avg_accuracy?.toFixed(3) ?? "—"}</p>
          </div>
          <div className="rounded border bg-white p-3">
            <p className="text-sm text-gray-500">Лучший ID</p>
            <p className="text-xl font-bold">{stats.best_id ?? "—"}</p>
          </div>
          <div className="rounded border bg-white p-3">
            <p className="text-sm text-gray-500">Completed</p>
            <p className="text-xl font-bold">{stats.by_status?.completed ?? 0}</p>
          </div>
        </div>
      )}

      <form className="flex flex-col gap-2 sm:flex-row">
        <input
          name="q"
          defaultValue={q}
          placeholder="Поиск: название, датасет, модель"
          className="flex-1 rounded border px-3 py-2"
        />
        <select name="status" defaultValue={status ?? ""} className="rounded border px-3 py-2">
          <option value="">Все статусы</option>
          <option value="planned">planned</option>
          <option value="running">running</option>
          <option value="completed">completed</option>
          <option value="failed">failed</option>
        </select>
        <input type="hidden" name="sort_by" value={sortBy} />
        <input type="hidden" name="sort_order" value={sortOrder} />
        <button className="rounded border bg-white px-4 py-2">Найти</button>
      </form>

      <div className="flex gap-4 text-sm">
        <span>Сортировка:</span>
        <Link href={withSort("created_at", "desc")} className="underline">новые</Link>
        <Link href={withSort("accuracy", "desc")} className="underline">по accuracy ↓</Link>
        <Link href={withSort("accuracy", "asc")} className="underline">по accuracy ↑</Link>
        <Link href={withSort("name", "asc")} className="underline">по имени</Link>
      </div>

      {items.length === 0 ? (
        <p className="text-gray-600">Ничего не найдено.</p>
      ) : (
        <ul className="space-y-3">
          {items.map((p) => (
            <li key={p.id} className="rounded border bg-white p-4">
              <Link href={`/experiments/${p.id}`} className="font-semibold hover:underline">
                {p.name}
              </Link>
              <p className="text-sm text-gray-600">
                {p.model_name} · {p.dataset} · {p.status}
                {p.accuracy != null ? ` · acc ${p.accuracy}` : ""}
              </p>
            </li>
          ))}
        </ul>
      )}

      <div className="flex justify-between">
        {current > 1 ? <Link href={link(current - 1)}>← Назад</Link> : <span />}
        {items.length === PAGE_SIZE && <Link href={link(current + 1)}>Далее →</Link>}
      </div>
    </section>
  );
}
