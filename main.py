from flask import Flask
from flask_sqlalchemy import SQLAlchemy

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Banco de dados criado!')
    app.run(debug=True)
