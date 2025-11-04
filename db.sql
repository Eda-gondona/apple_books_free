-- Создание таблицы пользователей
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT,
    last_name TEXT,
    role TEXT DEFAULT 'editor',
    tags TEXT[],
    created TIMESTAMP,
    modified TIMESTAMP
);

-- Индексы для пользователей
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Создание таблицы фильмов (из вашего кода)
CREATE TABLE movies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    director TEXT,
    created TIMESTAMP,
    modified TIMESTAMP,
    creator UUID REFERENCES users(id)
);

-- Индексы для фильмов
CREATE INDEX idx_movies_title ON movies(title);
CREATE INDEX idx_movies_director ON movies(director);

-- Создание таблицы книг
CREATE TABLE books (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    description TEXT,
    cover_image TEXT,
    content_file TEXT,
    publication_year INTEGER,
    isbn TEXT,
    genre TEXT,
    publisher TEXT,
    created TIMESTAMP,
    modified TIMESTAMP,
    creator UUID REFERENCES users(id)
);

-- Индексы для книг
CREATE INDEX idx_books_title ON books(title);
CREATE INDEX idx_books_author ON books(author);
CREATE INDEX idx_books_genre ON books(genre);
CREATE INDEX idx_books_publication_year ON books(publication_year);

-- Дополнительные таблицы (если нужны)
CREATE TABLE authors (
    author_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    middle_name VARCHAR(50)
);

-- Вставка тестовых данных
INSERT INTO authors (author_id, first_name, last_name, middle_name) 
VALUES (1, 'F. Scott', 'Fitzgerald', 'Francis');

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    middle_name VARCHAR(50),
    address VARCHAR(255),
    phone_number VARCHAR(20)
);

INSERT INTO customers (customer_id, first_name, last_name, middle_name, address, phone_number) 
VALUES (1, 'Jane', 'Doe', 'Smith', '456 Elm St', '555-4321');

-- Вставка тестовых пользователей
INSERT INTO users (id, email, password, first_name, last_name, role, tags, created, modified) 
VALUES 
    (gen_random_uuid(), 'admin@library.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/3oXoR9Xo5O5S5R5Ye', 'Admin', 'User', 'superuser', '{"admin","superuser"}', NOW(), NOW()),
    (gen_random_uuid(), 'editor@library.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhf8/3oXoR9Xo5O5S5R5Ye', 'Editor', 'User', 'editor', '{"editor"}', NOW(), NOW());

-- Вставка тестовых книг
INSERT INTO books (id, title, author, description, publication_year, genre, publisher, created, modified) 
VALUES 
    (gen_random_uuid(), 'Война и мир', 'Лев Толстой', 'Роман-эпопея, описывающий русское общество в эпоху войн против Наполеона.', 1869, 'Роман-эпопея', 'Русский вестник', NOW(), NOW()),
    (gen_random_uuid(), 'Преступление и наказание', 'Фёдор Достоевский', 'Психологический роман о бывшем студенте Родионе Раскольникове.', 1866, 'Психологический роман', 'Русский вестник', NOW(), NOW()),
    (gen_random_uuid(), 'Мастер и Маргарита', 'Михаил Булгаков', 'Роман о визите дьявола в Москву 1930-х годов.', 1967, 'Фантастика', 'Московский рабочий', NOW(), NOW()),
    (gen_random_uuid(), '1984', 'Джордж Оруэлл', 'Антиутопический роман о тоталитарном обществе.', 1949, 'Антиутопия', 'Secker & Warburg', NOW(), NOW()),
    (gen_random_uuid(), 'Гарри Поттер и философский камень', 'Дж. К. Роулинг', 'Первая книга о юном волшебнике Гарри Поттере.', 1997, 'Фэнтези', 'Bloomsbury', NOW(), NOW());

-- Создание представлений (опционально)
CREATE VIEW book_details AS
SELECT 
    b.id,
    b.title,
    b.author,
    b.description,
    b.cover_image,
    b.publication_year,
    b.isbn,
    b.genre,
    b.publisher,
    b.created,
    b.modified,
    u.first_name || ' ' || u.last_name as creator_name
FROM books b
LEFT JOIN users u ON b.creator = u.id;

-- Комментарии к таблицам
COMMENT ON TABLE users IS 'Таблица пользователей системы';
COMMENT ON TABLE books IS 'Таблица книг библиотеки';
COMMENT ON TABLE movies IS 'Таблица фильмов (дополнительная функциональность)';

-- Права доступа (если нужно)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO library_user;