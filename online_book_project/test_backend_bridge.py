from app import BackendBridge, load_books, save_books, DB_PATH
import json

# Backup and restore DB to avoid side effects
try:
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        orig = json.load(f)
except Exception:
    orig = None

b = BackendBridge()
print('Initial books:', len(b.get_books('All')))
new = b.add_book({'name': 'Test Book', 'author': 'Me', 'date': 2025, 'category': 'Novel'})
print('Added:', new)
print('Search result count:', len(b.search_books('Test Book')))
print('Delete result:', b.delete_book(new['id']))
print('After delete count:', len(b.get_books('All')))
print('Erase result:', b.erase_all())
print('After erase count:', len(b.get_books('All')))

# Restore DB
if orig is not None:
    save_books(orig)
else:
    save_books([])
print('DB restored')
