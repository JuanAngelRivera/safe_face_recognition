import os
from flask import (Flask, render_template, request, redirect, session, url_for)
from source.utils.connection import connect
from source.utils.recognize import recognize
from source.utils.load_users import load_user, get_admin
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
    respuesta = get_admin(nombre)

    if respuesta == False:
        print('El usuario no es administrador')
        return redirect("/login")

    encoding, id = load_user(nombre)
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
            select id_usuario, nombre, autorizado, administrador, fecha_registro::date
            from usuario
            order by id_usuario
            """
        )

    usuarios = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template(
        "users.html",
        usuarios = usuarios
        )

@app.route('/deactivate_user/<int:id_usuario>', methods=['POST'])
def desactivate_usuario(id_usuario):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("update usuario set autorizado = false where id_usuario = %s", (id_usuario,))
    connection.commit()

    return redirect(url_for('users'))

@app.route('/activate_user/<int:id_usuario>', methods=['POST'])
def activate_usuario(id_usuario):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("update usuario set autorizado = true where id_usuario = %s", (id_usuario,))
    connection.commit()
    return redirect(url_for('users'))

@app.route('/revoke_admin/<int:id_usuario>', methods=['POST'])
def revoke_admin(id_usuario):
    connection = connect()
    cursor = connection.cursor()
    cursor.execute("update usuario set administrador = false where id_usuario = %s", (id_usuario,))
    connection.commit()
    return redirect(url_for('users'))

@app.route("/register")
def register():
    if not session.get("authenticated"):
        return redirect("/login")
    return render_template("register.html")


@app.route("/register_user", methods=["POST"])
def register_user():
    if not session.get("authenticated"):
        return redirect("/login")

    nombre = request.form.get('nombre')
    administrador = request.form.get('administrador')
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

    administrador = administrador == 'true'

    respuesta = ru(nombre, administrador)

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
            select a.id_acceso, u.nombre, a.autorizado, a.fecha::date, to_char(a.fecha::time, 'HH24:MI:SS'), 
            to_char(((1 - a.confianza) * 100), 'FM999.99')
            from acceso a
            left join usuario u on a.id_usuario = u.id_usuario
            order by a.fecha desc
            """
        )

    logs = cursor.fetchall()

    cursor.close()
    connection.close()
    print(logs[5])

    return render_template(
            "logs.html",
            logs = logs
        )


if __name__ == "__main__":

    app.run(debug=True, port=5000 )