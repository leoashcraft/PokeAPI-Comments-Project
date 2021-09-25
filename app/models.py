from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from sqlalchemy import JSON

userpokemon = db.Table('userpokemon',
    db.Column('id', db.Integer, primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete="cascade")),
    db.Column('pokemon_id', db.Integer, db.ForeignKey('pokemon.id', ondelete="cascade")),
    )

class User(UserMixin,db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email =  db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    pokemons = db.relationship("Pokemon", secondary=userpokemon, backref=db.backref("users"))
    comments = db.relationship("Comment", backref="comments", lazy=True)

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.save()

    def hash_password(self, original_password):
        return generate_password_hash(original_password)
    
    def check_hashed_password(self, login_password):
        return check_password_hash(self.password,login_password)

    def save(self):
        db.session.add(self) #adds the user to the db session
        db.session.commit() #saves the changes into the db

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
    # Select * from user WHERE id=id

class Pokemon(db.Model):
    __tablename__ = "pokemon"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    hp = db.Column(JSON)
    attack = db.Column(JSON)
    defense = db.Column(JSON)
    special_attack = db.Column(JSON)
    special_defense = db.Column(JSON)
    speed = db.Column(JSON)
    spritedata = db.Column(db.String(200))
    comments = db.relationship("Comment", backref="pokemons", lazy=True)

    def __repr__(self):
        return f'{self.name}'

    def from_dict(self, data):
        self.name = data['name']
        self.hp = data['hp']
        self.attack = data['attack']
        self.defense = data['defense']
        self.special_attack = data['special_attack']
        self.special_defense = data['special_defense']
        self.speed = data['speed']
        self.spritedata = data['spritedata']
        self.save()

    def save(self):
        db.session.add(self) # adds the pokemon to the db session
        db.session.commit() # saves the changes into the db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    pokemon_id = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)
    pokemon_owner_id = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, nullable=False, default=dt.utcnow)

    def __repr__(self):
        return f'{self.content}'

    def user(self):
        user = User.query.filter_by(id = self.user_id).first()
        return user.first_name + " " + user.last_name

    def from_dict(self, data):
        self.content = data['content']
        self.user_id = data['user_id']
        self.pokemon_id = data['pokemon_id']
        self.pokemon_owner_id = data['pokemon_owner_id']
        self.save()

    def save(self):
        db.session.add(self) 
        db.session.commit() 