import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/login_page';
import NotasTable from './components/grades_stu_view';
import VistaProfesor from './components/view_profesor';
import MateriasCursoProfesor from './components/prof_materias';
import NotasCursoMateria from './components/grades_view';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/login" replace />} />
      <Route path="/login" element={<Login />} />
      <Route path="/notas/:materiaId" element={<NotasTable />} />
      <Route path="*" element={<Navigate to="/login" replace />} />
      <Route path="/profesor" element={<VistaProfesor />} />
      <Route path="/materiasCurso/:cursoId" element={<MateriasCursoProfesor />} />
      <Route
        path="/profesor/curso/:cursoId/materia/:materiaId/notas"
        element={<NotasCursoMateria />}
      />
      <Route 
        path="/profesor/curso/:cursoId/materia/:materiaId/actividad/:actividadId/notas" 
        element={<NotasCursoMateria />} />

    </Routes>
  );
}

export default App;
