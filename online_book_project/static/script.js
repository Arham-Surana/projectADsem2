// Global state
let books = [];
let selectedBookId = null;

// DOM Elements
const categoryFilter = document.getElementById('category-filter');
const searchInput = document.getElementById('search-input');
const searchBtn = document.getElementById('search-btn');
const newBtn = document.getElementById('new-btn');
const eraseBtn = document.getElementById('erase-btn');
const booksTbody = document.getElementById('books-tbody');
const addBookModal = document.getElementById('add-book-modal');
const deleteConfirmationModal = document.getElementById('delete-confirmation');
const addBookForm = document.getElementById('add-book-form');
const closeBtn = document.querySelector('.close-btn');
const confirmOk = document.getElementById('confirm-ok');

// Event Listeners
document.addEventListener('DOMContentLoaded', () => {
    loadBooks();
    setupEventListeners();
});

function setupEventListeners() {
    categoryFilter.addEventListener('change', loadBooks);
    searchBtn.addEventListener('click', searchBooks);
    searchInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') searchBooks();
    });
    newBtn.addEventListener('click', openAddBookModal);
    eraseBtn.addEventListener('click', handleErase);
    addBookForm.addEventListener('submit', handleAddBook);
    closeBtn.addEventListener('click', closeAddBookModal);
    confirmOk.addEventListener('click', closeDeleteModal);
    document.addEventListener('click', (e) => {
        if (e.target === addBookModal) closeAddBookModal();
        if (e.target === deleteConfirmationModal) closeDeleteModal();
    });
}

// Load books from server
async function loadBooks() {
    try {
        const category = categoryFilter.value;
        const url = category === 'All' 
            ? '/api/books' 
            : `/api/books?category=${encodeURIComponent(category)}`;
        
        const response = await fetch(url);
        books = await response.json();
        renderBooks();
        selectedBookId = null;
    } catch (error) {
        console.error('Error loading books:', error);
        alert('Error loading books');
    }
}

// Search books
async function searchBooks() {
    const searchTerm = searchInput.value.trim();
    
    if (!searchTerm) {
        loadBooks();
        return;
    }

    try {
        const response = await fetch('/api/books/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: searchTerm })
        });
        
        books = await response.json();
        renderBooks();
        selectedBookId = null;
    } catch (error) {
        console.error('Error searching books:', error);
        alert('Error searching books');
    }
}

// Render books in table
function renderBooks() {
    booksTbody.innerHTML = '';
    
    if (books.length === 0) {
        booksTbody.innerHTML = '<tr><td colspan="3" style="text-align: center; color: #999;">No books found</td></tr>';
        return;
    }

    books.forEach(book => {
        const row = document.createElement('tr');
        row.dataset.bookId = book.id;
        
        if (selectedBookId === book.id) {
            row.classList.add('selected');
        }

        row.innerHTML = `
            <td>${escapeHtml(book.name)}</td>
            <td>${escapeHtml(book.author)}</td>
            <td>${book.date}</td>
        `;

        row.addEventListener('click', () => selectBook(book.id));
        row.addEventListener('dblclick', () => deleteSelectedBook(book.id));
        
        booksTbody.appendChild(row);
    });
}

// Select book
function selectBook(bookId) {
    selectedBookId = selectedBookId === bookId ? null : bookId;
    renderBooks();
}

// Open add book modal
function openAddBookModal() {
    addBookForm.reset();
    addBookModal.style.display = 'flex';
}

// Close add book modal
function closeAddBookModal() {
    addBookModal.style.display = 'none';
}

// Close delete modal
function closeDeleteModal() {
    deleteConfirmationModal.style.display = 'none';
}

// Handle add book
async function handleAddBook(e) {
    e.preventDefault();

    const newBook = {
        name: document.getElementById('book-name').value.trim(),
        author: document.getElementById('book-author').value.trim(),
        date: document.getElementById('book-date').value.trim(),
        category: document.getElementById('book-category').value
    };

    if (!newBook.name || !newBook.author || !newBook.date || !newBook.category) {
        alert('Please fill all fields');
        return;
    }

    try {
        const response = await fetch('/api/books', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(newBook)
        });

        if (response.ok) {
            closeAddBookModal();
            loadBooks();
            searchInput.value = '';
        } else {
            alert('Error adding book');
        }
    } catch (error) {
        console.error('Error adding book:', error);
        alert('Error adding book');
    }
}

// Handle erase
function handleErase() {
    if (!selectedBookId) {
        deleteConfirmationModal.style.display = 'flex';
        return;
    }

    if (confirm('Are you sure you want to delete this book?')) {
        deleteSelectedBook(selectedBookId);
    }
}

// Delete selected book
async function deleteSelectedBook(bookId) {
    try {
        const response = await fetch(`/api/books/${bookId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            selectedBookId = null;
            loadBooks();
        } else {
            alert('Error deleting book');
        }
    } catch (error) {
        console.error('Error deleting book:', error);
        alert('Error deleting book');
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}
