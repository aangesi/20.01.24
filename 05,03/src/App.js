import React, { useEffect, useState } from 'react';

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
        <div>
            <h1>Данные с Flask API</h1>
            {data ? (
                <div>
                    <p>{data.message}</p>
                    <ul>
                        {data.items.map((item, index) => (
                            <li key={index}>{item}</li>
                        ))}
                    </ul>
                </div>
            ) : (
                <p>Загрузка...</p>
            )}

            <h2>Создать нового пользователя</h2>
            <form onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    name="username" 
                    placeholder="Имя пользователя" 
                    value={newUser.username} 
                    onChange={handleInputChange} 
                    required 
                />
                <input 
                    type="password" 
                    name="password" 
                    placeholder="Пароль" 
                    value={newUser.password} 
                    onChange={handleInputChange} 
                    required 
                />
                <input 
                    type="text" 
                    name="FIO" 
                    placeholder="ФИО" 
                    value={newUser.FIO} 
                    onChange={handleInputChange} 
                    required 
                />
                <input 
                    type="text" 
                    name="phone" 
                    placeholder="Телефон" 
                    value={newUser.phone} 
                    onChange={handleInputChange} 
                    required 
                />
                <button type="submit">Создать пользователя</button>
            </form>

            <h2>Список пользователей</h2>
            <ul>
                {users.map((user) => (
                    <li key={user.id}>{user.username} - {user.FIO}</li>
                ))}
            </ul>
        </div>
    );
}

export default App;