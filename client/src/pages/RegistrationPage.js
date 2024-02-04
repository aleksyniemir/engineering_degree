import React from 'react';
import Register from '../components/auth/Register';
import {
  MDBContainer,
} from 'mdb-react-ui-kit';


function RegistrationPage() {
  return (
    <MDBContainer className="p-3 my-5 d-flex flex-column w-50">
      <Register/>

      <div className="text-center">
        <p>Already a member? <a href="/">Login</a></p>
      </div>
      
    </MDBContainer>
  );
}

export default RegistrationPage;