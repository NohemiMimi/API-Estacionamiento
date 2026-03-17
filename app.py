from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# conexión a MongoDB Atlas
cliente = MongoClient("mongodb+srv://mimi:oaOKqX0tvwe8d7u2@cluster0.rkxwz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

# base de datos
db = cliente["Estacionamiento"]

# colección
usuarios = db["usuarios"]

# índice único para correo
usuarios.create_index("correo", unique=True)

# =========================
# CREAR USUARIO (solo usuarios normales)
# =========================
@app.route("/usuarios", methods=["POST"])
def crear_usuario():

    datos = request.json

    nombre = datos.get("nombre")
    correo = datos.get("correo")
    password = datos.get("password")

    if not nombre or not correo or not password:
        return jsonify({
            "success": False,
            "mensaje": "Faltan datos"
        })

    # validar duplicados
    usuario_existente = usuarios.find_one({
        "$or": [
            {"correo": correo},
            {"nombre": nombre}
        ]
    })

    if usuario_existente:
        return jsonify({
            "success": False,
            "mensaje": "El nombre o correo ya existen"
        })

    nuevo_usuario = {
        "nombre": nombre,
        "correo": correo,
        "password": password,
        "rol": "usuario"  # IMPORTANTE
    }

    resultado = usuarios.insert_one(nuevo_usuario)

    return jsonify({
        "success": True,
        "mensaje": "Usuario creado correctamente",
        "id": str(resultado.inserted_id)
    })

# =========================
# LOGIN (usuarios y admins)
# =========================
@app.route("/login", methods=["POST"])
def login():

    datos = request.json

    correo = datos.get("correo")
    password = datos.get("password")

    if not correo or not password:
        return jsonify({
            "success": False,
            "mensaje": "Faltan credenciales"
        })

    usuario = usuarios.find_one({
        "correo": correo,
        "password": password
    })

    if usuario:

        usuario["_id"] = str(usuario["_id"])

        return jsonify({
            "success": True,
            "usuario": {
                "_id": usuario["_id"],
                "nombre": usuario["nombre"],
                "correo": usuario["correo"],
                "rol": usuario.get("rol", "usuario")  # por si acaso
            }
        })

    else:
        return jsonify({
            "success": False,
            "mensaje": "Usuario o contraseña incorrectos"
        })

# =========================
# RUN
# =========================
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)