from app import db
from app.models.genre import Genre
from app.models.book import Book
from app.book_routes import validate_model
from flask import Blueprint, jsonify, abort, make_response, request

genres_bp = Blueprint("genres", __name__, url_prefix="/genres")

@genres_bp.route("", methods=["POST"])
def create_genre():
    request_body = request.get_json()
    new_genre = Genre(name=request_body["name"],)

    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(f"Genre {new_genre.name} successfully created"), 201)

@genres_bp.route("", methods=["GET"])
def read_all_genres():
    genres = Genre.query.all()

    genres_response = []
    for genre in genres:
        genres_response.append(
            {
                "name": genre.name
            }
        )
    return jsonify(genres_response)


# Nested Routes : Create a new book with its genre (and author)
@genres_bp.route("/<genre_id>/books", methods=["POST"])
def create_genre_for_book(genre_id): 
    # Query the Genre table to get the genre with genre_id
    genre = validate_model(Genre, genre_id)
    request_body = request.get_json()
    # Create a new book instance with data from the request_body and the genre
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author_id=request_body["author_id"],
        # We get the genre(s) from input
        genres=[genre]
    )

    # Commit our new book from the database
    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)

@genres_bp.route("/<genre_id>/books", methods=["GET"])
def read_all_genres_by_book(genre_id): 
    # Query the Genre table to get the genre with genre_id
    genre = validate_model(Genre, genre_id)
    # Iterate through the books with that genre
    books_response = []
    for book in genre.books: 
        # genre.books returns a list of Book instances associated with the Genre instance named genre
        books_response.append(book.to_dict())
    # Return a response as a list of dictionaries with information for each book in the specified genre.
    return jsonify(books_response)
