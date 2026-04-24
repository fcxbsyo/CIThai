import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client.js'
import Toast from '../components/Toast.jsx'

const STEPS = ['Title', 'Occasion', 'Genre', 'Voice Type', 'Mood', 'Lyrics']
const MOODS = ['HAPPY', 'SAD', 'ROMANTIC', 'ENERGETIC', 'CALM']
const VOICE_TYPES = ['MALE', 'FEMALE', 'CHILD', 'CHOIR', 'INSTRUMENTAL', 'DUET']

export default function CreateSongPage() {
  const navigate = useNavigate()
  const [step, setStep] = useState(0)
  const [genres, setGenres] = useState([])
  const [occasions, setOccasions] = useState([])
  const [form, setForm] = useState({ title: '', occasion: '', genre: '', voice_type: 'MALE', mood: 'HAPPY', custom_lyrics: '' })
  const [error, setError] = useState('')
  const [toast, setToast] = useState(null)

  useEffect(() => {
    api.getGenres().then(setGenres).catch(() => {})
    api.getOccasions().then(setOccasions).catch(() => {})
  }, [])

  function next() {
    setError('')
    if (step === 0 && !form.title.trim()) { setError('Please enter a song title'); return }
    if (step === 1 && !form.occasion) { setError('Please select an occasion'); return }
    if (step === 2 && !form.genre) { setError('Please select a genre'); return }
    setStep(s => s + 1)
  }

  function back() { setStep(s => s - 1); setError('') }

  async function handleSubmit() {
    try {
        await api.createSong({
        title: form.title,
        occasion: form.occasion,
        genre: form.genre,
        mood: form.mood,
        voice_type: form.voice_type,
        custom_lyrics: form.custom_lyrics || '',
        })
        setToast({ message: `"${form.title}" queued for generation!`, type: 'success' })
        setTimeout(() => navigate('/library'), 2000)
    } catch (err) {
        setToast({ message: err.detail || 'Failed to create song', type: 'error' })
    }
    }

  return (
    <div style={{ padding: '40px 48px', maxWidth: 640 }}>
      <div style={{ marginBottom: 32 }}>
        <div style={{ color: 'var(--text3)', fontSize: 12, fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8 }}>Step {step + 1} of {STEPS.length}</div>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 32, fontWeight: 800, letterSpacing: '-1px' }}>Create Song</h1>
      </div>

      {/* Progress bar */}
      <div style={{ height: 3, background: 'var(--bg3)', borderRadius: 2, marginBottom: 32, overflow: 'hidden' }}>
        <div style={{ height: '100%', width: `${(step / (STEPS.length - 1)) * 100}%`, background: 'var(--accent)', borderRadius: 2, transition: 'width 0.3s ease' }} />
      </div>

      {/* Step pills */}
      <div style={{ display: 'flex', gap: 8, marginBottom: 32, flexWrap: 'wrap' }}>
        {STEPS.map((s, i) => (
          <div key={s} style={{ padding: '4px 12px', borderRadius: 20, fontSize: 12, fontWeight: i === step ? 700 : 400, background: i === step ? 'var(--accent)' : i < step ? 'rgba(0,230,118,0.15)' : 'var(--bg3)', color: i === step ? '#000' : i < step ? 'var(--accent)' : 'var(--text3)' }}>{s}</div>
        ))}
      </div>

      {error && <div style={{ background: 'rgba(255,77,109,0.1)', border: '1px solid rgba(255,77,109,0.3)', borderRadius: 'var(--radius-sm)', padding: '10px 14px', color: 'var(--danger)', fontSize: 13, marginBottom: 24 }}>{error}</div>}

      {/* Step content */}
      <div style={{ marginBottom: 32 }}>
        {step === 0 && (
          <div>
            <label style={labelStyle}>Song Title</label>
            <input autoFocus type="text" placeholder="e.g. Happy Birthday Song for Mom" value={form.title} onChange={e => setForm(f => ({ ...f, title: e.target.value }))} style={{ fontSize: 16 }} />
          </div>
        )}

        {step === 1 && (
          <div>
            <label style={labelStyle}>Occasion</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, marginTop: 8 }}>
              {occasions.map(o => <OptionCard key={o.id} label={o.name} selected={form.occasion === o.id} onClick={() => setForm(f => ({ ...f, occasion: o.id }))} />)}
            </div>
          </div>
        )}

        {step === 2 && (
          <div>
            <label style={labelStyle}>Genre</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, marginTop: 8 }}>
              {genres.map(g => <OptionCard key={g.id} label={g.name} selected={form.genre === g.id} onClick={() => setForm(f => ({ ...f, genre: g.id }))} />)}
            </div>
          </div>
        )}

        {step === 3 && (
          <div>
            <label style={labelStyle}>Voice Type</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, marginTop: 8 }}>
              {VOICE_TYPES.map(v => <OptionCard key={v} label={v.charAt(0) + v.slice(1).toLowerCase()} selected={form.voice_type === v} onClick={() => setForm(f => ({ ...f, voice_type: v }))} />)}
            </div>
          </div>
        )}

        {step === 4 && (
          <div>
            <label style={labelStyle}>Mood</label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 12, marginTop: 8 }}>
              {MOODS.map(m => <OptionCard key={m} label={m.charAt(0) + m.slice(1).toLowerCase()} selected={form.mood === m} onClick={() => setForm(f => ({ ...f, mood: m }))} />)}
            </div>
          </div>
        )}

        {step === 5 && (
          <div>
            <label style={labelStyle}>Custom Lyrics <span style={{ color: 'var(--text3)', fontWeight: 400 }}>(optional)</span></label>
            <textarea placeholder="Add a personal story or theme…" value={form.custom_lyrics} onChange={e => setForm(f => ({ ...f, custom_lyrics: e.target.value }))} maxLength={1500} rows={6} style={{ resize: 'vertical' }} />
            <div style={{ color: 'var(--text3)', fontSize: 12, textAlign: 'right', marginTop: 4 }}>{form.custom_lyrics.length}/1500</div>

            {/* Summary */}
            <div style={{ marginTop: 24, padding: 20, background: 'var(--bg2)', borderRadius: 'var(--radius)', border: '1px solid var(--border)' }}>
              <div style={{ color: 'var(--text3)', fontSize: 11, fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 12 }}>Summary</div>
              {[['Title', form.title], ['Occasion', occasions.find(o => o.id === form.occasion)?.name || '—'], ['Genre', genres.find(g => g.id === form.genre)?.name || '—'], ['Voice', form.voice_type], ['Mood', form.mood]].map(([k, v]) => (
                <div key={k} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
                  <span style={{ color: 'var(--text3)', fontSize: 13 }}>{k}</span>
                  <span style={{ color: 'var(--text)', fontSize: 13, fontWeight: 500 }}>{v}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Navigation */}
      <div style={{ display: 'flex', gap: 12 }}>
        {step > 0 && <button onClick={back} style={{ background: 'var(--bg3)', color: 'var(--text2)', fontFamily: 'var(--font-display)', fontWeight: 600, fontSize: 14, padding: '12px 24px', borderRadius: 'var(--radius-sm)' }}>Back</button>}
        {step < STEPS.length - 1
          ? <button onClick={next} style={{ background: 'var(--accent)', color: '#000', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 14, padding: '12px 28px', borderRadius: 'var(--radius-sm)', flex: 1 }}>Continue →</button>
          : <button onClick={handleSubmit} style={{ background: 'var(--accent)', color: '#000', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 14, padding: '12px 28px', borderRadius: 'var(--radius-sm)', flex: 1 }}>✦ Generate Song</button>
        }
      </div>
      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}

function OptionCard({ label, selected, onClick }) {
  return (
    <button onClick={onClick} style={{ padding: '14px 16px', borderRadius: 'var(--radius)', background: selected ? 'rgba(0,230,118,0.1)' : 'var(--bg2)', border: `1px solid ${selected ? 'var(--accent)' : 'var(--border)'}`, color: selected ? 'var(--accent)' : 'var(--text)', fontWeight: selected ? 600 : 400, textAlign: 'left', transition: 'all 0.15s', cursor: 'pointer', fontSize: 14 }}>{label}</button>
  )
}

const labelStyle = { display: 'block', color: 'var(--text2)', fontSize: 12, fontWeight: 600, marginBottom: 8, textTransform: 'uppercase', letterSpacing: '0.06em' }