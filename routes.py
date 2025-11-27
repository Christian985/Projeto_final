from flask import request
import requests

# ATULIZAR COM O LINK DA API
base_url = "http://10.135.232.46:5000"

#=======================================================================================================================
# EXEMPLO DE FUNÇÕES
#=======================================================================================================================


#===========================================
# EXEMPLO DE POST
#===========================================
def post_login(email, senha):
    try:
        url = f"{base_url}/login"
        dados = {
            "email": email,
            "senha": senha,
        }
        response = requests.post(url, json=dados)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }

#===========================================
# EXEMPLO DE GET
#===========================================
def get_pessoas():
    try:
        response = requests.get(f"{base_url}/pessoas")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }
def get_produtos():
    try:
        response = requests.get(f"{base_url}/produtos/listar")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }
def get_categorias():
    try:
        url = f"{base_url}/categoria"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }
import requests

base_url = "http://10.135.232.46:5000"

def post_pessoa(form_data):
    try:
        # form_data vem do app.py — campos crus do form
        payload = {
            "nome_pessoa": form_data.get("nome_pessoa"),
            "cpf_pessoa": form_data.get("cpf_pessoa"),
            "cargo": form_data.get("cargo"),
            "senha": form_data.get("senha"),
            "status": form_data.get("status"),
        }

        # Normaliza CPF
        if payload["cpf_pessoa"]:
            payload["cpf_pessoa"] = ''.join(filter(str.isdigit, payload["cpf_pessoa"]))

        # Envia JSON para a API (isso faz request.get_json funcionar)
        response = requests.post(
            f"{base_url}/pessoas/cadastrar",
            json=payload
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}

def post_produtos(form_data):
    try:
        payload = {
            "id_categoria": form_data.get("id_categoria"),
            "nome_produto": form_data.get("nome_produto"),
            "tamanho": form_data.get("tamanho"),
            "genero": form_data.get("genero"),
            "marca_produto": form_data.get("marca_produto"),
            "custo_produto": form_data.get("custo_produto"),
            "status": form_data.get("status"),
        }
        response = requests.post(
            f"{base_url}/produtos/cadastrar/api",
            json=payload
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}




