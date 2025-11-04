from flask import Flask, render_template, jsonify,request, session, redirect  # ← ДОБАВИТЬ redirect
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("main")

app = Flask(__name__, template_folder="templates")
app.secret_key = 'dev-secret-key-123'

@app.route('/')
def home():
    # ДОБАВИТЬ ПРОВЕРКУ: если пользователь авторизован - показываем библиотеку
    if session.get('userid'):
        return render_template('book_list.html')  # ← показываем библиотеку для авторизованных
    
    # Если не авторизован - показываем приветственную страницу
    return """<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BookReader - Читайте с удовольствием</title>
    <style>
        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
        }
        
        body { 
            font-family: Arial, sans-serif; 
            background: white; 
            display: flex; 
            justify-content: center; 
            align-items: center; 
            min-height: 100vh;
        }
        
        .welcome-container { 
            background: white; 
            padding: 2rem; 
            border-radius: 8px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); 
            width: 100%; 
            max-width: 400px; 
            text-align: center;
            border: 1px solid #ddd;
        }
        
        .logo {
            font-size: 3rem;
            margin-bottom: 1rem;
            color: #007bff;
        }
        
        h1 {
            color: #333;
            margin-bottom: 0.5rem;
            font-size: 1.5rem;
        }
        
        .subtitle {
            color: #666;
            margin-bottom: 2rem;
            line-height: 1.5;
        }
        
        .btn { 
            width: 100%; 
            padding: 0.75rem; 
            border: none; 
            border-radius: 4px; 
            font-size: 1rem; 
            cursor: pointer; 
            text-decoration: none;
            display: block;
            text-align: center;
            transition: background-color 0.3s;
            background: #007bff; 
            color: white; 
        }
        
        .btn:hover { 
            background: #0056b3; 
        }
        
        .features {
            display: flex;
            justify-content: space-around;
            margin-top: 2rem;
            padding-top: 1.5rem;
            border-top: 1px solid #ddd;
        }
        
        .feature {
            text-align: center;
        }
        
        .feature-icon {
            font-size: 1.5rem;
            margin-bottom: 0.5rem;
        }
        
        .feature-text {
            font-size: 0.8rem;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="welcome-container">
        <div class="logo">📚</div>
        <h1>Добро пожаловать в BookReader</h1>
        <p class="subtitle">Читайте ваши любимые книги в любом месте и в любое время</p>
        
        <a href="/auth/login" class="btn">Регистрация</a>

        <div class="features">
            <div class="feature">
                <div class="feature-icon">📖</div>
                <div class="feature-text">Книги</div>
            </div>
            <div class="feature">
                <div class="feature-icon">⚡</div>
                <div class="feature-text">Быстро</div>
            </div>
            <div class="feature">
                <div class="feature-icon">📱</div>
                <div class="feature-text">Удобно</div>
            </div>
        </div>
    </div>
</body>
</html>"""

# Остальные маршруты остаются без изменений
@app.route('/auth/login')
def auth_login():
    return render_template('auth.html')

@app.route('/book_list', methods=['GET', 'POST'])
def book_list():
    if request.method == 'POST':
        # Здесь можно обработать данные формы если нужно
        mode = request.form.get('mode')
        email = request.form.get('email')
        print(f"Form submitted: {mode} for {email}")
    
    return render_template('book_list.html')

@app.route('/book/<book_id>')
def book_detail(book_id):
    books_data = {
        '1': {
            'id': 1,
            'title': 'Война и мир',
            'author': 'Лев Толстой',
            'description': 'Роман-эпопея, описывающий русское общество в эпоху войн против Наполеона.',
            'cover_image': None,
            'publication_year': 1869,
            'isbn': '978-5-699-12014-7',
            'genre': 'Роман-эпопея',
            'publisher': 'Русский вестник'
        },
        '2': {
            'id': 2,
            'title': 'Преступление и наказание',
            'author': 'Фёдор Достоевский',
            'description': 'Психологический роман о бывшем студенте Родионе Раскольникове.',
            'cover_image': None,
            'publication_year': 1866,
            'isbn': '978-5-04-105588-4',
            'genre': 'Психологический роман',
            'publisher': 'Русский вестник'
        },
        # ... добавьте остальные книги по аналогии
    }
    
    book = books_data.get(book_id, {
        'id': book_id,
        'title': 'Книга не найдена',
        'author': 'Неизвестен',
        'description': 'Книга временно недоступна',
        'cover_image': None,
        'publication_year': None,
        'isbn': 'Не указан',
        'genre': 'Неизвестен',
        'publisher': 'Неизвестно'
    })
    
    return render_template('book_detail.html', book=book)


@app.route('/read/<book_id>')
def read_book(book_id):
    # Данные для разных книг
    books_data = {
        '1': {
            'id': 1,
            'title': 'Война и мир',
            'author': 'Лев Толстой',
            'genre': 'Роман-эпопея',
            'year': '1869',
            'pages': '1225'
        },
        '2': {
            'id': 2,
            'title': 'Преступление и наказание',
            'author': 'Фёдор Достоевский',
            'genre': 'Психологический роман',
            'year': '1866',
            'pages': '672'
        },
        '3': {
            'id': 3,
            'title': 'Мастер и Маргарита',
            'author': 'Михаил Булгаков',
            'genre': 'Фантастический роман',
            'year': '1967',
            'pages': '480'
        },
        '4': {
            'id': 4,
            'title': 'Евгений Онегин',
            'author': 'Александр Пушкин',
            'genre': 'Роман в стихах',
            'year': '1833',
            'pages': '240'
        },
        '5': {
            'id': 5,
            'title': 'Отцы и дети',
            'author': 'Иван Тургенев',
            'genre': 'Роман',
            'year': '1862',
            'pages': '288'
        },
        '6': {
            'id': 6,
            'title': 'Анна Каренина',
            'author': 'Лев Толстой',
            'genre': 'Роман',
            'year': '1877',
            'pages': '864'
        },
        '7': {
            'id': 7,
            'title': 'Мёртвые души',
            'author': 'Николай Гоголь',
            'genre': 'Поэма',
            'year': '1842',
            'pages': '352'
        },
        '8': {
            'id': 8,
            'title': 'Герой нашего времени',
            'author': 'Михаил Лермонтов',
            'genre': 'Роман',
            'year': '1840',
            'pages': '224'
        }
    }
    
    book = books_data.get(book_id, {
        'id': book_id,
        'title': 'Книга не найдена',
        'author': 'Неизвестен',
        'genre': 'Неизвестен',
        'year': 'Неизвестен',
        'pages': '0'
    })
    
    return render_template('book_reader.html', book=book)

@app.route('/api/health')
def health():
    return jsonify({"status": "ok", "message": "✅ Все HTML страницы работают!"})

if __name__ == '__main__':
    log.info("🚀 Сервер запущен с HTML страницами!")
    log.info("🌐 Откройте: http://localhost:8100")
    app.run(host='0.0.0.0', port=8100, debug=True)