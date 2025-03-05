import React, { useEffect, useState } from 'react';
import Chat from './Chat';

function App() {
    const [data, setData] = useState(null);
    const [users, setUsers] = useState([]);
    const [newUser, setNewUser] = useState({
        username: '',
        password: '',
        FIO: '',
        phone: ''
    });

    useEffect(() => {
        fetchData();
        fetchUsers();
    }, []);

    const fetchData = () => {
        fetch('http://localhost:5000/api/data')
            .then(response => response.json())
            .then(data => setData(data))
            .catch(error => console.error("Ошибка:", error));
    };

    const fetchUsers = () => {
        fetch('http://localhost:5000/api/users')
            .then(response => response.json())
            .then(users => setUsers(users))
            .catch(error => console.error("Ошибка:", error));
    };

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setNewUser({ ...newUser, [name]: value });
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        fetch('http://localhost:5000/api/users', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(newUser),
        })
            .then(response => {
                if (response.ok) {
                    fetchUsers(); // Обновляем список пользователей
                    setNewUser({ username: '', password: '', FIO: '', phone: '' }); // Очищаем форму
                }
                return response.json();
            })
            .then(data => console.log(data))
            .catch(error => console.error("Ошибка:", error));
    };

    return (
      <Chat/>
    );
}

export default App;