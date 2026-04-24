import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { api } from '../api/client.js'

const STATUS = {
  READY: { bg: 'rgba(0,230,118,0.1)', color: 'var(--accent)', label: 'Ready' },
  GENERATING: { bg: 'rgba(255,183,3,0.1)', color: 'var(--warn)', label: 'Generating…' },
  FAILED: { bg: 'rgba(255,77,109,0.1)', color: 'var(--danger)', label: 'Failed' },
}

function formatDuration(secs) {
  if (!secs) return '—'
  return `${Math.floor(secs / 60)}:${String(secs % 60).padStart(2, '0')}`
}

function formatDate(iso) {
  return new Date(iso).toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
}

export default function LibraryPage() {
  const [songs, setSongs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api.getSongs()
      .then(setSongs)
      .catch(() => setError('Failed to load songs'))
      .finally(() => setLoading(false))
  }, [])

  return (
    <div style={{ padding: '40px 48px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 40 }}>
        <div>
          <div style={{ color: 'var(--text3)', fontSize: 12, fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 8 }}>Your Collection</div>
          <h1 style={{ fontFamily: 'var(--font-display)', fontSize: 36, fontWeight: 800, letterSpacing: '-1px' }}>My Library</h1>
        </div>
        <button onClick={() => navigate('/create')} style={{ background: 'var(--accent)', color: '#000', fontFamily: 'var(--font-display)', fontWeight: 700, fontSize: 13, padding: '10px 20px', borderRadius: 'var(--radius-sm)' }}>
          + New Song
        </button>
      </div>

      {loading && (
        <div style={{ color: 'var(--text3)' }}>Loading…</div>
      )}

      {error && (
        <div style={{ color: 'var(--danger)', padding: 16, background: 'rgba(255,77,109,0.1)', borderRadius: 'var(--radius)' }}>{error}</div>
      )}

      {!loading && !error && songs.length === 0 && (
        <div style={{ textAlign: 'center', padding: '80px 0', color: 'var(--text3)' }}>
          <div style={{ fontSize: 48, marginBottom: 16 }}>♪</div>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 20, fontWeight: 700, color: 'var(--text2)', marginBottom: 8 }}>No songs yet</div>
          <div style={{ marginBottom: 24 }}>Generate your first AI song to get started</div>
          <button onClick={() => navigate('/create')} style={{ background: 'var(--accent)', color: '#000', fontFamily: 'var(--font-display)', fontWeight: 700, padding: '10px 24px', borderRadius: 'var(--radius-sm)' }}>
            Create Song
          </button>
        </div>
      )}

      {!loading && songs.length > 0 && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 80px 90px', gap: 16, padding: '8px 16px', color: 'var(--text3)', fontSize: 11, fontWeight: 600, letterSpacing: '0.06em', textTransform: 'uppercase' }}>
            <span>Title</span><span>Genre</span><span>Occasion</span><span>Duration</span><span>Status</span>
          </div>

          {songs.map(song => {
            const s = STATUS[song.status] || STATUS.GENERATING
            return (
              <div key={song.id} onClick={() => navigate(`/songs/${song.id}`)}
                style={{ display: 'grid', gridTemplateColumns: '2fr 1fr 1fr 80px 90px', gap: 16, padding: '14px 16px', borderRadius: 'var(--radius)', cursor: 'pointer', alignItems: 'center', transition: 'background 0.15s' }}
                onMouseEnter={e => e.currentTarget.style.background = 'var(--bg2)'}
                onMouseLeave={e => e.currentTarget.style.background = 'transparent'}
              >
                <div style={{ display: 'flex', alignItems: 'center', gap: 14, minWidth: 0 }}>
                  <div style={{ width: 40, height: 40, borderRadius: 8, background: `hsl(${(song.id * 47) % 360}, 40%, 20%)`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 16, flexShrink: 0 }}>♪</div>
                  <div style={{ minWidth: 0 }}>
                    <div style={{ fontWeight: 500, whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>{song.title}</div>
                    <div style={{ color: 'var(--text3)', fontSize: 12 }}>{formatDate(song.generated_at)}</div>
                  </div>
                </div>
                <div style={{ color: 'var(--text2)', fontSize: 13 }}>{song.genre_name || '—'}</div>
                <div style={{ color: 'var(--text2)', fontSize: 13 }}>{song.occasion_name || '—'}</div>
                <div style={{ color: 'var(--text2)', fontSize: 13 }}>{formatDuration(song.duration_seconds)}</div>
                <div style={{ display: 'inline-flex', padding: '3px 8px', borderRadius: 20, fontSize: 11, fontWeight: 600, background: s.bg, color: s.color }}>{s.label}</div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}