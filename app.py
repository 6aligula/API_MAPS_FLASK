from flask import request, jsonify
from config import app, db
from werkzeug.security import generate_password_hash

# Definir el modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    # Validar que se hayan recibido los datos
    if not email or not password:
        return jsonify({"error": "Datos incompletos"}), 400

    # Verificar si el usuario ya existe
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    # Hashear la contraseña para almacenarla de forma segura
    hashed_password = generate_password_hash(password)

    # Crear y guardar el nuevo usuario en la base de datos
    new_user = User(email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    print(f"Registro exitoso: {email}")
    return jsonify({"message": "Registro exitoso"}), 200

if __name__ == '__main__':
    # Asegurarse de que existan las tablas en la base de datos
    with app.app_context():
        db.create_all()
    # Ejecutar el servidor en el host adecuado
    app.run(debug=True, host='0.0.0.0', port=5000)
