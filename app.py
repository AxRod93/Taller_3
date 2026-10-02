from flask import Flask, render_template, request, redirect, url_for
from model import db, Cliente

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def inicio():
    return render_template("inicio.html")


@app.route("/clientes")
def clientes():
    lista_clientes = Cliente.query.all()
    return render_template("clientes.html", clientes=lista_clientes)


@app.route("/agregar_cliente", methods=["GET", "POST"])
def agregar_cliente():
    if request.method == "POST":
        cliente = Cliente(
            nombre=request.form["nombre"],
            correo=request.form["correo"],
            telefono=request.form["telefono"]
        )
        db.session.add(cliente)
        db.session.commit()
        return redirect(url_for("clientes"))

    return render_template("agregar_clientes.html")


@app.route("/editar_cliente/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)

    if request.method == "POST":
        cliente.nombre = request.form["nombre"]
        cliente.correo = request.form["correo"]
        cliente.telefono = request.form["telefono"]
        db.session.commit()
        return redirect(url_for("clientes"))

    return render_template("editar_cliente.html", cliente=cliente)


@app.route("/borrar_cliente/<int:id>", methods=["POST"])
def borrar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return redirect(url_for("clientes"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)