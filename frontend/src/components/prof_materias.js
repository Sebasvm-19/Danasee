import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchWithAuth } from '../services/auth';
import Accordion from 'react-bootstrap/Accordion';
import Button from 'react-bootstrap/Button';
import Alert from 'react-bootstrap/Alert';
import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';

function MateriasCursoProfesor() {
  const { cursoId } = useParams();
  const [materias, setMaterias] = useState([]);
  const [actividades, setActividades] = useState({});
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [materiaSeleccionada, setMateriaSeleccionada] = useState(null);
  const [nuevaActividad, setNuevaActividad] = useState({
    nombre: '',
    porcentaje: '',
    comentario: '',
    periodo_academico: ''
  });

  const navigate = useNavigate();

  const cargarMateriasYActividades = async () => {
    try {
      const res = await fetchWithAuth(`http://localhost:8000/api/materiasProfesorCurso/${cursoId}/`);
      if (!res.ok) throw new Error(`HTTP ${res.status}: ${await res.text()}`);
      const data = await res.json();
      setMaterias(data);

      const actividadesData = {};
      for (const materia of data) {
        try {
          const actRes = await fetchWithAuth(`http://localhost:8000/api/materias/${materia.id}/actividades/`);
          if (actRes.ok) {
            const actJson = await actRes.json();
            actividadesData[materia.id] = actJson;
          } else {
            actividadesData[materia.id] = [];
          }
        } catch {
          actividadesData[materia.id] = [];
        }
      }
      setActividades(actividadesData);
    } catch (err) {
      console.error('Error al cargar materias o actividades:', err);
      setError(err.message);
    }
  };

  useEffect(() => {
    cargarMateriasYActividades();
  }, [cursoId]);

  const abrirModal = (materiaId) => {
    setMateriaSeleccionada(materiaId);
    setNuevaActividad({
      nombre: '',
      porcentaje: '',
      comentario: '',
      periodo_academico: ''
    });
    setShowModal(true);
  };

  const handleSubmitActividad = async (e) => {
    e.preventDefault();
    try {
      const res = await fetchWithAuth(`http://localhost:8000/api/materias/${materiaSeleccionada}/actividades/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(nuevaActividad)
      });
      if (!res.ok) throw new Error(await res.text());

      setShowModal(false);
      await cargarMateriasYActividades(); // recargar actividades
    } catch (err) {
      alert('Error al crear actividad: ' + err.message);
    }
  };

  return (
    <div style={{ padding: '1rem' }}>
      <Button variant="secondary" onClick={() => navigate(-1)}>
        ← Volver
      </Button>

      <h2>Materias y Actividades del Curso</h2>
      {error && <Alert variant="danger">Error al cargar materias: {error}</Alert>}

      <Accordion defaultActiveKey="0" alwaysOpen>
        {materias.map((materia, idx) => (
          <Accordion.Item eventKey={idx.toString()} key={materia.id}>
            <Accordion.Header>{materia.nombre_display || materia.nombre}</Accordion.Header>
            <Accordion.Body>
              <p><strong>Temática:</strong> {materia.tematica}</p>
              <p><strong>Descripción:</strong> {materia.descripcion}</p>

              <div style={{ marginBottom: '1rem' }}>
                <Button
                  variant="outline-primary"
                  size="sm"
                  onClick={() => abrirModal(materia.id)}
                >
                  ➕ Agregar Actividad
                </Button>
              </div>

              <h5>Actividades:</h5>
              {actividades[materia.id]?.length > 0 ? (
                <ul>
                  {actividades[materia.id].map((actividad) => (
                    <li key={actividad.id}>
                      <strong>{actividad.nombre}</strong> — {actividad.comentario} ({actividad.porcentaje}%)
                      <Button
                        variant="link"
                        onClick={() =>
                          navigate(`/profesor/curso/${cursoId}/materia/${materia.id}/actividad/${actividad.id}/notas`)
                        }
                      >
                        Ver Notas
                      </Button>
                    </li>
                  ))}
                </ul>
              ) : (
                <p>No hay actividades registradas.</p>
              )}
            </Accordion.Body>
          </Accordion.Item>
        ))}
      </Accordion>

      {/* Modal para agregar actividad */}
      <Modal show={showModal} onHide={() => setShowModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Agregar Actividad</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form onSubmit={handleSubmitActividad}>
            <Form.Group className="mb-3">
              <Form.Label>Nombre</Form.Label>
              <Form.Control
                type="text"
                value={nuevaActividad.nombre}
                onChange={(e) => setNuevaActividad({ ...nuevaActividad, nombre: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Porcentaje</Form.Label>
              <Form.Control
                type="number"
                value={nuevaActividad.porcentaje}
                onChange={(e) => setNuevaActividad({ ...nuevaActividad, porcentaje: e.target.value })}
                required
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Comentario</Form.Label>
              <Form.Control
                type="text"
                value={nuevaActividad.comentario}
                onChange={(e) => setNuevaActividad({ ...nuevaActividad, comentario: e.target.value })}
              />
            </Form.Group>
            <Form.Group className="mb-3">
              <Form.Label>Periodo Académico</Form.Label>
              <Form.Control
                type="number"
                value={nuevaActividad.periodo_academico}
                onChange={(e) => setNuevaActividad({ ...nuevaActividad, periodo_academico: e.target.value })}
                required
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Crear Actividad
            </Button>
          </Form>
        </Modal.Body>
      </Modal>
    </div>
  );
}

export default MateriasCursoProfesor;
