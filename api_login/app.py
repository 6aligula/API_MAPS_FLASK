from flask import Flask, request, jsonify
from config import app, db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os 
from flask import send_from_directory
from werkzeug.utils import secure_filename  

SECRET_KEY = "clave_secreta"

# Modelo de Usuario
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    profile = db.relationship('Profile', backref='user', uselist=False)

    def __repr__(self):
        return f'<User {self.email}>'

# Modelo para perfiles de usuario
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)

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

@app.route('/create_profile', methods=['POST'])
def create_profile():
    # 1. Obtener el token del header Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token no proporcionado"}), 401

    token = auth_header.split(" ")[1]

    # 2. Decodificar el token para obtener el user_id
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Verificar si el usuario ya tiene un perfil
    existing_profile = Profile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        return jsonify({"error": "El usuario ya tiene un perfil creado"}), 400

    # 3. Obtener los datos del body
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    image_url = data.get("imageUrl")

    if not name or not description:
        return jsonify({"error": "Datos incompletos"}), 400

    # 4. Verificar que el usuario existe
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    # 5. Crear el nuevo perfil
    new_profile = Profile(
        name=name,
        description=description,
        image_url=image_url,
        user_id=user_id
    )
    
    try:
        db.session.add(new_profile)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al crear el perfil"}), 500

    return jsonify({"message": "Perfil creado exitosamente"}), 200

    # Configuración para almacenar imágenes localmente
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para verificar si la extensión del archivo es permitida
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Endpoint para cargar imágenes
@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Verificar autenticación: se asume que se envía el token en el header Authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Token no proporcionado"}), 401

    token = auth_header.split(" ")[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido"}), 401

    # Validar que se envía el archivo con la clave 'image'
    if 'image' not in request.files:
        return jsonify({"error": "No se proporcionó imagen"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "Nombre de archivo inválido"}), 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            image.save(file_path)
            # Construir URL de la imagen
            image_url = f"http://localhost:5000/uploads/{filename}"
            
            # Obtener el perfil del usuario y actualizar la URL de la imagen
            user_profile = Profile.query.filter_by(user_id=user_id).first()
            if user_profile:
                user_profile.image_url = image_url
                db.session.commit()
            else:
                return jsonify({"error": "Perfil de usuario no encontrado"}), 404

            return jsonify({
                "message": "Imagen subida exitosamente",
                "image_url": image_url
            }), 200
        except Exception as e:
            return jsonify({"error": "Error al subir la imagen"}), 500

        return jsonify({"message": "Imagen subida exitosamente", "image_url": image_url}), 200
    else:
        return jsonify({"error": "Extensión de archivo no permitida"}), 400



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
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

# Inicializar la base de datos
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
