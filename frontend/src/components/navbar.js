import React from 'react';
import { useNavigate } from 'react-router-dom';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Button from 'react-bootstrap/Button';
import { clearTokens } from '../services/auth'; 

function Menu() {
  const navigate = useNavigate();

  const handleLogout = () => {
    clearTokens(); 
    navigate('/login');
  };

  return (
    <Navbar className="bg-body-tertiary">
      <Container>
        <Navbar.Brand href="/">
          <img
            alt=""
            src="/img/logo_GFC.png"
            width="30"
            height="30"
            className="d-inline-block align-top"
          />{' '}
          Colegio Fidel Cano
        </Navbar.Brand>

        <Button variant="outline-danger" onClick={handleLogout}>
          Cerrar sesión
        </Button>
      </Container>
    </Navbar>
  );
}

export default Menu;
