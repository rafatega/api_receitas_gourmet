from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)


# Configurações da aplicação


class Config:
    SECRET_KEY = 'sua_chave_secreta'
    CACHE_TYPE = 'simple'
    SWAGGER = {
        'title': 'Catálogo de Receitas Gourmet',
        'uiversion': 3
    }
    SQLALCHEMY_DATABASE_URI = 'sqlite:///recipes.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'sua_chave_jwt_secreta'


app = Flask(__name__)

app.config.from_object(Config)

db = SQLAlchemy(app)
jwt = JWTManager(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=True, nullable=False)


class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), unique=True, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    time_minutes = db.Column(db.Integer, nullable=False)


@app.route('/')
def home():
    return 'Página inicial'


@app.route('/register', methods=['POST'])
def register_user():
    """
    Registra um novo usuário.
    ---
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      201:
        description: Usuário criado com sucesso
      400:
        description: Usuário já existe
    """


data = request.get_json()
if User.query.filter_by(username=data['username']).first():
    return js


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Banco de dados criado!')
    app.run(debug=True)
