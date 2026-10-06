from flask import Flask, render_template, request, redirect, url_for
from model import db, Cliente, Producto   

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tienda.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


@app.route("/")
def inicio():
    return render_template("inicio.html")


# ---------- CLIENTES ----------
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


# ---------- PRODUCTOS ----------
@app.route("/productos")
def productos():
    lista_productos = Producto.query.all()
    return render_template("productos.html", productos=lista_productos)


@app.route("/agregar_producto", methods=["GET", "POST"])
def agregar_producto():
    if request.method == "POST":
        producto = Producto(
            nombre=request.form["nombre"],
            precio=float(request.form["precio"] or 0),
            stock=int(request.form["stock"] or 0)
        )
        db.session.add(producto)
        db.session.commit()
        return redirect(url_for("productos"))

    return render_template("agregar_producto.html")


@app.route("/editar_producto/<int:id>", methods=["GET", "POST"])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)

    if request.method == "POST":
        producto.nombre = request.form["nombre"]
        producto.precio = float(request.form["precio"] or 0)
        producto.stock = int(request.form["stock"] or 0)
        db.session.commit()
        return redirect(url_for("productos"))

    return render_template("editar_producto.html", producto=producto)


@app.route("/borrar_producto/<int:id>", methods=["POST"])
def borrar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    return redirect(url_for("productos"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)