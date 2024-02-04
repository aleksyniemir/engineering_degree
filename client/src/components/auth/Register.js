import React, { useState } from 'react';
import {
    MDBInput,
}
  from 'mdb-react-ui-kit';
import {
    useNavigate,
  } from 'react-router-dom';

const Register = () => {
    
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [repeatPassword, setRepeatPassword] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (password !== repeatPassword) {
      alert("Passwords do not match!");
      return;
    }

    const user = {
        nick: username,
        email: email,
        password: password
      };
    
    try {
        const response = await fetch('http://localhost:5000/auth/sign_up', {
            method: 'POST',
            headers: {
            'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
    });

    const data = await response.json();

    if (response.ok) {
      console.log('User registered successfully!');
      navigate('/');
    } else {
      console.log('Registration failed!', data.message);
      alert(data.message)
    }
  } catch (error) {
    console.error('There was an error!', error);
  }

  };

  return (
    <form onSubmit={handleSubmit}>
        <MDBInput
            label="Username"
            type="text"
            value={username}
            wrapperClass='mb-4' 
            onChange={e => setUsername(e.target.value)}
        />
        <MDBInput
            label="Email"
            type="email"
            value={email}
            wrapperClass='mb-4' 
            onChange={e => setEmail(e.target.value)}
        />
        <MDBInput
            label="Your password"
            type="password"
            value={password}
            wrapperClass='mb-4' 
            onChange={e => setPassword(e.target.value)}
        />
        <MDBInput
            label="Repeat your password"
            type="password"
            value={repeatPassword}
            wrapperClass='mb-4' 
            onChange={e => setRepeatPassword(e.target.value)}
        />
        <button 
            className="ripple ripple-surface ripple-surface-light btn btn-dark mb-4" 
            type="submit">
                Register
        </button>
    </form>
  );
}

export default Register;