import os

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "apps/web/src/lib/types.ts": """
export interface LevelMetric {
  extrapolation_distance: number;
  accuracy: number;
  error_rate: number;
  total: number;
}

export interface PredictionResult {
  task_id: string;
  complexity: number;
  extrapolation_distance: number;
  prediction: string;
  ground_truth: string;
  correct: boolean;
  input_representation: string;
}

export interface ExperimentResult {
  experiment_id: string;
  task_family: string;
  demonstration_coverage: number;
  extrapolation_levels: number[];
  level_metrics: Record<string, LevelMetric>;
  raw_results: PredictionResult[];
  cliff_detected: boolean;
  cliff_type: string;
  estimated_cliff_location: number | null;
}

export interface ExperimentConfig {
  master_seed: number;
  demonstration_count: number;
  demonstration_complexity: number;
  extrapolation_levels: number[];
  tasks_per_level: number;
  evaluator_type: string;
}
""",
    "apps/web/src/lib/api.ts": """
import { ExperimentConfig, ExperimentResult } from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://127.0.0.1:8000';

export async function runExperiment(config: ExperimentConfig): Promise<ExperimentResult> {
  const response = await fetch(`${API_BASE}/api/v1/experiments`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(config),
  });
  
  if (!response.ok) {
    const errorData = await response.json().catch(() => null);
    throw new Error(errorData?.detail || 'Experiment server is unavailable.');
  }
  
  return response.json();
}
""",
    "apps/web/src/app/globals.css": """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground font-sans;
  }
}
""",
    "apps/web/src/components/ExperimentPanel.tsx": """
'use client';
import { useState } from 'react';
import { runExperiment } from '../lib/api';
import { ExperimentResult, ExperimentConfig } from '../lib/types';
import { ResultView } from './ResultView';

export function ExperimentPanel() {
  const [config, setConfig] = useState<ExperimentConfig>({
    master_seed: 2026,
    demonstration_count: 3,
    demonstration_complexity: 2,
    extrapolation_levels: [0, 1, 2, 3, 4],
    tasks_per_level: 5,
    evaluator_type: "deterministic",
  });
  
  const [result, setResult] = useState<ExperimentResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      const res = await runExperiment(config);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto my-8 p-6 border rounded-xl shadow-sm bg-white">
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">Experiment Settings</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium mb-1">Seed</label>
            <input 
              type="number" 
              className="w-full border rounded p-2" 
              value={config.master_seed} 
              onChange={e => setConfig({...config, master_seed: parseInt(e.target.value)})} 
            />
          </div>
          <div>
            <label className="block text-sm font-medium mb-1">Demonstration Complexity (Coverage)</label>
            <input 
              type="number" 
              className="w-full border rounded p-2" 
              value={config.demonstration_complexity} 
              onChange={e => setConfig({...config, demonstration_complexity: parseInt(e.target.value)})} 
              min={1} max={5}
            />
          </div>
        </div>
        
        <button 
          onClick={handleRun}
          disabled={loading}
          className="mt-6 w-full bg-black text-white rounded-lg py-3 font-semibold hover:bg-gray-800 disabled:opacity-50"
        >
          {loading ? 'Running experiment...' : 'Start Experiment'}
        </button>
        {error && (
          <div className="mt-4 p-4 bg-red-50 text-red-700 rounded border border-red-200">
            {error}
          </div>
        )}
      </div>

      {result && <ResultView result={result} />}
    </div>
  );
}
""",
    "apps/web/src/components/ResultView.tsx": """
'use client';
import { useState } from 'react';
import { ExperimentResult, PredictionResult } from '../lib/types';
import { AccuracyChart } from './AccuracyChart';

export function ResultView({ result }: { result: ExperimentResult }) {
  const [activeTaskIndex, setActiveTaskIndex] = useState(0);
  const [showTruth, setShowTruth] = useState(false);

  const task = result.raw_results[activeTaskIndex];
  const maxIndex = result.raw_results.length - 1;

  const handleNext = () => {
    if (activeTaskIndex < maxIndex) {
      setActiveTaskIndex(i => i + 1);
      setShowTruth(false);
    }
  };

  const handlePrev = () => {
    if (activeTaskIndex > 0) {
      setActiveTaskIndex(i => i - 1);
      setShowTruth(false);
    }
  };

  return (
    <div className="mt-8 pt-8 border-t">
      <div className="mb-6 p-4 bg-gray-50 rounded-lg">
        <h3 className="font-bold mb-2">Coverage Cliff Analysis</h3>
        <p className="mb-1"><strong>Detected:</strong> {result.cliff_detected ? 'YES' : 'NO'}</p>
        <p className="mb-1"><strong>Type:</strong> {result.cliff_type.replace('_', ' ')}</p>
        {result.estimated_cliff_location !== null && (
          <p><strong>Location:</strong> Extrapolation distance {result.estimated_cliff_location}</p>
        )}
      </div>
      
      <AccuracyChart levelMetrics={result.level_metrics} />

      <div className="mt-8 border rounded-lg overflow-hidden">
        <div className="bg-gray-100 p-4 border-b flex justify-between items-center">
          <h4 className="font-semibold">Task Explorer</h4>
          <div className="text-sm">
            Task {activeTaskIndex + 1} of {result.raw_results.length} | Extrapolation: +{task.extrapolation_distance}
          </div>
        </div>
        
        <div className="p-6">
          <div className="mb-6 p-4 bg-slate-50 border rounded font-mono text-sm whitespace-pre-wrap">
            {task.input_representation}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 border rounded-lg bg-white shadow-sm">
              <h5 className="text-xs font-bold text-gray-500 mb-2 uppercase tracking-wider">Model Prediction</h5>
              <div className="text-xl font-mono font-bold text-center py-4">{task.prediction}</div>
            </div>
            
            <div className="p-4 border rounded-lg bg-white shadow-sm">
              <h5 className="text-xs font-bold text-gray-500 mb-2 uppercase tracking-wider flex justify-between">
                <span>Ground Truth</span>
                {!showTruth && (
                  <button onClick={() => setShowTruth(true)} className="text-blue-600 hover:underline">Reveal</button>
                )}
              </h5>
              
              {showTruth ? (
                <div className="text-center">
                  <div className="text-xl font-mono font-bold py-4">{task.ground_truth}</div>
                  <div className={`mt-2 font-bold ${task.correct ? 'text-green-600' : 'text-red-600'}`}>
                    {task.correct ? '✓ CORRECT' : '✕ INCORRECT'}
                  </div>
                </div>
              ) : (
                <div className="flex items-center justify-center py-4 h-full text-gray-400 italic">
                  Hidden
                </div>
              )}
            </div>
          </div>
          
          <div className="mt-6 flex justify-between">
            <button onClick={handlePrev} disabled={activeTaskIndex === 0} className="px-4 py-2 border rounded disabled:opacity-50">Previous Task</button>
            <button onClick={handleNext} disabled={activeTaskIndex === maxIndex} className="px-4 py-2 bg-black text-white rounded disabled:opacity-50">Next Task</button>
          </div>
        </div>
      </div>
    </div>
  );
}
""",
    "apps/web/src/components/AccuracyChart.tsx": """
'use client';
import { LevelMetric } from '../lib/types';

export function AccuracyChart({ levelMetrics }: { levelMetrics: Record<string, LevelMetric> }) {
  const data = Object.values(levelMetrics).sort((a, b) => a.extrapolation_distance - b.extrapolation_distance);
  
  const maxAccuracy = 1.0;
  
  return (
    <div className="p-6 border rounded-xl bg-white shadow-sm">
      <h3 className="font-bold text-lg mb-6">Performance Curve</h3>
      <div className="flex items-end h-64 gap-2 border-b border-l pb-2 pl-2">
        {data.map((point) => (
          <div key={point.extrapolation_distance} className="relative flex-1 flex flex-col justify-end items-center group">
            <div 
              className={`w-full max-w-[40px] rounded-t-sm transition-all duration-500 ${point.accuracy > 0.5 ? 'bg-black' : 'bg-red-500'}`}
              style={{ height: `${point.accuracy * 100}%` }}
            ></div>
            <div className="absolute -bottom-8 text-xs font-mono">+{point.extrapolation_distance}</div>
            <div className="opacity-0 group-hover:opacity-100 absolute -top-8 bg-black text-white text-xs py-1 px-2 rounded whitespace-nowrap z-10 transition-opacity">
              {Math.round(point.accuracy * 100)}%
            </div>
          </div>
        ))}
      </div>
      <div className="mt-10 text-center text-sm text-gray-500 uppercase tracking-widest">
        Extrapolation Distance
      </div>
    </div>
  );
}
""",
    "apps/web/src/app/page.tsx": """
import { ExperimentPanel } from '../components/ExperimentPanel';

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
      
      <footer className="mt-16 text-center text-sm text-gray-400 py-8 border-t">
        Coverage Cliff - Pathway / DataForge 2026
      </footer>
    </main>
  );
}
"""
}

for path, content in files.items():
    write_file(path, content)

print("Frontend scaffolding generated successfully.")
