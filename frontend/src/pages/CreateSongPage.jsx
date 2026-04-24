import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client.js'
import Toast from '../components/Toast.jsx'

const MOODS = ['HAPPY', 'SAD', 'ROMANTIC', 'ENERGETIC', 'CALM']
const VOICE_TYPES = ['MALE', 'FEMALE', 'CHILD', 'CHOIR', 'INSTRUMENTAL', 'DUET']

export default function CreateSongPage() {
  const navigate = useNavigate()
  const [genres, setGenres] = useState([])
  const [occasions, setOccasions] = useState([])
  const [form, setForm] = useState({ title: '', occasion: '', genre: '', voice_type: 'MALE', mood: 'HAPPY', custom_lyrics: '' })
  const [error, setError] = useState('')
  const [toast, setToast] = useState(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    api.getGenres().then(setGenres).catch(() => {})
    api.getOccasions().then(setOccasions).catch(() => {})
  }, [])

  async function handleSubmit() {
    setError('')
    if (!form.title.trim()) { setError('Please enter a song title'); return }
    if (!form.occasion) { setError('Please select an occasion'); return }
    if (!form.genre) { setError('Please select a genre'); return }
    setSubmitting(true)
    try {
        await api.generateSong({
        title: form.title,
        occasion: form.occasion,
        genre: form.genre,
        mood: form.mood,
        voice_type: form.voice_type,
        custom_lyrics: form.custom_lyrics || '',
        })
        setToast({ message: `"${form.title}" is generating in the background. Check your library for updates.`, type: 'success' })
        setTimeout(() => navigate('/library'), 2000)
    } catch (err) {
        setToast({ message: err.detail || 'Failed to start generation', type: 'error' })
    } finally {
        setSubmitting(false)
    }
}

  return (
    <div style={{ padding: '40px 48px' }}>
      <div style={{ marginBottom: 40 }}>
        <div style={{ color: 'var(--text3)', fontSize: 13, fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 10 }}>New Song</div>
        <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 36, fontWeight: 800, letterSpacing: '-1px' }}>Create Song</h1>
      </div>

      {error && (
        <div style={{ background: 'rgba(255,77,109,0.1)', border: '1px solid rgba(255,77,109,0.3)', borderRadius: 'var(--radius-sm)', padding: '12px 16px', color: 'var(--danger)', fontSize: 14, marginBottom: 32 }}>
          {error}
        </div>
      )}

      <div style={{ display: 'flex', flexDirection: 'column', gap: 40 }}>

        {/* Title */}
        <div>
          <label style={labelStyle}>Song Title <span style={{ color: 'var(--danger)' }}>*</span></label>
          <input
            type="text"
            placeholder="e.g. Happy Birthday Song for Mom"
            value={form.title}
            onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
            style={{ fontSize: 16, padding: '14px 16px', marginTop: 12 }}
          />
        </div>

        {/* Occasion */}
        <div>
          <label style={labelStyle}>Occasion <span style={{ color: 'var(--danger)' }}>*</span></label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginTop: 12 }}>
            {occasions.map(o => (
              <OptionCard key={o.id} label={o.name} selected={form.occasion === o.id} onClick={() => setForm(f => ({ ...f, occasion: o.id }))} />
            ))}
          </div>
        </div>

        {/* Genre */}
        <div>
          <label style={labelStyle}>Genre <span style={{ color: 'var(--danger)' }}>*</span></label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginTop: 12 }}>
            {genres.map(g => (
              <OptionCard key={g.id} label={g.name} selected={form.genre === g.id} onClick={() => setForm(f => ({ ...f, genre: g.id }))} />
            ))}
          </div>
        </div>

        {/* Voice Type */}
        <div>
          <label style={labelStyle}>Voice Type</label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginTop: 12 }}>
            {VOICE_TYPES.map(v => (
              <OptionCard key={v} label={v.charAt(0) + v.slice(1).toLowerCase()} selected={form.voice_type === v} onClick={() => setForm(f => ({ ...f, voice_type: v }))} />
            ))}
          </div>
        </div>

        {/* Mood */}
        <div>
          <label style={labelStyle}>Mood</label>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 12, marginTop: 12 }}>
            {MOODS.map(m => (
              <OptionCard key={m} label={m.charAt(0) + m.slice(1).toLowerCase()} selected={form.mood === m} onClick={() => setForm(f => ({ ...f, mood: m }))} />
            ))}
          </div>
        </div>

        {/* Lyrics */}
        <div>
          <label style={labelStyle}>
            Custom Lyrics{' '}
            <span style={{ color: 'var(--text3)', fontWeight: 400, textTransform: 'none', fontSize: 13 }}>(optional)</span>
          </label>
          <textarea
            placeholder="Add a personal story, theme, or specific lyrics you'd like incorporated…"
            value={form.custom_lyrics}
            onChange={e => setForm(f => ({ ...f, custom_lyrics: e.target.value }))}
            maxLength={1500}
            rows={5}
            style={{ resize: 'vertical', marginTop: 12, fontSize: 15 }}
          />
          <div style={{ color: 'var(--text3)', fontSize: 12, textAlign: 'right', marginTop: 4 }}>
            {form.custom_lyrics.length}/1500
          </div>
        </div>

        {/* Submit */}
        <div>
          <button
            onClick={handleSubmit}
            disabled={submitting}
            style={{
              background: 'var(--accent)',
              color: '#000',
              fontFamily: 'var(--font-display)',
              fontWeight: 700,
              fontSize: 16,
              padding: '16px 48px',
              borderRadius: 'var(--radius)',
              opacity: submitting ? 0.7 : 1,
            }}
          >
            {submitting ? 'Starting generation…' : '✦ Generate Song'}
          </button>
        </div>

      </div>

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}

function OptionCard({ label, selected, onClick }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: '16px 20px',
        borderRadius: 'var(--radius)',
        background: selected ? 'rgba(0,230,118,0.1)' : 'var(--bg2)',
        border: `1px solid ${selected ? 'var(--accent)' : 'var(--border)'}`,
        color: selected ? 'var(--accent)' : 'var(--text)',
        fontWeight: selected ? 600 : 400,
        textAlign: 'left',
        transition: 'all 0.15s',
        cursor: 'pointer',
        fontSize: 15,
      }}
    >
      {label}
    </button>
  )
}

const labelStyle = {
  display: 'block',
  color: 'var(--text2)',
  fontSize: 13,
  fontWeight: 600,
  textTransform: 'uppercase',
  letterSpacing: '0.06em',
}