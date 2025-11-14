from flask import Flask, jsonify, render_template, request, redirect, url_for, flash
from flask_jwt_extended import create_access_token, jwt_required, JWTManager

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "03050710"
jwt = JWTManager(app)

@app.route('/')
def index():
    return render_template('template.html')

@app.route('/clientes', methods=['GET', 'POST'])
def listar_clientes():
    return render_template('cadastro_pessoa.html')


# Inicia
if __name__ == '__main__':
    app.run(debug=True, port=5001)
