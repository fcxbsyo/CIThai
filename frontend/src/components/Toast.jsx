import { useEffect } from 'react'

export default function Toast({ message, type = 'success', onClose }) {
  useEffect(() => {
    const t = setTimeout(onClose, 3000)
    return () => clearTimeout(t)
  }, [onClose])

  const colors = {
    success: { bg: 'rgba(0,230,118,0.1)', border: 'rgba(0,230,118,0.3)', color: 'var(--accent)' },
    error: { bg: 'rgba(255,77,109,0.1)', border: 'rgba(255,77,109,0.3)', color: 'var(--danger)' },
  }
  const c = colors[type]

  return (
    <div style={{
      position: 'fixed', bottom: 32, right: 32, zIndex: 1000,
      background: c.bg, border: `1px solid ${c.border}`,
      color: c.color, borderRadius: 'var(--radius)',
      padding: '14px 20px', fontSize: 14, fontWeight: 500,
      boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      animation: 'fadeIn 0.2s ease',
    }}>
      {message}
    </div>
  )
}