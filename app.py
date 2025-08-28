from flask import Flask, render_template, request, redirect, url_for, request

app = Flask(__name__)


@app.route('/')
def inicial():
    return render_template('inicio.html')


@app.route('/cadastro_cliente')
def exemplos():
    return render_template('cadastro_cliente.html')


@app.route('/cadastro_calcados')
def exercicios():
    return render_template('cadastro_calcados.html')


@app.route('/cadastro_pedidos')
def exercicios():
    return render_template('cadastro_pedidos.html')


@app.route('/lista_calcados')
def exercicios():
    return render_template('lista_calcados.html')


@app.route('/lista_pedidos')
def exercicios():
    return render_template('lista_pedidos.html')


@app.route('/pedidos')
def exercicios():
    return render_template('pedidos.html')


if __name__ == '__main__':
    app.run(debug=True)
