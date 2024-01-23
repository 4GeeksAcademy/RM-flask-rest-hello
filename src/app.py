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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/favorites', methods=['GET'])
def get_favorites():
    response_body = {
        "id": Favorites.id,
        "user_id": Favorites.user_id,
        "planets_id": Favorites.planets_id,
        "people_id": Favorites.people_id
    }
    return jsonify(response_body), 200

@app.route('/favorites/<int:people_id>', methods=['DELETE'])
def delete_favorite(id): 
    favorite = Favorites.query.get_or_404(id)
    db.session.delete(id)
    db.session.commit()

@app.route('/favorites', methods=['POST'])
def add_favorite():
    favorite = request.get_json()
    new_favorite = Favorites(user_id=favorite['user_id'], planets_id=favorite['planets_id'], people_id=favorite['people_id'] )
    db.session.add()
    db.session.commit()
    return jsonify({"message": "Persona añadida a favoritos"})

@app.route('/planets', methods=['GET'])
def get_planets(): #Correcion
    planeta = Planets.query.all()
    if planeta == []:
        return jsonify({"msg": "No existe el planeta"})
    response_body = list(map(lambda planeta: planeta.serialize(), planeta))
    return jsonify(response_body), 200

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    if people == []:
        return jsonify({"msg": "No existe la persona"})
    response_body = list(map(lambda people: people.serialize(), people))
    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
