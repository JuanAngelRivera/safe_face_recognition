import os
from flask import (Flask, render_template, request, redirect, session)
from source.utils.connection import connect
from source.utils.recognize import recognize
from source.utils.load_users import load_user
from source.utils.register_user import register_user as ru


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask( __name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.secret_key = "safe_face_secret"

@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login_face", methods=["POST"])
def login_face():

    nombre = request.form["nombre"]

    encoding, id = load_user(nombre)

    if id is None:
        return redirect("/login")

    print('Encontró usuario + encoding')
    resultado = recognize(encoding, id)

    if resultado:
        session["authenticated"] = True
        session["usuario"] = nombre
        return redirect("/")
    else:
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

@app.route("/register")
def register():
    if not session.get("authenticated"):
        return redirect("/login")

    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    if not session.get("authenticated"):
        return redirect("/login")

    nombre = request.form["nombre"]
    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM usuario
        WHERE nombre = %s
        """,
        (nombre, )
    )

    existing_user = cursor.fetchone()

    if existing_user:
        print("Usuario ya existe")
        cursor.close()
        connection.close()
        return redirect("/register")

    respuesta = ru(nombre)

    if respuesta:
        print("Usuario guardado en BD")
        return redirect("/users")
    else:
        print('No se pudo registrar el usuario')
        return redirect('/register')

@app.route("/logs")
def logs():
    if not session.get("authenticated"):
        return redirect("/login")

    connection = connect()
    cursor = connection.cursor()

    cursor.execute(
        """
        select a.id_acceso, u.nombre, a.fecha, a.autorizado, a.confianza
        from acceso a
        left join usuario u on a.id_usuario = u.id_usuario
        order by a.fecha desc
        """
    )

    logs = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "logs.html",
        logs = logs
    )


if __name__ == "__main__":

    app.run(debug=True, port=5000 )
