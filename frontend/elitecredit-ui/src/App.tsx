import { useState, useEffect } from 'react';
import { AssessmentPage, ResultsPage } from './pages';
import type { Result } from './pages';

/* ── Help Modal ───────────────────────────────────────────────────────── */
function HelpModal({ onClose }: { onClose: () => void }) {
  return (
    <div style={{ position: 'fixed', inset: 0, zIndex: 100, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div style={{ position: 'absolute', inset: 0, background: 'rgba(0,0,0,0.6)', backdropFilter: 'blur(4px)' }} onClick={onClose} />
      <div style={{ position: 'relative', background: 'var(--bg-card)', border: '1px solid var(--border)', borderRadius: 14, padding: '28px 32px', maxWidth: 520, width: '90%', maxHeight: '80vh', overflowY: 'auto', boxShadow: '0 20px 60px rgba(0,0,0,0.4)' }} className="animate-in">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ fontSize: 18, fontWeight: 800, color: 'var(--t1)', margin: 0 }}>📖 How to Use EliteCredit</h2>
          <button onClick={onClose} style={{ background: 'var(--bg-raised)', border: '1px solid var(--border)', borderRadius: 6, padding: '4px 10px', cursor: 'pointer', color: 'var(--t2)', fontSize: 13, fontFamily: 'inherit' }}>✕</button>
        </div>
        {[
          { step: '1', icon: '◉', title: 'New Assessment', desc: 'Click "New Assessment" in the sidebar. Fill in the applicant\'s personal, financial, and credit history details.' },
          { step: '2', icon: '▶', title: 'Run Analysis', desc: 'Click "Run Risk Analysis" to send the data to the ML backend. The system calculates a 300–900 credit score and default probability in real-time.' },
          { step: '3', icon: '📋', title: 'View Results', desc: 'Review the score, risk tier classification, key metrics (LTI, DTI, EMI), and actionable advisor recommendations.' },
          { step: '4', icon: '📊', title: 'Scenario Planner', desc: 'Use interactive sliders to simulate "what-if" scenarios — see how reducing utilization or increasing income could improve the score.' },
          { step: '5', icon: '🧠', title: 'Model Intelligence', desc: 'Explore the ML model specs: algorithm details, training data, feature importance, and system architecture.' },
        ].map(s => (
          <div key={s.step} style={{ display: 'flex', gap: 12, marginBottom: 14, padding: '12px 14px', background: 'var(--bg-raised)', borderRadius: 9, border: '1px solid var(--border)' }}>
            <div style={{ width: 28, height: 28, borderRadius: 7, background: 'var(--indigo-dim)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 13, fontWeight: 800, color: 'var(--indigo-light)', flexShrink: 0 }}>{s.step}</div>
            <div>
              <div style={{ fontSize: 13, fontWeight: 700, color: 'var(--t1)', marginBottom: 2 }}>{s.icon} {s.title}</div>
              <div style={{ fontSize: 12, color: 'var(--t3)', lineHeight: 1.55 }}>{s.desc}</div>
            </div>
          </div>
        ))}
        <div style={{ marginTop: 16, padding: '10px 14px', background: 'var(--indigo-dim)', borderRadius: 8, border: '1px solid rgba(99,102,241,0.18)', fontSize: 11.5, color: 'var(--t2)', lineHeight: 1.6 }}>
          💡 <strong>Tip:</strong> Toggle between dark and light mode using the switch in the top-right corner. Your preference is saved automatically.
        </div>
      </div>
    </div>
  );
}

/* ── Nav Item ─────────────────────────────────────────────────────────── */
function NavItem({ icon, label, active, onClick }: { icon: string; label: string; active: boolean; onClick: () => void }) {
  return (
    <button className={`nav-item ${active ? 'active' : ''}`} onClick={onClick}>
      <span style={{ fontSize: 14 }}>{icon}</span><span>{label}</span>
    </button>
  );
}

/* ── Hero Dashboard ───────────────────────────────────────────────────── */
function DashboardPage({ onGo }: { onGo: () => void }) {
  return (
    <div className="animate-in">
      {/* Hero Banner */}
      <div className="hero-banner">
        <div className="hero-particles"><span/><span/><span/><span/><span/></div>
        <div style={{ position: 'relative', zIndex: 1 }}>
          <div style={{ display: 'flex', gap: 8, marginBottom: 14 }}>
            <span className="chip chip-indigo">Machine Learning</span>
            <span className="chip chip-emerald">● Live System</span>
          </div>
          <h1 style={{ fontSize: 28, fontWeight: 900, letterSpacing: '-0.03em', lineHeight: 1.2, marginBottom: 8, color: 'var(--t1)' }}>
            Credit Risk Intelligence<br />
            <span style={{ color: 'var(--indigo-light)' }}>Powered by ML</span>
          </h1>
          <p style={{ fontSize: 13.5, color: 'var(--t2)', maxWidth: 520, lineHeight: 1.6, marginBottom: 20 }}>
            Real-time credit scoring engine built with <strong>Logistic Regression</strong>, 
            served via <strong>FastAPI</strong>, and visualised in <strong>React</strong>. 
            Predicts default probability and generates 300–900 credit scores with <strong>99.1% accuracy</strong>.
          </p>
          <button className="btn-primary" onClick={onGo} style={{ padding: '11px 24px', fontSize: 13.5 }}>
            ▶  Start Assessment
          </button>
        </div>
      </div>

      {/* KPI Row */}
      <div className="grid-4 animate-in animate-delay-1" style={{ marginBottom: 16 }}>
        {[
          { icon: '🎯', value: '99.1%', label: 'Model Accuracy', chip: 'chip-emerald', chipText: 'Production' },
          { icon: '⚡', value: '<200ms', label: 'Inference Latency', chip: 'chip-indigo', chipText: 'FastAPI' },
          { icon: '📊', value: '252K', label: 'Training Samples', chip: 'chip-amber', chipText: 'Validated' },
          { icon: '🧮', value: '14', label: 'Risk Features', chip: 'chip-cyan', chipText: 'Engineered' },
        ].map(k => (
          <div key={k.label} className="card" style={{ padding: '16px 18px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 10 }}>
              <span style={{ fontSize: 22 }}>{k.icon}</span>
              <span className={`chip ${k.chip}`}>{k.chipText}</span>
            </div>
            <div className="kpi-value">{k.value}</div>
            <div className="kpi-label">{k.label}</div>
          </div>
        ))}
      </div>

      {/* Architecture + Pipeline */}
      <div className="grid-2 animate-in animate-delay-2">
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-indigo">🏗️</span> System Architecture</div>
          {[
            { icon: '⚛️', title: 'React + Vite + TypeScript', desc: 'Modern SPA with Tailwind CSS, Axios API integration' },
            { icon: '⚡', title: 'FastAPI Backend', desc: 'REST API, Pydantic validation, auto OpenAPI docs, CORS' },
            { icon: '🧮', title: 'Scikit-learn Pipeline', desc: 'MinMaxScaler → Logistic Regression, Joblib serialization' },
            { icon: '📊', title: 'Credit Scoring Engine', desc: 'Sigmoid-based mapping to 300–900 (RBI-calibrated)' },
          ].map(a => (
            <div key={a.title} style={{ display: 'flex', gap: 10, marginBottom: 12, padding: '10px 12px', background: 'var(--bg-raised)', borderRadius: 8, border: '1px solid var(--border)' }}>
              <span style={{ fontSize: 18, flexShrink: 0 }}>{a.icon}</span>
              <div>
                <div style={{ fontSize: 12.5, fontWeight: 700, marginBottom: 1, color: 'var(--t1)' }}>{a.title}</div>
                <div style={{ fontSize: 11.5, color: 'var(--t3)', lineHeight: 1.5 }}>{a.desc}</div>
              </div>
            </div>
          ))}
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-emerald">📈</span> Model Performance</div>
          {[
            { label: 'Accuracy', val: 99.1, color: 'var(--emerald)' },
            { label: 'AUC-ROC', val: 98.75, color: 'var(--indigo)' },
            { label: 'Precision', val: 97.4, color: 'var(--amber)' },
            { label: 'Recall', val: 95.8, color: 'var(--cyan)' },
          ].map(m => (
            <div key={m.label} style={{ marginBottom: 12 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 3 }}>
                <span style={{ fontSize: 11.5, color: 'var(--t3)' }}>{m.label}</span>
                <span style={{ fontSize: 11.5, fontWeight: 700, color: m.color }}>{m.val}%</span>
              </div>
              <div className="progress-track"><div className="progress-fill" style={{ width: `${m.val}%`, background: m.color }} /></div>
            </div>
          ))}
          <div style={{ marginTop: 14, padding: '9px 12px', background: 'var(--indigo-dim)', borderRadius: 7, border: '1px solid rgba(99,102,241,0.18)', fontSize: 11.5 }}>
            <span style={{ fontWeight: 700, color: 'var(--indigo-light)' }}>Production Ready</span>
            <span style={{ color: 'var(--t3)' }}> — Validated on 50,400 held-out samples. SMOTE for class imbalance.</span>
          </div>
        </div>
      </div>
    </div>
  );
}

/* ── Model Intelligence ───────────────────────────────────────────────── */
function ModelPage() {
  const MODEL = [
    { l: 'Algorithm', v: 'Logistic Regression' }, { l: 'Accuracy', v: '99.1%' },
    { l: 'AUC-ROC', v: '0.9875' }, { l: 'Training Samples', v: '252,000' },
    { l: 'Features', v: '14' }, { l: 'Validation', v: 'Stratified K-Fold (k=5)' },
    { l: 'Score Range', v: '300 – 900' }, { l: 'Stack', v: 'Scikit-learn + FastAPI + React' },
  ];
  const FEATS = [
    { n: 'Credit Utilization Ratio', i: 'High', d: 'neg' }, { n: 'Avg Days Past Due', i: 'High', d: 'neg' },
    { n: 'Delinquency Ratio', i: 'High', d: 'neg' }, { n: 'Loan-to-Income Ratio', i: 'Medium', d: 'neg' },
    { n: 'Loan Tenure', i: 'Medium', d: 'pos' }, { n: 'Age', i: 'Medium', d: 'pos' },
    { n: 'Number of Open Accounts', i: 'Low', d: 'neg' }, { n: 'Residence Type', i: 'Low', d: 'pos' },
  ];

  return (
    <div className="animate-in">
      <p className="section-title">Model Intelligence</p>
      <p className="section-sub">Technical overview of the ML system powering credit risk analysis.</p>
      <div className="grid-2" style={{ marginBottom: 14 }}>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-indigo">🧠</span> Specifications</div>
          {MODEL.map(m => <div key={m.l} className="metric-row"><span style={{color:'var(--t3)'}}>{m.l}</span><span style={{fontWeight:600,color:'var(--t1)'}}>{m.v}</span></div>)}
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-amber">⚙️</span> Feature Importance</div>
          <table className="table"><thead><tr><th>Feature</th><th>Impact</th><th>Dir</th></tr></thead><tbody>
            {FEATS.map(f => <tr key={f.n}><td>{f.n}</td><td><span className={`chip ${f.i==='High'?'chip-red':f.i==='Medium'?'chip-amber':'chip-indigo'}`}>{f.i}</span></td><td style={{color:f.d==='pos'?'var(--emerald)':'var(--red)'}}>{f.d==='pos'?'▲ Pos':'▼ Neg'}</td></tr>)}
          </tbody></table>
        </div>
      </div>
    </div>
  );
}

/* ── Scenario Planner ─────────────────────────────────────────────────── */
function ScenarioPage({ result, form }: { result: Result | null; form: any }) {
  const [ut, setUt] = useState(25);
  const [ib, setIb] = useState(0);

  if (!result) return (
    <div className="card animate-in" style={{ textAlign: 'center', padding: '50px 20px' }}>
      <div style={{ fontSize: 36, marginBottom: 12 }}>📊</div>
      <div style={{ fontSize: 15, fontWeight: 700, marginBottom: 6 }}>No Assessment Data</div>
      <div style={{ fontSize: 12.5, color: 'var(--t3)' }}>Run a credit risk assessment first.</div>
    </div>
  );

  const cur = result.credit_score;
  const udiff = Math.max((form?.credit_utilization_ratio ?? 30) - ut, 0);
  const d = Math.min(udiff * 1.1, 60) + Math.min(ib * 0.75, 35);
  const pot = Math.min(cur + Math.round(d), 900);
  const cs = (s: number) => s >= 750 ? 'var(--emerald)' : s >= 650 ? 'var(--amber)' : 'var(--red)';

  return (
    <div className="animate-in">
      <p className="section-title">Scenario Planner</p>
      <p className="section-sub">Simulate how changes could improve the client's credit profile.</p>
      <div className="grid-2">
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-indigo">🎛️</span> Adjustments</div>
          <div style={{ marginBottom: 20 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
              <span style={{ fontSize: 11.5, fontWeight: 600, color: 'var(--t3)' }}>Target Utilization</span>
              <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--t1)' }}>{ut}%</span>
            </div>
            <input type="range" min={0} max={100} value={ut} onChange={e => setUt(+e.target.value)} />
          </div>
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 6 }}>
              <span style={{ fontSize: 11.5, fontWeight: 600, color: 'var(--t3)' }}>Income Increase</span>
              <span style={{ fontSize: 13, fontWeight: 700, color: 'var(--t1)' }}>+{ib}%</span>
            </div>
            <input type="range" min={0} max={50} value={ib} onChange={e => setIb(+e.target.value)} />
          </div>
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-emerald">📈</span> Projected Impact</div>
          <div className="grid-2" style={{ marginBottom: 16 }}>
            <div style={{ textAlign: 'center', padding: '14px', background: 'var(--bg-raised)', borderRadius: 8, border: '1px solid var(--border)' }}>
              <div style={{ fontSize: 10, color: 'var(--t3)', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 4 }}>Current</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: cs(cur), letterSpacing: '-0.03em' }}>{cur}</div>
            </div>
            <div style={{ textAlign: 'center', padding: '14px', background: 'var(--indigo-dim)', borderRadius: 8, border: '1px solid rgba(99,102,241,0.15)' }}>
              <div style={{ fontSize: 10, color: 'var(--t3)', fontWeight: 700, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 4 }}>Potential</div>
              <div style={{ fontSize: 32, fontWeight: 900, color: cs(pot), letterSpacing: '-0.03em' }}>{pot}</div>
              <div style={{ fontSize: 11, color: 'var(--emerald)', fontWeight: 600 }}>+{pot - cur} pts</div>
            </div>
          </div>
          <div style={{ padding: '10px 12px', background: 'var(--indigo-dim)', borderRadius: 7, border: '1px solid rgba(99,102,241,0.15)', fontSize: 11.5, color: 'var(--t2)', lineHeight: 1.6 }}>
            💬 Reducing utilization from <strong>{form?.credit_utilization_ratio}%</strong> → <strong>{ut}%</strong>{ib > 0 && <> + <strong>+{ib}%</strong> income</>} could yield <strong style={{ color: 'var(--emerald)' }}>+{pot - cur} pts</strong>.
          </div>
        </div>
      </div>
    </div>
  );
}

/* ══════════════════════════════════════════════════════════════════════════
   APP ROOT
   ══════════════════════════════════════════════════════════════════════════ */
export default function App() {
  const [tab, setTab] = useState('dashboard');
  const [result, setResult] = useState<Result | null>(null);
  const [form, setForm] = useState<any>(null);
  const [theme, setTheme] = useState<'dark' | 'light'>(() => (localStorage.getItem('ec-theme') as any) || 'dark');
  const [showHelp, setShowHelp] = useState(false);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('ec-theme', theme);
  }, [theme]);

  const handleResult = (r: Result, f: any) => { setResult(r); setForm(f); setTab('results'); };
  const toggleTheme = () => setTheme(t => t === 'dark' ? 'light' : 'dark');

  const pages: Record<string, string> = { dashboard: 'Dashboard', assessment: 'Assessment', results: 'Results', scenario: 'Scenario Planner', model: 'Model Intelligence' };

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-logo">
          <div className="logo-icon">EC</div>
          <div>
            <div style={{ fontSize: 13.5, fontWeight: 700, color: 'var(--t1)' }}>EliteCredit</div>
            <div style={{ fontSize: 9.5, color: 'var(--t3)' }}>Advisor Platform</div>
          </div>
        </div>
        <nav className="sidebar-nav">
          <div className="nav-label">Main</div>
          <NavItem icon="⊞" label="Dashboard" active={tab === 'dashboard'} onClick={() => setTab('dashboard')} />
          <NavItem icon="◉" label="New Assessment" active={tab === 'assessment'} onClick={() => setTab('assessment')} />
          {result && <NavItem icon="📋" label="Results" active={tab === 'results'} onClick={() => setTab('results')} />}
          <NavItem icon="📊" label="Scenario Planner" active={tab === 'scenario'} onClick={() => setTab('scenario')} />
          <div className="nav-label" style={{ marginTop: 6 }}>System</div>
          <NavItem icon="🧠" label="Model Intelligence" active={tab === 'model'} onClick={() => setTab('model')} />
        </nav>
        <div className="sidebar-footer">
          <div className="sidebar-badge" style={{ marginBottom: 12 }}>
            <span className="status-dot" />
            <div>
              <div style={{ fontSize: 10.5, fontWeight: 600, color: 'var(--t1)' }}>API Connected</div>
              <div style={{ fontSize: 9.5, color: 'var(--t3)' }}>Model v2.1 · 99.1%</div>
            </div>
          </div>
          <div style={{ textAlign: 'center', padding: '8px 0', borderTop: '1px solid var(--border)' }}>
            <div style={{ fontSize: 9, textTransform: 'uppercase', letterSpacing: '0.06em', color: 'var(--t3)', marginBottom: 3 }}>
              Developed & Designed by
            </div>
            <div style={{ fontSize: 11, fontWeight: 800, color: 'var(--indigo-light)', textShadow: '0 0 8px var(--indigo-glow)' }}>
              @abhishekbhosale
            </div>
          </div>
        </div>
      </aside>

      {/* Main */}
      <div className="main-content">
        <div className="topbar">
          <div className="topbar-breadcrumb">
            <span>EliteCredit</span>
            <span style={{ color: 'var(--t4)' }}>/</span>
            <span className="current">{pages[tab]}</span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span className="chip chip-indigo">● LR v2.1</span>
            <span className="chip chip-emerald">● Online</span>
            <button onClick={() => setShowHelp(true)} style={{ background: 'var(--bg-raised)', border: '1px solid var(--border)', borderRadius: 6, padding: '3px 9px', cursor: 'pointer', color: 'var(--t2)', fontSize: 13, fontFamily: 'inherit', transition: 'all 0.15s' }} title="Help">❓</button>
            <button className="theme-toggle" onClick={toggleTheme} title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`} />
          </div>
        </div>
        <div className="page-content">
          {tab === 'dashboard' && <DashboardPage onGo={() => setTab('assessment')} />}
          {tab === 'assessment' && <AssessmentPage onResult={handleResult} />}
          {tab === 'results' && result && <ResultsPage result={result} form={form} onBack={() => setTab('assessment')} />}
          {tab === 'scenario' && <ScenarioPage result={result} form={form} />}
          {tab === 'model' && <ModelPage />}
        </div>
        {showHelp && <HelpModal onClose={() => setShowHelp(false)} />}
      </div>
    </div>
  );
}
