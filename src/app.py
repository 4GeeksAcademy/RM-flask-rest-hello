"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorites
#from models import Person
import json

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET', 'POST'])
def get_add_users():
    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
            name=user['name'],
        )
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"msg": "Usuario creado correctamente"})
    user = User.query.all()
    if user == []:
        return jsonify({"msg": "No existe el usuario"})
    response_body = list(map(lambda user: user.serialize(), user))
    return jsonify(response_body), 200

@app.route('/users/<int:user_id>', methods=['GET', 'DELETE', 'PUT'])
def get_edit_delete_user(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return jsonify({"msg": "No existe el usuario"}), 404
    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({"msg": "Usuario eliminada"}), 200
    if request.method == 'PUT':
        body = json.loads(request.data)
        if "email" in body:
            user.email = body['email']
        db.session.commit()
        return jsonify(user.serialize()), 200
    return jsonify(user.serialize()), 200

@app.route('/favorites', methods=['GET', 'POST'])
def get_add_favorites():
    if request.method == 'POST':
        favorito = json.loads(request.data)
        new_favorite = Planets(
            user_id=favorito['user_id'],
            planets_id=favorito['planets_id'],
            people_id=favorito['people_id']
        )
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify({"msg": "Favorito creado correctamente"})
    favorite = Favorites.query.all()
    if favorite == []:
        return jsonify({"msg": "No hay favorito"})
    response_body = list(map(lambda favorite: favorite.serialize(), favorite))
    return jsonify(response_body), 200

@app.route('/favorites/<int:favorites_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_edit_favorites(favorites_id):
    favorite = Favorites.query.filter_by(id = favorites_id).first()
    if favorite is None:
        return jsonify({"msg": "No existe el Favorito"}), 404
    if request.method == 'DELETE':
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"msg": "Favorito eliminada"}), 200
    if request.method == 'PUT':
        body = json.loads(request.data)
        if "name" in body:
            favorite.name = body['name']
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    return jsonify(favorite.serialize()), 200

@app.route('/planets', methods=['GET', 'POST'])
def get_add_planets():
    if request.method == 'POST': #Correcion
        planeta = json.loads(request.data)
        new_planet = Planets(
            name=planeta['name'],
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify({"msg": "Planeta creado correctamente"})
    planeta = Planets.query.all()
    if planeta == []:
        return jsonify({"msg": "No existe el planeta"}), 404
    response_body = list(map(lambda planeta: planeta.serialize(), planeta))
    return jsonify(response_body), 200

@app.route('/planets/<int:planets_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_edit_planet(planets_id):
    planet = Planets.query.filter_by(id = planets_id).first()
    if planet is None:
        return jsonify({"msg": "No existe el planeta"}), 404
    if request.method == 'DELETE':
        db.session.delete(planet)
        db.session.commit()
        return jsonify({"msg": "Persona eliminada"}), 200
    if request.method == 'PUT':
        body = json.loads(request.data)
        if "name" in body:
            planet.name = body['name']
        db.session.commit()
        return jsonify(planet.serialize()), 200
    return jsonify(planet.serialize()), 200

@app.route('/people', methods=['GET', 'POST'])
def get_add_people():
    if request.method == 'POST': #Correcion
        persona = json.loads(request.data)
        new_person = People(
            name=persona['name'],
        )
        db.session.add(new_person)
        db.session.commit()
        return jsonify({"msg": "Persona creado correctamente"})
    people = People.query.all()
    if people == []:
        return jsonify({"msg": "No existe la persona"}), 404
    response_body = list(map(lambda people: people.serialize(), people))
    return jsonify(response_body), 200

@app.route('/people/<int:people_id>', methods=['GET', 'DELETE', 'PUT'])
def get_delete_edit_person(people_id):
    person = People.query.filter_by(id = people_id).first()
    if person is None:
        return jsonify({"msg": "No existe la persona"}), 404
    if request.method == 'DELETE':
        db.session.delete(person)
        db.session.commit()
        return jsonify({"msg": "Persona eliminada"}), 200
    if request.method == 'PUT':
        body = json.loads(request.data)
    if "name" in body:
        person.name = body['name']
        db.session.commit()
        return jsonify(person.serialize()), 200
    return jsonify(person.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
