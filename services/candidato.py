from db.conexao import conectar


def listar_candidatos():
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM candidatos ORDER BY nome")
        dados = cursor.fetchall()
        return dados
    except Exception as erro:
        print("Erro ao listar candidatos:", erro)
        return []
    finally:
        if conexao:
            conexao.close()


def cadastrar_candidato(nome, numero, partido):
    conexao = conectar()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO candidatos (nome, numero, partido) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, numero, partido))
        conexao.commit()
        return True
    except Exception as erro:
        print("Falha no cadastro do candidato:", erro)
        return False
    finally:
        if conexao:
            conexao.close()


def buscar_candidato_por_numero(numero):
    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM candidatos WHERE numero = %s", (numero,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as erro:
        print("Erro na busca do candidato:", erro)
        return None
    finally:
        if conexao:
            conexao.close()


def editar_candidato(numero_atual, novo_nome, novo_numero, novo_partido):
    conexao = conectar()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        sql = "UPDATE candidatos SET nome = %s, numero = %s, partido = %s WHERE numero = %s"
        valores = (novo_nome, novo_numero, novo_partido, numero_atual)
        cursor.execute(sql, valores)
        conexao.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as erro:
        print("Erro ao editar candidato:", erro)
        return False
    finally:
        if conexao:
            conexao.close()


def remover_candidato(numero):
    conexao = conectar()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM candidatos WHERE numero = %s", (numero,))
        conexao.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as erro:
        print("Erro ao remover candidato:", erro)
        return False
    finally:
        if conexao:
            conexao.close()