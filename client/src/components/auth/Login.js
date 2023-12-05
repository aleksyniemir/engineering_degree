import React, { useState } from 'react';
import {
    MDBInput,
  }
  from 'mdb-react-ui-kit';

const Login = ({ onLoginSuccess }) => {
    const [nick, setNick] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://localhost:5000/auth/login', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({ 
                    nick, 
                    password 
                }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('token', data.token);
                console.log('Success:', data);
                onLoginSuccess();
            } else {
                console.log('Login failed.')
            }
        } catch (error) {
            console.error('An error occoured', error);
        }
    };

    return (
        
        <form onSubmit={handleSubmit} >
            <MDBInput 
                onChange={(e) => setNick(e.target.value)} 
                value={nick} 
                wrapperClass='mb-4' 
                label='Username'  
                type='text'
                />
            <MDBInput 
                onChange={(e) => setPassword(e.target.value)} 
                value={password} 
                wrapperClass='mb-4' 
                label='Password'  
                type='password'
                />          
            <button 
                class="ripple ripple-surface ripple-surface-light btn btn-dark mb-4" 
                type="submit">
                    Sign in
            </button>
        </form>
    );
};

export default Login;