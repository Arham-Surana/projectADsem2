import sys
import os
import json
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
from PyQt5.QtWebChannel import QWebChannel
from PyQt5.QtCore import QUrl

DB_PATH = os.path.join(os.path.dirname(__file__), 'media.json')
BASE_DIR = os.path.dirname(__file__)


def load_books():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def save_books(books):
    with open(DB_PATH, 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)


def init_database():
    if os.path.exists(DB_PATH):
        return
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


class BackendBridge(QtCore.QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.pyqtSlot(str, result='QVariant')
    def get_books(self, category='All'):
        books = load_books()
        if category and category != 'All':
            books = [b for b in books if b.get('category') == category]
        return books

    @QtCore.pyqtSlot(str, result='QVariant')
    def search_books(self, name=''):
        term = (name or '').lower()
        books = load_books()
        results = [b for b in books if term in (b.get('name') or '').lower()]
        return results

    @QtCore.pyqtSlot('QVariant', result='QVariant')
    def add_book(self, book):
        books = load_books()
        new_id = max([b.get('id', 0) for b in books], default=0) + 1
        new_book = {
            'id': new_id,
            'name': book.get('name'),
            'author': book.get('author'),
            'date': int(book.get('date') or 0),
            'category': book.get('category') or 'Novel'
        }
        books.append(new_book)
        save_books(books)
        return new_book

    @QtCore.pyqtSlot(int, result=bool)
    def delete_book(self, book_id):
        books = load_books()
        books = [b for b in books if b.get('id') != book_id]
        save_books(books)
        return True

    @QtCore.pyqtSlot(result=bool)
    def erase_all(self):
        save_books([])
        return True



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Online Library — Arham')
        self.resize(1000, 700)

        central = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(central)
        self.setCentralWidget(central)

        self.view = QtWebEngineWidgets.QWebEngineView()
        layout.addWidget(self.view)

        # Initialize data file if missing
        init_database()

        # Create and register web channel
        self.channel = QWebChannel()
        self.backend = BackendBridge()
        self.channel.registerObject('backend', self.backend)

        # Set channel on the page
        self.view.page().setWebChannel(self.channel)

        # Load the HTML file and inject absolute paths for CSS and JS
        index_path = os.path.join(BASE_DIR, 'templates', 'index.html')
        css_path = os.path.join(BASE_DIR, 'static', 'style.css').replace('\\', '/')
        js_path = os.path.join(BASE_DIR, 'static', 'script.js').replace('\\', '/')
        
        # Read HTML and replace placeholders
        with open(index_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        html_content = html_content.replace('file:///PLACEHOLDER_CSS_PATH', f'file:///{css_path}')
        html_content = html_content.replace('file:///PLACEHOLDER_JS_PATH', f'file:///{js_path}')
        
        # Load the modified HTML
        self.view.setHtml(html_content, QUrl.fromLocalFile(index_path))




def main():
    app = QtWidgets.QApplication(sys.argv)

    # Ensure Qt WebEngine is initialized
    QtWebEngineWidgets.QWebEngineSettings.globalSettings()

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
