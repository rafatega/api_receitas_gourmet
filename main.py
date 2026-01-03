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


@app.route("/checkusers", methods=["GET"])
def checkusers():
    """
    Checa todas informações dos usuários cadastrados
    ---
    """
    users = User.query.all()
    return jsonify([{"id": u.id, "username": u.username, "password": u.password} for u in users]), 200


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
        return jsonify({'message': 'Usuário já existe'}), 400
    new_user = User(username=data['username'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso'}), 201


@app.route("/login", methods=["POST"])
def login():
    """
    Faz o login e gera um token JWT.
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
    response:
      200: 
        description: Login bem sucedido, retorna JWT
      401:
        description: Credenciais inválidas
    """

    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and user.password == data['password']:
        # Converter o ID para string
        token = create_access_token(identity=str(user.id))
        return jsonify({"access_token": token}), 200
    return jsonify({"error": "Invalid credential"}), 401


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Retorna a identidade usada na criação do token
    current_user_id = get_jwt_identity()
    return jsonify({"msg": f"Usuário com ID {current_user_id} acessou a rota protegida"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print('Banco de dados criado!')
    app.run(debug=True)
# Inicializa o banco de dados
