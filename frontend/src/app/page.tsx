import Link from "next/link";

export default function HomePage() {
  return (
    <section className="space-y-4">
      <h1 className="text-3xl font-bold">Дашборд результатов экспериментов</h1>
      <p>
        Приложение для исследования по анализу данных: хранит результаты ML-экспериментов
        (датасет, модель, статус, accuracy, длительность), позволяет искать, сравнивать
        и вести учёт запусков. Пользователь — исследователь / докторант.
      </p>
      <Link
        href="/experiments"
        className="inline-block rounded bg-blue-700 px-4 py-2 text-white"
      >
        Перейти к экспериментам
      </Link>
    </section>
  );
}
