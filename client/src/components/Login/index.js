import React, { useState } from 'react'

const Login = ({ onLoginSuccess }) => { 
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        
        try {
            const response = await fetch('http://localhost:5000/login', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify({ 
                    username, 
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

    }

    return (
        <form onSubmit={handleSubmit} className="login-form">
            <input 
                type="text" 
                value={username} 
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Username" 
            />
            <input 
                type="password" 
                value={password} 
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password" 
            />
            <button type="submit">Login</button>
        </form>
    );
}

export default Login;
