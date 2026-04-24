import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './hooks/useAuth.jsx'
import Layout from './components/Layout.jsx'
import LoginPage from './pages/LoginPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import LibraryPage from './pages/LibraryPage.jsx'
import CreateSongPage from './pages/CreateSongPage.jsx'
import SongDetailPage from './pages/SongDetailPage.jsx'
import SharedSongPage from './pages/SharedSongPage.jsx'
import OAuthCallbackPage from './pages/OAuthCallbackPage.jsx'

function PrivateRoute({ children }) {
  const { user } = useAuth()
  return user ? children : <Navigate to="/login" replace />
}

export default function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/share/:token" element={<SharedSongPage />} />
          <Route path="/oauth-callback" element={<OAuthCallbackPage />} />
          <Route path="/" element={<PrivateRoute><Layout /></PrivateRoute>}>
            <Route index element={<Navigate to="/library" replace />} />
            <Route path="library" element={<LibraryPage />} />
            <Route path="create" element={<CreateSongPage />} />
            <Route path="songs/:id" element={<SongDetailPage />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}