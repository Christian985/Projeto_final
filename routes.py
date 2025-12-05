from flask import request
import requests

# ATULIZAR COM O LINK DA API
base_url = "http://10.135.232.46:5009"


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
        resp = requests.get(f"{base_url}/pessoas", timeout=5)
        resp.raise_for_status()
        data = resp.json()
        # Normaliza: se não houver a chave 'pessoas', retorna lista vazia junto com o erro
        if not isinstance(data, dict) or "pessoas" not in data:
            logger.error("Resposta inesperada de /pessoas: %s", data)
            return {"pessoas": [], "error": "Resposta inválida da API", "raw": data}
        return data
    except requests.exceptions.RequestException as e:
        logger.exception("Falha ao chamar API /pessoas")
        return {"pessoas": [], "error": str(e)}
    except ValueError as e:
        # JSON inválido
        logger.exception("JSON inválido recebido de /pessoas")
        return {"pessoas": [], "error": "JSON inválido", "raw_text": resp.text if 'resp' in locals() else None}

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
        url = f"{base_url}/categorias"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }


def get_vendas():
    try:
        url = f"{base_url}/vendas"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }



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
            "qtd_produto": form_data.get("qtd_produto"),
            "marca_produto": form_data.get("marca_produto"),
            "custo_produto": form_data.get("custo_produto"),
            "status": form_data.get("status"),
        }
        response = requests.post(
            f"{base_url}/produtos/cadastrar",
            json=payload
        )
        return response.json()
    except Exception as e:
        return {"error": str(e)}




def post_categoria(form_data):
    try:
        payload = {
            "nome_categoria": form_data.get("nome_categoria")
        }

        # manda lá pra API doida
        response = requests.post(
            f"{base_url}/cadastrar_categorias",
            json=payload
        )

        return response.json()

    except Exception as e:
        return {"error": str(e)}
