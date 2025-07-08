import React, { useEffect, useState } from 'react';
import { fetchWithAuth } from '../services/auth';
import Accordion from 'react-bootstrap/Accordion';
import Table from 'react-bootstrap/Table';
import Alert from 'react-bootstrap/Alert';

function NotasEstudianteVista() {
  const [materias, setMaterias] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    (async () => {
      try {
        const res = await fetchWithAuth(`http://localhost:8000/api/materiasEstudiante/`);
        if (!res.ok) {
          const text = await res.text();
          throw new Error(`HTTP ${res.status}: ${text}`);
        }

        const data = await res.json();
        setMaterias(data);
      } catch (err) {
        console.error('Error al cargar materias y notas:', err);
        setError(err.message);
      }
    })();
  }, []);

  return (
    <div style={{ padding: '0 1rem' }}>
      <h2>Mis Notas por Materia</h2>

      {error && <Alert variant="danger">Error: {error}</Alert>}

      <Accordion alwaysOpen>
        {materias.map((materia, idx) => {
          const notas = materia.notas || [];

          const notaAcumulada = notas.reduce((acc, nota) => {
            const valor = parseFloat(nota.valor || 0);
            const porcentaje = parseFloat(nota.porcentaje || 0);
            return acc + (valor * porcentaje / 100);
          }, 0);

          return (
            <Accordion.Item eventKey={idx.toString()} key={materia.id}>
              <Accordion.Header>{materia.nombre_display || materia.nombre}</Accordion.Header>
              <Accordion.Body>
                <p><strong>Descripción:</strong> {materia.descripcion}</p>
                <p><strong>Temática:</strong> {materia.tematica}</p>
                {notas.length > 0 && (
                  <p><strong>Nota acumulada (ponderada):</strong> {notaAcumulada.toFixed(2)}</p>
                )}

                {notas.length > 0 ? (
                  <Table striped bordered hover responsive>
                    <thead>
                      <tr>
                        <th>#</th>
                        <th>Nombre</th>
                        <th>Fecha</th>
                        <th>Comentario</th>
                        <th>Periodo</th>
                        <th>Porcentaje</th>
                        <th>Valor</th>
                      </tr>
                    </thead>
                    <tbody>
                      {notas.map((nota, i) => (
                        <tr key={nota.id || i}>
                          <td>{i + 1}</td>
                          <td>{nota.nombre}</td>
                          <td>{nota.fecha}</td>
                          <td>{nota.comentario}</td>
                          <td>{nota.periodo_academico}</td>
                          <td>{nota.porcentaje}%</td>
                          <td>{nota.valor}</td>
                        </tr>
                      ))}
                    </tbody>
                  </Table>
                ) : (
                  <p>No hay notas registradas para esta materia.</p>
                )}
              </Accordion.Body>
            </Accordion.Item>
          );
        })}
      </Accordion>
    </div>
  );
}

export default NotasEstudianteVista;
