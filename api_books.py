
from flask import request, jsonify
from playhouse.shortcuts import dict_to_model, update_model_from_dict
import db
import util
from webutil import app, login_required, get_myself
import logging

log = logging.getLogger("api.books")

@app.route('/api/books/', methods=['GET'])
def book_query():
    input = request.args
    page = int(input.get("page", 0))
    limit = int(input.get("limit", 20))
    search = input.get("search", "")
    genre = input.get("genre", "")
    
    booklist = db.query_books(page=page, limit=limit, search=search, genre=genre)
    return jsonify([book.serialize() for book in booklist]), 200

@app.route('/api/books/<id>', methods=['GET'])
def book_get(id):
    book = db.get_book(id)
    return jsonify(book.serialize()), 200

@app.route('/api/books/', methods=['POST'])
@login_required(role='editor')
def book_create():
    input = request.json
    input.pop("id", None)
    
    book = dict_to_model(db.Book, input)
    book.modified = book.created = util.utcnow()
    book.creator = get_myself()
    
    book.save()
    return jsonify(book.serialize()), 201

@app.route('/api/books/<id>', methods=['PUT'])
@login_required(role='editor')
def book_update(id):
    input = request.json
    input.pop("created", None)
    input.pop("creator", None)
    
    book = db.get_book(id)
    update_model_from_dict(book, input)
    book.modified = util.utcnow()
    book.save()
    
    return jsonify(book.serialize()), 200

@app.route('/api/books/<id>', methods=['DELETE'])
@login_required(role='editor')
def book_delete(id):
    book = db.get_book(id)
    book.delete_instance()
    return jsonify(book.serialize()), 200