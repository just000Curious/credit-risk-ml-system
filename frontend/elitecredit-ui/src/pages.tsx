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

const fmt = (n: number) => n.toLocaleString('en-IN');
const sc = (s: number) => s >= 750 ? 'var(--emerald)' : s >= 650 ? 'var(--amber)' : 'var(--red)';
const chip = (s: number) => s >= 750 ? 'chip-emerald' : s >= 650 ? 'chip-amber' : 'chip-red';
const tier = (s: number) => s >= 750 ? 'Elite — Tier 1' : s >= 650 ? 'Standard — Tier 2' : 'Development — Tier 3';

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

export function AssessmentPage({ onResult }: { onResult: (r: Result, f: any) => void }) {
  const [form, setForm] = useState({
    age: 32, annual_income: 1200000, loan_amount: 3500000,
    loan_tenure_months: 36, avg_dpd_per_delinquency: 5,
    delinquency_ratio: 10, credit_utilization_ratio: 30,
    num_open_accounts: 3, residence_type: 'Owned',
    loan_purpose: 'Home', loan_type: 'Secured',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handle = (e: any) => {
    const { name, value } = e.target;
    setForm(p => ({ ...p, [name]: ['residence_type','loan_purpose','loan_type'].includes(name) ? value : Number(value) }));
  };

  const submit = async (e: any) => {
    e.preventDefault();
    setLoading(true); setError('');
    try {
      const { data } = await axios.post('http://localhost:8000/api/predict', form);
      onResult(data, form);
    } catch {
      setError('Cannot reach the API. Ensure FastAPI is running on port 8000.');
    } finally { setLoading(false); }
  };

  return (
    <div className="animate-in">
      <p className="section-title">Credit Risk Assessment</p>
      <p className="section-sub">Complete the applicant profile to generate an AI-powered risk analysis.</p>
      {error && <div style={{ padding: '10px 14px', background: 'var(--red-dim)', border: '1px solid rgba(239,68,68,0.25)', borderRadius: 8, color: 'var(--red)', fontSize: 12.5, marginBottom: 18 }}>⚠ {error}</div>}
      <form onSubmit={submit}>
        <div className="grid-2" style={{ marginBottom: 14 }}>
          <div className="card">
            <div className="card-header"><span className="card-header-icon icon-indigo">👤</span> Personal</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <Field label="Age" name="age" value={form.age} onChange={handle} />
              <Field label="Residence" name="residence_type" value={form.residence_type} onChange={handle} options={['Owned','Rented']} />
              <Field label="Open Accounts" name="num_open_accounts" value={form.num_open_accounts} onChange={handle} />
            </div>
          </div>
          <div className="card">
            <div className="card-header"><span className="card-header-icon icon-emerald">₹</span> Financial</div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              <Field label="Annual Income (₹)" name="annual_income" value={form.annual_income} onChange={handle} />
              <Field label="Loan Amount (₹)" name="loan_amount" value={form.loan_amount} onChange={handle} />
              <Field label="Tenure (Months)" name="loan_tenure_months" value={form.loan_tenure_months} onChange={handle} />
            </div>
          </div>
        </div>
        <div className="card" style={{ marginBottom: 14 }}>
          <div className="card-header"><span className="card-header-icon icon-amber">◈</span> Credit History</div>
          <div className="grid-3">
            <Field label="Utilization (%)" name="credit_utilization_ratio" value={form.credit_utilization_ratio} onChange={handle} />
            <Field label="Delinquency (%)" name="delinquency_ratio" value={form.delinquency_ratio} onChange={handle} />
            <Field label="Avg Days Past Due" name="avg_dpd_per_delinquency" value={form.avg_dpd_per_delinquency} onChange={handle} />
          </div>
        </div>
        <div className="card" style={{ marginBottom: 20 }}>
          <div className="card-header"><span className="card-header-icon icon-cyan">◉</span> Loan Details</div>
          <div className="grid-2">
            <Field label="Purpose" name="loan_purpose" value={form.loan_purpose} onChange={handle} options={['Home','Personal','Education','Auto']} />
            <Field label="Type" name="loan_type" value={form.loan_type} onChange={handle} options={['Secured','Unsecured']} />
          </div>
        </div>
        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button type="submit" className="btn-primary" disabled={loading} style={{ padding: '11px 28px' }}>
            {loading ? 'Analysing...' : '▶  Run Risk Analysis'}
          </button>
        </div>
      </form>
    </div>
  );
}

export function ResultsPage({ result, form, onBack }: { result: Result; form: any; onBack: () => void }) {
  const prob = result.probability * 100;
  const lti = result.loan_to_income_ratio;
  const dti = result.debt_to_income_ratio;

  return (
    <div className="animate-in">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 22 }}>
        <div><p className="section-title">Assessment Complete</p><p className="section-sub" style={{ marginBottom: 0 }}>AI risk analysis generated.</p></div>
        <button className="btn-ghost" onClick={onBack}>← New Assessment</button>
      </div>

      {/* Tier */}
      <div className={`rec-card ${result.credit_score >= 750 ? 'good' : result.credit_score >= 650 ? 'warn' : 'bad'}`} style={{ marginBottom: 14, alignItems: 'center', borderRadius: 10 }}>
        <div style={{ fontSize: 24 }}>{result.credit_score >= 750 ? '🏆' : result.credit_score >= 650 ? '✅' : '⚠️'}</div>
        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 700, fontSize: 14, color: sc(result.credit_score) }}>{tier(result.credit_score)}</div>
          <div style={{ fontSize: 11.5, color: 'var(--t3)', marginTop: 2 }}>
            {result.credit_score >= 750 ? 'Fast-track · Preferential rates · Priority RM' : result.credit_score >= 650 ? 'Standard processing · Market rates' : 'Enhanced verification required'}
          </div>
        </div>
        <span className={`chip ${chip(result.credit_score)}`}>Score: {result.credit_score}</span>
      </div>

      {/* Score + KPIs */}
      <div style={{ display: 'grid', gridTemplateColumns: '200px 1fr', gap: 14, marginBottom: 14 }}>
        <div className="card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', padding: '24px 14px', textAlign: 'center' }}>
          <div style={{ fontSize: 10, fontWeight: 700, letterSpacing: '0.1em', textTransform: 'uppercase', color: 'var(--t3)', marginBottom: 6 }}>Credit Score</div>
          <div style={{ fontSize: 56, fontWeight: 900, color: sc(result.credit_score), letterSpacing: '-0.04em', lineHeight: 1, marginBottom: 6 }}>{result.credit_score}</div>
          <span className={`chip ${chip(result.credit_score)}`}>{result.rating}</span>
          <div style={{ marginTop: 14, width: '100%' }}>
            <div className="progress-track"><div className="progress-fill" style={{ width: `${((result.credit_score - 300) / 600) * 100}%`, background: sc(result.credit_score) }} /></div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 9.5, color: 'var(--t3)', marginTop: 3 }}><span>300</span><span>900</span></div>
          </div>
        </div>
        <div className="card">
          <div className="card-header"><span className="card-header-icon icon-indigo">📊</span> Key Risk Metrics</div>
          <div className="grid-2">
            {[
              { label: 'Default Probability', value: `${prob.toFixed(1)}%`, sub: prob < 10 ? 'Low' : prob < 25 ? 'Moderate' : 'High', c: prob < 10 ? 'var(--emerald)' : prob < 25 ? 'var(--amber)' : 'var(--red)' },
              { label: 'Loan-to-Income', value: `${lti.toFixed(1)}%`, sub: lti < 30 ? 'Optimal' : lti < 50 ? 'Moderate' : 'Elevated', c: lti < 30 ? 'var(--emerald)' : lti < 50 ? 'var(--amber)' : 'var(--red)' },
              { label: 'Debt-to-Income', value: `${dti.toFixed(1)}%`, sub: dti < 20 ? 'Affordable' : dti < 35 ? 'Manageable' : 'Elevated', c: dti < 20 ? 'var(--emerald)' : dti < 35 ? 'var(--amber)' : 'var(--red)' },
              { label: 'Monthly EMI', value: `₹${fmt(Math.round(result.monthly_emi))}`, sub: 'Estimated', c: 'var(--indigo)' },
            ].map(m => (
              <div key={m.label} style={{ padding: '10px 12px', background: 'var(--bg-raised)', borderRadius: 7, border: '1px solid var(--border)' }}>
                <div style={{ fontSize: 10.5, color: 'var(--t3)', marginBottom: 4, fontWeight: 600 }}>{m.label}</div>
                <div style={{ fontSize: 22, fontWeight: 800, color: m.c, letterSpacing: '-0.02em', marginBottom: 2 }}>{m.value}</div>
                <div style={{ fontSize: 10.5, color: 'var(--t3)' }}>{m.sub}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recommendations */}
      <div className="card">
        <div className="card-header"><span className="card-header-icon icon-indigo">💡</span> Advisor Recommendations</div>
        <div className="grid-2">
          {result.credit_score >= 750 ? (<>
            <div className="rec-card good"><div className="rec-icon" style={{background:'var(--emerald-dim)'}}>✅</div><div><div style={{fontSize:12.5,fontWeight:600,color:'var(--emerald)'}}>Offer Preferential Rate</div><div style={{fontSize:11.5,color:'var(--t3)',marginTop:1}}>7–9% p.a. elite pricing</div></div></div>
            <div className="rec-card good"><div className="rec-icon" style={{background:'var(--emerald-dim)'}}>🚀</div><div><div style={{fontSize:12.5,fontWeight:600,color:'var(--emerald)'}}>Fast-Track Processing</div><div style={{fontSize:11.5,color:'var(--t3)',marginTop:1}}>24-hr approval SLA</div></div></div>
          </>) : result.credit_score >= 650 ? (<>
            <div className="rec-card warn"><div className="rec-icon" style={{background:'var(--amber-dim)'}}>📋</div><div><div style={{fontSize:12.5,fontWeight:600,color:'var(--amber)'}}>Standard Processing</div><div style={{fontSize:11.5,color:'var(--t3)',marginTop:1}}>10–12% market rate</div></div></div>
            <div className="rec-card warn"><div className="rec-icon" style={{background:'var(--amber-dim)'}}>📂</div><div><div style={{fontSize:12.5,fontWeight:600,color:'var(--amber)'}}>Additional Docs</div><div style={{fontSize:11.5,color:'var(--t3)',marginTop:1}}>Income proof required</div></div></div>
          </>) : (<>
            <div className="rec-card bad"><div className="rec-icon" style={{background:'var(--red-dim)'}}>⛔</div><div><div style={{fontSize:12.5,fontWeight:600,color:'var(--red)'}}>Hold Application</div><div style={{fontSize:11.5,color:'var(--t3)',marginTop:1}}>Additional review needed</div></div></div>
            <div className="rec-card bad"><div className="rec-icon" style={{background:'var(--red-dim)'}}>📉</div><div><div style={{fontSize:12.5,fontWeight:600,color:'var(--red)'}}>Credit Rebuild</div><div style={{fontSize:11.5,color:'var(--t3)',marginTop:1}}>Reduce utilization, clear arrears</div></div></div>
          </>)}
        </div>
      </div>
    </div>
  );
}
