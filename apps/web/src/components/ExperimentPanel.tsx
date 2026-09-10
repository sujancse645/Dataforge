'use client';
import { useEffect, useRef, useState } from 'react';
import { runExperimentStream } from '../lib/api';
import { ExperimentResult, ExperimentConfig, ExperimentStreamEvent } from '../lib/types';
import { ResultView } from './ResultView';
import { AccuracyChart } from './AccuracyChart';

interface LogEntry {
  id: number;
  text: string;
  tone: 'info' | 'correct' | 'incorrect';
}

const toneClass: Record<LogEntry['tone'], string> = {
  info: 'text-slate-400',
  correct: 'text-green-400',
  incorrect: 'text-red-400',
};

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
  const [phase, setPhase] = useState('');
  const [progress, setProgress] = useState({ completed: 0, total: 0 });
  const [log, setLog] = useState<LogEntry[]>([]);
  const [liveMetrics, setLiveMetrics] = useState<Record<number, { correct: number; total: number }>>({});

  const logIdRef = useRef(0);
  const logEndRef = useRef<HTMLDivElement | null>(null);
  const abortRef = useRef<AbortController | null>(null);
  // Guards against a stale/aborted run's events landing after a newer run
  // has already started — see note in handleRun below.
  const runTokenRef = useRef(0);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ block: 'nearest' });
  }, [log]);

  useEffect(() => () => abortRef.current?.abort(), []);

  const pushLog = (text: string, tone: LogEntry['tone'] = 'info') => {
    logIdRef.current += 1;
    setLog(prev => [...prev.slice(-49), { id: logIdRef.current, text, tone }]);
  };

  const sleep = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));

  const handleRun = async () => {
    if (loading) return;

    abortRef.current?.abort();
    const controller = new AbortController();
    abortRef.current = controller;
    // On a fast local backend the whole stream can arrive in one network
    // chunk, so a superseded run's events could otherwise still resolve
    // after a fresh run's and silently overwrite it. Every state update
    // below is gated on this token still being the active one.
    const myRun = ++runTokenRef.current;
    const isCurrent = () => runTokenRef.current === myRun;

    setLoading(true);
    setError(null);
    setResult(null);
    setLog([]);
    setProgress({ completed: 0, total: 0 });
    setLiveMetrics({});
    setPhase('CONNECTING TO ENGINE...');

    try {
      await runExperimentStream(config, async (event: ExperimentStreamEvent) => {
        if (!isCurrent()) return;

        switch (event.type) {
          case 'demo_generated':
            setPhase(`GENERATING DEMONSTRATIONS (${event.index}/${event.total})`);
            pushLog(`Generated demonstration ${event.index}/${event.total}`);
            await sleep(120);
            break;

          case 'coverage_computed':
            setPhase('DISPATCHING EXTRAPOLATION TASKS...');
            pushLog(`Demonstration coverage established — Cmax = ${event.coverage}`);
            await sleep(180);
            break;

          case 'task_evaluated': {
            setProgress({ completed: event.completed, total: event.total });
            setPhase(`EVALUATING · LEVEL +${event.level} · TASK ${event.task_index}/${event.tasks_per_level}`);
            const ok = event.result.correct;
            pushLog(
              `[+${event.level}] task ${event.task_index}/${event.tasks_per_level} -> ${ok ? 'CORRECT' : 'INCORRECT'}`,
              ok ? 'correct' : 'incorrect'
            );
            setLiveMetrics(prev => {
              const cur = prev[event.level] ?? { correct: 0, total: 0 };
              return {
                ...prev,
                [event.level]: { correct: cur.correct + (ok ? 1 : 0), total: cur.total + 1 },
              };
            });
            // Pace rendering so the live feed stays visible regardless of
            // task count, without slowing the actual engine computation.
            await sleep(Math.max(12, Math.min(70, 1800 / event.total)));
            break;
          }

          case 'level_complete':
            pushLog(`Level +${event.level} complete — accuracy ${Math.round(event.metrics.accuracy * 100)}%`);
            await sleep(180);
            break;

          case 'done':
            setPhase('CLIFF DETECTION COMPLETE');
            pushLog(
              event.result.cliff_detected ? 'Coverage cliff detected.' : 'No coverage cliff detected.',
              event.result.cliff_detected ? 'incorrect' : 'correct'
            );
            setResult(event.result);
            break;

          case 'error':
            throw new Error(event.message);
        }
      }, controller.signal);
    } catch (err: unknown) {
      if (err instanceof DOMException && err.name === 'AbortError') return;
      if (!isCurrent()) return;
      const message = err instanceof Error ? err.message : 'Experiment service unavailable. Please start the backend and try again.';
      setError(message);
      pushLog(message, 'incorrect');
    } finally {
      if (isCurrent()) setLoading(false);
    }
  };

  const liveChartData = Object.fromEntries(
    Object.entries(liveMetrics).map(([lvl, m]) => [lvl, { accuracy: m.total ? m.correct / m.total : 0, total: m.total }])
  );
  const progressPct = progress.total ? Math.round((progress.completed / progress.total) * 100) : 0;

  return (
    <div className="w-full max-w-4xl mx-auto my-8 relative">

      <div className="glass-card p-8 mb-8 border-t-4 border-t-cyan-500 relative overflow-hidden">
        {loading && (
          <div className="absolute inset-0 bg-slate-900/90 backdrop-blur-md z-20 flex flex-col items-center justify-center rounded-xl border border-purple-500/50 px-8">
            <div className="animate-spin rounded-full h-10 w-10 border-t-2 border-b-2 border-cyan-400 mb-4 shadow-[0_0_15px_rgba(34,211,238,0.5)]"></div>
            <div className="font-mono text-xs sm:text-sm font-bold tracking-widest text-glow-cyan text-cyan-300 text-center">{phase}</div>
            {progress.total > 0 && (
              <div className="w-full max-w-xs mt-4">
                <div className="h-1.5 w-full bg-slate-800 rounded-full overflow-hidden border border-slate-700">
                  <div
                    className="h-full bg-gradient-to-r from-purple-500 to-cyan-400 transition-all duration-300 ease-out"
                    style={{ width: `${progressPct}%` }}
                  ></div>
                </div>
                <div className="text-center text-[10px] font-mono text-slate-500 mt-1">
                  {progress.completed}/{progress.total} tasks · {progressPct}%
                </div>
              </div>
            )}
          </div>
        )}

        <h3 className="font-bold text-slate-100 mb-6 uppercase tracking-widest border-b border-slate-700 pb-2 flex items-center gap-3">
          <span className="inline-block w-2 h-2 rounded-full bg-cyan-400 animate-pulse"></span>
          Experiment Configuration
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-8">
          <div className="group">
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2 tracking-wider group-hover:text-cyan-300 transition-colors">
              Random Seed
            </label>
            <input
              type="number"
              value={config.master_seed}
              onChange={e => setConfig({...config, master_seed: parseInt(e.target.value) || 0})}
              className="w-full p-4 border border-slate-700 rounded bg-slate-900/80 text-slate-100 font-mono focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 outline-none transition-all shadow-inner hover:border-slate-500"
            />
            <p className="text-xs text-slate-500 mt-2">Drives generator determinism</p>
          </div>
          <div className="group">
            <label className="block text-xs font-bold text-slate-400 uppercase mb-2 tracking-wider group-hover:text-purple-300 transition-colors">
              Demonstration Coverage (Cmax)
            </label>
            <input
              type="number"
              value={config.demonstration_complexity}
              onChange={e => setConfig({...config, demonstration_complexity: parseInt(e.target.value) || 0})}
              className="w-full p-4 border border-slate-700 rounded bg-slate-900/80 text-slate-100 font-mono focus:border-purple-500 focus:ring-1 focus:ring-purple-500 outline-none transition-all shadow-inner hover:border-slate-500"
              min="1"
              max="5"
            />
            <p className="text-xs text-slate-500 mt-2">Tested in-coverage baseline</p>
          </div>
        </div>

        <div className="flex flex-col md:flex-row gap-4">
          <button
            onClick={handleRun}
            disabled={loading}
            className="flex-1 bg-gradient-to-r from-purple-600 to-cyan-600 text-white rounded-lg py-4 font-extrabold text-lg tracking-widest hover:from-purple-500 hover:to-cyan-500 disabled:opacity-50 transition-all shadow-[0_0_20px_rgba(168,85,247,0.3)] neon-border hover:shadow-[0_0_30px_rgba(34,211,238,0.5)] transform hover:-translate-y-1"
          >
            {loading ? 'ENGINE RUNNING...' : 'RUN THE EXPERIMENT'}
          </button>

          {result && (
            <button
              onClick={() => {
                setConfig({...config, master_seed: config.master_seed + 1});
                setResult(null);
              }}
              className="md:w-1/3 bg-slate-800 text-slate-100 border border-slate-600 rounded-lg py-4 font-bold text-sm uppercase tracking-wider hover:bg-slate-700 transition-all shadow-md hover:border-slate-400"
            >
              Challenge the Claim
            </button>
          )}
        </div>

        {result && !error && (
          <div className="mt-4 text-center text-xs text-slate-500 italic">
            Same seed + config always reproduces the same result — that&apos;s intentional determinism, not a bug.
            Does the cliff move if we change the experiment? Click &apos;Challenge the Claim&apos;.
          </div>
        )}

        {error && (
          <div className="mt-6 p-4 bg-red-900/30 text-red-300 rounded border border-red-700 font-medium">
            {error}
          </div>
        )}
      </div>

      {loading && (
        <div className="glass-card p-6 mb-8 border-t-4 border-t-purple-500 animate-in fade-in duration-300">
          <h3 className="font-bold text-slate-100 mb-4 uppercase tracking-widest border-b border-slate-700 pb-2 flex items-center gap-3">
            <span className="inline-block w-2 h-2 rounded-full bg-purple-400 animate-pulse"></span>
            Real-Time Engine Feed
          </h3>

          {Object.keys(liveChartData).length > 0 && (
            <div className="mb-6">
              <AccuracyChart levelMetrics={liveChartData} cliffLocation={null} />
            </div>
          )}

          <div className="bg-slate-950/70 border border-slate-800 rounded-lg p-4 h-48 overflow-y-auto font-mono text-xs space-y-1 shadow-inner">
            {log.length === 0 && <div className="text-slate-600">Waiting for engine output...</div>}
            {log.map(entry => (
              <div key={entry.id} className={toneClass[entry.tone]}>
                <span className="text-slate-600">$</span> {entry.text}
              </div>
            ))}
            <div ref={logEndRef} />
          </div>
        </div>
      )}

      {result && <ResultView result={result} seed={config.master_seed} />}
    </div>
  );
}
