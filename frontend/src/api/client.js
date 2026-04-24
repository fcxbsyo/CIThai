const BASE = '/api'

function getToken() {
  return localStorage.getItem('access_token')
}

async function request(method, path, body = null, auth = true) {
  const headers = { 'Content-Type': 'application/json' }
  if (auth) headers['Authorization'] = `Bearer ${getToken()}`
  const res = await fetch(`${BASE}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }))
    throw err
  }
  if (res.status === 204) return null
  return res.json()
}

export const api = {
  register: (data) => request('POST', '/auth/register/', data, false),
  login: (data) => request('POST', '/auth/login/', data, false),
  createSong: (data) => request('POST', '/songs/', data),
  getSongs: () => request('GET', '/songs/'),
  getSong: (id) => request('GET', `/songs/${id}/`),
  deleteSong: (id) => request('DELETE', `/songs/${id}/`),
  shareSong: (id) => request('POST', `/songs/${id}/share/`),
  getGenres: () => request('GET', '/genres/'),
  getOccasions: () => request('GET', '/occasions/'),
  getGenerations: () => request('GET', '/generations/'),
  getSharedSong: (token) => request('GET', `/share/${token}/`, null, false),
  getSharedWithMe: () => request('GET', '/songs/shared-with-me/'),
}