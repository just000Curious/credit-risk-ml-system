import { useState, useEffect } from 'react';
import { AssessmentPage, ResultsPage } from './pages';
import type { Result, FormState } from './pages';
import {
  LayoutDashboard, ClipboardCheck, BarChart3, Brain,
  HelpCircle,
  Target, Zap, Database, Hash,
  Server, Cpu, PieChart, Activity,
  CheckCircle2, ArrowRight, SlidersHorizontal, TrendingUp,
} from 'lucide-react';

const GitHubIcon = () => <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>;
const LinkedInIcon = () => <svg width="13" height="13" viewBox="0 0 24 24" fill="currentColor"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>;

function HelpModal({ onClose }: { onClose: () => void }) {
  // Fix P2: close on ESC key
  useEffect(() => {
    const handler = (e: KeyboardEvent) => { if (e.key === 'Escape') onClose(); };
    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
  }, [onClose]);

  return (
    <div style={{ position:'fixed',inset:0,zIndex:200,display:'flex',alignItems:'center',justifyContent:'center' }}>
      <div style={{ position:'absolute',inset:0,background:'rgba(0,0,0,0.5)',backdropFilter:'blur(4px)' }} onClick={onClose} />
      <div style={{ position:'relative',background:'var(--bg-card)',border:'1px solid var(--border)',borderRadius:6,padding:'24px 28px',maxWidth:500,width:'90%',maxHeight:'80vh',overflowY:'auto',boxShadow:'var(--shadow-lg)' }} className="animate-in">
        <div style={{ display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:18 }}>
          <h2 className="heading" style={{ fontSize:15,fontWeight:600,color:'var(--t1)',margin:0 }}>How to Use EliteCredit</h2>
          <button onClick={onClose} aria-label="Close help" style={{ background:'var(--bg-raised)',border:'1px solid var(--border)',borderRadius:4,padding:'3px 8px',cursor:'pointer',color:'var(--t2)',fontSize:13,fontFamily:'inherit' }}>✕</button>
        </div>
        {[
          { step:'1', title:'New Assessment', desc:'Click "Assessment" in the nav. Fill in the applicant details.' },
          { step:'2', title:'Run Analysis', desc:'Click "Run Risk Analysis" — the ML backend predicts a 300–900 credit score in real-time.' },
          { step:'3', title:'View Results', desc:'Review score, tier, metrics (LTI, DTI, EMI), and advisor recommendations.' },
          { step:'4', title:'Scenario Planner', desc:'Use sliders to simulate how changes could improve the score.' },
          { step:'5', title:'Model Intelligence', desc:'Explore model specs, feature importance, and system architecture.' },
        ].map(s => (
          <div key={s.step} style={{ display:'flex',gap:10,marginBottom:8,padding:'10px 12px',background:'var(--bg-raised)',borderRadius:4,border:'1px solid var(--border)' }}>
            <div style={{ width:22,height:22,borderRadius:4,background:'var(--accent-dim)',display:'flex',alignItems:'center',justifyContent:'center',fontSize:11,fontWeight:600,color:'var(--accent-light)',flexShrink:0,fontFamily:'DM Mono, monospace' }}>{s.step}</div>
            <div><div style={{ fontSize:13,fontWeight:600,color:'var(--t1)',marginBottom:1 }}>{s.title}</div><div style={{ fontSize:11.5,color:'var(--t3)',lineHeight:1.5 }}>{s.desc}</div></div>
          </div>
        ))}
      </div>
    </div>
  );
}

function DashboardPage({ onGo }: { onGo: () => void }) {
  const tech = ['Python 3.11','FastAPI','React','TypeScript','Scikit-learn','Logistic Regression','Joblib'];
  return (
    <div className="animate-in">
      <div className="hero-banner">
        <div style={{ position:'relative',zIndex:1 }}>
          <div style={{ display:'flex',gap:6,marginBottom:14 }}>
            <span className="chip chip-emerald">Live System</span>
            <span className="chip chip-indigo">ML Powered</span>
            <span className="chip chip-violet">Production Ready</span>
          </div>
          <h1 className="heading" style={{ fontSize:28,fontWeight:600,letterSpacing:'-0.015em',lineHeight:1.2,marginBottom:10 }}>
            Credit Risk Intelligence<br/>
            <span style={{ color:'var(--accent)' }}>Powered by Machine Learning</span>
          </h1>
          <p style={{ fontSize:14,color:'var(--t2)',maxWidth:540,lineHeight:1.7,marginBottom:22 }}>
            Real-time credit scoring engine trained on <strong style={{color:'var(--t1)'}}>252,000+ samples</strong>, served via <strong style={{color:'var(--t1)'}}>FastAPI</strong>, and visualised in <strong style={{color:'var(--t1)'}}>React</strong>. Generates 300–900 credit scores with <strong style={{color:'var(--accent)'}}>99.1% accuracy</strong>.
          </p>
          <button className="btn-primary" onClick={onGo} style={{ padding:'11px 24px',fontSize:14 }}>
            <ArrowRight size={14} /> Start Assessment
          </button>
          <div className="tech-stack">{tech.map(t => <span key={t} className="tech-badge">{t}</span>)}</div>
        </div>
      </div>

      <div className="grid-4 animate-in animate-delay-1" style={{ marginBottom:16 }}>
        {[
          { icon: Target,   value:'99.1%',  label:'Model Accuracy',   chip:'chip-emerald', ct:'Validated' },
          { icon: Zap,      value:'<200ms', label:'Inference Latency', chip:'chip-cyan',    ct:'FastAPI' },
          { icon: Database, value:'252K',   label:'Training Samples',  chip:'chip-amber',   ct:'SMOTE' },
          { icon: Hash,     value:'14',     label:'Risk Features',     chip:'chip-violet',  ct:'Engineered' },
        ].map(k => (
          <div key={k.label} className="card" style={{ padding:'16px' }}>
            <div style={{ display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:10 }}>
              <k.icon size={16} style={{ color:'var(--t3)' }} />
              <span className={`chip ${k.chip}`}>{k.ct}</span>
            </div>
            <div className="kpi-value">{k.value}</div><div className="kpi-label">{k.label}</div>
          </div>
        ))}
      </div>

      <div className="grid-2 animate-in animate-delay-2">
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-cyan"><Server size={11} /></span> System Architecture</div>
          {[
            { icon: Cpu, title:'React + Vite + TypeScript', desc:'Modern SPA with Axios API integration' },
            { icon: Zap, title:'FastAPI Backend', desc:'REST API, Pydantic validation, OpenAPI docs' },
            { icon: PieChart, title:'Scikit-learn Pipeline', desc:'MinMaxScaler → Logistic Regression, Joblib' },
            { icon: Activity, title:'Credit Scoring Engine', desc:'Sigmoid mapping to 300–900 (RBI-calibrated)' },
          ].map(a => (
            <div key={a.title} style={{ display:'flex',gap:10,marginBottom:8,padding:'9px 10px',background:'var(--bg-raised)',borderRadius:4,border:'1px solid var(--border)' }}>
              <a.icon size={15} style={{ color:'var(--t3)',flexShrink:0,marginTop:1 }} />
              <div><div style={{ fontSize:12.5,fontWeight:600,color:'var(--t1)',marginBottom:1 }}>{a.title}</div><div style={{ fontSize:11.5,color:'var(--t3)',lineHeight:1.5 }}>{a.desc}</div></div>
            </div>
          ))}
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-emerald"><Activity size={11} /></span> Model Performance</div>
          {[
            { label:'Accuracy',  val:99.1,  pct:99.1,  color:'var(--emerald)' },
            { label:'AUC-ROC',  val:0.9875, pct:98.75, color:'var(--accent)' },
            { label:'Precision', val:97.4,  pct:97.4,  color:'var(--amber)' },
            { label:'Recall',    val:95.8,  pct:95.8,  color:'var(--violet)' },
          ].map(m => (
            <div key={m.label} style={{ marginBottom:12 }}>
              <div style={{ display:'flex',justifyContent:'space-between',marginBottom:3 }}>
                <span style={{ fontSize:12,color:'var(--t3)' }}>{m.label}</span>
                <span style={{ fontSize:12,fontWeight:600,color:m.color,fontFamily:'DM Mono, monospace' }}>
                  {m.label === 'AUC-ROC' ? m.val.toFixed(4) : `${m.val}%`}
                </span>
              </div>
              <div className="progress-track"><div className="progress-fill" style={{ width:`${m.pct}%`,background:m.color }} /></div>
            </div>
          ))}
          <div style={{ marginTop:6,padding:'8px 10px',background:'var(--emerald-dim)',borderRadius:4,border:'1px solid rgba(34,151,122,0.15)',fontSize:11.5 }}>
            <span style={{ fontWeight:600,color:'var(--emerald-light)' }}>Production Validated</span><span style={{ color:'var(--t3)' }}> — 50.4K held-out samples · SMOTE.</span>
          </div>
        </div>
      </div>
    </div>
  );
}

function ModelPage() {
  const M = [{l:'Algorithm',v:'Logistic Regression'},{l:'Accuracy',v:'99.1%'},{l:'AUC-ROC',v:'0.9875'},{l:'Training Samples',v:'252,000'},{l:'Features',v:'14'},{l:'Validation',v:'Stratified K-Fold (k=5)'},{l:'Score Range',v:'300 – 900'},{l:'Stack',v:'Scikit-learn + FastAPI + React'}];
  const F = [{n:'Credit Utilization Ratio',i:'High',d:'neg'},{n:'Avg Days Past Due',i:'High',d:'neg'},{n:'Delinquency Ratio',i:'High',d:'neg'},{n:'Loan-to-Income Ratio',i:'Medium',d:'neg'},{n:'Loan Tenure',i:'Medium',d:'pos'},{n:'Age',i:'Medium',d:'pos'},{n:'Number of Open Accounts',i:'Low',d:'neg'},{n:'Residence Type',i:'Low',d:'pos'}];
  return (
    <div className="animate-in">
      <p className="section-title">Model Intelligence</p>
      <p className="section-sub">Technical overview of the ML system powering credit risk analysis.</p>
      <div className="grid-2">
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-indigo"><Brain size={11} /></span> Specifications</div>
          {M.map(m => <div key={m.l} className="metric-row"><span style={{color:'var(--t3)'}}>{m.l}</span><span style={{fontWeight:600,color:'var(--t1)',fontFamily:'DM Mono, monospace'}}>{m.v}</span></div>)}
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-amber"><SlidersHorizontal size={11} /></span> Feature Importance</div>
          <table className="table"><thead><tr><th>Feature</th><th>Impact</th><th>Dir</th></tr></thead><tbody>
            {F.map(f => <tr key={f.n}><td>{f.n}</td><td><span className={`chip ${f.i==='High'?'chip-red':f.i==='Medium'?'chip-amber':'chip-indigo'}`}>{f.i}</span></td><td style={{color:f.d==='pos'?'var(--emerald)':'var(--red)',fontWeight:600}}>{f.d==='pos'?'▲ Pos':'▼ Neg'}</td></tr>)}
          </tbody></table>
        </div>
      </div>
    </div>
  );
}

function ScenarioPage({ result, form }: { result: Result|null; form: FormState|null }) {
  const [ut,setUt]=useState(25); const [ib,setIb]=useState(0);
  if (!result) return <div className="card animate-in" style={{textAlign:'center',padding:'50px 20px'}}><BarChart3 size={32} style={{color:'var(--t3)',marginBottom:12}} /><div className="heading" style={{fontSize:15,fontWeight:600,marginBottom:4}}>No Assessment Data</div><div style={{fontSize:13,color:'var(--t3)'}}>Run a credit risk assessment first.</div></div>;
  const cur=result.credit_score;
  const udiff = Math.max((form?.credit_utilization_ratio ?? 30) - ut, 0);
  const d = Math.min(udiff * 1.1, 60) + Math.min(ib * 0.75, 35);
  const pot = Math.min(cur + Math.round(d), 900);
  // delta is always >= 0 since pot >= cur (sliders only improve score)
  const delta = pot - cur;
  const cs = (s: number) => s >= 750 ? 'var(--emerald)' : s >= 650 ? 'var(--amber)' : 'var(--red)';
  return (
    <div className="animate-in">
      <p className="section-title">Scenario Planner</p><p className="section-sub">Simulate how changes could improve the client's credit profile.</p>
      <div className="grid-2">
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-cyan"><SlidersHorizontal size={11} /></span> Adjustments</div>
          <div style={{marginBottom:20}}>
            <div style={{display:'flex',justifyContent:'space-between',marginBottom:6}}><span style={{fontSize:12,fontWeight:500,color:'var(--t3)'}}>Target Utilization</span><span style={{fontSize:13,fontWeight:600,color:'var(--accent)',fontFamily:'DM Mono, monospace'}}>{ut}%</span></div>
            <input type="range" min={0} max={100} value={ut} onChange={e=>setUt(+e.target.value)} />
          </div>
          <div>
            <div style={{display:'flex',justifyContent:'space-between',marginBottom:6}}><span style={{fontSize:12,fontWeight:500,color:'var(--t3)'}}>Income Increase</span><span style={{fontSize:13,fontWeight:600,color:'var(--accent)',fontFamily:'DM Mono, monospace'}}>+{ib}%</span></div>
            <input type="range" min={0} max={50} value={ib} onChange={e=>setIb(+e.target.value)} />
          </div>
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-emerald"><TrendingUp size={11} /></span> Projected Impact</div>
          <div className="grid-2" style={{marginBottom:14}}>
            <div style={{textAlign:'center',padding:'14px',background:'var(--bg-raised)',borderRadius:4,border:'1px solid var(--border)'}}>
              <div style={{fontSize:10,color:'var(--t3)',fontWeight:600,letterSpacing:'0.06em',textTransform:'uppercase',marginBottom:4}}>Current</div>
              <div style={{fontSize:32,fontWeight:700,color:cs(cur),fontFamily:'DM Mono, monospace'}}>{cur}</div>
            </div>
            <div style={{textAlign:'center',padding:'14px',background:'var(--accent-dim)',borderRadius:4,border:'1px solid rgba(207,120,62,0.12)'}}>
              <div style={{fontSize:10,color:'var(--t3)',fontWeight:600,letterSpacing:'0.06em',textTransform:'uppercase',marginBottom:4}}>Potential</div>
              <div style={{fontSize:32,fontWeight:700,color:cs(pot),fontFamily:'DM Mono, monospace'}}>{pot}</div>
              <div style={{fontSize:12,color:'var(--emerald-light)',fontWeight:600,marginTop:2}}>+{delta} pts</div>
            </div>
          </div>
          <div style={{padding:'8px 10px',background:'var(--accent-dim)',borderRadius:4,border:'1px solid rgba(207,120,62,0.1)',fontSize:12,color:'var(--t2)',lineHeight:1.6}}>
            Reducing utilization from <strong>{form?.credit_utilization_ratio}%</strong> → <strong>{ut}%</strong>{ib>0&&<> + <strong>+{ib}%</strong> income</>} could yield <strong style={{color:'var(--emerald-light)'}}>+{delta} pts</strong>.
          </div>
        </div>
      </div>
    </div>
  );
}

export default function App() {
  const [tab,setTab]    = useState('dashboard');
  const [result,setResult] = useState<Result|null>(null);
  const [form,setForm]   = useState<FormState|null>(null);
  const [theme,setTheme] = useState<'dark'|'light'>(
    () => (localStorage.getItem('ec-theme') as 'dark'|'light') || 'dark'
  );
  const [showHelp,setShowHelp]=useState(false);
  useEffect(()=>{document.documentElement.setAttribute('data-theme',theme);localStorage.setItem('ec-theme',theme)},[theme]);
  const handleResult = (r: Result, f: FormState) => { setResult(r); setForm(f); setTab('results'); };
  const tabs: {id:string;icon:React.ElementType;label:string}[] = [
    {id:'dashboard', icon:LayoutDashboard, label:'Dashboard'},
    {id:'assessment', icon:ClipboardCheck,  label:'Assessment'},
    ...(result ? [{id:'results',  icon:CheckCircle2, label:'Results'}]  : []),
    ...(result ? [{id:'scenario', icon:BarChart3,    label:'Scenarios'}] : []),
    {id:'model', icon:Brain, label:'Model'},
  ];

  return (
    <>
      <nav className="pill-nav-wrapper">
        <div className="pill-logo"><div className="logo-icon">EC</div><span className="pill-logo-text">EliteCredit</span></div>
        {tabs.map(t=><button key={t.id} className={`pill-tab ${tab===t.id?'active':''}`} onClick={()=>setTab(t.id)}><t.icon size={14} />{t.label}</button>)}
        <div className="pill-right">
          <button onClick={()=>setShowHelp(true)} className="pill-link" title="Help"><HelpCircle size={13} /></button>
          <a className="pill-link" href="https://github.com/just000Curious" target="_blank" rel="noreferrer" title="GitHub"><GitHubIcon /></a>
          <a className="pill-link" href="https://www.linkedin.com/in/abhishek-sambhaji-bhosale/" target="_blank" rel="noreferrer" title="LinkedIn"><LinkedInIcon /></a>
          <button
            className="pill-theme"
            onClick={() => setTheme(t => t==='dark'?'light':'dark')}
            aria-label={`Switch to ${theme==='dark'?'light':'dark'} mode`}
            title={`Switch to ${theme==='dark'?'light':'dark'} mode`}
          />
        </div>
      </nav>

      <div className="main-content">
        <div className="page-content">
          {tab==='dashboard'&&<DashboardPage onGo={()=>setTab('assessment')}/>}
          {tab==='assessment'&&<AssessmentPage onResult={handleResult}/>}
          {tab==='results'&&result&&<ResultsPage result={result} onBack={()=>setTab('assessment')}/>}
          {tab==='scenario'&&<ScenarioPage result={result} form={form}/>}
          {tab==='model'&&<ModelPage/>}
        </div>
        <footer className="site-footer">
          <div className="footer-left">Designed & Developed by <strong>Abhishek Bhosale</strong> &nbsp;·&nbsp; <span className="status-dot"/> API Online</div>
          <div className="footer-links">
            <a className="footer-link" href="https://github.com/just000Curious" target="_blank" rel="noreferrer"><GitHubIcon /> GitHub</a>
            <a className="footer-link" href="https://www.linkedin.com/in/abhishek-sambhaji-bhosale/" target="_blank" rel="noreferrer"><LinkedInIcon /> LinkedIn</a>
          </div>
        </footer>
      </div>
      {showHelp&&<HelpModal onClose={()=>setShowHelp(false)}/>}
    </>
  );
}
