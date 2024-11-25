# backend/app.py
from flask import Flask, request, jsonify
from flask_cors import CORS 
import sqlite3
import os

app = Flask(__name__)
CORS(app, resources={
    r"/books*": {
        "origins": ["http://localhost:8080"],  # Especifica el origen exacto
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database and create books table if it doesn't exist"""
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

def get_book_by_id(book_id):
    """Retrieve a single book by its ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    conn.close()
    return book

@app.route('/books', methods=['GET', 'POST'])
def books():
    """Handle GET and POST requests for books"""
    if request.method == 'GET':
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM books')
        rows = cursor.fetchall()
        conn.close()
        
        # Convert Row objects to dictionaries
        books = [dict(book) for book in rows]
        return jsonify(books)

    if request.method == 'POST':
        data = request.json
        
        # Validate input
        if not all(key in data for key in ['title', 'author', 'publication_year']):
            return jsonify({'error': 'Missing required fields'}), 400
        
        title = data['title']
        author = data['author']
        publication_year = data['publication_year']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO books (title, author, publication_year) VALUES (?, ?, ?)", 
                (title, author, publication_year)
            )
            conn.commit()
            book_id = cursor.lastrowid
        except sqlite3.Error as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 500
        finally:
            conn.close()
        
        return jsonify({
            'message': 'Book added successfully', 
            'book_id': book_id
        }), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a specific book"""
    # First, check if the book exists
    existing_book = get_book_by_id(book_id)
    if not existing_book:
        return jsonify({'error': 'Book not found'}), 404

    data = request.get_json()
    
    # Validate input
    if not all(key in data for key in ['title', 'author', 'publication_year']):
        return jsonify({'error': 'Missing required fields'}), 400

    title = data['title']
    author = data['author']
    publication_year = data['publication_year']

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE books 
            SET title = ?, author = ?, publication_year = ?
            WHERE id = ?
        """, (title, author, publication_year, book_id))
        conn.commit()
        
        # Check if any row was actually updated
        if cursor.rowcount == 0:
            return jsonify({'error': 'Book could not be updated'}), 404
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': 'Book updated successfully'}), 200

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a specific book"""
    # First, check if the book exists
    existing_book = get_book_by_id(book_id)
    if not existing_book:
        return jsonify({'error': 'Book not found'}), 404

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
        conn.commit()
        
        # Check if any row was actually deleted
        if cursor.rowcount == 0:
            return jsonify({'error': 'Book could not be deleted'}), 404
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

    return jsonify({'message': f'Book with ID {book_id} deleted successfully'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001, debug=True)