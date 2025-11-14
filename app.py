from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)

# Renderiza a Primeira Página/Início
@app.route('/')
def index():
    return render_template('template.html')

# Renderiza o Cadastro de Pessoas
@app.route('/pessoas', methods=['GET', 'POST'])
def listar_clientes():
    return render_template('cadastro_pessoa.html')

# Renderiza o Cadastro de Produtos
@app.route('/produtos', methods=['GET', 'POST'])
def listar_produtos():
    return render_template('cadastro_produtos.html')

# Renderiza o Cadastro de Vendas
@app.route('/vendas', methods=['GET', 'POST'])
def listar_vendas():
    return render_template('cadastro_vendas.html')

# Renderiza o Cadastro de Categoria
@app.route('/categoria', methods=['GET', 'POST'])
def listar_categorias():
    return render_template('cadastro_categorias.html')

# Inicia
if __name__ == '__main__':
    app.run(debug=True, port=5001)
