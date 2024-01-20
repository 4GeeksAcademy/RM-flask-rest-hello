from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
    
class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planets_id = db.Column(db.Integer, db.ForeignKey("planets.id"))
    people_id = db.Column(db.Integer, db.ForeignKey("people.id"))

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planets_id": self.planets_id, 
            "people_id": self.people_id
        }

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=False)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    hair_color = db.Column(db.String(45))
    skin_color = db.Column(db.String(45))
    eye_color = db.Column(db.String(45))
    birth_year = db.Column(db.String(45))
    gender = db.Column(db.String(45))
    homeworld = db.Column(db.String(45))
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height, 
            "mass": self.mass,
            "hair_color": self.hair_color, 
            "skin_color": self.skin_color, 
            "eye_color": self.eye_color, 
            "birth_color": self.birth_year, 
            "gender": self.gender,
            "homeworld": self.homeworld, 
        }

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=False)
    rotation_period = db.Column(db.String(45))
    orbital_period = db.Column(db.String(45))
    diameter = db.Column(db.String(45))
    climate = db.Column(db.String(45))
    gravity = db.Column(db.String(45))
    terrain = db.Column(db.String(45))
    surface_water = db.Column(db.String(45))
    population = db.Column(db.Integer)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<Planets %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "rotation_period": self.rotation_period, 
            "orbital_period": self.orbital_period,
            "diameter": self.diameter,
            "climate": self.climate,
            "gravity": self.gravity, 
            "terrain": self.terrain, 
            "surface_water": self.surface_water, 
            "population": self.population
        }
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorites = db.relationship("Favorites")

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "is_active": self.is_active
        }
    