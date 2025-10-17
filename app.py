from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route('/')
def template():
    return render_template('template.html')


@app.route('/cadastro_cliente')
def cadastro_cliente():
    return render_template('cadastro_clientes.html')


@app.route('/cadastro_calcados')
def cadastro_calcados():
    return render_template('cadastro_calcados.html')


@app.route('/cadastro_pedidos')
def cadastro_pedidos():
    return render_template('cadastro_pedidos.html')


@app.route('/lista_calcados')
def lista_calcados():
    return render_template('lista_calcados.html')


@app.route('/lista_pedidos')
def lista_pedidos():
    return render_template('lista_pedidos.html')


@app.route('/pedidos')
def pedidos():
    return render_template('pedidos.html')


@app.route('/lista_clientes')
def lista_clientes():
    return render_template('lista_clientes.html')


@app.route('/submit', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    tipo = request.form['tipo']

    # Aqui você faria a verificação com banco de dados
    if tipo == 'admin' and email == 'admin@site.com' and senha == 'admin123':
        return redirect('/admin-dashboard')
    elif tipo == 'usuario' and email == 'usuario@site.com' and senha == 'usuario123':
        return redirect('/usuario-dashboard')
    else:
        return "Credenciais inválidas", 401


if __name__ == '__main__':
    app.run(debug=True, port=5002, host="0.0.0.0")
