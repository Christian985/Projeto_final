from flask import Flask, render_template, request, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def inicio():
    return render_template('template.html')


@app.route('/cadastro_cliente')
def cadastro_de_cliente():
    return render_template('cadastro_cliente.html')


@app.route('/cadastro_calcados')
def cadastro_de_calcados():
    return render_template('cadastro_calcados.html')


@app.route('/cadastro_pedidos')
def cadastro_de_pedidos():
    return render_template('cadastro_pedidos.html')


@app.route('/lista_calcados')
def lista_de_calcados():
    return render_template('lista_calcados.html')


@app.route('/lista_pedidos')
def lista_de_pedidos():
    return render_template('lista_pedidos.html')


@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')


if __name__ == '__main__':
    app.run(debug=True)
