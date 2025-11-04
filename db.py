import uuid
from peewee import *
from playhouse.shortcuts import model_to_dict
from flask import abort
import config1
import logging

log = logging.getLogger("db")

if config1.IS_SQLITE:
    database = SqliteDatabase(config1.DATABASE_HOST, pragmas={})
else:
    from playhouse.postgres_ext import PostgresqlExtDatabase, ArrayField
    import psycopg2.extras
    psycopg2.extras.register_uuid()
    
    database = PostgresqlExtDatabase(config1.DATABASE_NAME,
        user=config1.DATABASE_USER, password=config1.DATABASE_PASSWORD,
        host=config1.DATABASE_HOST, port=config1.DATABASE_PORT)

class BaseModel(Model):
    EXCLUDE_FIELDS = []

    def serialize(self):
        d = model_to_dict(self, recurse=False, exclude=self.EXCLUDE_FIELDS)
        d["id"] = str(d["id"])
        return d

    class Meta:
        database = database

def get_object_or_404(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        log.warning("NO OBJECT {} {}".format(model, kwargs))
        abort(404)

def get_object_or_none(model, **kwargs):
    try:
        return model.get(**kwargs)
    except model.DoesNotExist:
        return None

class User(BaseModel):
    if not config1.IS_SQLITE:
        id = UUIDField(primary_key=True, default=uuid.uuid4)
    else:
        id = AutoField()
    
    email = TextField()
    password = TextField()
    first_name = TextField()
    last_name = TextField()
    role = TextField()
    
    if not config1.IS_SQLITE:
        tags = ArrayField(TextField)
    else:
        tags = TextField()

    created = DateTimeField()
    modified = DateTimeField()

    EXCLUDE_FIELDS = [password]

    def is_superuser(self):
        return self.role == "superuser"

    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name or '')

    def serialize(self):
        d = super(User, self).serialize()
        d["fullname"] = self.full_name()
        d["tags"] = self.tags or []
        return d

    def __str__(self):
        return "<User {}, {}, role={}>".format(self.id, self.email, self.role)

    class Meta:
        db_table = 'users'

def get_user(uid):
    return get_object_or_404(User, id=uid)

def get_user_by_email(email):
    if not email:
        return None
    try:
        if config1.IS_SQLITE:
            sql = "SELECT * FROM users where email = ? LIMIT 1"
            args = (email.lower(),)
        else:
            sql = "SELECT * FROM users where LOWER(email) = LOWER(%s) LIMIT 1"
            args = (email,)
        return list(User.raw(sql, args))[0]
    except IndexError:
        return None

def query_users(page=0, limit=1000, search=None):
    page = int(page or 0)
    limit = int(limit or 1000)

    q = User.select()
    if search:
        search = "%"+search+"%"
        q = q.where(User.first_name ** search | User.last_name ** search |
                User.email ** search)
    q = q.paginate(page, limit).order_by(User.id.desc())
    return q

class Book(BaseModel):
    if not config1.IS_SQLITE:
        id = UUIDField(primary_key=True, default=uuid.uuid4)
    else:
        id = AutoField()
        
    title = TextField()
    author = TextField()
    description = TextField(null=True)
    cover_image = TextField(null=True)
    content_file = TextField(null=True)
    publication_year = IntegerField(null=True)
    isbn = TextField(null=True)
    genre = TextField(null=True)
    publisher = TextField(null=True)
    
    created = DateTimeField()
    modified = DateTimeField()
    creator = ForeignKeyField(User, null=True)

    class Meta:
        db_table = 'books'

def get_book(id):
    return get_object_or_404(Book, id=id)

def query_books(page=0, limit=20, search='', genre=None):
    page = int(page or 0)
    limit = int(limit or 20)
    
    q = Book.select()
    if search:
        search = f"%{search}%"
        q = q.where(Book.title ** search | Book.author ** search)
    if genre:
        q = q.where(Book.genre == genre)
    return q.paginate(page, limit).order_by(Book.id.desc())