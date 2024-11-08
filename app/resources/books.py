from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.book import Book
from ..models.user import User

books_blueprint = Blueprint('books_blueprint', __name__)

@books_blueprint.route('/books', methods=['POST'])
@jwt_required()
def register_book():
    """
    Registra um novo livro.

    Este endpoint recebe dados JSON com as informações do livro (título, descrição, gênero)
    e o usuário atualmente autenticado. Verifica se o livro já existe e, se não, salva o novo livro no banco de dados.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    data = request.get_json()
    title = data['title']
    description = data['description']
    gender = data['gender']
    current_user = User.query.filter_by(id=get_jwt_identity()).first()

    if Book.book_exists(title):
        return jsonify({"message" : "Book already exists!"}), 409  # Conflict
    
    new_book = Book(title=title, description=description, gender=gender, registered_by=current_user.email)
    try:
        new_book.save_book()
    except:
        return jsonify({"message" : "An internal error occurred trying to save book!"}), 500  # Internal Server Error

    return jsonify({"message" : "Book created successfully!"}), 201  # Created


@books_blueprint.route('/books', methods=['GET'])
def get_all_books():
    """
    Retorna todos os livros cadastrados, incluindo todas as reviews relacionadas.

    Este endpoint não recebe parâmetros.
    
    Retorna:
        Response: Uma resposta JSON com a lista de todos os livros cadastrados e suas reviews associadas.
    """
    books = Book.query.all()
    all_books = [] 
    
    for book in books: 
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
        all_books.append(book_data) 
    
    return jsonify(all_books), 200  # OK


@books_blueprint.route('/books/<string:title>', methods=['GET'])
def get_book(title):
    """
    Retorna informações de um livro existente, incluindo todas as reviews relacionadas.

    Este endpoint recebe o título do livro pela URL,
    verifica se o livro existe e retorna suas informações junto com as reviews associadas.
    
    Retorna:
        Response: Uma resposta JSON com as informações do livro e suas reviews, ou uma mensagem de erro e o código de status HTTP apropriado.
    """
    book = Book.query.filter_by(title=title).first()

    if not book:
        return jsonify({"message" : "Book not exists!"}), 404  # Not Found
    
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

    return jsonify({
        "title" : book.title,
        "description" : book.description,
        "gender" : book.gender,
        "registered_by" : book.registered_by,
        "reviews": reviews
    }), 200  # OK


@books_blueprint.route('/books/<string:title>', methods=['PUT'])
@jwt_required()
def edit_book(title):
    """
    Edita um livro existente.

    Este endpoint recebe o título do livro pela URL e dados JSON contendo as alterações.
    Verifica se o livro existe, se o usuário atual é o proprietário do livro, e aplica as alterações.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    data = request.get_json()
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    book = Book.query.filter_by(title=title).first()

    if not book:
        return jsonify({"message" : "Book not exists!"}), 404  # Not Found
    if current_user.email != book.registered_by:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    if 'title' not in data and 'description' not in data and 'gender' not in data and 'registered_by' not in data:
        return jsonify({"message" : "No data has been changed!"}), 400  # Bad Request
    if 'title' in data:
        if Book.book_exists(data['title']):
            return jsonify({"message" : "Book already exists!"}), 409  # Conflict
        book.title = data['title']
    if 'description' in data:
        book.description = data['description']
    if 'gender' in data:
        book.gender = data['gender']
    if 'registered_by' in data:
        if not User.query.filter_by(email=data['registered_by']).first():
            return jsonify({"message" : "User not exists!"}), 404  # Not Found
        if book.registered_by != data['registered_by']:
            book.registered_by = data['registered_by']
    
    try:
        book.save_book()
    except:
        return jsonify({"message" : "An internal error occurred trying to save book!"}), 500  # Internal Server Error

    return jsonify({"message" : "Book edited successfully!"}), 200  # OK


@books_blueprint.route('/books/<string:title>', methods=['DELETE'])
@jwt_required()
def delete_book(title):
    """
    Deleta um livro existente.

    Este endpoint recebe o título do livro pela URL,
    verifica se o livro existe e se o usuário atual é o proprietário do livro, e deleta o livro.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    book = Book.query.filter_by(title=title).first()

    if not book:
        return jsonify({"message" : "Book not exists!"}), 404  # Not Found
    if current_user.email != book.registered_by:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    
    book.delete_book()
    return jsonify({"message" : "Book deleted successfully!"}), 200  # OK