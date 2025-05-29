from flask import Flask, request, redirect, url_for, session, flash, send_from_directory
import mysql.connector
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, static_url_path='', static_folder='HTML')
app.secret_key = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = os.path.join('HTML/uploads')

# Conexão com o banco
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

# Página inicial (HTML estático)
@app.route('/')
def index():
    return send_from_directory('HTML', 'index.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute('SELECT * FROM usuario WHERE email = %s', (email,))
        usuario = cursor.fetchone()
        conn.close()

        if usuario and usuario['senha'] == senha:
            session['usuario_id'] = usuario['id']
            return redirect(url_for('index'))
        else:
            flash('Login inválido.')

    return send_from_directory('HTML', 'login.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_id', None)
    return redirect(url_for('index'))

# Cadastro de usuário
@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuario (nome, email, senha) VALUES (%s, %s, %s)', (nome, email, senha))
        conn.commit()
        conn.close()

        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('index'))

    return send_from_directory('HTML', 'conta.html')

# Cadastro de produto
@app.route('/cadastro_produto', methods=['GET', 'POST'])
def cadastro_produto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        print("Recebi o formulário:", request.form)  # Debug no terminal

        nome = request.form['nome']
        categoria = request.form['categoria']
        descricao = request.form['descricao']
        cidade_id = request.form['cidade']
        entrega_ids = request.form.getlist('entregas')
        imagem = request.files['imagem']
        filename = secure_filename(imagem.filename)
        imagem_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        imagem.save(imagem_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO produto (nome, categoria, descricao, imagem, usuario_id, cidade_id) VALUES (%s, %s, %s, %s, %s, %s)', 
                       (nome, categoria, descricao, 'uploads/' + filename, session['usuario_id'], cidade_id))
        produto_id = cursor.lastrowid

        for entrega_id in entrega_ids:
            cursor.execute('INSERT INTO produto_entrega (produto_id, entrega_id) VALUES (%s, %s)', (produto_id, entrega_id))

        conn.commit()
        conn.close()

        flash('Produto cadastrado com sucesso!')
        return redirect(url_for('index'))

    return send_from_directory('HTML', 'cadproduto.html')

# Servir CSS
@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('HTML/css', filename)

# Servir imagens
@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('HTML/img', filename)

# Servir JS
@app.route('/script/<path:filename>')
def serve_script(filename):
    return send_from_directory('HTML/script', filename)

if __name__ == '__main__':
    app.run(debug=True)
