from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    
    # Aquí puedes implementar la lógica de validación y almacenamiento en la base de datos
    if email and password:
        # Simula un registro exitoso
        print(f"Registro exitoso: {email}")
        return jsonify({"message": "Registro exitoso"}), 200
    else:
        return jsonify({"error": "Datos incompletos"}), 400

if __name__ == '__main__':
    # Ejecuta el servidor en el host adecuado para ser accesible desde otros dispositivos
    app.run(debug=True, host='0.0.0.0', port=5000)
