from flask import Flask, render_template
from source.arduino.main.utils.connection import connect

app = Flask(__name__)

@app.route("/")
def home():
    print('Home')
    return render_template("index.html")

@app.route("/users")
def users():
    print('Users')

    connection = connect()
    cursor = connection.cursor()

    usuarios = cursor.execute('select * from usuario;').fetchall()

    return render_template("users.html",usuarios = usuarios)

if __name__ == "__main__":
    app.run(debug=True)