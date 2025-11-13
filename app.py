import json
from time import strftime

from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime
from models import *
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_required, login_user, logout_user, current_user
app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)

# Cadastro (POST)
@app.route('/pessoas', methods=['POST'])
def cadastrar_pessoas():
    db_session = local_session()
    try:
        dados_pessoas = request.get_json()

        campos_obrigatorios = ["nome_pessoa", "cpf_pessoa", "cargo", "senha"]

        if not all(campo in dados_pessoas for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_pessoas[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            nome_pessoa = dados_pessoas["nome_pessoa"]
            cpf = dados_pessoas["cpf_pessoa"]
            cargo = dados_pessoas["cargo"]
            senha = dados_pessoas["senha"]

            if not cpf or len(cpf) != 11:
                return jsonify({"msg": "O CPF deve conter exatamente 11 dígitos numéricos."}), 400


            form_nova_pessoa = Pessoa(
                nome_pessoa=nome_pessoa,
                cpf_pessoa=cpf,
                cargo=cargo
            )
            form_nova_pessoa.set_senha_hash(senha)
            form_nova_pessoa.save(db_session)
            dicio = form_nova_pessoa.serialize()
            resultado = {"success": "Cadastrado com sucesso", "pessoas": dicio}

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()


@app.route('/produtos', methods=['POST'])
def cadastrar_produto():
    db_session = local_session()
    try:
        dados_produto = request.get_json()

        campos_obrigatorios = ["id_categoria", "nome_produto", "tamanho", "genero", "marca_produto", "custo_produto"]

        if not all(campo in dados_produto for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        if any(not dados_produto[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        else:
            id_categoria = dados_produto['id_categoria']
            nome_produto = dados_produto['nome_produto']
            tamanho = dados_produto['tamanho']
            marca_produto = dados_produto['marca_produto']
            custo_produto = dados_produto['custo_produto']
            genero = dados_produto['genero']
            form_novo_produto = Produto(
                id_categoria=id_categoria,
                nome_produto=nome_produto,
                tamanho=tamanho,
                marca_produto=marca_produto,
                custo_produto=custo_produto,
                genero=genero
            )
            form_novo_produto.save(db_session)
            dicio = form_novo_produto.serialize()
            resultado = {"success": "Cadastrado com sucesso", "produtos": dicio}

            return jsonify(resultado), 201

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route("/entradas", methods=["POST"])
def cadastrar_entrada():
    dados = request.json

    # Campos obrigatórios
    campos_obrigatorios = ["id_pessoa", "id_produto", "quantidade", "nota_fiscal", "valor_entrada"]
    if not all(campo in dados for campo in campos_obrigatorios):
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    if any(dados[campo] == "" for campo in campos_obrigatorios):
        return jsonify({"error": "Preencha todos os campos"}), 400

    # Verificar se o produto existe
    produto = local_session.query(Produto).filter_by(id_produto=dados["id_produto"]).first()
    if not produto:
        return jsonify({"error": "Insumo não encontrado"}), 404
    # Verificar se a pessoa existe
    pessoa = local_session.query(Pessoa).filter_by(id_pessoa=dados["id_pessoa"]).first()
    if not produto:
        return jsonify({"error": "Insumo não encontrado"}), 404

    data_entrada = str(datetime.now())

    # Validações numéricas
    try:
        qtd = int(dados["quantidade"])
        valor = float(dados["valor_entrada"])
    except ValueError:
        return jsonify({"error": "Quantidade e valor devem ser numéricos"}), 400

    if qtd <= 0 or valor <= 0:
        return jsonify({"error": "Quantidade e valor devem ser maiores que zero"}), 400

    # Atualiza o estoque do insumo
    produto.qtd_produto += qtd

    # Cria a entrada
    nova_entrada = Entrada(
        nota_fiscal=dados["nota_fiscal"],
        data_entrada=data_entrada,
        quantidade=qtd,
        valor_entrada=valor,
        id_produto=produto.id_produto,
        id_pessoa=pessoa.id_pessoa
    )

    try:
        nova_entrada.save(local_session)
        produto.save(local_session)

        return jsonify({
            "success": "Entrada cadastrada com sucesso",
            "entrada": nova_entrada.serialize()
        }), 201

    except Exception as e:
        return jsonify({"error": f"Erro ao salvar entrada: {str(e)}"}), 500

@app.route('/vendas', methods=['POST'])
def cadastrar_venda():
    db_session = local_session()
    try:
        dados = request.get_json()
        campos = ["forma_pagamento", "quantidade", "id_pessoa", "id_produto"]

        if not all(campo in dados for campo in campos):
            return jsonify({"error": "Campos obrigatórios não informados"}), 400

        forma_pagamento = dados["forma_pagamento"]
        quantidade = dados["quantidade"]
        data_emissao = str(datetime.now())
        id_produto = dados["id_produto"]
        id_pessoa = dados["id_pessoa"]

        produto = db_session.query(Produto).filter_by(id_produto=id_produto).first()
        pessoa = db_session.query(Pessoa).filter_by(id_pessoa=id_pessoa).first()

        if not produto:
            return jsonify({"error": "produto não encontrado"}), 404
        if not pessoa:
            return jsonify({"error": "Pessoa não encontrada"}), 404

        # Verificar estoque
        if produto.qtd_produto < quantidade:
            return jsonify({"error": f"Estoque insuficiente para: {produto.nome_produto}"}), 400

        # Dar baixa no produto
        produto = db_session.query(Produto).filter_by(id_produto=id_produto).first()
        produto.qtd_produto -= quantidade
        db_session.add(produto)

        # Registrar vendas
        vendas_registradas = []
        for _ in range(quantidade):
            nova_venda = Venda(
                data_emissao=data_emissao,
                id_produto=id_produto,
                id_pessoa=id_pessoa,
                quantidade=quantidade,
                valor_venda=produto.custo_produto,
                forma_pagamento=forma_pagamento,
            )
            nova_venda.save(db_session)
            venda_dict = nova_venda.serialize()
            # converter de volta para int no retorno
            vendas_registradas.append(venda_dict)

        return jsonify({
            "success": f"{quantidade} vendas registradas com sucesso",
            "vendas": vendas_registradas
        }), 201

    except Exception as e:
        db_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

@app.route('/categorias', methods=['POST'])
def cadastrar_categoria():
    db_session = local_session()
    try:
        dados_categoria = request.get_json()

        if not 'nome_categoria' in dados_categoria:
            return jsonify({
                "error": "Campo inexistente",
            })
        if dados_categoria['nome_categoria'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            })
        else:
            nome_categoria = dados_categoria['nome_categoria']
            form_nova_categoria = Categoria(
                nome_categoria=nome_categoria,
            )
            form_nova_categoria.save(db_session)

            dicio = form_nova_categoria.serialize()
            resultado = {"success": "Categoria cadastrada com sucesso", "categorias": dicio}

            return jsonify(resultado), 201
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

# LISTAR (GET)
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    db_session = local_session()
    try:

        sql_produto = select(Produto)
        resultado_produtos = db_session.execute(sql_produto).scalars()
        produtos = []

        for n in resultado_produtos:
            produtos.append(n.serialize())
        return jsonify({
            "produtos": produtos,
            "success": "Listado com sucesso",
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/categorias', methods=['GET'])
def listar_categorias():
    db_session = local_session()
    try:
        sql_categorias = select(Categoria)
        resultado_categorias = db_session.execute(sql_categorias).scalars()
        categorias = []
        for n in resultado_categorias:
            categorias.append(n.serialize())
        return jsonify({
            "categorias": categorias,
            "success": "Listado com sucesso",
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/entradas', methods=['GET'])
def listar_entradas():
    db_session = local_session()
    try:
        sql_entradas = select(Entrada)
        resultado_entradas = db_session.execute(sql_entradas).scalars()
        entradas = []
        for n in resultado_entradas:
            entradas.append(n.serialize())
        return jsonify({
            "entradas": entradas,
            "success": "Listado com sucesso",
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/vendas', methods=['GET'])
def listar_vendas():
    db_session = local_session()
    try:
        sql_vendas = select(Venda)
        venda_resultado = db_session.execute(sql_vendas).scalars()
        vendas = []
        for n in venda_resultado:
            vendas.append(n.serialize())
        return jsonify({
            "vendas": vendas
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/pessoas', methods=['GET'])
def listar_pessoas():
    db_session = local_session()
    try:
        sql_pessoa = select(Pessoa)
        resultado_pessoas = db_session.execute(sql_pessoa).scalars()
        pessoas = []
        for n in resultado_pessoas:
            pessoas.append(n.serialize())

        return jsonify({
            "pessoas": pessoas,
            "success": "Listado com sucesso"
        })
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

# EDITAR (PUT)
@app.route('/produtos/<id_produto>', methods=['PUT'])
def editar_produto(id_produto):
    db_session = local_session()
    try:
        dados_editar_produto = request.get_json()

        produto_resultado = db_session.execute(select(Produto).filter_by(id_produto=int(id_produto))).scalar()


        if not produto_resultado:
            return jsonify({"error": "produto não encontrado"}), 400

        campos_obrigatorios = ["id_categoria", "nome_produto", "tamanho", "genero", "marca_produto", "custo_produto"]

        if any(not dados_editar_produto[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        if not all(campo in dados_editar_produto for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        else:
            produto_resultado.nome_produto = dados_editar_produto['nome_produto']
            produto_resultado.tamanho = dados_editar_produto['tamanho']
            produto_resultado.marca_produto = dados_editar_produto['marca_produto']
            produto_resultado.custo_produto = dados_editar_produto['custo_produto']
            produto_resultado.genero = dados_editar_produto['genero']
            produto_resultado.id_categoria = dados_editar_produto['id_categoria']

            produto_resultado.save(db_session)
            dicio = produto_resultado.serialize()
            resultado = {"success": "produto editado com sucesso", "produtos": dicio}

            return jsonify(resultado), 201

    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
        }), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        db_session.close()

@app.route('/categorias/<id_categoria>', methods=['PUT'])
def editar_categoria(id_categoria):
    db_session = local_session()
    try:
        dados_editar_categoria = request.get_json()

        categoria_resultado = db_session.execute(select(Categoria).filter_by(id_categoria=int(id_categoria))).scalar()

        # Caso não exista a Categoria
        if not categoria_resultado:
            return jsonify({
                "error": "Categoria não encontrada"
            })

        # Caso o Campo não exista
        if not 'nome_categoria' in dados_editar_categoria:
            return jsonify({
                "error": "Campo inexistente"
            }), 400

        # Caso não tenha Preenchido todos os Campos
        if dados_editar_categoria['nome_categoria'] == "":
            return jsonify({
                "error": "Preencher todos os campos"
            }), 400

        # Tabela para Editar Categoria
        else:
            categoria_resultado.nome_categoria = dados_editar_categoria['nome_categoria']

            # Salva a Categoria
            categoria_resultado.save(db_session)

            dicio = categoria_resultado.serialize()
            resultado = {"success": "categoria editado com sucesso", "categorias": dicio}

            return jsonify(resultado), 200

    # Caso o Valor Inserido seja Inválido
    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
        }), 400

    # Caso exista algum Erro
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

@app.route('/pessoas/<id_pessoa>', methods=['PUT'])
# @jwt_required()
def editar_pessoa(id_pessoa):
    db_session = local_session()
    try:
        # Pega a Informação
        dados_editar_pessoa = request.get_json()

        pessoa_resultado = db_session.execute(select(Pessoa).filter_by(id_pessoa=int(id_pessoa))).scalar()

        # Caso não exista a Pessoa
        if not pessoa_resultado:
            return jsonify({"error": "Pessoa não encontrada"}), 400

        campos_obrigatorios = ["nome_pessoa", "cargo", "senha", "cpf_pessoa"]

        # Caso não tenha Preenchido todos os Campos
        if any(not dados_editar_pessoa[campo] for campo in campos_obrigatorios):
            return jsonify({"error": "Preencher todos os campos"}), 400

        # Caso não exista o Campo
        if not all(campo in dados_editar_pessoa for campo in campos_obrigatorios):
            return jsonify({"error": "Campo inexistente"}), 400

        # Edita a Tabela Pessoa
        else:
            pessoa_resultado.nome_pessoa = dados_editar_pessoa['nome_pessoa']
            pessoa_resultado.cargo = dados_editar_pessoa['cargo']
            pessoa_resultado.senha = dados_editar_pessoa['senha']
            pessoa_resultado.cpf_pessoa = dados_editar_pessoa['cpf_pessoa']

            # Salva a Senha Nova
            pessoa_resultado.set_senha_hash(pessoa_resultado.senha)
            pessoa_resultado.save(db_session)

            dicio = pessoa_resultado.serialize()
            resultado = {"success": "Pessoa editada com sucesso", "pessoas": dicio}

            return jsonify(resultado), 200

    # Caso o Valor Inserido seja Inválido
    except ValueError:
        return jsonify({
            "error": "Valor inserido inválido"
        })

    # Caso ocorra algum Erro
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        db_session.close()

# Inicia
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)