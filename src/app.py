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

@app.route('/users', methods=['GET', 'POST'])
def get_add_users():
    if request.method == 'POST':
        user = json.loads(request.data)
        new_user = User(
            email=user['email'],
            password=user['password'],
            is_active=user['is_active']
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
        return jsonify({"msg": "Usuario eliminad0"}), 200
    if request.method == 'PUT':
        body = json.loads(request.data)
        if "email" in body:
            user.email = body['email']
        if "password" in body:
            user.password = body['password']
        if "is_active" in body:
            user.is_active = body['is_active']
        db.session.commit()
        return jsonify(user.serialize()), 200
    return jsonify(user.serialize()), 200

@app.route('/favorites', methods=['GET', 'POST'])
def get_add_favorites():
    if request.method == 'POST':
        favorito = json.loads(request.data)
        new_favorite = Favorites(
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
        if "user_id" in body:
            favorite.user_id = body['user_id']
        if "planets_id" in body:
            favorite.planets_id = body['planets_id']
        if "people_id" in body:
            favorite.people_id = body['people_id']
        db.session.commit()
        return jsonify(favorite.serialize()), 200
    return jsonify(favorite.serialize()), 200

@app.route('/planets', methods=['GET', 'POST'])
def get_add_planets():
    if request.method == 'POST': #Correcion
        planeta = json.loads(request.data)
        new_planet = Planets(
            name=planeta['name'],
            rotation_period=planeta['rotation_period'], 
            orbital_period=planeta['orbital_period'],
            diameter=planeta['diameter'],
            climate=planeta['climate'],
            gravity=planeta['gravity'], 
            terrain=planeta['terrain'], 
            surface_water=planeta['surface_water'], 
            population=planeta['population']
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
        return jsonify({"msg": "Planeta eliminada"}), 200
    if request.method == 'PUT':
        body = json.loads(request.data)
        if "name" in body:
            planet.name = body['name']
        if "rotation_period" in body:
            planet.rotation_period = body['rotation_period']
        if "orbital_period" in body:
            planet.orbital_period = body['orbital_period']
        if "diameter" in body:
            planet.diameter = body['diameter']
        if "climate" in body:
            planet.climate = body['climate']
        if "gravity" in body:
            planet.gravity = body['gravity']
        if "terrain" in body:
            planet.terrain = body['terrain']
        if "surface_water" in body:
            planet.surface_water = body['surface_water']
        if "population" in body:
            planet.population = body['population']
        db.session.commit()
        return jsonify(planet.serialize()), 200
    return jsonify(planet.serialize()), 200

@app.route('/people', methods=['GET', 'POST'])
def get_add_people():
    if request.method == 'POST': #Correcion
        persona = json.loads(request.data)
        new_person = People(
            name=persona['name'],
            height=persona['height'], 
            mass=persona['mass'],
            hair_color=persona['hair_color'], 
            skin_color=persona['skin_color'], 
            eye_color=persona['eye_color'], 
            birth_year=persona['birth_year'], 
            gender=persona['gender'],
            homeworld=persona['homeworld']
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
        if "height" in body:
            person.height = body['height']
        if "mass" in body:
            person.mass = body['mass']
        if "hair_color" in body:
            person.hair_color = body['hair_color']
        if "skin_color" in body:
            person.skin_color = body['skin_color']
        if "eye_color" in body:
            person.eye_color = body['eye_color']
        if "birth_year" in body:
            person.birth_year = body['birth_year']
        if "gender" in body:
            person.gender = body['gender']
        if "homeworld" in body:
            person.homeworld = body['homeworld']    
        db.session.commit()
        return jsonify(person.serialize()), 200
    return jsonify(person.serialize()), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
