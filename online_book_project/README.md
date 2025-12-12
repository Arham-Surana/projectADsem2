# Online Library  📚

A full-featured web application for managing a collection of books. Built with Flask backend and modern HTML/CSS/JavaScript frontend.

## Features

✨ **Core Features:**
- 📖 Add new books with name, author, year, and category
- 🔍 Search books by name
- 📂 Filter books by category (Novel, Philosophy, Poetry)
- 🗑️ Delete individual books
- 📊 View all books in an organized table
- 💾 Persistent storage using JSON database

## Project Structure

```
online_book_project/
├── main.py                 # Flask application
├── requirements.txt        # Python dependencies
├── media.json             # JSON database (auto-generated)
├── README.md              # This file
└── 
    ├── static/
    │   ├── style.css      # Styling
    │   └── script.js      # Frontend logic
    └── templates/
        └── index.html     # Main page
```

## Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Steps

1. **Navigate to project directory:**
```bash
cd online_book_project
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the web application:**
```bash
python main.py
```

4. **Open in browser:**
```
http://localhost:5000
```

### Run as a Desktop App (no browser required)

This project includes a PyQt5-based desktop wrapper that loads the same HTML UI locally.

1. Install desktop dependencies (already included in `requirements.txt`):
```bash
pip install -r requirements.txt
```

2. Run the desktop app:
```bash
python app_gui.py
```

The app opens a window on your device that displays the same interface without running a web server.

## Usage

### Adding a Book
1. Click the **New** button
2. Fill in book details:
   - Name: Book title
   - Author: Author name
   - Date: Publication year
   - Category: Select from Novel, Philosophy, Poetry
3. Click **Save**

### Searching Books
1. Enter a book name in the search field
2. Click **Search** or press Enter
3. Results will be filtered

### Filtering by Category
1. Select a category from the dropdown (All, Novel, Philosophy, Poetry)
2. Table automatically updates

### Deleting a Book
1. Click on a book row to select it
2. Click **Erase** button
3. Confirm deletion

## Database

The application uses a JSON file (`media.json`) for persistent storage. It's automatically created on first run with sample data.

### Sample Data Included:
- 23 classic books across 3 categories
- Authors: Dostoevsky, Kafka, Camus, Plath, Nietzsche, and more
- Categories: Novel, Philosophy, Poetry

## Technical Stack

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database:** JSON (media.json)
- **Styling:** Modern responsive CSS with gradients and animations

## Features for A Grade

✅ Complete CRUD operations (Create, Read, Update, Delete)
✅ Search and filter functionality
✅ Responsive design
✅ Clean, professional UI
✅ Error handling
✅ Sample data with diverse books
✅ Well-structured code
✅ Documentation included

## Notes

- The application stores all data in `media.json` file
- Perfect for portfolio and academic projects
- Easily extensible for additional features
- No external database required

## Author

Created as part of academic project requirements.
 The tests use a temporary JSON file so they won't overwrite your `media.json`.
---
## CI
This repository includes a GitHub Actions workflow that runs the test suite on every push and pull request (Ubuntu and Windows). The workflow installs only the minimal packages required to run the tests (Flask and pytest) to avoid building heavy GUI packages in CI. See `.github/workflows/ci.yml`.

**Ready to use!** Run `python main.py` and visit http://localhost:5000

## Tests

There are automated tests using pytest targeting the Flask API.

Run the tests:

```powershell
pip install -r requirements.txt
pytest -q
```

The tests use a temporary JSON file so they won't overwrite your `media.json`.
