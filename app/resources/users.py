from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

from sql_alchemy import db
from blacklist import BLACKLIST
from ..models.user import User

users_blueprint = Blueprint('users_blueprint', __name__)

@users_blueprint.route('/register', methods=['POST'])
def register_user():
    """ 
    Registra um novo usuário.

    Este endpoint recebe dados JSON com o email e a senha do usuário, valida o email, verifica se o usuário já existe,
    gera um hash da senha e salva o novo usuário no banco de dados.
    
    Retorna: 
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado. 
    """
    data = request.get_json()
    email = data['email']
    hashed_password = generate_password_hash(data['password'])

    if not User.is_valid_email(email):
        return jsonify({"message" : "Email not valid!"}), 401
    if User.user_exists(email):
        return jsonify({"message" : "User already exists!"}), 401

    new_user = User(email=email, password=hashed_password)
    try:
        new_user.save_user()
    except:
        return jsonify({"message" : "An internal error occurred trying to save user!"}), 500

    return jsonify({"message" : "User created successfully!"}), 201

@users_blueprint.route('/users/<string:email>', methods=['PUT'])
@jwt_required()
def edit_user(email):
    """ 
    Edita um usuário.

    Este endpoint recebe o email pela URL, valida se existe um usuário com aquele email, 
    verifica se a requisição vem do usuário correto, se o novo email já pertence a outro usuário existente e se os dados foram passados.
    
    Retorna: 
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado. 
    """
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message" : "User not exists!"}), 404
    if user.id != current_user_id:
        return jsonify({"message" : "Access denied!"}), 401
    if 'email' not in data and 'password' not in data:
        return jsonify({"message" : "No data has been changed!"}), 401
    if 'email' in data:
        if User.user_exists(data['email']):
            return jsonify({"message" : "User already exists!"}), 401
        user.email = data['email']
    if 'password' in data:
        user.password = generate_password_hash(data['password'])
    
    try:
        user.save_user()
    except:
        return jsonify({"message" : "An internal error occurred trying to save user!"}), 500

    return jsonify({"message" : "User edited successfully!"}), 200

@users_blueprint.route('/users/<string:email>', methods=['DELETE'])
@jwt_required()
def delete_user(email):
    """ 
    Deleta um usuário.

    Este endpoint recebe o email pela URL, verifica se o usuário existe, 
    valida se a requisição vem do próprio usuário e, em caso positivo, deleta o usuário.
    
    Retorna: 
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado. 
    """
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"message" : "User not exists!"}), 404
    if user.id != current_user_id:
        return jsonify({"message" : "Access denied!"}), 401
    
    user.delete_user()
    BLACKLIST.add(get_jwt()['jti'])
    return jsonify({"message" : "User deleted successfully!"}), 200

@users_blueprint.route('/users/<string:email>', methods=['GET'])
@jwt_required()
def get_user(email):
    """ 
    Retorna informações do usuário.

    Este endpoint recebe o email pela URL, valida se o usuário existe e se a requisição vem do próprio usuário.
    
    Retorna: 
        Response: Uma resposta JSON com o email do usuário ou uma mensagem de erro e o código de status HTTP apropriado. 
    """
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"message" : "User not exists!"}), 404
    if user.id != current_user_id:
        return jsonify({"message" : "Access denied!"}), 401
    
    return jsonify({"id" : "{}".format(user.id),
                    "email" : "{}".format(user.email)}), 200

@users_blueprint.route('/login', methods=['POST'])
def login():
    """ 
    Realiza o login de um usuário existente.
    
    Este endpoint recebe dados JSON com o email e a senha do usuário, verifica as credenciais e retorna um token de acesso se as credenciais forem válidas.
    
    Retorna: 
        Response: Uma resposta JSON com um token de acesso ou uma mensagem de erro e o código de status HTTP apropriado. 
    """
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({"message" : "User does not exist!"}), 404
    if not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Invalid credentials"}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token" : access_token}), 200

@users_blueprint.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """ 
    Realiza o logout de um usuário.
    
    Este endpoint invalida o token JWT atual, adicionando-o à lista negra (BLACKLIST).
    
    Retorna: 
        Response: Uma resposta JSON com uma mensagem de sucesso. 
    """
    BLACKLIST.add(get_jwt()['jti'])
    return jsonify({"message" : "Successfully logged out!"}), 200