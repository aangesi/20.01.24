import React, { useState } from 'react';
import './App.css'; // Import the CSS file

function App() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [FIO, setFIO] = useState('');
  const [phone, setPhone] = useState('');
  const [message, setMessage] = useState('');

  // Phone number pattern (10 digits)
  const phonePattern = /^[0-9]{10}$/; // 10-digit phone number validation

  // Function for sending data to the server
  const handleSubmit = async (e) => {
    e.preventDefault();

    const newUser = {
      username,
      password,
      FIO,
      phone,
    };

    try {
      const response = await fetch('http://127.0.0.1:5000/api/users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newUser),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('User created successfully');
        // Clear form after success
        setUsername('');
        setPassword('');
        setFIO('');
        setPhone('');
      } else {
        setMessage(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('An error occurred while creating the user');
    }
  };

  return (
    <div className="App">
      <h1>Register User</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="username">Username</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="password">Password</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <div>
          <label htmlFor="FIO">Full Name (FIO)</label>
          <input
            type="text"
            id="FIO"
            value={FIO}
            onChange={(e) => setFIO(e.target.value)}
          />
        </div>

        <div>
          <label htmlFor="phone">Phone</label>
          <input
            type="text"
            id="phone"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            pattern={phonePattern.source} // Use the regex source for pattern validation
            title="Phone number should be 10 digits"
            required
          />
        </div>

        <button type="submit">Submit</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  );
}

export default App;
