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
  const [loadingText, setLoadingText] = useState("");

  const handleRun = async () => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    // Fake loading steps to visually indicate backend work pipeline
    setLoadingText("GENERATING CONTROLLED TASKS...");
    
    try {
      setTimeout(() => setLoadingText("VALIDATING GROUND TRUTH..."), 400);
      setTimeout(() => setLoadingText("EVALUATING PREDICTIONS..."), 800);
      setTimeout(() => setLoadingText("COMPUTING ACCURACY..."), 1200);
      
      const res = await runExperiment(config);
      setResult(res);
    } catch (err: any) {
      setError(err.message || 'Experiment service unavailable. Please start the backend and try again.');
    } finally {
      setTimeout(() => setLoading(false), 1300);
    }
  };

  return (
    <div className="w-full max-w-4xl mx-auto my-8">
      <div className="bg-white p-8 border rounded-xl shadow-lg relative overflow-hidden">
        
        {loading && (
          <div className="absolute inset-0 bg-white/90 backdrop-blur-sm z-10 flex flex-col items-center justify-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-black mb-4"></div>
            <div className="font-mono text-sm font-bold tracking-widest">{loadingText}</div>
          </div>
        )}

        <div className="text-center mb-8">
          <h2 className="text-3xl font-extrabold">The Laboratory</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8 bg-gray-50 p-6 rounded-lg border">
          <div>
            <label className="block text-sm font-bold mb-1 text-gray-900">How much has the model seen?</label>
            <div className="text-xs text-gray-500 mb-2">Demonstration Coverage</div>
            <input 
              type="number" 
              className="w-full border rounded p-2" 
              value={config.demonstration_complexity} 
              onChange={e => setConfig({...config, demonstration_complexity: parseInt(e.target.value)})} 
              min={1} max={5}
            />
          </div>
          <div>
            <label className="block text-sm font-bold mb-1 text-gray-900">How far should we push beyond it?</label>
            <div className="text-xs text-gray-500 mb-2">Extrapolation Range (Max)</div>
            <input 
              type="number" 
              className="w-full border rounded p-2" 
              value={Math.max(...config.extrapolation_levels)} 
              onChange={e => {
                const max = parseInt(e.target.value);
                const levels = Array.from({length: max + 1}, (_, i) => i);
                setConfig({...config, extrapolation_levels: levels});
              }} 
              min={1} max={8}
            />
          </div>
          <div>
            <label className="block text-sm font-bold mb-1 text-gray-900">Try a different world</label>
            <div className="text-xs text-gray-500 mb-2">Random Seed</div>
            <input 
              type="number" 
              className="w-full border rounded p-2" 
              value={config.master_seed} 
              onChange={e => setConfig({...config, master_seed: parseInt(e.target.value)})} 
            />
          </div>
        </div>
        
        <div className="flex flex-col md:flex-row gap-4">
          <button 
            onClick={handleRun}
            disabled={loading}
            className="flex-1 bg-black text-white rounded-lg py-4 font-bold text-lg hover:bg-gray-800 disabled:opacity-50 transition-all shadow-md"
          >
            RUN THE EXPERIMENT
          </button>
          
          {result && (
            <button 
              onClick={() => {
                setConfig({...config, master_seed: config.master_seed + 1});
                setResult(null);
                // Trigger click visually later
              }}
              className="md:w-1/3 bg-white text-black border-2 border-black rounded-lg py-4 font-bold text-lg hover:bg-gray-50 transition-all"
            >
              CHALLENGE THE CLAIM
            </button>
          )}
        </div>
        
        {result && (
          <div className="mt-4 text-center text-xs text-gray-500 italic">
            Does the cliff move if we change the experiment? Click 'Challenge the Claim'.
          </div>
        )}
        
        {error && (
          <div className="mt-6 p-4 bg-red-50 text-red-700 rounded border border-red-200 text-sm font-medium">
            {error}
          </div>
        )}
      </div>

      {result && <ResultView result={result} seed={config.master_seed} />}
    </div>
  );
}
