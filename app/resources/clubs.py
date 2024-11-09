from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.club import Club
from ..models.user import User
from ..models.book import Book

clubs_blueprint = Blueprint('clubs_blueprint', __name__)

@clubs_blueprint.route('/clubs', methods=['POST'])
@jwt_required()
def register_club():
    """
    Registra um novo clube.

    Este endpoint recebe dados JSON com o nome do clube e o ID do proprietário,
    verifica se o clube já existe, e salva o novo clube no banco de dados.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    data = request.get_json()
    name = data['name']
    owner_id = get_jwt_identity()

    if Club.club_exists(name):
        return jsonify({"message" : "Club already exists!"}), 409  # Conflict
    
    new_club = Club(name=name, owner_id=owner_id)
    try:
        new_club.save_club()
    except:
        return jsonify({"message" : "An internal error occurred trying to save club!"}), 500  # Internal Server Error

    return jsonify({"message" : "Club created successfully!"}), 201  # Created


@clubs_blueprint.route('/clubs', methods=['GET'])
def get_all_clubs():
    """
    Retorna uma lista de todos os clubes, incluindo informações detalhadas dos livros e reviews relacionados.

    Este endpoint não recebe parâmetros.

    Retorna:
        Response: Uma resposta JSON com a lista de todos os clubes e suas respectivas informações detalhadas.
    """
    clubs = Club.query.all()
    all_clubs = []

    for club in clubs:
        books = []
        for book in club.books:
            reviews = []
            for review in book.reviews:
                review_data = {
                    'id': review.id,
                    'rating': review.rating,
                    'comment': review.comment,
                    'user_email': review.user_email,
                    'created_at': review.created_at
                }
                reviews.append(review_data)
            
            book_data = {
                'id': book.id,
                'title': book.title,
                'description': book.description,
                'gender': book.gender,
                'registered_by': book.registered_by,
                'reviews': reviews
            } 
            books.append(book_data)
        
        club_data = {
            'id': club.id,
            'name': club.name,
            'owner_id': club.owner_id,
            'books': books
        }
        all_clubs.append(club_data)
    
    return jsonify(all_clubs), 200  # OK


@clubs_blueprint.route('/clubs/<string:name>', methods=['GET'])
def get_club(name):
    """
    Retorna informações de um clube existente, incluindo todos os livros relacionados.

    Este endpoint recebe o nome do clube pela URL,
    verifica se o clube existe e retorna suas informações juntamente com os livros relacionados.
    
    Retorna:
        Response: Uma resposta JSON com as informações do clube e seus livros, ou uma mensagem de erro e o código de status HTTP apropriado.
    """
    club = Club.query.filter_by(name=name).first()

    if not club:
        return jsonify({"message" : "Club not exists!"}), 404  # Not Found

    owner = User.query.filter_by(id=club.owner_id).first()

    books = []
    for book in club.books:
        book_data = {
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'gender': book.gender,
            'registered_by': book.registered_by
        }
        books.append(book_data)

    return jsonify({
        "name" : club.name,
        "owner" : owner.email,
        "books" : books
    }), 200  # OK


@clubs_blueprint.route('/clubs/<string:name>', methods=['PUT'])
@jwt_required()
def edit_club(name):
    """
    Edita um clube existente.

    Este endpoint recebe o nome do clube pela URL, e dados JSON contendo as alterações.
    Verifica se o clube existe, se o usuário atual é o proprietário, e aplica as alterações.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    data = request.get_json()
    current_user_id = get_jwt_identity()
    club = Club.query.filter_by(name=name).first()

    if not club:
        return jsonify({"message" : "Club not exists!"}), 404  # Not Found
    if current_user_id != club.owner_id:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    if 'name' not in data and 'owner_id' not in data:
        return jsonify({"message" : "No data has been changed!"}), 400  # Bad Request
    if 'name' in data:
        if Club.club_exists(data['name']):
            return jsonify({"message" : "Club already exists!"}), 409  # Conflict
        club.name = data['name']
    if 'owner_id' in data:
        if not User.query.filter_by(id=data['owner_id']).first():
            return jsonify({"message" : "User not exists!"}), 404  # Not Found
        if club.owner_id != data['owner_id']:
            club.owner_id = data['owner_id']
    
    try:
        club.save_club()
    except:
        return jsonify({"message" : "An internal error occurred trying to save club!"}), 500  # Internal Server Error

    return jsonify({"message" : "Club edited successfully!"}), 200  # OK


@clubs_blueprint.route('/clubs/<string:name>', methods=['DELETE'])
@jwt_required()
def delete_club(name):
    """
    Deleta um clube existente.

    Este endpoint recebe o nome do clube pela URL,
    verifica se o clube existe e se o usuário atual é o proprietário, e deleta o clube.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    current_user_id = get_jwt_identity()
    club = Club.query.filter_by(name=name).first()

    if not club:
        return jsonify({"message" : "Club not exists!"}), 404  # Not Found
    if current_user_id != club.owner_id:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    
    club.delete_club()
    return jsonify({"message" : "Club deleted successfully!"}), 200  # OK


@clubs_blueprint.route('/clubs/addbook/<string:name>/<string:title>', methods=['POST'])
@jwt_required()
def add_book(name, title):
    """
    Adiciona um livro a um clube existente.

    Este endpoint recebe o nome do clube e o título do livro pela URL,
    verifica se o clube e o livro existem, se o usuário autenticado é o proprietário do clube,
    e adiciona o livro ao clube.

    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    current_user_id = get_jwt_identity()
    club = Club.query.filter_by(name=name).first()
    book = Book.query.filter_by(title=title).first()

    if not club:
        return jsonify({"message" : "Club not exists!"}), 404  # Not Found
    if not book:
        return jsonify({"message" : "Book not exists!"}), 404  # Not Found
    if current_user_id != club.owner_id:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    for bk in club.books:
        if bk.title == title:
            return jsonify({"message" : "This book already exists in this club!"}), 409  # Conflict
    club.books.append(book)
    
    try:
        club.save_club()
    except:
        return jsonify({"message" : "An internal error occurred trying to save club!"}), 500  # Internal Server Error
    
    return jsonify({"message" : "Book added to club successfully!"}), 200  # OK


@clubs_blueprint.route('/clubs/average-books-read', methods=['GET'])
def average_number_of_books_read_by_clubs():
    """
    Calcula a média de livros lidos por clubes.

    Este endpoint não recebe parâmetros.

    Retorna:
        Response: Uma resposta JSON com a média de livros lidos por clubes.
    """
    clubs = Club.query.all()
    total_number_of_books = 0

    for club in clubs:
        total_number_of_books += len(club.books)
    
    if len(clubs) > 0:
        average_number_of_books_read_by_clubs = round(total_number_of_books / len(clubs), 2)
    else:
        average_number_of_books_read_by_clubs = 0

    return jsonify({"average number of books read by clubs": average_number_of_books_read_by_clubs}), 200  # OK