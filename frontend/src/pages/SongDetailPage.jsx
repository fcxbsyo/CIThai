import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { api } from '../api/client.js'
import Toast from '../components/Toast.jsx'

function formatDuration(secs) {
  if (!secs) return '0:00'
  return `${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}`
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

export default function SongDetailPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [song, setSong] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [toast, setToast] = useState(null)
  const [playing, setPlaying] = useState(false)
  const [progress, setProgress] = useState(0)
  const [shareUrl, setShareUrl] = useState('')
  const audioRef = useRef(null)

  useEffect(() => {
    api.getSong(id)
      .then(setSong)
      .catch(() => setError('Failed to load song'))
      .finally(() => setLoading(false))
  }, [id])

  function togglePlay() {
    const audio = audioRef.current
    if (!audio) return
    if (playing) { audio.pause() } else { audio.play() }
    setPlaying(!playing)
  }

  function handleTimeUpdate() {
    const audio = audioRef.current
    if (!audio) return
    setProgress((audio.currentTime / audio.duration) * 100)
  }

  function handleSeek(e) {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = (e.target.value / 100) * audio.duration
    setProgress(e.target.value)
  }

  async function handleShare() {
    try {
      const data = await api.shareSong(id)
      const url = `${window.location.origin}/share/${data.token}`
      setShareUrl(url)
      navigator.clipboard.writeText(url).catch(() => {})
      setToast({ message: 'Share link copied to clipboard!', type: 'success' })
    } catch {
      setToast({ message: 'Failed to generate share link', type: 'error' })
    }
  }

  async function handleDelete() {
    if (!window.confirm(`Delete "${song.title}"? This cannot be undone.`)) return
    try {
      await api.deleteSong(id)
      navigate('/library')
    } catch {
      setToast({ message: 'Failed to delete song', type: 'error' })
    }
  }

  if (loading) return <div style={{ padding: 40, color: 'var(--text3)' }}>Loading…</div>
  if (error) return <div style={{ padding: 40, color: 'var(--danger)' }}>{error}</div>
  if (!song) return null

  return (
    <div style={{ padding: '40px 48px', maxWidth: 700 }}>
      {/* Back */}
      <button onClick={() => navigate('/library')} style={{ color: 'var(--text3)', fontSize: 13, marginBottom: 32, display: 'flex', alignItems: 'center', gap: 6 }}>
        ← Back to Library
      </button>

      {/* Song header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: 24, marginBottom: 40 }}>
        <div style={{ width: 80, height: 80, borderRadius: 16, background: `hsl(${(song.id * 47) % 360}, 40%, 20%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 32, flexShrink: 0 }}>♪</div>
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 28, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 6 }}>{song.title}</h1>
          <div style={{ color: 'var(--text3)', fontSize: 13 }}>{formatDate(song.generated_at)} · {formatDuration(song.duration_seconds)}</div>
        </div>
      </div>

      {/* Player */}
      {song.audio_file_reference && (
        <div style={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 24, marginBottom: 32 }}>
          <audio ref={audioRef} src={song.audio_file_reference} onTimeUpdate={handleTimeUpdate} onEnded={() => setPlaying(false)} />
          
          {/* Seek bar */}
          <input type="range" min="0" max="100" value={progress} onChange={handleSeek}
            style={{ width: '100%', marginBottom: 16, accentColor: 'var(--accent)', background: 'transparent', cursor: 'pointer' }} />

          {/* Controls */}
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 24 }}>
            <button onClick={togglePlay} style={{
              width: 48, height: 48, borderRadius: '50%',
              background: 'var(--accent)', color: '#000',
              display: 'flex', alignItems: 'center', justifyContent: 'center',
              fontSize: 18, fontWeight: 700,
            }}>
              {playing ? '⏸' : '▶'}
            </button>
          </div>
        </div>
      )}

      {/* Metadata */}
      <div style={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 24, marginBottom: 32 }}>
        <div style={{ color: 'var(--text3)', fontSize: 11, fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 16 }}>Details</div>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
          {[['Mood', song.mood], ['Voice Type', song.voice_type], ['Duration', formatDuration(song.duration_seconds)], ['Created', formatDate(song.generated_at)]].map(([k, v]) => (
            <div key={k}>
              <div style={{ color: 'var(--text3)', fontSize: 11, marginBottom: 4 }}>{k}</div>
              <div style={{ color: 'var(--text)', fontWeight: 500 }}>{v || '—'}</div>
            </div>
          ))}
        </div>
        {song.custom_lyrics && (
          <div style={{ marginTop: 16, paddingTop: 16, borderTop: '1px solid var(--border)' }}>
            <div style={{ color: 'var(--text3)', fontSize: 11, marginBottom: 8 }}>CUSTOM LYRICS</div>
            <div style={{ color: 'var(--text2)', fontSize: 13, lineHeight: 1.6 }}>{song.custom_lyrics}</div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: 12 }}>
        <button onClick={handleShare} style={{ background: 'var(--bg3)', color: 'var(--text)', border: '1px solid var(--border)', padding: '10px 20px', borderRadius: 'var(--radius-sm)', fontWeight: 500, fontSize: 13 }}>
          Share
        </button>
        <button onClick={handleDelete} style={{ background: 'rgba(255,77,109,0.1)', color: 'var(--danger)', border: '1px solid rgba(255,77,109,0.3)', padding: '10px 20px', borderRadius: 'var(--radius-sm)', fontWeight: 500, fontSize: 13 }}>
          Delete
        </button>
      </div>

      {shareUrl && (
        <div style={{ marginTop: 16, padding: '10px 14px', background: 'var(--bg3)', borderRadius: 'var(--radius-sm)', fontSize: 12, color: 'var(--text2)', wordBreak: 'break-all' }}>
          {shareUrl}
        </div>
      )}

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}