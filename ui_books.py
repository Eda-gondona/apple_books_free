
from flask import render_template
from webutil import app
import db

@app.route('/book/<book_id>')
def book_detail(book_id):
    book = db.get_book(book_id)
    return render_template('book_detail.html', book=book)

@app.route('/read/<book_id>')
def read_book_content(book_id):
    book = db.get_book(book_id)
    return render_template('book_reader.html', book=book)