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
