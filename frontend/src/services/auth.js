
export const getAccessToken = () => localStorage.getItem('access');

export const getRefreshToken = () => localStorage.getItem('refresh');

export const setAccessToken = (token) => localStorage.setItem('access', token);

export const clearTokens = () => {
  localStorage.removeItem('access');
  localStorage.removeItem('refresh');
};

export async function login(correo, contrasena) {
  const res = await fetch('http://localhost:8000/api/token/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ correo, password: contrasena }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || 'Login fallido');
  }
  const data = await res.json();
  setAccessToken(data.access);
  localStorage.setItem('refresh', data.refresh);
  return data;
}

export async function refreshToken() {
  const refresh = getRefreshToken();
  if (!refresh) throw new Error('No hay refresh token');
  const res = await fetch('http://localhost:8000/api/token/refresh/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refresh }),
  });
  if (!res.ok) {
    clearTokens();
    throw new Error('Refresh token inválido o expirado');
  }
  const data = await res.json();
  setAccessToken(data.access);
  return data.access;
}

export async function fetchWithAuth(url, options = {}) {
  let access = getAccessToken();

  const headers = {
    ...(options.headers || {}),
    Authorization: `Bearer ${access}`,
  };

  let res = await fetch(url, { ...options, headers });

  if (res.status === 401) {
    try {
      access = await refreshToken();
    } catch (err) {
      clearTokens();
      window.location.href = 'components/login';
      throw err;
    }
    const retryHeaders = {
      ...(options.headers || {}),
      Authorization: `Bearer ${access}`,
    };
    res = await fetch(url, { ...options, headers: retryHeaders });
  }

  return res;
}

