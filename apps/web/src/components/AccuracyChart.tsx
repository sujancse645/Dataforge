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
