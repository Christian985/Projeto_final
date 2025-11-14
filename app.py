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
    return render_template('cadastro_pessoas.html')

# Renderiza a Lista de Pessoas
@app.route('/pessoas')
def listar_clientes():
    return render_template('cadastro_pessoas.html')


# Renderiza a Lista de Produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    vendas = routes.get_produtos()
    
    return render_template('cadastro_produtos.html')


# Renderiza a Lista de Vendas
@app.route('/vendas', methods=['GET', 'POST'])
def listar_vendas():
    return render_template('cadastro_vendas.html')


# Renderiza a Lista de Categoria
@app.route('/categorias', methods=['GET', 'POST'])
def listar_categorias():
    return render_template('cadastro_categorias.html')


# Inicia
if __name__ == '__main__':
    app.run(debug=True, port=5001)
