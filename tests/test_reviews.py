import unittest
from flask import json
from flask_testing import TestCase
from flask_jwt_extended import create_access_token

from app import create_app, db
from app.models.user import User
from app.models.book import Book
from app.models.review import Review

class ReviewTestCase(TestCase):
    def create_app(self):
        # Configura a aplicação Flask para o ambiente de teste
        app = create_app('testing')
        return app

    def setUp(self):
        db.create_all()
        self.client = self.app.test_client()

        # Adiciona um usuário, um livro e uma resenha para teste
        hashed_password = 'password123'  # Evita a necessidade de gerar um hash para o teste
        user = User(email='test@example.com', password=hashed_password)
        book = Book(title='Test Book', description='Test Description', gender='Fiction', registered_by=user.email)
        db.session.add(user)
        db.session.add(book)
        db.session.commit()

        self.user_id = user.id
        self.book_title = book.title
        self.token = create_access_token(identity=self.user_id)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_review(self):
        """
        Testa o registro de uma nova resenha.
        
        Este teste verifica se uma nova resenha pode ser registrada corretamente.
        """
        response = self.client.post('/reviews', data=json.dumps({
            'rating': '5',
            'comment': 'Great book!',
            'book_title': self.book_title
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Review created successfully!', response.json['message'])

    def test_get_all_reviews(self):
        """
        Testa a obtenção de uma lista de todas as resenhas.
        
        Este teste verifica se todas as resenhas podem ser obtidas corretamente.
        """
        review = Review(rating='5', comment='Great book!', user_email='test@example.com', book_title=self.book_title)
        db.session.add(review)
        db.session.commit()

        response = self.client.get('/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['comment'], 'Great book!')

    def test_get_all_reviews_by_book(self):
        """
        Testa a obtenção de uma lista de todas as resenhas de um livro específico.
        
        Este teste verifica se todas as resenhas de um livro podem ser obtidas corretamente.
        """
        review = Review(rating='5', comment='Great book!', user_email='test@example.com', book_title=self.book_title)
        db.session.add(review)
        db.session.commit()

        response = self.client.get(f'/reviews/{self.book_title}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)
        self.assertEqual(response.json[0]['comment'], 'Great book!')

    def test_get_review(self):
        """
        Testa a obtenção de informações de uma resenha específica.
        
        Este teste verifica se as informações de uma resenha podem ser obtidas corretamente.
        """
        review = Review(rating='5', comment='Great book!', user_email='test@example.com', book_title=self.book_title)
        db.session.add(review)
        db.session.commit()

        response = self.client.get(f'/reviews/{review.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['comment'], 'Great book!')

    def test_edit_review(self):
        """
        Testa a edição das informações de uma resenha existente.
        
        Este teste verifica se as informações de uma resenha podem ser editadas corretamente.
        """
        review = Review(rating='5', comment='Great book!', user_email='test@example.com', book_title=self.book_title)
        db.session.add(review)
        db.session.commit()

        response = self.client.put(f'/reviews/{review.id}', data=json.dumps({
            'rating': '4',
            'comment': 'Good book!'
        }), headers={
            'Authorization': f'Bearer {self.token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Review edited successfully!', response.json['message'])

    def test_delete_review(self):
        """
        Testa a exclusão de uma resenha existente.
        
        Este teste verifica se uma resenha pode ser excluída corretamente.
        """
        review = Review(rating='5', comment='Great book!', user_email='test@example.com', book_title=self.book_title)
        db.session.add(review)
        db.session.commit()

        response = self.client.delete(f'/reviews/{review.id}', headers={
            'Authorization': f'Bearer {self.token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('Review deleted successfully!', response.json['message'])

    def test_average_rating_of_book(self):
        """
        Testa o cálculo da média das classificações de um livro específico.
        
        Este teste verifica se a média das classificações de um livro pode ser calculada corretamente.
        """
        review1 = Review(rating='5', comment='Great book!', user_email='test@example.com', book_title=self.book_title)
        review2 = Review(rating='4', comment='Good book!', user_email='test@example.com', book_title=self.book_title)
        db.session.add(review1)
        db.session.add(review2)
        db.session.commit()

        response = self.client.get(f'/reviews/avarage-rating/{self.book_title}')
    
    if __name__ == '__main__':
        unittest.main()