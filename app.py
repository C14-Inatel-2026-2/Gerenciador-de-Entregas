from flask import Flask

# Cria a aplicação que o Gunicorn vai procurar
app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "Gerenciador de Entregas rodando com sucesso!"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)