import { ExperimentPanel } from '../components/ExperimentPanel';
import { BdhCqModule } from '../components/BdhCqModule';

export default function Home() {
  return (
    <main className="min-h-screen p-8 max-w-6xl mx-auto">
      <header className="mb-16 text-center pt-12">
        <h1 className="text-5xl font-extrabold tracking-tight mb-4">
          Can an AI generalize beyond what you showed it?
        </h1>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Give a model a few examples. Then push the same rule beyond the complexity it has seen.
        </p>
      </header>

      <section className="mb-16 max-w-3xl mx-auto text-center">
        <h2 className="text-xs font-bold uppercase tracking-widest text-gray-500 mb-2">Our Claim</h2>
        <p className="text-2xl italic font-serif text-gray-800">
          "A model can appear to generalize successfully within the complexity of its demonstrations, yet fail sharply when the same underlying rule is pushed beyond that demonstrated coverage."
        </p>
        <p className="mt-4 text-gray-600">This is testable. Let's try to break it.</p>
      </section>

      <ExperimentPanel />

      <section className="mt-24 max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-8 text-sm text-gray-600">
        <div>
          <h3 className="font-bold text-gray-900 mb-2 uppercase text-xs tracking-widest">Methodology</h3>
          <p className="mb-2">1. Generate a hidden transitive rule.</p>
          <p className="mb-2">2. Generate demonstrations and measure their structural coverage.</p>
          <p className="mb-2">3. Generate test tasks at increasing extrapolation distances.</p>
          <p className="mb-2">4. Compute exact ground truth independently (via Z3 solver).</p>
          <p className="mb-2">5. Evaluate model predictions and compare with ground truth.</p>
          <p>6. Detect whether the observed accuracy drops sharply (a Coverage Cliff).</p>
        </div>
        <div>
          <h3 className="font-bold text-gray-900 mb-2 uppercase text-xs tracking-widest">What this does not prove</h3>
          <p className="mb-4">
            A single experiment does not prove that every AI model has the same extrapolation boundary. A detected cliff is evidence for this experimental setup, not a universal law.
          </p>
          <h3 className="font-bold text-gray-900 mb-2 uppercase text-xs tracking-widest">Provenance</h3>
          <p>Experiment Engine: Python + Z3<br/>API: FastAPI<br/>Interface: Next.js</p>
        </div>
      </section>
      
      <BdhCqModule />

      <footer className="mt-16 text-center text-sm text-gray-400 py-8 border-t">
        Coverage Cliff - Pathway / DataForge 2026
      </footer>
    </main>
  );
}
