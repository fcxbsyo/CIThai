import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../api/client.js'

function formatDuration(secs) {
  if (!secs) return '0:00'
  return `${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}`
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

export default function SharedSongPage() {
  const { token } = useParams()
  const [song, setSong] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    api.getSharedSong(token)
      .then(setSong)
      .catch(() => setError('This share link is invalid or has expired.'))
      .finally(() => setLoading(false))
  }, [token])

  if (loading) return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text3)' }}>
      Loading…
    </div>
  )

  if (error) return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', flexDirection: 'column', gap: 16 }}>
      <div style={{ fontSize: 48 }}>✕</div>
      <div style={{ color: 'var(--danger)', fontSize: 16 }}>{error}</div>
      <Link to="/login" style={{ color: 'var(--accent)', fontSize: 14 }}>Go to CIThai</Link>
    </div>
  )

  return (
    <div style={{ minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 24 }}>
      <div style={{ width: '100%', maxWidth: 480, background: 'var(--bg2)', border: '1px solid var(--border)', borderRadius: 16, padding: 40 }}>
        
        {/* Logo */}
        <div style={{ fontFamily: 'var(--font-display)', fontSize: 18, fontWeight: 800, color: 'var(--accent)', marginBottom: 32 }}>CIThai</div>

        {/* Song info */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 20, marginBottom: 32 }}>
          <div style={{ width: 64, height: 64, borderRadius: 12, background: `hsl(${(song.id * 47) % 360}, 40%, 20%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24, flexShrink: 0 }}>♪</div>
          <div>
            <div style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 800, marginBottom: 4 }}>{song.title}</div>
            <div style={{ color: 'var(--text3)', fontSize: 13 }}>by {song.owner_display_name}</div>
          </div>
        </div>

        {/* Metadata */}
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 32 }}>
          {[['Duration', formatDuration(song.duration_seconds)], ['Created', formatDate(song.generated_at)], ['Genre', song.genre_name || '—'], ['Mood', song.mood]].map(([k, v]) => (
            <div key={k} style={{ background: 'var(--bg3)', borderRadius: 'var(--radius-sm)', padding: '12px 16px' }}>
              <div style={{ color: 'var(--text3)', fontSize: 11, marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.06em' }}>{k}</div>
              <div style={{ color: 'var(--text)', fontWeight: 500 }}>{v}</div>
            </div>
          ))}
        </div>

        {/* Login to play */}
        <div style={{ background: 'rgba(0,230,118,0.05)', border: '1px solid rgba(0,230,118,0.2)', borderRadius: 'var(--radius)', padding: 20, textAlign: 'center' }}>
          <div style={{ color: 'var(--text2)', fontSize: 13, marginBottom: 16 }}>Sign in to play this song</div>
          <Link to="/login" style={{ background: 'var(--accent)', color: '#000', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 14, padding: '10px 28px', borderRadius: 'var(--radius-sm)', display: 'inline-block' }}>
            Sign in to Play
          </Link>
        </div>
      </div>
    </div>
  )
}