import os
from dotenv import load_dotenv
load_dotenv()
import face_recognition
import numpy as np
from flask import (Flask, render_template, request, redirect, session )
from source.utils.connection import connect
from source.web.recognize_users import recognize_user


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask( __name__, template_folder=os.path.join(BASE_DIR, "templates"))

app.secret_key = "safe_face_secret"

print("APP WEB CORRECTA")


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/login_face", methods=["POST"])
def login_face():

    nombre = request.form["nombre"]

    print("Intentando login:", nombre)

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT id_usuario
        FROM usuario
        WHERE nombre = %s
        """,
        (nombre,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    connection.close()


    if usuario is None:

        print("Usuario no existe")

        return redirect("/login")

    print("Usuario encontrado")


    resultado = recognize_user(nombre)

    if resultado:

        print("LOGIN CORRECTO")

        session["authenticated"] = True
        session["usuario"] = nombre

        return redirect("/")


    else:

        print("LOGIN FALLIDO")

        return redirect("/login")



@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

@app.route("/")
def home():

    if not session.get("authenticated"):

        return redirect("/login")

    print("Home")

    return render_template(
        "index.html",
        usuario=session.get("usuario")
    )


@app.route("/users")
def users():

    if not session.get("authenticated"):

        return redirect("/login")

    print("Users")

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuario
        """
    )

    usuarios = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "users.html",
        usuarios=usuarios
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register")
def register():

    if not session.get("authenticated"):

        return redirect("/login")

    print("ENTRO REGISTER")

    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():

    if not session.get("authenticated"):

        return redirect("/login")

    print("REGISTRANDO USUARIO")

    nombre = request.form["nombre"]

    imagen = request.files["imagen"]

    # =====================================================
    # CONEXIÓN
    # =====================================================

    connection = connect()
    cursor = connection.cursor()

    # =====================================================
    # VALIDAR DUPLICADOS
    # =====================================================

    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE nombre = %s
        """,
        (nombre,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        print("Usuario ya existe")

        cursor.close()
        connection.close()

        return redirect("/register")

    # =====================================================
    # GUARDAR IMAGEN
    # =====================================================

    upload_folder = os.path.join(
        BASE_DIR,
        "static",
        "uploads"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    image_path = os.path.join(
        upload_folder,
        imagen.filename
    )

    imagen.save(image_path)

    print("Imagen guardada")

    # =====================================================
    # GENERAR EMBEDDING
    # =====================================================

    image = face_recognition.load_image_file(
        image_path
    )

    encodings = face_recognition.face_encodings(
        image
    )

    if len(encodings) == 0:

        print("No se detectó rostro")

        return redirect("/register")

    embedding = encodings[0]

    # =====================================================
    # GUARDAR EMBEDDING
    # =====================================================

    embedding_dir = os.path.join(
        "storage",
        "embeddings"
    )

    os.makedirs(
        embedding_dir,
        exist_ok=True
    )

    embedding_path = os.path.join(
        embedding_dir,
        f"{nombre}.npy"
    )

    np.save(
        embedding_path,
        embedding
    )

    print("Embedding guardado")

    # =====================================================
    # INSERTAR USUARIO
    # =====================================================

    cursor.execute(
        """
        INSERT INTO usuario(nombre)
        VALUES(%s)
        """,
        (nombre,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    print("Usuario guardado en BD")

    return redirect("/users")


# =========================================================
# LOGS
# =========================================================

@app.route("/logs")
def logs():

    if not session.get("authenticated"):

        return redirect("/login")

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            l.id_log,
            u.nombre,
            l.fecha,
            l.autorizado,
            l.distancia

        FROM log_acceso l

        LEFT JOIN usuario u
        ON l.id_usuario = u.id_usuario

        ORDER BY l.fecha DESC
        """
    )

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "logs.html",
        logs=logs
    )


if __name__ == "__main__":

    app.run(debug=True, port=5000 )
