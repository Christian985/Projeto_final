from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)


# Renderiza a Primeira Página/Início
@app.route('/')
def index():
    return render_template('template.html')


# Renderiza a Lista de Pessoas
@app.route('/pessoas')
def listar_clientes():
    return render_template('lista_clientes.html')


# Renderiza o Cadastro de Pessoas
@app.route('/pessoa')
def cadastrar_clientes():
    return render_template('cadastro_pessoas.html')


# Renderiza a Lista de Produtos
@app.route('/produtos')
def listar_produtos():
    produtos = routes.get_produtos()
    return render_template('lista_calcados.html', produtos=produtos['produtos'])


# Renderiza o Cadastro de Produtos
@app.route('/produto')
def cadastrar_produto():
    return render_template('cadastro_produto.html')


# Renderiza o Cadastro de Vendas
@app.route('/venda')
def cadastrar_vendas():
    return render_template('cadastro_vendas.html')


# Renderiza a Lista de Vendas
@app.route('/vendas')
def listar_vendas():
    return  render_template('cadastro_vendas.html')


# Renderiza a Lista de Categoria
@app.route('/categorias')
def listar_categorias():
    return render_template('cadastro_categorias.html')


# Renderiza o Cadastro de Pedidos
@app.route('/pedido', methods=['GET', 'POST'])
def cadastrar_pedidos():
    return render_template('cadastro_pedidos.html')


# Renderiza a Lista de Pedidos
@app.route('/pedidos')
def listar_pedidos():
    print('listar_pedidos')
    return render_template('pedidos.html')


# Inicia
if __name__ == '__main__':
    app.run(debug=True, port=5002)
