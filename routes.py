import requests

# ATULIZAR COM O LINK DA API
base_url = "http://10.135.233.149:5000"

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
def get_usuarios():
    try:
        url = f"{base_url}/usuarios"
        # response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }
def get_produtos():
    try:
        url = f"{base_url}/produtos"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(e)
        return {
            "error": f"{e}",
        }
# print(get_produtos()['produtos'])