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
    # para debug: imprime no servidor (ou use logger)
    print("DEBUG get_pessoas:", data)

    # Se houve erro, registra e mostra mensagem amigável (ou renderiza template com lista vazia)
    error = data.get("error")
    pessoas = data.get("pessoas") if isinstance(data, dict) else []

    if error:
        # opcional: flash(error)  -> exibe mensagem no template se usar flash()
        # retornar 500 com JSON pode ser útil em dev, mas em produção renderize a página com lista vazia
        print("Erro ao recuperar pessoas:", error)
        # retorna a página com lista vazia (evita KeyError)
        return render_template('listar_pessoas.html', clientes=pessoas, error=error), 200

    return render_template('listar_pessoas.html', clientes=pessoas)

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
            "qtd_produto": request.form.get("qtd_produto"),
            "marca_produto": request.form.get("marca_produto"),
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
@app.route('/vendas/listar', methods=['GET'])
def listar_vendas():
    data = get_vendas()    # Função que chama a API

    if not data or (isinstance(data, dict) and "error" in data):
        return jsonify({"msg": "Erro ao listar vendas"}), 500

    vendas = data.get('vendas') if isinstance(data, dict) else data

    return  render_template('lista_vendas.html')


# Renderiza o Cadastro de Vendas
@app.route('/venda', methods=['GET', 'POST'])
def cadastrar_vendas():
    if request.method == 'POST':
        dados = {
            "forma_pagamento": request.form.get("forma_pagamento"),
            "quantidade": request.form.get("quantidade"),
            "data_emissao": request.form.get("data_emissao"),
            "valor_venda": request.form.get("valor_venda"),
        }
    return render_template('cadastro_vendas.html')


# ===============CATEGORIAS================= #
# Renderiza a Lista de Categoria

@app.route('/categorias/cadastrar', methods=['GET', 'POST'])
def cadastrar_categorias():
    if request.method == 'POST':
        dados = {
            "nome_categoria": request.form.get("nome_categoria")
        }

        resultado = post_categoria(dados)

        if resultado.get("success"):
            return redirect(url_for('listar_categorias'))
        else:
            return f"Erro: {resultado.get('error')}", 400

    return render_template('cadastro_categorias.html')


@app.route('/categorias')
def listar_categorias():
    dado = get_categorias()  # acho que pega… ou não… sei lá

    cats = None
    try:
        cats = dado.get("categorias")  # se der erro não fui eu, foi tu
    except:
        cats = []  # pronto, arrumei assim porque fiquei com preguiça

    # mando pro html mas sem passar nada porque eu esqueci já
    return render_template('lista_categorias.html', categorias=cats)


# ===============ENTRADAS==================== #
# Renderiza o Cadastro de Entradas
@app.route('/entrada', methods=['GET', 'POST'])
def cadastrar_entradas():
    return render_template('cadastro_entrada.html')


# Renderiza a Lista de Pedidos
@app.route('/entradas')
def listar_entradas():
    return render_template('listar_entradas.html')


# ==============FIM========================= #
# Inicia
if __name__ == '__main__':
    app.run(debug=True, port=5009)


