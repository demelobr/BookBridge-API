import unittest
from flask import json
from flask_testing import TestCase
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.user import User
from app.models.club import Club
from app.models.book import Book

class ClubTestCase(TestCase):
    def create_app(self):
        # Configura a aplicação Flask para o ambiente de teste
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

        # Adiciona um usuário e um clube para teste
        hashed_password = 'password123'  # Evita a necessidade de gerar um hash para o teste
        user = User(email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.token = create_access_token(identity=self.user_id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_club(self):
        """
        Testa o registro de um novo clube.
        
        Este teste verifica se um novo clube pode ser registrado corretamente.
        """
        response = self.client.post('/clubs', data=json.dumps({
            'name': 'Book Club'
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Club created successfully!', response.json['message'])

    def test_get_all_clubs(self):
        """
        Testa a obtenção de uma lista de todos os clubes.
        
        Este teste verifica se todos os clubes podem ser obtidos corretamente.
        """
        club = Club(name='Book Club', owner_id=self.user_id)
        db.session.add(club)
        db.session.commit()

        response = self.client.get('/clubs')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['name'], 'Book Club')

    def test_get_club(self):
        """
        Testa a obtenção de informações de um clube específico.
        
        Este teste verifica se as informações de um clube podem ser obtidas corretamente.
        """
        club = Club(name='Book Club', owner_id=self.user_id)
        db.session.add(club)
        db.session.commit()

        response = self.client.get('/clubs/Book Club')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Book Club')

    def test_edit_club(self):
        """
        Testa a edição das informações de um clube existente.
        
        Este teste verifica se as informações de um clube podem ser editadas corretamente.
        """
        club = Club(name='Book Club', owner_id=self.user_id)
        db.session.add(club)
        db.session.commit()

        response = self.client.put('/clubs/Book Club', data=json.dumps({
            'name': 'Updated Book Club'
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Club edited successfully!', response.json['message'])

    def test_delete_club(self):
        """
        Testa a exclusão de um clube existente.
        
        Este teste verifica se um clube pode ser excluído corretamente.
        """
        club = Club(name='Book Club', owner_id=self.user_id)
        db.session.add(club)
        db.session.commit()

        response = self.client.delete('/clubs/Book Club', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Club deleted successfully!', response.json['message'])

    def test_add_book_to_club(self):
        """
        Testa a adição de um livro a um clube existente.
        
        Este teste verifica se um livro pode ser adicionado a um clube corretamente.
        """
        club = Club(name='Book Club', owner_id=self.user_id)
        book = Book(title='Book Title', description='Book Description', gender='Fiction', registered_by='test@example.com')
        db.session.add(club)
        db.session.add(book)
        db.session.commit()

        response = self.client.post('/clubs/addbook/Book Club/Book Title', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Book added to club successfully!', response.json['message'])

    def test_average_books_read_by_clubs(self):
        """
        Testa o cálculo da média de livros lidos por clubes.
        
        Este teste verifica se a média de livros lidos por clubes pode ser calculada corretamente.
        """
        club1 = Club(name='Book Club 1', owner_id=self.user_id)
        club2 = Club(name='Book Club 2', owner_id=self.user_id)
        book1 = Book(title='Book Title 1', description='Book Description', gender='Fiction', registered_by='test@example.com')
        book2 = Book(title='Book Title 2', description='Book Description', gender='Fiction', registered_by='test@example.com')
        club1.books.append(book1)
        club2.books.append(book2)
        db.session.add(club1)
        db.session.add(club2)
        db.session.commit()

        response = self.client.get('/clubs/average-books-read')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['average number of books read by clubs'], 1.0)

if __name__ == '__main__':
    unittest.main()