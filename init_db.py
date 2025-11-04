import os
import sys
import logging
from peewee import *
import datetime

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("init_db")

# Используем SQLite для простоты
DATABASE = 'book_library.db'
database = SqliteDatabase(DATABASE)

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    email = CharField(unique=True)
    password = CharField()
    first_name = CharField()
    last_name = CharField()
    role = CharField(default='user')
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)

class Book(BaseModel):
    title = CharField()
    author = CharField()
    description = TextField(null=True)
    cover_image = CharField(null=True)
    content_file = CharField(null=True)
    publication_year = IntegerField(null=True)
    isbn = CharField(null=True)
    genre = CharField(null=True)
    publisher = CharField(null=True)
    created = DateTimeField(default=datetime.datetime.now)
    modified = DateTimeField(default=datetime.datetime.now)
    creator = ForeignKeyField(User, backref='books', null=True)

def create_tables():
    tables = [User, Book]
    
    try:
        database.connect()
        database.create_tables(tables)
        log.info("✅ Таблицы успешно созданы")
        
        # Создаем тестового пользователя
        from account import hash_password
        user = User(
            email="admin@library.com",
            password=hash_password("admin123"),
            first_name="Администратор",
            last_name="Библиотеки",
            role="admin"
        )
        user.save()
        log.info("✅ Тестовый пользователь создан: admin@library.com / admin123")
        
        # Создаем тестовые книги
        sample_books = [
            {
                'title': 'Война и мир',
                'author': 'Лев Толстой',
                'description': 'Роман-эпопея, описывающий русское общество в эпоху войн против Наполеона.',
                'publication_year': 1869,
                'genre': 'Роман-эпопея',
                'publisher': 'Русский вестник'
            },
            {
                'title': 'Преступление и наказание',
                'author': 'Фёдор Достоевский', 
                'description': 'Психологический роман о бывшем студенте Родионе Раскольникове.',
                'publication_year': 1866,
                'genre': 'Психологический роман',
                'publisher': 'Русский вестник'
            }
        ]
        
        for book_data in sample_books:
            book = Book(**book_data, creator=user)
            book.save()
            log.info(f"✅ Добавлена книга: {book_data['title']}")
            
    except Exception as e:
        log.error(f"❌ Ошибка при создании таблиц: {e}")
    finally:
        if not database.is_closed():
            database.close()

if __name__ == '__main__':
    print("📚 ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ БИБЛИОТЕКИ")
    
    if os.path.exists(DATABASE):
        response = input("База данных уже существует. Пересоздать? (y/n): ")
        if response.lower() == 'y':
            database.drop_tables([User, Book])
            create_tables()
        else:
            print("Операция отменена.")
    else:
        create_tables()