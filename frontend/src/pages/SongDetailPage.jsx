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

  function handleSkipBack() {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = 0
    setProgress(0)
  }

  function handleSkipForward() {
    const audio = audioRef.current
    if (!audio) return
    audio.currentTime = audio.duration
    setProgress(100)
  }

  async function handleDownload() {
    try {
      const token = localStorage.getItem('access_token')
      const res = await fetch(`/api/songs/${id}/download/`, {
        headers: { 'Authorization': `Bearer ${token}` }
      })
      window.open(res.url, '_blank')
    } catch {
      setToast({ message: 'Failed to download song', type: 'error' })
    }
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

  if (loading) return <div style={{ padding: 48, color: 'var(--text3)', fontSize: 16 }}>Loading…</div>
  if (error) return <div style={{ padding: 48, color: 'var(--danger)', fontSize: 16 }}>{error}</div>
  if (!song) return null

  return (
    <div style={{ padding: '40px 48px' }}>
      <button onClick={() => navigate('/library')} style={{ color: 'var(--text3)', fontSize: 15, marginBottom: 32, display: 'flex', alignItems: 'center', gap: 6 }}>
        ← Back to Library
      </button>

      <div style={{ display: 'flex', alignItems: 'center', gap: 28, marginBottom: 40 }}>
        <div style={{ width: 88, height: 88, borderRadius: 16, background: `hsl(${(song.id * 47) % 360}, 40%, 20%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 36, flexShrink: 0 }}>♪</div>
        <div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 32, fontWeight: 800, letterSpacing: '-0.5px', marginBottom: 8 }}>{song.title}</h1>
          <div style={{ color: 'var(--text3)', fontSize: 15 }}>{formatDate(song.generated_at)} · {formatDuration(song.duration_seconds)}</div>
        </div>
      </div>

      {/* Player */}
      {song.audio_file_reference && (
        <div style={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 32, marginBottom: 32 }}>
          <audio ref={audioRef} src={song.audio_file_reference} onTimeUpdate={handleTimeUpdate} onEnded={() => setPlaying(false)} />

          <input type="range" min="0" max="100" value={progress} onChange={handleSeek}
            style={{ width: '100%', marginBottom: 24, accentColor: 'var(--accent)', cursor: 'pointer' }} />

          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 24 }}>
            <button onClick={handleSkipBack} style={{ color: 'var(--text3)', fontSize: 22, padding: 8 }}>⏮</button>
            <button onClick={togglePlay} style={{ width: 56, height: 56, borderRadius: '50%', background: 'var(--accent)', color: '#000', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22, paddingLeft: playing ? 0 : 6 }}>
              {playing ? '⏸' : '▶'}
            </button>
            <button onClick={handleSkipForward} style={{ color: 'var(--text3)', fontSize: 22, padding: 8 }}>⏭</button>
          </div>
        </div>
      )}

      {/* Metadata */}
      <div style={{ background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 'var(--radius)', padding: 32, marginBottom: 32 }}>
        <div style={{ color: 'var(--text3)', fontSize: 12, fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 24 }}>Details</div>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 24 }}>
          {[['Mood', song.mood], ['Voice Type', song.voice_type], ['Duration', formatDuration(song.duration_seconds)], ['Created', formatDate(song.generated_at)]].map(([k, v]) => (
            <div key={k}>
              <div style={{ color: 'var(--text3)', fontSize: 13, marginBottom: 6 }}>{k}</div>
              <div style={{ color: 'var(--text)', fontWeight: 500, fontSize: 16 }}>{v || '—'}</div>
            </div>
          ))}
        </div>
        {song.custom_lyrics && (
          <div style={{ marginTop: 24, paddingTop: 24, borderTop: '1px solid var(--border)' }}>
            <div style={{ color: 'var(--text3)', fontSize: 12, fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 12 }}>Custom Lyrics</div>
            <div style={{ color: 'var(--text2)', fontSize: 15, lineHeight: 1.7 }}>{song.custom_lyrics}</div>
          </div>
        )}
      </div>

      {/* Actions */}
      <div style={{ display: 'flex', gap: 12 }}>
        <button
            onClick={handleShare}
            disabled={song.status !== 'READY'}
            style={{
                background: song.status !== 'READY' ? 'var(--bg4)' : 'var(--bg3)',
                color: song.status !== 'READY' ? 'var(--text3)' : 'var(--text)',
                border: '1px solid var(--border)',
                padding: '12px 24px',
                borderRadius: 'var(--radius-sm)',
                fontWeight: 500,
                fontSize: 15,
                cursor: song.status !== 'READY' ? 'not-allowed' : 'pointer',
            }}
        >
            {song.status !== 'READY' ? 'Share (unavailable)' : 'Share'}
        </button>
        <button onClick={handleDownload} style={{ background: 'var(--bg3)', color: 'var(--text)', border: '1px solid var(--border)', padding: '12px 24px', borderRadius: 'var(--radius-sm)', fontWeight: 500, fontSize: 15 }}>
          Download
        </button>
        <button onClick={handleDelete} style={{ background: 'rgba(255,77,109,0.1)', color: 'var(--danger)', border: '1px solid rgba(255,77,109,0.3)', padding: '12px 24px', borderRadius: 'var(--radius-sm)', fontWeight: 500, fontSize: 15 }}>
          Delete
        </button>
      </div>

      {shareUrl && (
        <div style={{ marginTop: 16, padding: '12px 16px', background: 'var(--bg3)', borderRadius: 'var(--radius-sm)', fontSize: 14, color: 'var(--text2)', wordBreak: 'break-all' }}>
          {shareUrl}
        </div>
      )}

      {toast && <Toast message={toast.message} type={toast.type} onClose={() => setToast(null)} />}
    </div>
  )
}