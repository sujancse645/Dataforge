'use client';
import { useState } from 'react';
import { ExperimentResult, PredictionResult } from '../lib/types';
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
    <div className="mt-12">
      <div className="text-center mb-6">
        <span className="inline-block bg-green-100 text-green-800 text-[10px] font-bold px-2 py-0.5 rounded uppercase border border-green-200 mb-2">OUR LIVE EXPERIMENT</span>
        <div className="text-sm text-gray-500 font-mono">Experiment Seed: {seed} | Reproducible from configuration</div>
      </div>
      
      <div className={`p-8 rounded-xl border-2 mb-8 ${result.cliff_detected ? 'bg-red-50 border-red-200' : 'bg-slate-50 border-slate-200'}`}>
        <h3 className={`font-black text-2xl mb-2 ${result.cliff_detected ? 'text-red-700' : 'text-slate-800'}`}>
          {cliffTitle}
        </h3>
        {result.estimated_cliff_location !== null && (
          <p className="font-mono text-sm mb-4">Estimated boundary: Extrapolation distance {result.estimated_cliff_location}</p>
        )}
        
        <div className="mt-4 pt-4 border-t border-black/10">
          <h4 className="font-bold text-sm uppercase tracking-widest mb-2">What this experiment shows</h4>
          <p className="text-sm text-gray-700">
            {isSharpCliff ? 
              `Under this experiment's conditions, the evaluator remained correct through the tested in-coverage and near-boundary levels, then failed sharply at extrapolation distance ${result.estimated_cliff_location}.` :
              `Under this experiment's conditions, the evaluator exhibited ${result.cliff_type.toLowerCase().replace('_', ' ')}.`
            }
          </p>
        </div>
      </div>
      
      <AccuracyChart levelMetrics={result.level_metrics} cliffLocation={result.estimated_cliff_location} />

      <div className="mt-12 border rounded-xl overflow-hidden bg-white shadow-sm">
        <div className="bg-gray-900 text-white p-6">
          <h4 className="font-bold text-lg mb-2">Task Explorer</h4>
          <div className="text-sm text-gray-300">
            Task {activeTaskIndex + 1} of {result.raw_results.length} | Extrapolation Distance: +{task.extrapolation_distance}
          </div>
        </div>
        
        <div className="p-8">
          <div className="mb-8 p-6 bg-slate-50 border rounded-lg font-mono text-sm whitespace-pre-wrap leading-relaxed">
            {task.input_representation}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
            <div className="p-6 border-2 border-gray-200 rounded-xl bg-white relative">
              <div className="absolute -top-3 left-4 bg-white px-2 text-xs font-bold uppercase tracking-widest text-gray-500">Evaluator Prediction</div>
              <div className="text-2xl font-mono font-bold text-center py-6">{task.prediction}</div>
            </div>
            
            <div className={`p-6 border-2 rounded-xl bg-white relative transition-colors duration-500 ${showTruth ? (task.correct ? 'border-green-400 bg-green-50' : 'border-red-400 bg-red-50') : 'border-gray-200'}`}>
              <div className="absolute -top-3 left-4 bg-white px-2 text-xs font-bold uppercase tracking-widest text-gray-500 flex items-center gap-2">
                Ground Truth
              </div>
              
              {showTruth ? (
                <div className="text-center">
                  <div className="text-2xl font-mono font-bold py-6">{task.ground_truth}</div>
                  <div className={`mt-2 font-black text-lg ${task.correct ? 'text-green-600' : 'text-red-600'}`}>
                    {task.correct ? '✓ CORRECT' : '✕ INCORRECT'}
                  </div>
                </div>
              ) : (
                <div className="flex flex-col items-center justify-center py-4 h-full">
                  <p className="text-xs text-gray-400 mb-3 text-center px-4">Ground truth is generated independently from the evaluator via a Z3 exact solver.</p>
                  <button 
                    onClick={() => setShowTruth(true)} 
                    className="bg-black text-white px-6 py-2 rounded-full font-bold hover:bg-gray-800 transition-colors"
                  >
                    Reveal Ground Truth
                  </button>
                </div>
              )}
            </div>
          </div>
          
          <div className="flex justify-between items-center border-t pt-6">
            <button onClick={handlePrev} disabled={activeTaskIndex === 0} className="px-6 py-2 border-2 rounded-lg font-bold disabled:opacity-30 hover:bg-gray-50">Previous</button>
            <button onClick={handleNext} disabled={activeTaskIndex === maxIndex} className="px-6 py-2 bg-black text-white rounded-lg font-bold disabled:opacity-30 hover:bg-gray-800">Next Task</button>
          </div>
        </div>
      </div>
      
      <div className="mt-8 bg-blue-50 border border-blue-200 p-6 rounded-xl flex items-start gap-4">
        <div className="text-blue-500 mt-1">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
        </div>
        <div>
          <h4 className="font-bold text-blue-900 mb-1">Methodology: Ground Truth is Trustworthy</h4>
          <p className="text-sm text-blue-800">
            Ground truth is generated independently from the evaluator via an exact mathematical solver. The evaluator does not receive the hidden rule, ground truth, or generator internals. Zero data leakage is mathematically guaranteed.
          </p>
        </div>
      </div>
    </div>
  );
}
