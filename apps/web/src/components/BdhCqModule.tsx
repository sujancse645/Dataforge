export function BdhCqModule() {
  return (
    <div className="mt-24 border-t border-slate-800 pt-16 max-w-4xl mx-auto mb-16 relative">
      
      {/* Decorative background glow */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-3/4 h-32 bg-cyan-900/10 blur-[80px] pointer-events-none rounded-full"></div>

      <div className="text-center mb-12 relative">
        <h2 className="text-3xl font-extrabold mb-4 text-glow-cyan text-slate-100">The BDH-CQ Context</h2>
        <p className="text-slate-400 max-w-2xl mx-auto">
          Coverage Cliff explores the boundaries of in-context learning. We connect this concept to BDH-CQ, a research architecture designed to test demonstration-driven rule learning without a written chain-of-thought trace.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-12">
        <div className="glass-card p-8 border-l-4 border-l-blue-500 hover:border-l-blue-400 transition-colors">
          <h3 className="font-bold mb-4 flex items-center text-slate-200">
            <span className="inline-block bg-blue-900/50 text-blue-300 text-[10px] px-2 py-0.5 rounded uppercase mr-3 border border-blue-700/50 shadow-[0_0_10px_rgba(59,130,246,0.3)]">PUBLISHED</span>
            Core BDH-CQ Mechanism
          </h3>
          <p className="text-sm text-slate-400 mb-6 leading-relaxed">
            BDH-CQ (Böhm-Defined Hypothesis - Coverage Query) relies on updating a latent state across sequential demonstration pairs, forming an implicit hypothesis before making a final prediction.
          </p>
          <div className="bg-slate-950 p-4 rounded-lg text-xs font-mono text-cyan-300 border border-slate-700 shadow-inner">
            <div className="text-slate-600 mb-2"># Educational abstraction of recurrent latent-state updating</div>
            <div className="text-slate-600 mb-3"># This is a simplified pedagogical abstraction, not the official BDH-CQ equation.</div>
            <span className="text-purple-400">h_(t+1)</span> = f(<span className="text-cyan-400">h_t</span>, <span className="text-green-400">x</span>)
          </div>
        </div>

        <div className="glass-card p-8 border-l-4 border-l-slate-600 hover:border-l-slate-400 transition-colors">
          <h3 className="font-bold mb-4 flex items-center text-slate-200">
            <span className="inline-block bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded uppercase mr-3 border border-slate-600">ILLUSTRATIVE</span>
            The Cliff Connection
          </h3>
          <p className="text-sm text-slate-400 leading-relaxed mb-6">
            If a model perfectly captures the hypothesis in its latent state, it should theoretically generalize infinitely. A Coverage Cliff implies the latent state only captured a localized approximation of the rule bounded by <strong className="text-purple-400 text-glow">Cmax</strong>.
          </p>
          <div className="h-24 bg-gradient-to-r from-slate-900 via-purple-900/20 to-slate-900 rounded-lg border border-slate-700 flex flex-col items-center justify-center text-xs text-slate-500 shadow-inner">
            <div className="flex gap-2 items-end h-8 mb-2">
              <div className="w-2 h-2 bg-cyan-500 rounded-full animate-pulse"></div>
              <div className="w-2 h-4 bg-cyan-500 rounded-full animate-pulse delay-75"></div>
              <div className="w-2 h-6 bg-cyan-500 rounded-full animate-pulse delay-150"></div>
              <div className="w-2 h-8 bg-cyan-500 rounded-full animate-pulse delay-300"></div>
              <div className="w-2 h-2 bg-red-500 rounded-full"></div>
            </div>
            [ Latent State Approximation ]
          </div>
        </div>
      </div>
      
      <div className="bg-slate-900/80 p-6 rounded-xl border border-slate-700 glass">
        <h4 className="font-bold text-sm uppercase tracking-widest text-slate-400 mb-4 border-b border-slate-800 pb-2">Scientific Limitations</h4>
        <ul className="text-sm text-slate-400 space-y-3 list-disc list-inside">
          <li>We <strong className="text-slate-200">did not</strong> run the official BDH-CQ model in this experiment.</li>
          <li>We <strong className="text-slate-200">did not</strong> establish whether BDH-CQ itself suffers from a Coverage Cliff.</li>
          <li>The deterministic evaluator used here is a structural sandbox to prove the boundary can be measured, not a claim about live LLM performance.</li>
        </ul>
      </div>
    </div>
  );
}
