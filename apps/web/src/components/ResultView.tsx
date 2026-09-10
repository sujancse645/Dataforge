'use client';
import { useState } from 'react';
import { ExperimentResult } from '../lib/types';
import { AccuracyChart } from './AccuracyChart';

export function ResultView({ result, seed }: { result: ExperimentResult, seed: number }) {
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

  const isSharpCliff = result.cliff_detected && result.cliff_type === 'SHARP_CLIFF';
  const cliffTitle = result.cliff_detected ? 'COVERAGE CLIFF DETECTED' : (result.cliff_type === 'STABLE' ? 'NO COVERAGE CLIFF DETECTED' : result.cliff_type.replace('_', ' '));

  return (
    <div className="mt-12 animate-in fade-in slide-in-from-bottom-4 duration-700">
      <div className="text-center mb-6">
        <span className="inline-block bg-green-900/50 text-green-400 text-[10px] font-bold px-3 py-1 rounded uppercase border border-green-700/50 mb-2 shadow-[0_0_10px_rgba(34,197,94,0.3)]">OUR LIVE EXPERIMENT</span>
        <div className="text-sm text-slate-500 font-mono">Experiment Seed: <span className="text-purple-400">{seed}</span> | Reproducible from configuration</div>
      </div>
      
      <div className={`p-8 rounded-xl border mb-8 glass ${result.cliff_detected ? 'bg-red-950/30 border-red-900/50 shadow-[0_0_30px_rgba(220,38,38,0.15)]' : 'bg-slate-900/50 border-slate-700/50'}`}>
        <h3 className={`font-black text-2xl mb-2 ${result.cliff_detected ? 'text-red-400 text-glow' : 'text-slate-200'}`}>
          {cliffTitle}
        </h3>
        {result.estimated_cliff_location !== null && (
          <p className="font-mono text-sm mb-4 text-slate-300">Estimated boundary: <span className="text-cyan-400 font-bold">Extrapolation distance {result.estimated_cliff_location}</span></p>
        )}
        
        <div className="mt-4 pt-4 border-t border-slate-700/50">
          <h4 className="font-bold text-xs uppercase tracking-widest mb-2 text-slate-400">What this experiment shows</h4>
          <p className="text-sm text-slate-300 leading-relaxed">
            {isSharpCliff ? 
              `Under this experiment's conditions, the evaluator remained correct through the tested in-coverage and near-boundary levels, then failed sharply at extrapolation distance ${result.estimated_cliff_location}.` :
              `Under this experiment's conditions, the evaluator exhibited ${result.cliff_type.toLowerCase().replace('_', ' ')}.`
            }
          </p>
        </div>
      </div>
      
      <div className="glass-card p-4 sm:p-6 mb-12 border-t-4 border-purple-500">
         <AccuracyChart levelMetrics={result.level_metrics} cliffLocation={result.estimated_cliff_location} />
      </div>

      <div className="border border-slate-700 rounded-xl overflow-hidden glass shadow-2xl">
        <div className="bg-slate-950/80 text-white p-6 border-b border-slate-800">
          <h4 className="font-bold text-lg mb-2 text-glow-cyan">Task Explorer</h4>
          <div className="text-sm text-slate-400">
            Task {activeTaskIndex + 1} of {result.raw_results.length} | <span className="text-purple-400">Extrapolation Distance: +{task.extrapolation_distance}</span>
          </div>
        </div>
        
        <div className="p-8">
          <div className="mb-8 p-6 bg-slate-950/50 border border-slate-800 rounded-lg font-mono text-sm whitespace-pre-wrap leading-relaxed text-cyan-100 shadow-inner">
            {task.input_representation}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div className="p-6 border border-slate-700 rounded-xl bg-slate-900/80 relative shadow-lg">
              <div className="absolute -top-3 left-4 bg-slate-800 px-3 py-0.5 rounded text-xs font-bold uppercase tracking-widest text-cyan-400 border border-slate-700">Evaluator Prediction</div>
              <div className="text-2xl font-mono font-bold text-center py-6 text-slate-200">{task.prediction}</div>
            </div>
            
            <div className={`p-6 border rounded-xl relative transition-all duration-700 shadow-lg ${showTruth ? (task.correct ? 'border-green-500/50 bg-green-950/30 shadow-[0_0_20px_rgba(34,197,94,0.2)]' : 'border-red-500/50 bg-red-950/30 shadow-[0_0_20px_rgba(239,68,68,0.2)]') : 'border-slate-700 bg-slate-900/80'}`}>
              <div className="absolute -top-3 left-4 bg-slate-800 px-3 py-0.5 rounded text-xs font-bold uppercase tracking-widest text-purple-400 border border-slate-700 flex items-center gap-2">
                Ground Truth
              </div>
              
              {showTruth ? (
                <div className="text-center animate-in zoom-in-95 duration-300">
                  <div className="text-2xl font-mono font-bold py-6 text-slate-200">{task.ground_truth}</div>
                  <div className={`mt-2 font-black text-lg tracking-widest ${task.correct ? 'text-green-400 text-glow' : 'text-red-400 text-glow'}`}>
                    {task.correct ? '✓ CORRECT' : '✗ INCORRECT'}
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-4 h-full">
                  <p className="text-xs text-slate-400 mb-4 text-center px-4">Ground truth is generated independently from the evaluator via a Z3 exact solver.</p>
                  <button 
                    onClick={() => setShowTruth(true)} 
                    className="bg-slate-800 text-slate-200 border border-slate-600 px-6 py-2 rounded-full font-bold hover:bg-slate-700 hover:text-white transition-all hover:border-purple-500 hover:shadow-[0_0_15px_rgba(168,85,247,0.4)]"
                  >
                    Reveal Ground Truth
                  </button>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex justify-between items-center border-t border-slate-800 pt-6">
            <button onClick={handlePrev} disabled={activeTaskIndex === 0} className="px-6 py-2 border border-slate-700 rounded-lg font-bold disabled:opacity-30 hover:bg-slate-800 text-slate-300 transition-colors">Previous</button>
            <button onClick={handleNext} disabled={activeTaskIndex === maxIndex} className="px-6 py-2 bg-gradient-to-r from-purple-700 to-cyan-700 text-white rounded-lg font-bold disabled:opacity-30 hover:from-purple-600 hover:to-cyan-600 transition-all shadow-md">Next Task</button>
          </div>
        </div>
      </div>
      
      <div className="mt-12 bg-blue-950/30 border border-blue-900/50 p-6 rounded-xl flex items-start gap-4 glass">
        <div className="text-blue-400 mt-1">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        </div>
        <div>
          <h4 className="font-bold text-blue-300 mb-1">Methodology: Ground Truth is Trustworthy</h4>
          <p className="text-sm text-blue-200/70 leading-relaxed">
            Ground truth is generated independently from the evaluator via an exact mathematical solver. The evaluator does not receive the hidden rule, ground truth, or generator internals. Zero data leakage is mathematically guaranteed.
          </p>
        </div>
      </div>
    </div>
  );
}
