import json
import os
import tempfile
import pytest
from main import app, save_books

@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary JSON file for tests
    tmp_db = tmp_path / "test_media.json"
    tmp_db.write_text('[]', encoding='utf-8')

    # Monkeypatch DB_PATH in main module
    monkeypatch.setenv('TEST_DB_PATH', str(tmp_db))

    # In main.py DB_PATH is a module-level variable; set it directly
    import importlib
    m = importlib.import_module('main')
    m.DB_PATH = str(tmp_db)

    with m.app.test_client() as client:
        yield client


def test_get_books_empty(client):
    # Initially empty
    resp = client.get('/api/books')
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, list)
    assert data == []


def test_add_and_delete_book(client):
    # Add a book
    new_book = {"name": "Test Book", "author": "Tester", "date": 2025, "category": "Novel"}
    resp = client.post('/api/books', json=new_book)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body['success'] is True
    book = body['book']
    assert book['name'] == new_book['name']

    # Confirm it appears in GET
    resp = client.get('/api/books')
    data = resp.get_json()
    assert any(b['id'] == book['id'] for b in data)

    # Delete it
    resp = client.delete(f"/api/books/{book['id']}")
    assert resp.status_code == 200
    resp = client.get('/api/books')
    data = resp.get_json()
    assert all(b['id'] != book['id'] for b in data)


def test_search_books(client):
    # Add a known book
    new_book = {"name": "UniqueSearchTitle", "author": "SearchAuthor", "date": 2020, "category": "Poetry"}
    resp = client.post('/api/books', json=new_book)
    assert resp.status_code == 201

    # Search for it
    resp = client.post('/api/books/search', json={"name": "UniqueSearchTitle"})
    assert resp.status_code == 200
    results = resp.get_json()
    assert len(results) >= 1
    assert any('UniqueSearchTitle' in b['name'] for b in results)
