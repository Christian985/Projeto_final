from flask import Blueprint, render_template, request, redirect, url_for
from models import Categoria, Produto, Pessoa, Venda, Entrada, local_session

routes = Blueprint('routes', __name__)

# =====================================
# PÁGINA INICIAL
# =====================================
@routes.route('/')
def index():
    return render_template('index.html')


# =====================================
# CATEGORIA
# =====================================
@routes.route('/categorias')
def listar_categorias():
    categorias = local_session.query(Categoria).all()
    return render_template('categoria/listar.html', categorias=categorias)

@routes.route('/categorias/novo', methods=['GET', 'POST'])
def nova_categoria():
    if request.method == 'POST':
        nome = request.form['nome_categoria']
        categoria = Categoria(nome_categoria=nome)
        categoria.save(local_session)
        return redirect(url_for('routes.listar_categorias'))
    return render_template('categoria/novo.html')

@routes.route('/categorias/editar/<int:id_categoria>', methods=['GET', 'POST'])
def editar_categoria(id_categoria):
    categoria = local_session.query(Categoria).get(id_categoria)
    if request.method == 'POST':
        categoria.nome_categoria = request.form['nome_categoria']
        categoria.save(local_session)
        return redirect(url_for('routes.listar_categorias'))
    return render_template('categoria/editar.html', categoria=categoria)

@routes.route('/categorias/deletar/<int:id_categoria>')
def deletar_categoria(id_categoria):
    categoria = local_session.query(Categoria).get(id_categoria)
    categoria.delete(local_session)
    return redirect(url_for('routes.listar_categorias'))


# =====================================
# PRODUTO
# =====================================
@routes.route('/produtos')
def listar_produtos():
    produtos = local_session.query(Produto).all()
    return render_template('produto/listar.html', produtos=produtos)

@routes.route('/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    categorias = local_session.query(Categoria).all()

    if request.method == 'POST':
        produto = Produto(
            nome_produto=request.form['nome_produto'],
            qtd_produto=request.form['qtd_produto'],
            tamanho=request.form['tamanho'],
            marca_produto=request.form['marca_produto'],
            custo_produto=request.form['custo_produto'],
            genero=request.form['genero'],
            disponivel=True,
            id_categoria=request.form['id_categoria']
        )
        produto.save(local_session)
        return redirect(url_for('routes.listar_produtos'))

    return render_template('produto/novo.html', categorias=categorias)

@routes.route('/produtos/editar/<int:id_produto>', methods=['GET', 'POST'])
def editar_produto(id_produto):
    produto = local_session.query(Produto).get(id_produto)
    categorias = local_session.query(Categoria).all()

    if request.method == 'POST':
        produto.nome_produto = request.form['nome_produto']
        produto.qtd_produto = request.form['qtd_produto']
        produto.tamanho = request.form['tamanho']
        produto.marca_produto = request.form['marca_produto']
        produto.custo_produto = request.form['custo_produto']
        produto.genero = request.form['genero']
        produto.id_categoria = request.form['id_categoria']
        produto.save(local_session)
        return redirect(url_for('routes.listar_produtos'))

    return render_template('produto/editar.html', produto=produto, categorias=categorias)

@routes.route('/produtos/deletar/<int:id_produto>')
def deletar_produto(id_produto):
    produto = local_session.query(Produto).get(id_produto)
    produto.delete(local_session)
    return redirect(url_for('routes.listar_produtos'))


# =====================================
# PESSOA
# =====================================
@routes.route('/pessoas')
def listar_pessoas():
    pessoas = local_session.query(Pessoa).all()
    return render_template('pessoa/listar.html', pessoas=pessoas)

@routes.route('/pessoas/novo', methods=['GET', 'POST'])
def nova_pessoa():
    if request.method == 'POST':
        pessoa = Pessoa(
            nome_pessoa=request.form['nome_pessoa'],
            cpf_pessoa=request.form['cpf_pessoa'],
            cargo=request.form['cargo'],
            status=True
        )
        pessoa.set_senha_hash(request.form['senha'])
        pessoa.save(local_session)
        return redirect(url_for('routes.listar_pessoas'))

    return render_template('pessoa/novo.html')

@routes.route('/pessoas/editar/<int:id_pessoa>', methods=['GET', 'POST'])
def editar_pessoa(id_pessoa):
    pessoa = local_session.query(Pessoa).get(id_pessoa)

    if request.method == 'POST':
        pessoa.nome_pessoa = request.form['nome_pessoa']
        pessoa.cpf_pessoa = request.form['cpf_pessoa']
        pessoa.cargo = request.form['cargo']

        if request.form['senha']:
            pessoa.set_senha_hash(request.form['senha'])

        pessoa.save(local_session)
        return redirect(url_for('routes.listar_pessoas'))

    return render_template('pessoa/editar.html', pessoa=pessoa)

@routes.route('/pessoas/deletar/<int:id_pessoa>')
def deletar_pessoa(id_pessoa):
    pessoa = local_session.query(Pessoa).get(id_pessoa)
    pessoa.delete(local_session)
    return redirect(url_for('routes.listar_pessoas'))


# =====================================
# ENTRADAS
# =====================================
@routes.route('/entradas')
def listar_entradas():
    entradas = local_session.query(Entrada).all()
    return render_template('entrada/listar.html', entradas=entradas)

@routes.route('/entradas/nova', methods=['GET', 'POST'])
def nova_entrada():
    pessoas = local_session.query(Pessoa).all()
    produtos = local_session.query(Produto).all()

    if request.method == 'POST':
        entrada = Entrada(
            nota_fiscal=request.form['nota_fiscal'],
            valor_entrada=request.form['valor_entrada'],
            quantidade=request.form['quantidade'],
            data_entrada=request.form['data_entrada'],
            id_pessoa=request.form['id_pessoa'],
            id_produto=request.form['id_produto']
        )
        entrada.save(local_session)
        return redirect(url_for('routes.listar_entradas'))

    return render_template('entrada/nova.html', pessoas=pessoas, produtos=produtos)


# =====================================
# VENDAS
# =====================================
@routes.route('/vendas')
def listar_vendas():
    vendas = local_session.query(Venda).all()
    return render_template('venda/listar.html', vendas=vendas)

@routes.route('/vendas/nova', methods=['GET', 'POST'])
def nova_venda():
    pessoas = local_session.query(Pessoa).all()
    produtos = local_session.query(Produto).all()

    if request.method == 'POST':
        venda = Venda(
            forma_pagamento=request.form['forma_pagamento'],
            quantidade=request.form['quantidade'],
            data_emissao=request.form['data_emissao'],
            valor_venda=request.form['valor_venda'],
            id_pessoa=request.form['id_pessoa'],
            id_produto=request.form['id_produto']
        )
        venda.save(local_session)
        return redirect(url_for('routes.listar_vendas'))

    return render_template('venda/nova.html', pessoas=pessoas, produtos=produtos)
