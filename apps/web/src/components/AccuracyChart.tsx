'use client';

type ChartLevelMetric = number | { accuracy: number };

export function AccuracyChart({ levelMetrics, cliffLocation }: { levelMetrics: Record<string, ChartLevelMetric>, cliffLocation: number | null }) {
  // Handle both possible backend formats: if it's an object with extrapolation_distance or just a number
  const data = Object.entries(levelMetrics).map(([key, value]) => {
    const extDist = parseInt(key);
    const accuracy = typeof value === 'number' ? value : value.accuracy;
    return { extrapolation_distance: extDist, accuracy };
  }).sort((a, b) => a.extrapolation_distance - b.extrapolation_distance);
  
  return (
    <div className="p-8 border border-slate-700 rounded-xl bg-slate-900/50 shadow-xl mt-8 glass">
      <h3 className="font-bold text-xl mb-2 text-slate-100 text-glow-cyan">Accuracy vs Extrapolation Distance</h3>
      <p className="text-sm text-slate-400 mb-8">This is actual experiment data returned by the backend.</p>
      
      <div className="relative flex items-end h-72 gap-4 border-b border-l border-slate-600 pb-2 pl-2">
        {/* Y Axis labels */}
        <div className="absolute -left-12 bottom-0 text-xs font-mono text-slate-500">0%</div>
        <div className="absolute -left-12 top-0 text-xs font-mono text-slate-500">100%</div>
        
        {data.map((point) => {
          const isAtOrPastCliff = cliffLocation !== null && point.extrapolation_distance >= cliffLocation;
          
          return (
            <div key={point.extrapolation_distance} className="relative flex-1 flex flex-col justify-end items-center group h-full">
              <div 
                className={`w-full max-w-[60px] rounded-t transition-all duration-1000 ease-out flex items-center justify-center shadow-lg
                  ${isAtOrPastCliff ? 'bg-red-500/80 shadow-[0_0_15px_rgba(239,68,68,0.6)]' : 'bg-cyan-500/80 shadow-[0_0_15px_rgba(34,211,238,0.6)]'}
                  hover:brightness-125 hover:scale-105 transform origin-bottom
                `}
                style={{ height: `${Math.max(point.accuracy * 100, 1)}%` }} /* Min height for visibility */
              >
                {point.accuracy > 0.1 && (
                  <span className="text-slate-950 text-xs font-bold drop-shadow-sm">{Math.round(point.accuracy * 100)}%</span>
                )}
              </div>
              
              <div className="absolute -bottom-8 text-sm font-mono font-bold text-slate-300 group-hover:text-cyan-300 transition-colors">
                +{point.extrapolation_distance}
              </div>
              
              {point.accuracy <= 0.1 && (
                <div className="absolute bottom-2 text-red-200 text-xs font-bold">{Math.round(point.accuracy * 100)}%</div>
              )}
            </div>
          );
        })}
      </div>
      
      <div className="mt-12 text-center">
        <span className="inline-block px-4 py-2 bg-slate-800 text-slate-300 border border-slate-600 font-bold text-xs uppercase tracking-widest rounded-full shadow-inner">
          Extrapolation Distance (Dext)
        </span>
      </div>
    </div>
  );
}
