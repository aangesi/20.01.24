-- Генерация пользователей
INSERT INTO User (lastname, name, surname, role_id, username, password)
VALUES 
('Иванов', 'Иван', 'Иванович', 1, 'ivanov', 'hashed_password'),
('Петров', 'Петр', 'Петрович', 1, 'petrov', 'hashed_password'),
('Сидоров', 'Алексей', 'Сидорович', 2, 'sidorov', 'hashed_password'),
('Васильев', 'Михаил', 'Васильевич', 2, 'vasilyev', 'hashed_password'),
('Федоров', 'Дмитрий', 'Федорович', 2, 'fedorov', 'hashed_password'),
('Козлов', 'Олег', 'Анатольевич', 2, 'kozlova', 'hashed_password'),
('Морозов', 'Евгений', 'Морозович', 2, 'morozov', 'hashed_password'),
('Гордеев', 'Сергей', 'Гордеевич', 2, 'gordeev', 'hashed_password'),
('Крылов', 'Станислав', 'Крылович', 2, 'krylov', 'hashed_password'),
('Шмидт', 'Роман', 'Шмидтович', 2, 'schmidt', 'hashed_password');
