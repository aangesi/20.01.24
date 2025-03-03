import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Убираем ссылки на отсутствующие файлы
// import './index.css';  // Удалите эту строку
// import reportWebVitals from './reportWebVitals';  // Удалите эту строку

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// Удалите вызов reportWebVitals
// reportWebVitals();

