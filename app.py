from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nome = request.form.get("nome", "")#Faço o get no form pelo name "nome"
        idade = request.form.get("idade", "")#Faço o get no form pelo name "idade"
        # Passa as variáveis via URL
        return redirect(url_for("home", nome=nome, idade=idade))
    return render_template("register.html")#se for GET, ou seja, apenas abrir a página, mostra o formulário HTML

@app.route("/home")
def home():
    # Pega as variáveis da URL
    nome = request.args.get("nome", "")#Pego o valor da variável nome via URL
    idade = request.args.get("idade", "")#Pego o valor da variável idade via URL
    if not nome or not idade or not idade.isdigit():
        return redirect(url_for("register"))
    else:
        return render_template("home.html", nome=nome, idade=idade)

if __name__ == "__main__":
    app.run(debug=True)