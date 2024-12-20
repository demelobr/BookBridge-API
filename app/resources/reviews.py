from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..models.review import Review
from ..models.book import Book
from ..models.user import User

review_blueprint = Blueprint('review_blueprint', __name__)

@review_blueprint.route('/reviews', methods=['POST'])
@jwt_required()
def register_review():
    """
    Registra uma nova resenha.

    Este endpoint recebe dados JSON com as informações da resenha (classificação, comentário, título do livro)
    e o usuário atualmente autenticado. Verifica se o livro existe e se a classificação está no intervalo permitido,
    salvando a nova resenha no banco de dados.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    data = request.get_json()
    current_user = User.query.filter_by(id=get_jwt_identity()).first()

    if 'rating' in data and 'comment' in data and 'book_title' in data:
        if not Book.book_exists(data['book_title']):
            return jsonify({"message" : "Book not exists!"}), 404  # Not Found
        if not data['rating'].isdigit() or int(data['rating']) < 0 or int(data['rating']) > 5:
            return jsonify({"message" : "The review value must be from 0 to 5!"}), 400  # Bad Request

        book = Book.query.filter_by(title=data['book_title']).first()
        new_review = Review(rating=data['rating'], comment=data['comment'], user_email=current_user.email, book_title=book.title)
        try:
            new_review.save_review()
        except:
            return jsonify({"message" : "An internal error occurred trying to save review!"}), 500  # Internal Server Error

        return jsonify({"message" : "Review created successfully!"}), 201  # Created

    return jsonify({"message" : "Information is missing to make a review!"}), 400  # Bad Request


@review_blueprint.route('/reviews/', methods=['GET'])
def get_all_reviews():
    """
    Retorna uma lista de todas as resenhas.

    Este endpoint não recebe parâmetros.

    Retorna:
        Response: Uma resposta JSON com a lista de todas as resenhas.
    """
    reviews = Review.query.all()
    all_reviews = []

    for review in reviews:
        review_data = {
            'id': review.id,
            'book_title': review.book_title,
            'rating': review.rating,
            'comment': review.comment,
            'user_email': review.user_email,
            'created_at': review.created_at
        }
        all_reviews.append(review_data)
    
    return jsonify(all_reviews), 200  # OK


@review_blueprint.route('/reviews/<string:title>', methods=['GET'])
def get_all_reviews_by_book(title):
    """
    Retorna uma lista de todas as resenhas de um livro específico.

    Este endpoint recebe o título do livro pela URL.

    Parâmetros:
        title (str): O título do livro cujas resenhas serão retornadas.

    Retorna:
        Response: Uma resposta JSON com a lista de todas as resenhas do livro especificado.
    """
    reviews = Review.query.all()
    all_reviews = []

    for review in reviews:
        if review.book_title == title:
            review_data = {
                'id': review.id,
                'book_title': review.book_title,
                'rating': review.rating,
                'comment': review.comment,
                'user_email': review.user_email,
                'created_at': review.created_at
            }
            all_reviews.append(review_data)
    
    return jsonify(all_reviews), 200  # OK


@review_blueprint.route('/reviews/<int:id>', methods=['GET'])
def get_review(id):
    """
    Retorna informações de uma resenha existente.

    Este endpoint recebe o ID da resenha pela URL,
    verifica se a resenha existe e retorna suas informações.
    
    Retorna:
        Response: Uma resposta JSON com as informações da resenha ou uma mensagem de erro e o código de status HTTP apropriado.
    """
    review = Review.query.filter_by(id=id).first()

    if not review:
        return jsonify({"message" : "Review not exists!"}), 404  # Not Found
    
    return jsonify({"id" : "{}".format(review.id),
                    "book_title": "{}".format(review.book_title),
                    "rating" : "{}".format(review.rating),
                    "comment" : "{}".format(review.comment),
                    "user_email" : "{}".format(review.user_email),
                    "book_title" : "{}".format(review.book_title),
                    "created_at" : "{}".format(review.created_at)}), 200  # OK


@review_blueprint.route('/reviews/<int:id>', methods=['PUT'])
@jwt_required()
def edit_review(id):
    """
    Edita uma resenha existente.

    Este endpoint recebe o ID da resenha pela URL e dados JSON contendo as alterações.
    Verifica se a resenha existe, se o usuário atual é o autor da resenha, e aplica as alterações.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    data = request.get_json()
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    review = Review.query.filter_by(id=id).first()

    if not review:
        return jsonify({"message" : "Review not exists!"}), 404  # Not Found
    if current_user.email != review.user_email:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    if 'rating' not in data and 'comment' not in data and 'user_email' not in data and 'book_title' not in data:
        return jsonify({"message" : "No data has been changed!"}), 400  # Bad Request
    if 'rating' in data:
        if not data['rating'].isdigit() or int(data['rating']) < 0 or int(data['rating']) > 5:
            return jsonify({"message" : "The review value must be from 0 to 5!"}), 400  # Bad Request
        review.rating = data['rating']
    if 'comment' in data and review.comment != data['comment']:
        review.comment = data['comment']
    if 'book_title' in data:
        if not Book.book_exists(data['book_title']):
            return jsonify({"message" : "Book not exists!"}), 404  # Not Found
        review.book_title = data['book_title']
    
    try:
        review.save_review()
    except:
        return jsonify({"message" : "An internal error occurred trying to save review!"}), 500  # Internal Server Error
    
    return jsonify({"message" : "Review edited successfully!"}), 200  # OK


@review_blueprint.route('/reviews/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_review(id):
    """
    Deleta uma resenha existente.

    Este endpoint recebe o ID da resenha pela URL,
    verifica se a resenha existe e se o usuário atual é o autor da resenha, e deleta a resenha.
    
    Retorna:
        Response: Uma resposta JSON com uma mensagem de sucesso ou erro e o código de status HTTP apropriado.
    """
    current_user = User.query.filter_by(id=get_jwt_identity()).first()
    review = Review.query.filter_by(id=id).first()

    if not review:
        return jsonify({"message" : "Review not exists!"}), 404  # Not Found
    if current_user.email != review.user_email:
        return jsonify({"message" : "Access denied!"}), 403  # Forbidden
    
    review.delete_review()
    return jsonify({"message" : "Review deleted successfully!"}), 200  # OK


@review_blueprint.route('/reviews/avarage-rating/<string:title>', methods=['GET'])
def average_rating_of_book(title):
    """
    Calcula a média das classificações de um livro específico.

    Este endpoint recebe o título do livro pela URL.

    Parâmetros:
        title (str): O título do livro cuja média de classificações será calculada.

    Retorna:
        Response: Uma resposta JSON com a média das classificações do livro especificado.
    """
    reviews = Review.query.all()
    total_rating_of_book = 0
    total_of_reviews = 0

    for review in reviews:
        if review.book_title == title:
            total_rating_of_book += review.rating
            total_of_reviews += 1
    
    avarage_rating = round(total_rating_of_book / total_of_reviews, 2)

    return jsonify({"avarage rating of book" : "{}".format(avarage_rating)}), 200  # OK