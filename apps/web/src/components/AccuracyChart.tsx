'use client';
import { LevelMetric } from '../lib/types';

export function AccuracyChart({ levelMetrics, cliffLocation }: { levelMetrics: Record<string, LevelMetric>, cliffLocation: number | null }) {
  const data = Object.values(levelMetrics).sort((a, b) => a.extrapolation_distance - b.extrapolation_distance);
  
  return (
    <div className="p-8 border rounded-xl bg-white shadow-sm mt-8">
      <h3 className="font-bold text-xl mb-2">Accuracy vs Extrapolation Distance</h3>
      <p className="text-sm text-gray-500 mb-8">This is actual experiment data returned by the backend.</p>
      
      <div className="relative flex items-end h-72 gap-4 border-b-2 border-l-2 border-gray-300 pb-2 pl-2">
        {/* Y Axis labels */}
        <div className="absolute -left-12 bottom-0 text-xs font-mono text-gray-400">0%</div>
        <div className="absolute -left-12 top-0 text-xs font-mono text-gray-400">100%</div>
        
        {data.map((point) => {
          const isAtOrPastCliff = cliffLocation !== null && point.extrapolation_distance >= cliffLocation;
          
          return (
            <div key={point.extrapolation_distance} className="relative flex-1 flex flex-col justify-end items-center group h-full">
              <div 
                className={`w-full max-w-[60px] rounded-t transition-all duration-700 ease-out flex items-center justify-center
                  ${isAtOrPastCliff ? 'bg-red-500' : 'bg-black'}
                  hover:opacity-80
                `}
                style={{ height: `${Math.max(point.accuracy * 100, 2)}%` }} /* Min height for visibility if 0 */
              >
                {point.accuracy > 0.1 && (
                  <span className="text-white text-xs font-bold">{Math.round(point.accuracy * 100)}%</span>
                )}
              </div>
              
              <div className="absolute -bottom-8 text-sm font-mono font-bold text-gray-600">
                +{point.extrapolation_distance}
              </div>
              
              {point.accuracy <= 0.1 && (
                <div className="absolute bottom-2 text-red-100 text-xs font-bold">{Math.round(point.accuracy * 100)}%</div>
              )}
            </div>
          );
        })}
      </div>
      
      <div className="mt-12 text-center">
        <span className="inline-block px-4 py-2 bg-gray-100 text-gray-700 font-bold text-xs uppercase tracking-widest rounded">
          Extrapolation Distance (Dext)
        </span>
      </div>
    </div>
  );
}
