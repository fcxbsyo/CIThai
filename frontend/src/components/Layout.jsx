import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.jsx'

const NAV = [
  { to: '/library', label: 'My Library', icon: '♪' },
  { to: '/create', label: 'Create Song', icon: '+' },
]

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <div style={{ display: 'flex', height: '100vh', overflow: 'hidden' }}>
      {/* Sidebar */}
      <aside style={{
        width: 'var(--sidebar-w)',
        background: 'var(--bg2)',
        borderRight: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        padding: '24px 0',
        flexShrink: 0,
      }}>
        <div style={{ padding: '0 24px 32px' }}>
          <div style={{ fontFamily: 'var(--font-display)', fontSize: 22, fontWeight: 800, color: 'var(--accent)' }}>CIThai</div>
          <div style={{ color: 'var(--text3)', fontSize: 11, marginTop: 2 }}>AI Music Generation</div>
        </div>

        <nav style={{ flex: 1, padding: '0 12px' }}>
          <div style={{ color: 'var(--text3)', fontSize: 11, fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', padding: '0 12px 8px' }}>Menu</div>
          {NAV.map(({ to, label, icon }) => (
            <NavLink key={to} to={to} style={({ isActive }) => ({
              display: 'flex', alignItems: 'center', gap: 10,
              padding: '10px 12px', borderRadius: 'var(--radius-sm)',
              color: isActive ? 'var(--accent)' : 'var(--text2)',
              background: isActive ? 'rgba(0,230,118,0.08)' : 'transparent',
              fontWeight: isActive ? 500 : 400, marginBottom: 2,
              transition: 'all 0.15s',
            })}>
              <span style={{ fontSize: 16, width: 20, textAlign: 'center' }}>{icon}</span>
              {label}
            </NavLink>
          ))}
        </nav>

        <div style={{ padding: '16px 24px', borderTop: '1px solid var(--border)' }}>
          <div style={{ color: 'var(--text)', fontWeight: 500, fontSize: 13, marginBottom: 2 }}>{user?.display_name}</div>
          <div style={{ color: 'var(--text3)', fontSize: 11, marginBottom: 12 }}>{user?.email}</div>
          <button
            onClick={handleLogout}
            style={{ color: 'var(--text3)', fontSize: 12 }}
            onMouseEnter={e => e.target.style.color = 'var(--danger)'}
            onMouseLeave={e => e.target.style.color = 'var(--text3)'}
          >Sign out</button>
        </div>
      </aside>

      {/* Main content */}
      <main style={{ flex: 1, overflow: 'auto', background: 'var(--bg)' }}>
        <Outlet />
      </main>
    </div>
  )
}