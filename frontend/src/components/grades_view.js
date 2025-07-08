import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { fetchWithAuth } from '../services/auth';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';
import Alert from 'react-bootstrap/Alert';
import { useNavigate } from 'react-router-dom';

function NotasCursoMateria() {
  const { cursoId, materiaId, actividadId } = useParams();
  const [notas, setNotas] = useState([]);
  const [valoresEditados, setValoresEditados] = useState({});
  const [error, setError] = useState(null);
  const [mensajeExito, setMensajeExito] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchWithAuth(`http://localhost:8000/api/profesor/curso/${cursoId}/materia/${materiaId}/actividad/${actividadId}/notas/`);
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`HTTP ${res.status}: ${text}`);
        }
        const data = await res.json();
        setNotas(data);
        setError(null);
      } catch (err) {
        console.error('Error cargando notas:', err);
        setError(err.message);
      }
    })();
  }, [cursoId, materiaId, actividadId]);

  const handleValorChange = (notaId, nuevoValor) => {
    setValoresEditados(prev => ({
      ...prev,
      [notaId]: {
        ...prev[notaId],
        valor: nuevoValor,
      },
    }));
  };

  const handleComentarioChange = (notaId, nuevoComentario) => {
    setValoresEditados(prev => ({
      ...prev,
      [notaId]: {
        ...prev[notaId],
        comentario: nuevoComentario,
      },
    }));
  };

  const handleGuardar = async (notaId) => {
    const cambios = valoresEditados[notaId];
    if (!cambios) return;

    try {
      const res = await fetchWithAuth(`http://localhost:8000/api/profesor/curso/${cursoId}/materia/${materiaId}/notas/`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ nota_id: notaId, ...cambios }),
      });

      if (!res.ok) {
        const text = await res.text();
        throw new Error(`Error: ${text}`);
      }

      setNotas(notas.map(n => n.id === notaId ? { ...n, ...cambios } : n));
      setValoresEditados(prev => {
        const updated = { ...prev };
        delete updated[notaId];
        return updated;
      });

      setMensajeExito('Nota actualizada correctamente');
      setTimeout(() => setMensajeExito(''), 3000);

    } catch (err) {
      console.error('Error actualizando nota:', err);
      alert('No se pudo actualizar la nota');
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <Button variant="secondary" onClick={() => navigate(-1)}>
        ← Volver
      </Button>
      <h2>Notas de la Actividad</h2>

      {mensajeExito && <Alert variant="success">{mensajeExito}</Alert>}
      {error && <Alert variant="danger">Error: {error}</Alert>}

      <Table striped bordered hover responsive>
        <thead>
          <tr>
            <th>#</th>
            <th>Nombre de la Nota</th>
            <th>Estudiante</th>
            <th>Fecha</th>
            <th>Comentario</th>
            <th>Valor</th>
            <th>Guardar</th>
          </tr>
        </thead>
        <tbody>
          {notas.map((n, idx) => (
            <tr key={n.id}>
              <td>{idx + 1}</td>
              <td>{n.nombre}</td>
              <td>{n.estudiante_nombre}</td>
              <td>{n.fecha}</td>
              <td>
                <Form.Control
                  type="text"
                  defaultValue={n.comentario}
                  onChange={(e) => handleComentarioChange(n.id, e.target.value)}
                />
              </td>
              <td>
                <Form.Control
                  type="number"
                  defaultValue={n.valor}
                  onChange={(e) => handleValorChange(n.id, e.target.value)}
                  style={{ maxWidth: '80px' }}
                />
              </td>
              <td>
                <Button
                  variant="success"
                  size="sm"
                  onClick={() => handleGuardar(n.id)}
                  disabled={!valoresEditados[n.id]}
                >
                  Guardar
                </Button>
              </td>
            </tr>
          ))}
        </tbody>
      </Table>
    </div>
  );
}

export default NotasCursoMateria;
