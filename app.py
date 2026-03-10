from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# conexión a MongoDB Atlas
cliente = MongoClient("mongodb+srv://mimi:oaOKqX0tvwe8d7u2@cluster0.rkxwz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# base de datos
db = cliente["Estacionamiento"]

# colección correcta
usuarios = db["usuarios"]

@app.route("/usuarios", methods=["POST"])
def crear_usuario():

    datos = request.json

    nuevo_usuario = {
        "nombre": datos["nombre"],
        "correo": datos["correo"],
        "password": datos["password"]
    }

    resultado = usuarios.insert_one(nuevo_usuario)

    return jsonify({
        "mensaje": "Usuario creado",
        "id": str(resultado.inserted_id)
    })

@app.route("/login", methods=["POST"])
def login():

    datos = request.json

    correo = datos["correo"]
    password = datos["password"]

    usuario = usuarios.find_one({
        "correo": correo,
        "password": password
    })

    if usuario:

        usuario["_id"] = str(usuario["_id"])

        return jsonify({
            "success": True,
            "usuario": usuario
        })

    else:

        return jsonify({
            "success": False,
            "mensaje": "Usuario o contraseña incorrectos"
        })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)


