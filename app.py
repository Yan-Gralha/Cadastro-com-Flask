import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

JSON = "users.json"

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome", "")#Faço o get no form pelo name "nome"
        idade = request.form.get("idade", "")#Faço o get no form pelo name "idade"
        
        if nome != "" and idade != "":
            # Se o arquivo não existir, cria com lista vazia
            if not os.path.exists(JSON):
                with open(JSON, "w", encoding="utf-8") as f:
                    json.dump([], f)

            # Lê os dados existentes
            with open(JSON, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            # Gera ID único
            if usuarios:
                novo_id = max(u["id"] for u in usuarios) + 1
            else:
                novo_id = 1

            novo_usuario = {
                "id": novo_id,
                "nome": nome,
                "idade": idade
            }
            
            # Adiciona novo usuário
            usuarios.append(novo_usuario)

            # Salva novamente no arquivo
            with open(JSON, "w", encoding="utf-8") as f:
                json.dump(usuarios, f, ensure_ascii=False, indent=4)

            return redirect(url_for("login"))

    return render_template("register.html")#se for GET, ou seja, apenas abrir a página, mostra o formulário HTML
    
@app.route("/login", methods =["GET", "POST"])
def login():
    erro = ""
    if request.method == "POST":
        nome = request.form.get("nome", "")#Faço o get no form pelo name "nome"
        idade = request.form.get("idade", "")#Faço o get no form pelo name "idade"
        erro = "Erro: nome ou idade inválidos"
        if nome != "" and idade != "":
            with open(JSON, "r", encoding="utf-8") as f:
                usuarios = json.load(f)

            for i in usuarios:
                if i["nome"] == nome and i["idade"] == idade:
                    return redirect(url_for("home", nome=nome, idade=idade))               

    return render_template("login.html", erro=erro)

@app.route("/home")
def home():
    # Pega as variáveis da URL
    nome = request.args.get("nome", "")#Pego o valor da variável nome via URL
    idade = request.args.get("idade", "")#Pego o valor da variável idade via URL
    if not nome or not idade or not idade.isdigit():
        return redirect(url_for("login"))
    else:
        return render_template("home.html", nome=nome, idade=idade)


if __name__ == "__main__":
    app.run(debug=True)