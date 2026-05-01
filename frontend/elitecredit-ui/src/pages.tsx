import { useState } from 'react';
import axios from 'axios';

export interface Result {
  probability: number;
  credit_score: number;
  rating: string;
  loan_to_income_ratio: number;
  debt_to_income_ratio: number;
  monthly_emi: number;
}

const fmt  = (n: number) => n.toLocaleString('en-IN');
const sc   = (s: number) => s >= 750 ? 'var(--emerald)' : s >= 650 ? 'var(--amber)' : 'var(--red)';
const chip = (s: number) => s >= 750 ? 'chip-emerald' : s >= 650 ? 'chip-amber' : 'chip-red';
const tier = (s: number) => s >= 750 ? 'Elite — Tier 1' : s >= 650 ? 'Standard — Tier 2' : 'Development — Tier 3';

/* ── Field ─────────────────────────────────────────────────────────────── */
function Field({ label, name, type = 'number', value, onChange, options }: any) {
  return (
    <div>
      <label className="input-label">{label}</label>
      {options ? (
        <select name={name} value={value} onChange={onChange} className="input-field">
          {options.map((o: string) => <option key={o}>{o}</option>)}
        </select>
      ) : (
        <input type={type} name={name} value={value} onChange={onChange} className="input-field" />
      )}
    </div>
  );
}

/* ── Score Ring ────────────────────────────────────────────────────────── */
function ScoreRing({ score }: { score: number }) {
  const R = 70;
  const circ = 2 * Math.PI * R;
  const pct = (score - 300) / 600;
  const offset = circ - pct * circ;
  const color = sc(score);
  return (
    <div className="score-ring-wrap" style={{ width:170, height:170 }}>
      <svg className="score-ring-svg" width="170" height="170">
        <circle className="score-ring-track" cx="85" cy="85" r={R} />
        <circle
          className="score-ring-fill"
          cx="85" cy="85" r={R}
          stroke={color}
          strokeDasharray={circ}
          strokeDashoffset={offset}
        />
      </svg>
      <div className="score-ring-inner">
        <div style={{ fontSize:10,color:'var(--t3)',fontWeight:700,letterSpacing:'0.08em',textTransform:'uppercase',marginBottom:2 }}>Score</div>
        <div className="score-number" style={{ color }}>{score}</div>
        <span className={`chip ${chip(score)}`} style={{ fontSize:10,marginTop:4 }}>{score >= 750 ? 'Elite' : score >= 650 ? 'Standard' : 'Review'}</span>
      </div>
    </div>
  );
}

/* ── Stepper ────────────────────────────────────────────────────────────── */
function Stepper({ step }: { step: number }) {
  const steps = ['Personal', 'Financial', 'Credit', 'Analyze'];
  return (
    <div className="stepper">
      {steps.map((s, i) => (
        <div key={s} style={{ display:'flex',alignItems:'center',flex: i < steps.length-1 ? '1' : 'none' }}>
          <div className="step-item">
            <div className={`step-dot ${i < step ? 'done' : i === step ? 'active' : 'idle'}`}>
              {i < step ? '✓' : i+1}
            </div>
            <span className={`step-label ${i === step ? 'active' : ''}`}>{s}</span>
          </div>
          {i < steps.length-1 && <div className={`step-connector ${i < step ? 'done' : ''}`} style={{ flex:1 }} />}
        </div>
      ))}
    </div>
  );
}

/* ── Assessment Page ───────────────────────────────────────────────────── */
export function AssessmentPage({ onResult }: { onResult: (r: Result, f: any) => void }) {
  const [form, setForm] = useState({
    age: 32, annual_income: 1200000, loan_amount: 3500000,
    loan_tenure_months: 36, avg_dpd_per_delinquency: 5,
    delinquency_ratio: 10, credit_utilization_ratio: 30,
    num_open_accounts: 3, residence_type: 'Owned',
    loan_purpose: 'Home', loan_type: 'Secured',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');

  const handle = (e: any) => {
    const { name, value } = e.target;
    setForm(p => ({ ...p, [name]: ['residence_type','loan_purpose','loan_type'].includes(name) ? value : Number(value) }));
  };

  const submit = async (e: any) => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
      const { data } = await axios.post(`${API_URL}/api/predict`, form);
      onResult(data, form);
    } catch {
      setError('Cannot reach the API. Ensure FastAPI is running on port 8000.');
    } finally { setLoading(false); }
  };

  return (
    <div className="animate-in">
      <p className="section-title">Credit Risk Assessment</p>
      <p className="section-sub">Complete the applicant profile to generate an AI-powered risk analysis.</p>
      <Stepper step={3} />

      {error && (
        <div style={{ padding:'10px 14px',background:'var(--red-dim)',border:'1px solid rgba(239,68,68,0.25)',borderRadius:9,color:'var(--red)',fontSize:12.5,marginBottom:18 }}>
          ⚠ {error}
        </div>
      )}

      <form onSubmit={submit}>
        <div className="grid-2" style={{ marginBottom:16 }}>
          {/* Personal */}
          <div className="card card-glow">
            <div className="card-header"><span className="card-header-icon icon-teal">👤</span> Personal</div>
            <div style={{ display:'flex',flexDirection:'column',gap:13 }}>
              <Field label="Age" name="age" value={form.age} onChange={handle} />
              <Field label="Residence" name="residence_type" value={form.residence_type} onChange={handle} options={['Owned','Rented']} />
              <Field label="Open Accounts" name="num_open_accounts" value={form.num_open_accounts} onChange={handle} />
            </div>
          </div>
          {/* Financial */}
          <div className="card card-glow">
            <div className="card-header"><span className="card-header-icon icon-emerald">₹</span> Financial</div>
            <div style={{ display:'flex',flexDirection:'column',gap:13 }}>
              <Field label="Annual Income (₹)" name="annual_income" value={form.annual_income} onChange={handle} />
              <Field label="Loan Amount (₹)" name="loan_amount" value={form.loan_amount} onChange={handle} />
              <Field label="Tenure (Months)" name="loan_tenure_months" value={form.loan_tenure_months} onChange={handle} />
            </div>
          </div>
        </div>

        {/* Credit History */}
        <div className="card card-glow" style={{ marginBottom:16 }}>
          <div className="card-header"><span className="card-header-icon icon-amber">◈</span> Credit History</div>
          <div className="grid-3">
            <Field label="Utilization (%)" name="credit_utilization_ratio" value={form.credit_utilization_ratio} onChange={handle} />
            <Field label="Delinquency (%)" name="delinquency_ratio" value={form.delinquency_ratio} onChange={handle} />
            <Field label="Avg Days Past Due" name="avg_dpd_per_delinquency" value={form.avg_dpd_per_delinquency} onChange={handle} />
          </div>
        </div>

        {/* Loan Details */}
        <div className="card card-glow" style={{ marginBottom:22 }}>
          <div className="card-header"><span className="card-header-icon icon-cyan">◉</span> Loan Details</div>
          <div className="grid-2">
            <Field label="Purpose" name="loan_purpose" value={form.loan_purpose} onChange={handle} options={['Home','Personal','Education','Auto']} />
            <Field label="Type" name="loan_type" value={form.loan_type} onChange={handle} options={['Secured','Unsecured']} />
          </div>
        </div>

        <button type="submit" className="btn-primary btn-primary-full" disabled={loading}>
          {loading ? (
            <>
              <span style={{ display:'inline-block',width:14,height:14,border:'2px solid rgba(255,255,255,0.3)',borderTopColor:'white',borderRadius:'50%',animation:'spin 0.7s linear infinite' }} />
              Analysing...
            </>
          ) : '▶ \u00A0Run Risk Analysis'}
        </button>
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </form>
    </div>
  );
}

/* ── Results Page ──────────────────────────────────────────────────────── */
export function ResultsPage({ result, onBack }: { result: Result; onBack: () => void }) {
  const prob = result.probability * 100;
  const lti  = result.loan_to_income_ratio;
  const dti  = result.debt_to_income_ratio;

  return (
    <div className="animate-in">
      <div style={{ display:'flex',justifyContent:'space-between',alignItems:'flex-end',marginBottom:22 }}>
        <div>
          <p className="section-title">Assessment Complete</p>
          <p className="section-sub" style={{ marginBottom:0 }}>AI risk analysis generated successfully.</p>
        </div>
        <button className="btn-ghost" onClick={onBack}>← New Assessment</button>
      </div>

      {/* Tier Banner */}
      <div className={`rec-card ${result.credit_score >= 750 ? 'good' : result.credit_score >= 650 ? 'warn' : 'bad'}`} style={{ marginBottom:18,alignItems:'center',borderRadius:12 }}>
        <div style={{ fontSize:26 }}>{result.credit_score >= 750 ? '🏆' : result.credit_score >= 650 ? '✅' : '⚠️'}</div>
        <div style={{ flex:1 }}>
          <div style={{ fontWeight:700,fontSize:15,color:sc(result.credit_score),fontFamily:'Space Grotesk,sans-serif' }}>{tier(result.credit_score)}</div>
          <div style={{ fontSize:12,color:'var(--t3)',marginTop:3 }}>
            {result.credit_score >= 750 ? 'Fast-track · Preferential rates · Priority RM' : result.credit_score >= 650 ? 'Standard processing · Market rates' : 'Enhanced verification required'}
          </div>
        </div>
        <span className={`chip ${chip(result.credit_score)}`} style={{ fontSize:12 }}>Score: {result.credit_score}</span>
      </div>

      {/* Score Ring + KPIs */}
      <div style={{ display:'grid',gridTemplateColumns:'200px 1fr',gap:16,marginBottom:16 }}>
        <div className="card card-glow" style={{ display:'flex',flexDirection:'column',alignItems:'center',justifyContent:'center',padding:'24px 14px',textAlign:'center' }}>
          <ScoreRing score={result.credit_score} />
          <div style={{ marginTop:12,width:'100%' }}>
            <div style={{ display:'flex',justifyContent:'space-between',fontSize:9.5,color:'var(--t3)',marginBottom:3 }}><span>300</span><span>900</span></div>
            <div className="progress-track">
              <div className="progress-fill" style={{ width:`${((result.credit_score-300)/600)*100}%`,background:sc(result.credit_score) }} />
            </div>
          </div>
        </div>

        <div className="card card-glow">
          <div className="card-header"><span className="card-header-icon icon-teal">📊</span> Key Risk Metrics</div>
          <div className="grid-2">
            {[
              { label:'Default Probability', value:`${prob.toFixed(1)}%`, sub: prob<10?'Low':prob<25?'Moderate':'High', c: prob<10?'var(--emerald)':prob<25?'var(--amber)':'var(--red)' },
              { label:'Loan-to-Income',      value:`${lti.toFixed(1)}%`, sub: lti<30?'Optimal':lti<50?'Moderate':'Elevated', c: lti<30?'var(--emerald)':lti<50?'var(--amber)':'var(--red)' },
              { label:'Debt-to-Income',      value:`${dti.toFixed(1)}%`, sub: dti<20?'Affordable':dti<35?'Manageable':'Elevated', c: dti<20?'var(--emerald)':dti<35?'var(--amber)':'var(--red)' },
              { label:'Monthly EMI',         value:`₹${fmt(Math.round(result.monthly_emi))}`, sub:'Estimated', c:'var(--teal)' },
            ].map(m => (
              <div key={m.label} style={{ padding:'12px 14px',background:'var(--bg-raised)',borderRadius:10,border:'1px solid var(--border)' }}>
                <div style={{ fontSize:10.5,color:'var(--t3)',marginBottom:5,fontWeight:600 }}>{m.label}</div>
                <div style={{ fontSize:24,fontWeight:800,color:m.c,letterSpacing:'-0.02em',marginBottom:2,fontFamily:'Space Grotesk,sans-serif' }}>{m.value}</div>
                <div style={{ fontSize:10.5,color:'var(--t3)' }}>{m.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card card-glow">
        <div className="card-header"><span className="card-header-icon icon-emerald">💡</span> Advisor Recommendations</div>
        <div className="grid-2">
          {result.credit_score >= 750 ? (<>
            <div className="rec-card good"><div className="rec-icon" style={{background:'var(--emerald-dim)'}}>✅</div><div><div style={{fontSize:13,fontWeight:600,color:'var(--emerald)'}}>Offer Preferential Rate</div><div style={{fontSize:12,color:'var(--t3)',marginTop:2}}>7–9% p.a. elite pricing</div></div></div>
            <div className="rec-card good"><div className="rec-icon" style={{background:'var(--emerald-dim)'}}>🚀</div><div><div style={{fontSize:13,fontWeight:600,color:'var(--emerald)'}}>Fast-Track Processing</div><div style={{fontSize:12,color:'var(--t3)',marginTop:2}}>24-hr approval SLA</div></div></div>
          </>) : result.credit_score >= 650 ? (<>
            <div className="rec-card warn"><div className="rec-icon" style={{background:'var(--amber-dim)'}}>📋</div><div><div style={{fontSize:13,fontWeight:600,color:'var(--amber)'}}>Standard Processing</div><div style={{fontSize:12,color:'var(--t3)',marginTop:2}}>10–12% market rate</div></div></div>
            <div className="rec-card warn"><div className="rec-icon" style={{background:'var(--amber-dim)'}}>📂</div><div><div style={{fontSize:13,fontWeight:600,color:'var(--amber)'}}>Additional Docs</div><div style={{fontSize:12,color:'var(--t3)',marginTop:2}}>Income proof required</div></div></div>
          </>) : (<>
            <div className="rec-card bad"><div className="rec-icon" style={{background:'var(--red-dim)'}}>⛔</div><div><div style={{fontSize:13,fontWeight:600,color:'var(--red)'}}>Hold Application</div><div style={{fontSize:12,color:'var(--t3)',marginTop:2}}>Additional review needed</div></div></div>
            <div className="rec-card bad"><div className="rec-icon" style={{background:'var(--red-dim)'}}>📉</div><div><div style={{fontSize:13,fontWeight:600,color:'var(--red)'}}>Credit Rebuild Plan</div><div style={{fontSize:12,color:'var(--t3)',marginTop:2}}>Reduce utilization, clear arrears</div></div></div>
          </>)}
        </div>
      </div>
    </div>
  );
}
