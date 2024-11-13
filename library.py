from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# Database Exist?
def init_db():
    if not os.path.exists('library.db'):
        conn = sqlite3.connect('library.db')
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                publication_year INTEGER NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

class Book:
    def __init__(self, id, title, author, publication_year):
        self.id = id
        self.title = title
        self.author = author
        self.publication_year = publication_year

    def __str__(self):
        return f"{self.title} by {self.author} ({self.publication_year})"

@app.route('/')
def index():
    try:
        books = get_all_books()
        return render_template('index.html', books=books)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

@app.route('/manage', methods=['GET', 'POST'])
def manage_books():
    try:
        if request.method == 'POST':
            action = request.form['action']
            if action == 'add':
                title = request.form['title']
                author = request.form['author']
                publication_year = request.form['publication_year']
                add_new_book(title, author, publication_year)
            elif action == 'update':
                book_id = int(request.form['book_id'])
                book = get_book_by_id(book_id)
                if book:
                    book.title = request.form['title']
                    book.author = request.form['author']
                    book.publication_year = request.form['publication_year']
                    update_book_in_db(book)
            elif action == 'delete':
                book_id = int(request.form['book_id'])
                delete_book_from_db(book_id)
            return redirect(url_for('manage_books'))

        books = get_all_books()
        return render_template('manage.html', books=books)
    except Exception as e:
        return f"An error occurred: {str(e)}", 500

def get_all_books():
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    books = [Book(row[0], row[1], row[2], row[3]) for row in rows]
    print (books)
    conn.close()
    return books

def add_new_book(title, author, publication_year):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)", 
                  (title, author, publication_year))
    conn.commit()
    conn.close()

def get_book_by_id(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    row = cursor.fetchone()
    book = Book(row[0], row[1], row[2], row[3]) if row else None
    conn.close()
    return book

def update_book_in_db(book):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE books SET title = ?, author = ?, publication_year = ? WHERE id = ?", 
                  (book.title, book.author, book.publication_year, book.id))
    conn.commit()
    conn.close()

def delete_book_from_db(book_id):
    conn = sqlite3.connect('library.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()  # Initialize database
    app.run(host='0.0.0.0', port=5001, debug=True)
    print (Book)
