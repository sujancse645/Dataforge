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
