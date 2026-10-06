import { ExperimentForm } from "@/components/ExperimentForm";
import { createExperiment } from "../actions";

export default function NewExperimentPage() {
  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-bold">Новый эксперимент</h1>
      <ExperimentForm action={createExperiment} />
    </section>
  );
}
