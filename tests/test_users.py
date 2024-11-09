import unittest
from flask import json
from flask_testing import TestCase
from werkzeug.security import generate_password_hash

from app import create_app, db
from app.models.user import User
from blacklist import BLACKLIST

class UserTestCase(TestCase):
    def create_app(self):
        # Configura a aplicação Flask para o ambiente de teste
        app = create_app('testing')
        return app

    def setUp(self):
        # Configura o banco de dados e cria um cliente de teste
        db.create_all()
        self.client = self.app.test_client()

        # Adiciona um usuário para teste
        hashed_password = generate_password_hash('password123')
        user = User(email='test@example.com', password=hashed_password)
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        # Remove a sessão e destrói o banco de dados após cada teste
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        """
        Testa o registro de um novo usuário.
        
        Este teste verifica se um novo usuário pode ser registrado corretamente.
        """
        response = self.client.post('/register', data=json.dumps({
            'email': 'newuser@example.com',
            'password': 'password123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully!', response.json['message'])

    def test_get_user(self):
        """
        Testa a obtenção de informações de um usuário.
        
        Este teste verifica se um usuário pode obter suas informações com um token de acesso válido.
        """
        # Faz o login para obter um token JWT
        login_response = self.client.post('/login', data=json.dumps({
            'email': 'test@example.com',
            'password': 'password123'
        }), content_type='application/json')
        token = login_response.json['access_token']

        # Usa o token JWT para obter as informações do usuário
        response = self.client.get('/users/test@example.com', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['email'], 'test@example.com')

    def test_edit_user(self):
        """
        Testa a edição das informações de um usuário.
        
        Este teste verifica se um usuário pode editar suas informações com um token de acesso válido.
        """
        # Faz o login para obter um token JWT
        login_response = self.client.post('/login', data=json.dumps({
            'email': 'test@example.com',
            'password': 'password123'
        }), content_type='application/json')
        token = login_response.json['access_token']

        # Usa o token JWT para editar as informações do usuário
        response = self.client.put('/users/test@example.com', data=json.dumps({
            'email': 'updated@example.com'
        }), headers={
            'Authorization': f'Bearer {token}'
        }, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User edited successfully!', response.json['message'])

    def test_delete_user(self):
        """
        Testa a exclusão de um usuário.
        
        Este teste verifica se um usuário pode excluir sua conta com um token de acesso válido.
        """
        # Faz o login para obter um token JWT
        login_response = self.client.post('/login', data=json.dumps({
            'email': 'test@example.com',
            'password': 'password123'
        }), content_type='application/json')
        token = login_response.json['access_token']

        # Usa o token JWT para excluir o usuário
        response = self.client.delete('/users/test@example.com', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('User deleted successfully!', response.json['message'])

    def test_login(self):
        """
        Testa o login de um usuário existente.
        
        Este teste verifica se um usuário pode fazer login com credenciais válidas.
        """
        response = self.client.post('/login', data=json.dumps({
            'email': 'test@example.com',
            'password': 'password123'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)

    def test_logout(self):
        """
        Testa o logout de um usuário.
        
        Este teste verifica se um usuário pode fazer logout e invalidar o token JWT.
        """
        # Faz o login para obter um token JWT
        login_response = self.client.post

if __name__ == '__main__':
    unittest.main()