import unittest
from flask import json
from flask_testing import TestCase
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.user import User
from app.models.book import Book

class BookTestCase(TestCase):
    def create_app(self):
        # Configura a aplicação Flask para o ambiente de teste
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

        # Adiciona um usuário e um livro para teste
        hashed_password = 'password123'  # Evita a necessidade de gerar um hash para o teste
        user = User(email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.token = create_access_token(identity=self.user_id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_book(self):
        """
        Testa o registro de um novo livro.
        
        Este teste verifica se um novo livro pode ser registrado corretamente.
        """
        response = self.client.post('/books', data=json.dumps({
            'title': 'New Book',
            'description': 'Description of new book',
            'gender': 'Fiction'
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Book created successfully!', response.json['message'])

    def test_get_all_books(self):
        """
        Testa a obtenção de uma lista de todos os livros.
        
        Este teste verifica se todos os livros podem ser obtidos corretamente.
        """
        book = Book(title='New Book', description='Description of new book', gender='Fiction', registered_by='test@example.com')
        db.session.add(book)
        db.session.commit()

        response = self.client.get('/books')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['title'], 'New Book')

    def test_get_book(self):
        """
        Testa a obtenção de informações de um livro específico.
        
        Este teste verifica se as informações de um livro podem ser obtidas corretamente.
        """
        book = Book(title='New Book', description='Description of new book', gender='Fiction', registered_by='test@example.com')
        db.session.add(book)
        db.session.commit()

        response = self.client.get('/books/New Book')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'New Book')

    def test_edit_book(self):
        """
        Testa a edição das informações de um livro existente.
        
        Este teste verifica se as informações de um livro podem ser editadas corretamente.
        """
        book = Book(title='New Book', description='Description of new book', gender='Fiction', registered_by='test@example.com')
        db.session.add(book)
        db.session.commit()

        response = self.client.put('/books/New Book', data=json.dumps({
            'title': 'Updated Book',
            'description': 'Updated description of book',
            'gender': 'Non-Fiction'
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book edited successfully!', response.json['message'])

    def test_delete_book(self):
        """
        Testa a exclusão de um livro existente.
        
        Este teste verifica se um livro pode ser excluído corretamente.
        """
        book = Book(title='New Book', description='Description of new book', gender='Fiction', registered_by='test@example.com')
        db.session.add(book)
        db.session.commit()

        response = self.client.delete('/books/New Book', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book deleted successfully!', response.json['message'])

if __name__ == '__main__':
    unittest.main()