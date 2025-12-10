from flask import Flask, render_template, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

# Database file path
DB_PATH = 'media.json'

def load_books():
    """Load books from JSON file"""
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_books(books):
    """Save books to JSON file"""
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

def init_database():
    """Initialize database with sample books"""
    books = [
        {"id": 1, "name": "Madonna in a Fur Coat", "author": "Sabahattin Ali", "date": 1943, "category": "Novel"},
        {"id": 2, "name": "Notes from Underground", "author": "Fyodor Dostoevsky", "date": 1864, "category": "Novel"},
        {"id": 3, "name": "Crime and Punishment", "author": "Fyodor Dostoevsky", "date": 1866, "category": "Novel"},
        {"id": 4, "name": "White Nights", "author": "Fyodor Dostoevsky", "date": 1848, "category": "Novel"},
        {"id": 5, "name": "Letters to Milena", "author": "Franz Kafka", "date": 1952, "category": "Novel"},
        {"id": 6, "name": "The Metamorphosis", "author": "Franz Kafka", "date": 1915, "category": "Novel"},
        {"id": 7, "name": "The First Man", "author": "Albert Camus", "date": 1994, "category": "Novel"},
        {"id": 8, "name": "The Stranger", "author": "Albert Camus", "date": 1942, "category": "Novel"},
        {"id": 9, "name": "The Idiot", "author": "Fyodor Dostoevsky", "date": 1869, "category": "Novel"},
        {"id": 10, "name": "No Longer Human", "author": "Osamu Dazai", "date": 1948, "category": "Novel"},
        {"id": 11, "name": "Kokoro", "author": "Natsume Sōseki", "date": 1914, "category": "Novel"},
        {"id": 12, "name": "I Am a Cat", "author": "Natsume Sōseki", "date": 1906, "category": "Novel"},
        {"id": 13, "name": "Pachinko", "author": "Min Jin Lee", "date": 2017, "category": "Novel"},
        {"id": 14, "name": "I Have the Right to Destroy Myself", "author": "Kim Young-ha", "date": 1996, "category": "Novel"},
        {"id": 15, "name": "Ali and Nino", "author": "Kurban Said", "date": 1937, "category": "Novel"},
        {"id": 16, "name": "The Devil", "author": "Huseyn Javid", "date": 1924, "category": "Novel"},
        {"id": 17, "name": "The Bell Jar", "author": "Sylvia Plath", "date": 1963, "category": "Novel"},
        {"id": 18, "name": "Orlando: A Biography", "author": "Virginia Woolf", "date": 1928, "category": "Novel"},
        {"id": 19, "name": "On Truth and Lies in a Nonmoral Sense", "author": "Friedrich Nietzsche", "date": 1896, "category": "Philosophy"},
        {"id": 20, "name": "Beyond Good and Evil: Prelude to a Philosophy of the Future", "author": "Friedrich Nietzsche", "date": 1886, "category": "Philosophy"},
        {"id": 21, "name": "A Room of One's Own", "author": "Virginia Woolf", "date": 1929, "category": "Philosophy"},
        {"id": 22, "name": "Milk and honey", "author": "Rupi Kaur", "date": 2014, "category": "Poetry"},
        {"id": 23, "name": "Tulips", "author": "Sylvia Plath", "date": 1965, "category": "Poetry"},
    ]
    save_books(books)

@app.route('/')
def index():
    """Home page - display all books"""
    books = load_books()
    categories = sorted(set([book['category'] for book in books]))
    return render_template('index.html', books=books, categories=categories)

@app.route('/api/books', methods=['GET'])
def get_books():
    """API endpoint to get all books"""
    category = request.args.get('category', 'All')
    books = load_books()
    
    if category != 'All':
        books = [book for book in books if book['category'] == category]
    
    return jsonify(books)

@app.route('/api/books/search', methods=['POST'])
def search_books():
    """API endpoint to search books by name"""
    data = request.json
    search_term = data.get('name', '').lower()
    books = load_books()
    
    results = [book for book in books if search_term in book['name'].lower()]
    return jsonify(results)

@app.route('/api/books', methods=['POST'])
def add_book():
    """API endpoint to add a new book"""
    data = request.json
    books = load_books()
    
    # Generate new ID
    new_id = max([book['id'] for book in books], default=0) + 1
    
    new_book = {
        'id': new_id,
        'name': data.get('name'),
        'author': data.get('author'),
        'date': int(data.get('date', 0)),
        'category': data.get('category', 'Novel')
    }
    
    books.append(new_book)
    save_books(books)
    
    return jsonify({'success': True, 'book': new_book}), 201

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """API endpoint to delete a book"""
    books = load_books()
    books = [book for book in books if book['id'] != book_id]
    save_books(books)
    
    return jsonify({'success': True}), 200

@app.route('/api/books/erase', methods=['POST'])
def erase_all():
    """API endpoint to erase all books"""
    save_books([])
    return jsonify({'success': True}), 200

def show_summary(event):
    """Save summary back to JSON"""
    # This function is called to save summary data
    pass

def save_summary():
    """Save summary of current books"""
    books = load_books()
    summary = {
        'total_books': len(books),
        'categories': {},
        'timestamp': datetime.now().isoformat()
    }
    
    for book in books:
        category = book['category']
        if category not in summary['categories']:
            summary['categories'][category] = 0
        summary['categories'][category] += 1
    
    return summary

if __name__ == '__main__':
    # Initialize database with sample data if it doesn't exist
    if not os.path.exists(DB_PATH):
        init_database()
    
    app.run(debug=True, host='localhost', port=5000)
