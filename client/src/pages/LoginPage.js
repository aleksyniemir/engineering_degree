import React from 'react';
import Login from '../components/auth/Login';
import {
  MDBContainer,
} from 'mdb-react-ui-kit';

function LoginPage({ onLoginSuccess }) {
  return (
    <MDBContainer className="p-3 my-5 d-flex flex-column w-50">
      <Login onLoginSuccess={onLoginSuccess} />

      <div className="text-center">
        <p>Not a member? <a href="/register">Register</a></p>
      </div>
      
    </MDBContainer>
  );
}

export default LoginPage;
