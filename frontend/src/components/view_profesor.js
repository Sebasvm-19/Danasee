import React, { useEffect, useState } from 'react';
import { fetchWithAuth } from '../services/auth';
import { useNavigate } from 'react-router-dom';
import Card from 'react-bootstrap/Card';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Button from 'react-bootstrap/Button';

function VistaProfesor() {
  const [cursos, setCursos] = useState([]);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

    useEffect(() => {
    (async () => {
        try {
        const res = await fetchWithAuth('http://localhost:8000/api/profesorCursos/');

        if (!res.ok) {
            const text = await res.text();  // 🔍 Captura el HTML o mensaje de error
            console.error('Respuesta no OK:', text);  // Muestra la respuesta cruda
            throw new Error(`HTTP ${res.status}: ${text}`);
        }

        const data = await res.json();
        setCursos(data);
        } catch (err) {
        console.error('Error al cargar cursos:', err);
        setError(err.message);
        }
    })();
    }, []);

  return (
    <div style={{ padding: '1rem' }}>
      <h2>Cursos Asignados</h2>
      <Row xs={1} md={2} lg={3} className="g-4">
        {cursos.map(curso => (
          <Col key={curso.id}>
            <Card>
              <Card.Body>
                <Card.Title>{curso.nombre_display || curso.nombre}</Card.Title>
                <Button
                    variant="primary"
                    onClick={() => navigate(`/materiasCurso/${curso.id}`)}
                    >
                    Ver detalles
                </Button>
              </Card.Body>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
}

export default VistaProfesor;
