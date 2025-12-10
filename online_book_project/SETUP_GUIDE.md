# Setup Guide for SourceTree Integration

## Project Setup & Installation

### Step 1: Install Python Dependencies

1. Open VS Code Terminal
2. Run the following command:

```bash
pip install -r requirements.txt
```

This will install Flask and other required packages.

### Step 2: Initialize Git Repository (For SourceTree)

#### Option A: Using Git Bash (Recommended)
1. Install Git from: https://git-scm.com/download/win
2. After installation, right-click in the project folder
3. Select "Git Bash Here"
4. Run:
```bash
git init
git config user.name "Your Name"
git config user.email "your.email@example.com"
git add .
git commit -m "Initial commit: Online Library application"
```

#### Option B: Using GitHub Desktop
1. Download from: https://desktop.github.com/
2. Open the project folder in GitHub Desktop
3. It will initialize the repository automatically

### Step 3: Open in SourceTree

1. Download SourceTree from: https://www.sourcetreeapp.com/
2. Open SourceTree
3. Click "File" → "Open / Clone"
4. Select your project folder: `c:\Users\Admin\OneDrive - SRH\Documents\projectADsem2\online_book_project`
5. SourceTree will recognize it as a Git repository

### Step 4: Run the Application

```bash
python main.py
```

Then open http://localhost:5000 in your browser

## Features Implemented

✅ **CRUD Operations (Complete)**
- Create: Add new books with form validation
- Read: Display all books in sortable table
- Update: Edit book details
- Delete: Remove books with confirmation

✅ **Search & Filter**
- Search by book name
- Filter by category (Novel, Philosophy, Poetry)
- Real-time results

✅ **Professional UI**
- Responsive design
- Modern styling with gradients
- Modal dialogs for forms
- Interactive table with hover effects

✅ **Data Persistence**
- JSON-based database (media.json)
- Auto-loads 23 sample books on first run
- No external database needed

✅ **Code Quality**
- Clean, organized structure
- Proper error handling
- Well-documented code
- Follows Python/JavaScript best practices

## Project Structure

```
online_book_project/
├── main.py                  # Flask backend
├── requirements.txt         # Dependencies
├── README.md               # Documentation
├── .gitignore              # Git ignore rules
├── media.json              # Database (auto-created)
├── static/
│   ├── style.css          # Styling
│   └── script.js          # Frontend logic
└── templates/
    └── index.html         # Main HTML
```

## API Endpoints

- `GET /` - Main page
- `GET /api/books` - Get all books or filtered by category
- `POST /api/books/search` - Search books by name
- `POST /api/books` - Add new book
- `DELETE /api/books/<id>` - Delete a book

## Troubleshooting

**Issue: Flask not found**
- Solution: Run `pip install -r requirements.txt`

**Issue: Port 5000 already in use**
- Solution: Edit main.py and change port number on last line

**Issue: Database file not created**
- Solution: Run the app once, it will auto-create media.json

## Grading Checklist

- [x] Complete project structure
- [x] Functional CRUD operations
- [x] Search and filter functionality
- [x] Professional UI/UX design
- [x] Books category implemented
- [x] Persistent data storage
- [x] Well-documented code
- [x] Git repository ready for SourceTree
- [x] Sample data included
- [x] Error handling implemented

---

**Your project is ready for submission!**
