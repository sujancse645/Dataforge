import os

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

files = {
    "apps/web/src/components/EvidenceBadge.tsx": """
import React from 'react';

type EvidenceLevel = 'PUBLISHED' | 'LIVE' | 'PRECOMPUTED' | 'TOY' | 'ILLUSTRATIVE' | 'INTERPRETATION';

export function EvidenceBadge({ level, source }: { level: EvidenceLevel, source?: string }) {
  const colors = {
    PUBLISHED: 'bg-blue-100 text-blue-800 border-blue-200',
    LIVE: 'bg-green-100 text-green-800 border-green-200',
    PRECOMPUTED: 'bg-purple-100 text-purple-800 border-purple-200',
    TOY: 'bg-orange-100 text-orange-800 border-orange-200',
    ILLUSTRATIVE: 'bg-gray-100 text-gray-800 border-gray-200',
    INTERPRETATION: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  };

  return (
    <div className="inline-flex items-center gap-2 mb-2">
      <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase tracking-wider border ${colors[level]}`}>
        {level}
      </span>
      {source && <span className="text-xs text-gray-500 italic">Source: {source}</span>}
    </div>
  );
}
""",
    "apps/web/src/components/BdhCqModule.tsx": """
'use client';
import { useState } from 'react';
import { EvidenceBadge } from './EvidenceBadge';

export function BdhCqModule() {
  const [updates, setUpdates] = useState(2);

  return (
    <div className="w-full max-w-4xl mx-auto my-16 pt-16 border-t-2 border-dashed border-gray-300">
      <div className="text-center mb-12">
        <h2 className="text-3xl font-extrabold mb-4">From Demonstrations to Latent Reasoning</h2>
        <p className="text-xl text-gray-600 max-w-2xl mx-auto">
          Our experiment showed WHAT happens when we push beyond demonstrated coverage. Now we ask a different question: How can an architecture learn from demonstrations and perform reasoning without writing out a chain of thought?
        </p>
      </div>

      <div className="bg-slate-50 p-6 rounded-xl border mb-8">
        <h3 className="font-bold uppercase text-xs tracking-widest text-gray-500 mb-2">BDH-CQ Learning Objective</h3>
        <p className="font-medium text-gray-800">
          After using this module, the learner can explain how BDH-CQ's recurrent latent state updates allow demonstration-driven reasoning without a written chain-of-thought trace, and clearly distinguish this internal mechanism from the deterministic demonstration-coverage experiment used in Coverage Cliff.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div>
          <h3 className="text-xl font-bold mb-4">What is BDH-CQ?</h3>
          <EvidenceBadge level="PUBLISHED" source="BDH-CQ Technical Report" />
          <p className="text-gray-700 mb-4 text-sm leading-relaxed">
            <strong>BDH</strong> is a brain-inspired post-transformer architecture family. <strong>BDH-CQ</strong> is a later system in that family designed to learn from demonstrations and perform reasoning over a latent state, all without producing a written chain-of-thought trace.
          </p>
          <p className="text-gray-700 text-sm leading-relaxed">
            Instead of generating intermediate textual reasoning steps (e.g., Output: "Since A > B and B > C, therefore A > C"), the architecture maintains an internal hidden state that undergoes iterative computation before emitting the final answer.
          </p>
        </div>
        
        <div className="border p-6 rounded-xl bg-white shadow-sm flex flex-col justify-center">
          <EvidenceBadge level="ILLUSTRATIVE" source="Conceptual architecture — simplified from published description" />
          <div className="mt-4 flex flex-col items-center text-sm font-mono space-y-2">
            <div className="px-4 py-2 border rounded bg-gray-50 text-center w-full">INPUT (Demonstrations + Query)</div>
            <div className="text-gray-400">↓</div>
            <div className="px-4 py-4 border-2 border-black rounded-lg bg-indigo-50 text-center w-full relative">
              <span className="font-bold text-indigo-900">INTERNAL STATE (h_t)</span>
              <div className="mt-2 text-xs italic text-indigo-700">↻ Recurrent Updates ↻</div>
            </div>
            <div className="text-gray-400">↓</div>
            <div className="px-4 py-2 border rounded bg-gray-50 text-center w-full">OUTPUT (Final Answer)</div>
          </div>
        </div>
      </div>

      <div className="bg-white border rounded-xl p-8 mb-12 shadow-sm">
        <h3 className="text-xl font-bold mb-4">The Latent Update Equation</h3>
        <EvidenceBadge level="PUBLISHED" source="From Attention to Synapses: Deriving BDH" />
        <div className="my-6 text-center">
          <code className="text-2xl font-mono font-bold text-indigo-600 bg-indigo-50 px-4 py-2 rounded">
            h_(t+1) = f(h_t, x)
          </code>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm text-gray-700 mt-6">
          <div className="border-t-2 border-gray-200 pt-2">
            <strong>x (Input)</strong><br/>The encoded representation of the task and demonstrations.
          </div>
          <div className="border-t-2 border-gray-200 pt-2">
            <strong>f(h_t, x) (Update)</strong><br/>The internal reasoning transformation applied to the current hidden state.
          </div>
          <div className="border-t-2 border-gray-200 pt-2">
            <strong>h_(t+1) (Output)</strong><br/>The newly evolved latent state, ready for another step or final emission.
          </div>
        </div>
      </div>

      <div className="border-2 border-orange-200 bg-orange-50 rounded-xl p-8 mb-12">
        <div className="flex justify-between items-start mb-4">
          <h3 className="text-xl font-bold text-orange-900">Interactive Latent Mechanism</h3>
          <EvidenceBadge level="TOY" source="Our educational reimplementation - not official BDH-CQ" />
        </div>
        <p className="text-sm text-orange-800 mb-6">
          Change the number of recurrent internal updates to observe how a latent state evolves step-by-step before producing an answer.
        </p>
        
        <div className="mb-6">
          <label className="block text-sm font-bold text-orange-900 mb-2">Recurrent Updates: {updates}</label>
          <input 
            type="range" 
            min="1" max="5" 
            value={updates} 
            onChange={(e) => setUpdates(parseInt(e.target.value))}
            className="w-full accent-orange-600"
          />
        </div>
        
        <div className="flex gap-2 items-center overflow-x-auto pb-4">
          <div className="p-3 border border-orange-300 bg-white rounded text-center shrink-0 min-w-[80px]">
            <div className="text-xs text-gray-500">Input</div>
            <div className="font-mono font-bold mt-1">x</div>
          </div>
          
          {Array.from({length: updates}).map((_, i) => (
            <React.Fragment key={i}>
              <div className="text-orange-400 font-bold">→</div>
              <div className="p-3 border-2 border-orange-400 bg-orange-100 rounded text-center shrink-0 min-w-[80px]">
                <div className="text-xs text-orange-800">Step {i+1}</div>
                <div className="font-mono font-bold mt-1 text-orange-900">h_{i+1}</div>
              </div>
            </React.Fragment>
          ))}
          
          <div className="text-orange-400 font-bold">→</div>
          <div className="p-3 border border-orange-300 bg-white rounded text-center shrink-0 min-w-[80px]">
            <div className="text-xs text-gray-500">Answer</div>
            <div className="font-mono font-bold mt-1 text-green-600">TRUE</div>
          </div>
        </div>
      </div>

      <div className="mb-12">
        <h3 className="text-xl font-bold mb-4 bg-yellow-100 inline-block px-2 py-1 rounded">Common Misconception</h3>
        <p className="text-gray-800 font-medium italic">"Latent reasoning means unlimited generalization and automatically solves the Coverage Cliff."</p>
        <p className="mt-2 text-gray-700">
          <strong>Not necessarily.</strong> A reasoning architecture changes HOW computation is performed (internally vs written). It does not automatically guarantee success on every extrapolation regime. Mechanism ≠ Guaranteed Generalization.
        </p>
      </div>

      <div className="bg-white border rounded-xl overflow-hidden mb-12">
        <div className="bg-gray-100 px-6 py-4 border-b">
          <h3 className="font-bold text-gray-800">Related Questions — Different Experiments</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-gray-50 border-b text-gray-500 uppercase">
              <tr>
                <th className="px-6 py-3">Dimension</th>
                <th className="px-6 py-3">Coverage Cliff</th>
                <th className="px-6 py-3">BDH-CQ</th>
              </tr>
            </thead>
            <tbody className="divide-y text-gray-700">
              <tr>
                <td className="px-6 py-4 font-bold">Question</td>
                <td className="px-6 py-4">What happens when test complexity exceeds demos?</td>
                <td className="px-6 py-4">How does a system reason from demos without CoT?</td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-bold">Substrate</td>
                <td className="px-6 py-4">Our deterministic experiment</td>
                <td className="px-6 py-4">Published BDH-CQ system</td>
              </tr>
              <tr>
                <td className="px-6 py-4 font-bold">Evaluation</td>
                <td className="px-6 py-4">Live execution</td>
                <td className="px-6 py-4">Published evidence (Precomputed)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-slate-900 text-slate-300 p-8 rounded-xl text-sm">
        <h3 className="text-white font-bold text-lg mb-4 uppercase tracking-widest">Limitations & Disclosures</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <strong className="text-white">Demonstrated Here</strong>
            <p className="mt-1 mb-4">A deterministic extrapolation experiment and an integrated educational overview of published BDH-CQ evidence.</p>
            
            <strong className="text-white">Established by Source</strong>
            <p className="mt-1">BDH-CQ effectively learns to reason from demonstrations using latent state updates instead of written traces.</p>
          </div>
          <div>
            <strong className="text-white">What We Did Not Do</strong>
            <p className="mt-1 mb-4">We did not run an official BDH-CQ checkpoint. We did not reproduce the authors' training pipeline. Our toy is strictly a conceptual abstraction.</p>
            
            <strong className="text-white">Open Question</strong>
            <p className="mt-1">We have NOT established that BDH-CQ has, or does not have, a Coverage Cliff under these exact experimental conditions.</p>
          </div>
        </div>
      </div>

    </div>
  );
}
"""
}

for path, content in files.items():
    write_file(path, content)

print("BDH Frontend Scaffold Generated Successfully.")
