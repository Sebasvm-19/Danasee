// src/components/login_page.js
import React, { useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import { login, setAccessToken } from '../services/auth';
import { useNavigate } from 'react-router-dom';
import Card from 'react-bootstrap/Card';

function Login() {
  const [correo, setCorreo] = useState('');
  const [contrasena, setContrasena] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await login(correo, contrasena);

      if (!response || !response.access) {
        throw new Error('No se recibió un token válido');
      }

      setAccessToken(response.access);

      const decoded = jwtDecode(response.access);
      console.log('Token decodificado:', decoded);

      const permiso = decoded.permiso;

      if (permiso === 1) {
        navigate('/notas/:materiaId');
      } else if (permiso === 2) {
        navigate('/profesor');
      } else {
        console.warn('Permiso no reconocido:', permiso);
        navigate('/');
      }
    } catch (err) {
      console.error('Error en login:', err);
      setError('Correo o contraseña incorrectos');
    }
  };

  return (
    <div style={{ maxWidth: 400, margin: '2rem auto' }}>
      <Card className="text-center">
        <Card.Header>Iniciar sesión</Card.Header>
        <Card.Body>
          <Card.Title>Ingreso al sistema</Card.Title>
          {error && <div style={{ color: 'red' }}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <div>
              <label>Correo:</label><br />
              <input
                type="email"
                value={correo}
                onChange={(e) => setCorreo(e.target.value)}
                required
              />
            </div>
            <div style={{ marginTop: '1rem' }}>
              <label>Contraseña:</label><br />
              <input
                type="password"
                value={contrasena}
                onChange={(e) => setContrasena(e.target.value)}
                required
              />
            </div>
            <button type="submit" style={{ marginTop: '1rem' }}>
              Ingresar
            </button>
          </form>
        </Card.Body>
      </Card>
    </div>
  );
}

export default Login;
