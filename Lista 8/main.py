import psycopg2
from psycopg2 import sql
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

############################################
# CONFIGURAÇÕES DO BANCO    
############################################

DB_HOST = 'localhost'
DB_PORT = 5432
DB_NAME = 'seu_banco_de_dados'
DB_USER = 'seu_usuario'
DB_PASSWORD = 'sua_senha'

def get_connection():
    """
    Retorna uma conexão ativa com o PostgreSQL.
    """
    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )
    return conn

############################################
# CRIAÇÃO DAS TABELAS
############################################

def criar_tabelas():
    """
    Cria as tabelas no banco, caso não existam.
    """
    create_table_queries = [
        """
        CREATE TABLE IF NOT EXISTS usuario (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pedido (
            id SERIAL PRIMARY KEY,
            usuario_id INT NOT NULL,
            data_criacao TIMESTAMP NOT NULL,
            CONSTRAINT fk_usuario
                FOREIGN KEY(usuario_id)
                REFERENCES usuario(id)
                ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS produto (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL,
            preco NUMERIC(10, 2) NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS pedido_produto (
            id SERIAL PRIMARY KEY,
            pedido_id INT NOT NULL,
            produto_id INT NOT NULL,
            quantidade INT NOT NULL,
            CONSTRAINT fk_pedido
                FOREIGN KEY(pedido_id)
                REFERENCES pedido(id)
                ON DELETE CASCADE,
            CONSTRAINT fk_produto
                FOREIGN KEY(produto_id)
                REFERENCES produto(id)
                ON DELETE CASCADE
        );
        """
    ]

    conn = get_connection()
    cur = conn.cursor()
    for query in create_table_queries:
        cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()


############################################
# POPULANDO DADOS DE TESTE
############################################

def popular_dados_teste():
    """
    Insere dados de teste nas tabelas para demonstração.
    """
    conn = get_connection()
    cur = conn.cursor()

    # Inserir alguns usuários
    users = [
        ("João da Silva", "joao@example.com"),
        ("Maria Oliveira", "maria@example.com"),
        ("Pedro Santos", "pedro@example.com")
    ]
    for (nome, email) in users:
        cur.execute(
            "INSERT INTO usuario (nome, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING",
            (nome, email)
        )

    # Inserir alguns produtos
    produtos = [
        ("Laptop", 3500.00),
        ("Smartphone", 2000.00),
        ("Cadeira Gamer", 800.00),
        ("Monitor", 1200.00),
    ]
    for (nome, preco) in produtos:
        cur.execute(
            "INSERT INTO produto (nome, preco) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (nome, preco)
        )

    # Inserir um pedido para cada usuário
    cur.execute("SELECT id FROM usuario;")
    user_ids = [row[0] for row in cur.fetchall()]
    for uid in user_ids:
        cur.execute(
            """
            INSERT INTO pedido (usuario_id, data_criacao) 
            VALUES (%s, %s)
            RETURNING id
            """,
            (uid, datetime.datetime.now())
        )
        pedido_id = cur.fetchone()[0]

        # Vincular alguns produtos ao pedido (pedido_produto)
        cur.execute("SELECT id FROM produto;")
        product_ids = [row[0] for row in cur.fetchall()]

        # Exemplo: adicionar 2 produtos para cada pedido
        for produto_id in product_ids[:2]:
            cur.execute(
                """
                INSERT INTO pedido_produto (pedido_id, produto_id, quantidade) 
                VALUES (%s, %s, %s)
                """,
                (pedido_id, produto_id, 1)  # quantidade = 1
            )

    conn.commit()
    cur.close()
    conn.close()

############################################
# CRUD - USUÁRIO
############################################

@app.route('/usuarios', methods=['POST'])
def criar_usuario():
    data = request.json
    nome = data.get('nome')
    email = data.get('email')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO usuario (nome, email) VALUES (%s, %s) RETURNING id", (nome, email))
    novo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Usuário criado com sucesso!", "id": novo_id}), 201

@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email FROM usuario;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    usuarios = []
    for row in rows:
        usuarios.append({
            "id": row[0],
            "nome": row[1],
            "email": row[2],
        })
    return jsonify(usuarios), 200

@app.route('/usuarios/<int:usuario_id>', methods=['GET'])
def obter_usuario(usuario_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, email FROM usuario WHERE id = %s;", (usuario_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        usuario = {
            "id": row[0],
            "nome": row[1],
            "email": row[2]
        }
        return jsonify(usuario), 200
    else:
        return jsonify({"mensagem": "Usuário não encontrado"}), 404

@app.route('/usuarios/<int:usuario_id>', methods=['PUT'])
def atualizar_usuario(usuario_id):
    data = request.json
    nome = data.get('nome')
    email = data.get('email')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE usuario 
        SET nome = %s, email = %s
        WHERE id = %s
    """, (nome, email, usuario_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Usuário atualizado com sucesso!"}), 200

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def deletar_usuario(usuario_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM usuario WHERE id = %s", (usuario_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Usuário deletado com sucesso!"}), 200

############################################
# CRUD - PEDIDO
############################################

@app.route('/pedidos', methods=['POST'])
def criar_pedido():
    data = request.json
    usuario_id = data.get('usuario_id')
    data_criacao = datetime.datetime.now()  # ou data fornecida

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pedido (usuario_id, data_criacao)
        VALUES (%s, %s)
        RETURNING id
    """, (usuario_id, data_criacao))
    pedido_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Pedido criado com sucesso!", "pedido_id": pedido_id}), 201

@app.route('/pedidos', methods=['GET'])
def listar_pedidos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, usuario_id, data_criacao FROM pedido;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    pedidos = []
    for row in rows:
        pedidos.append({
            "id": row[0],
            "usuario_id": row[1],
            "data_criacao": row[2].isoformat()
        })
    return jsonify(pedidos), 200

@app.route('/pedidos/<int:pedido_id>', methods=['GET'])
def obter_pedido(pedido_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, usuario_id, data_criacao FROM pedido WHERE id = %s;", (pedido_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        pedido = {
            "id": row[0],
            "usuario_id": row[1],
            "data_criacao": row[2].isoformat()
        }
        return jsonify(pedido), 200
    else:
        return jsonify({"mensagem": "Pedido não encontrado"}), 404

@app.route('/pedidos/<int:pedido_id>', methods=['PUT'])
def atualizar_pedido(pedido_id):
    data = request.json
    # Exemplo simples: atualizar apenas o usuario_id
    usuario_id = data.get('usuario_id')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE pedido
        SET usuario_id = %s
        WHERE id = %s
    """, (usuario_id, pedido_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Pedido atualizado com sucesso!"}), 200

@app.route('/pedidos/<int:pedido_id>', methods=['DELETE'])
def deletar_pedido(pedido_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pedido WHERE id = %s", (pedido_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Pedido deletado com sucesso!"}), 200

############################################
# CRUD - PRODUTO
############################################

@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.json
    nome = data.get('nome')
    preco = data.get('preco')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO produto (nome, preco)
        VALUES (%s, %s)
        RETURNING id
    """, (nome, preco))
    produto_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Produto criado com sucesso!", "produto_id": produto_id}), 201

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco FROM produto;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    produtos = []
    for row in rows:
        produtos.append({
            "id": row[0],
            "nome": row[1],
            "preco": float(row[2])
        })
    return jsonify(produtos), 200

@app.route('/produtos/<int:produto_id>', methods=['GET'])
def obter_produto(produto_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, nome, preco FROM produto WHERE id = %s;", (produto_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        produto = {
            "id": row[0],
            "nome": row[1],
            "preco": float(row[2])
        }
        return jsonify(produto), 200
    else:
        return jsonify({"mensagem": "Produto não encontrado"}), 404

@app.route('/produtos/<int:produto_id>', methods=['PUT'])
def atualizar_produto(produto_id):
    data = request.json
    nome = data.get('nome')
    preco = data.get('preco')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE produto
        SET nome = %s, preco = %s
        WHERE id = %s
    """, (nome, preco, produto_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Produto atualizado com sucesso!"}), 200

@app.route('/produtos/<int:produto_id>', methods=['DELETE'])
def deletar_produto(produto_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM produto WHERE id = %s", (produto_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Produto deletado com sucesso!"}), 200

############################################
# CRUD - PEDIDO_PRODUTO
############################################

@app.route('/pedido_produto', methods=['POST'])
def adicionar_produto_ao_pedido():
    data = request.json
    pedido_id = data.get('pedido_id')
    produto_id = data.get('produto_id')
    quantidade = data.get('quantidade')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pedido_produto (pedido_id, produto_id, quantidade)
        VALUES (%s, %s, %s)
        RETURNING id
    """, (pedido_id, produto_id, quantidade))
    pp_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Produto adicionado ao pedido com sucesso!", "id": pp_id}), 201

@app.route('/pedido_produto', methods=['GET'])
def listar_pedido_produto():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, pedido_id, produto_id, quantidade
        FROM pedido_produto
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    lista = []
    for row in rows:
        lista.append({
            "id": row[0],
            "pedido_id": row[1],
            "produto_id": row[2],
            "quantidade": row[3]
        })
    return jsonify(lista), 200

@app.route('/pedido_produto/<int:pp_id>', methods=['GET'])
def obter_pedido_produto(pp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, pedido_id, produto_id, quantidade
        FROM pedido_produto
        WHERE id = %s
    """, (pp_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row:
        item = {
            "id": row[0],
            "pedido_id": row[1],
            "produto_id": row[2],
            "quantidade": row[3]
        }
        return jsonify(item), 200
    else:
        return jsonify({"mensagem": "Relacionamento não encontrado"}), 404

@app.route('/pedido_produto/<int:pp_id>', methods=['PUT'])
def atualizar_pedido_produto(pp_id):
    data = request.json
    quantidade = data.get('quantidade')

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE pedido_produto
        SET quantidade = %s
        WHERE id = %s
    """, (quantidade, pp_id))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Quantidade atualizada com sucesso!"}), 200

@app.route('/pedido_produto/<int:pp_id>', methods=['DELETE'])
def deletar_pedido_produto(pp_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM pedido_produto WHERE id = %s", (pp_id,))
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"mensagem": "Produto removido do pedido com sucesso!"}), 200

############################################
# CONSULTAS COMPLEXAS (JOINS, AGREGAÇÕES, ETC.)
############################################

@app.route('/relatorios/pedidos_por_usuario', methods=['GET'])
def pedidos_por_usuario():
    """
    Exemplo de consulta usando JOIN e agregação:
    - Retorna quantos pedidos cada usuário já fez.
    """
    conn = get_connection()
    cur = conn.cursor()
    # Exemplo de LEFT JOIN para trazer usuários sem pedidos também:
    cur.execute("""
        SELECT u.id, u.nome, COUNT(p.id) AS total_pedidos
        FROM usuario u
        LEFT JOIN pedido p ON u.id = p.usuario_id
        GROUP BY u.id
        ORDER BY total_pedidos DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "usuario_id": row[0],
            "nome": row[1],
            "total_pedidos": row[2]
        })

    return jsonify(resultado), 200

@app.route('/relatorios/faturamento_por_pedido', methods=['GET'])
def faturamento_por_pedido():
    """
    Exemplo de JOINs para calcular o faturamento de cada pedido:
    1. Une pedido com pedido_produto (INNER JOIN)
    2. Une produto para buscar o preço
    3. Calcula total do pedido = SUM(preco * quantidade)
    4. Agrupa por pedido
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            p.id AS pedido_id,
            u.nome AS nome_usuario,
            SUM(prod.preco * pp.quantidade) AS valor_total
        FROM pedido p
        INNER JOIN usuario u ON p.usuario_id = u.id
        INNER JOIN pedido_produto pp ON p.id = pp.pedido_id
        INNER JOIN produto prod ON pp.produto_id = prod.id
        GROUP BY p.id, u.nome
        ORDER BY valor_total DESC;
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()

    resultado = []
    for row in rows:
        resultado.append({
            "pedido_id": row[0],
            "nome_usuario": row[1],
            "valor_total": float(row[2])
        })

    return jsonify(resultado), 200

############################################
# MAIN
############################################

if __name__ == '__main__':
    # 1. Cria as tabelas
    criar_tabelas()
    
    # 2. (Opcional) Popula alguns dados de teste.
    popular_dados_teste()
    
    # 3. Executa o servidor Flask
    app.run(debug=True, port=5000)
