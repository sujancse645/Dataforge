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
