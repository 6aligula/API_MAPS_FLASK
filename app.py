from flask import Flask, request, jsonify
from config import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

import datetime
SECRET_KEY = "clave_secreta"

# Modelo de Usuario (ya existente)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Nuevo modelo para perfiles de usuario
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Ruta para registrar usuarios (ya existente)
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registro exitoso"}), 200

# Ruta para registrar un perfil
@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("image_url")
    user_id = data.get("user_id")  # Se asocia con un usuario registrado

    if not name or not description or not user_id:
        return jsonify({"error": "Datos incompletos"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    new_profile = Profile(name=name, description=description, image_url=image_url, user_id=user_id)
    db.session.add(new_profile)
    db.session.commit()

    return jsonify({"message": "Perfil creado exitosamente"}), 200

# Ruta para login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Credenciales incorrectas"}), 401

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=123)
    }, SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Login exitoso", "token": token, "user_id": user.id}), 200

# Inicializar la base de datos si no existe
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
