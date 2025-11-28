from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
import routes
from routes import *

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)


# ==============INÍCIO====================== #
# Renderiza a Primeira Página/Início
@app.route('/')
def index():
    return render_template('template.html')


# =============PESSOAS====================== #
# Renderiza a Lista de Pessoas
@app.route('/pessoas/listar', methods=['GET'])
def listar_clientes():
    data = get_pessoas()
    print(data)
    if not data or ("msg" in data if isinstance(data, dict) else False):
        return jsonify({"msg": "Erro ao listar pessoas"}), 500

    return render_template('listar_pessoas.html', clientes=data['pessoas'])



# Renderiza o Cadastro de Pessoas
@app.route('/pessoas/cadastrar', methods=['GET', 'POST'])
def cadastrar_pessoas():
    if request.method == 'POST':
        dados = {
            "nome_pessoa": request.form.get("nome_pessoa"),
            "cpf_pessoa": request.form.get("cpf_pessoa"),
            "cargo": request.form.get("cargo"),
            "senha": request.form.get("senha"),
            "status": request.form.get("status"),
        }

        resultado = post_pessoa(dados)

        if resultado.get("success"):
            return redirect(url_for('listar_clientes'))
        else:
            return f"Erro: {resultado.get('error')}", 400

    return render_template("cadastro_pessoas.html")




# ==============PRODUTOS==================== #
# Renderiza a Lista de Produtos
@app.route('/produtos/listar', methods=['GET'])
def listar_produtos():
    data = get_produtos()   # função que chama a API

    if not data or (isinstance(data, dict) and "error" in data):
        return jsonify({"msg": "Erro ao listar produtos"}), 500

    produtos = data.get('produtos') if isinstance(data, dict) else data

    return render_template('listar_produtos.html', produtos=produtos)


# Renderiza o Cadastro de Produtos
@app.route('/produtos/cadastrar', methods=['GET', 'POST'])
def cadastrar_produto():
    if request.method == 'POST':
        dados = {
            "id_categoria": request.form.get("id_categoria"),
            "nome_produto": request.form.get("nome_produto"),
            "tamanho": request.form.get("tamanho"),
            "genero": request.form.get("genero"),
            "marca_produto": request.form.get("marca_produto"),  # ⚠️ corrigido
            "custo_produto": request.form.get("custo_produto"),
        }

        resultado = post_produtos(dados)

        if resultado.get("success"):
            return redirect(url_for('listar_produtos'))
        else:
            return f"Erro: {resultado.get('error')}", 400

    return render_template('cadastro_produto.html')



# ===============VENDAS===================== #
# Renderiza a Lista de Vendas
@app.route('/vendas')
def listar_vendas():
    data = get_vendas()    # Função que chama a API

    if not data or (isinstance(data, dict) and "error" in data):
        return jsonify({"msg": "Erro ao listar vendas"}), 500

    vendas = data.get('vendas') if isinstance(data, dict) else data

    return  render_template('listar_vendas.html')


# Renderiza o Cadastro de Vendas
@app.route('/venda')
def cadastrar_vendas():
    return render_template('cadastro_vendas.html')


# ===============CATEGORIAS================= #
# Renderiza a Lista de Categoria
@app.route('/categorias')
def listar_categorias():
    return render_template('cadastro_categorias.html')


# ===============PEDIDOS==================== #
# Renderiza o Cadastro de Pedidos
@app.route('/pedido', methods=['GET', 'POST'])
def cadastrar_pedidos():
    return render_template('cadastro_pedidos.html')


# Renderiza a Lista de Pedidos
@app.route('/pedidos')
def listar_pedidos():
    print('listar_pedidos')
    return render_template('pedidos.html')


# ==============FIM========================= #
# Inicia
if __name__ == '__main__':
    app.run(debug=True, port=5002)
