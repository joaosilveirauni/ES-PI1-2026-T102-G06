from db.conexao import conectar

def listar_eleitores():
    """Retorna uma lista com nome e título de todos os eleitores."""
    conexao = conectar()
    
    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT nome, titulo_eleitor FROM eleitores")
        dados = cursor.fetchall()
        return dados
    except Exception as erro:
        print(f"Erro ao listar eleitores: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

def cadastrar_eleitor(nome, cpf, titulo, chave):
    """Insere um novo eleitor no banco de dados."""
    conexao = conectar()
    if not conexao:
        return False
    try:
        cursor = conexao.cursor()
        sql = """
            INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso) 
            VALUES (%s, %s, %s, %s)
        """
        valores = (nome, cpf, titulo, chave)
        cursor.execute(sql, valores)
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Falha no cadastro: {erro}")
        return False
    finally:
        if conexao:
            conexao.close()

def buscar_eleitor_por_titulo(titulo):
    """Busca os dados completos de um eleitor através do título."""
    conexao = conectar()
    if not conexao:
        return None
    try:
        cursor = conexao.cursor(dictionary=True)
        sql = "SELECT * FROM eleitores WHERE titulo_eleitor = %s"
        cursor.execute(sql, (titulo,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as erro:
        print(f"Erro na busca: {erro}")
        return None
    finally:
        if conexao:
            conexao.close()
