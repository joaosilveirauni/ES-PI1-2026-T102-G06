from db.conexao import conectar
from services.criptografia import gerar_protocolo, criptografar_protocolo


def zerar_votos():
    conexao = conectar()

    if not conexao:
        return False, []

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM votos")
        conexao.commit()

        cursor.execute("SELECT nome, numero, partido FROM candidatos ORDER BY nome")

        colunas = ["nome", "numero", "partido"]
        linhas = cursor.fetchall()

        candidatos = []
        for linha in linhas:
            candidato = {}
            for i in range(len(colunas)):
                candidato[colunas[i]] = linha[i]
            candidatos.append(candidato)

        return True, candidatos

    except Exception as erro:
        print("Erro ao zerar votos:", erro)
        return False, []

    finally:
        conexao.close()


def registrar_voto(eleitor_id, candidato_id, numero_candidato, tipo):
    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT ja_votou FROM eleitores WHERE id = %s", (eleitor_id,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Eleitor nao encontrado no banco.")
            return None

        if resultado[0]:
            print("Eleitor ja votou! Voto nao registrado.")
            return None

        protocolo_original = gerar_protocolo(numero_candidato)
        protocolo_criptografado = criptografar_protocolo(protocolo_original)

        cursor.execute(
            "INSERT INTO votos (candidato_id, tipo, protocolo) VALUES (%s, %s, %s)",
            (candidato_id, tipo, protocolo_criptografado)
        )

        cursor.execute(
            "UPDATE eleitores SET ja_votou = TRUE WHERE id = %s",
            (eleitor_id,)
        )

        conexao.commit()

        return protocolo_original

    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar voto:", erro)
        return None

    finally:
        conexao.close()


def buscar_resultado():
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        sql = """
            SELECT c.nome, c.numero, c.partido, COUNT(v.id) AS total_votos
            FROM candidatos c
            LEFT JOIN votos v ON v.candidato_id = c.id AND v.tipo = 'VALIDO'
            GROUP BY c.id, c.nome, c.numero, c.partido
            ORDER BY c.nome
        """
        cursor.execute(sql)
        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao buscar resultado:", erro)
        return []

    finally:
        conexao.close()


def buscar_votos_nulos():
    conexao = conectar()

    if not conexao:
        return 0

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM votos WHERE tipo = 'NULO'")
        return cursor.fetchone()[0]

    except Exception as erro:
        print("Erro ao contar votos nulos:", erro)
        return 0

    finally:
        conexao.close()


def buscar_estatisticas():
    conexao = conectar()

    if not conexao:
        return 0, 0

    try:
        cursor_votaram = conexao.cursor()
        cursor_votaram.execute("SELECT COUNT(*) FROM eleitores WHERE ja_votou = TRUE")
        votaram = cursor_votaram.fetchone()[0]

        cursor_total = conexao.cursor()
        cursor_total.execute("SELECT COUNT(*) FROM eleitores")
        total = cursor_total.fetchone()[0]

        return votaram, total

    except Exception as erro:
        print("Erro ao buscar estatisticas:", erro)
        return 0, 0

    finally:
        conexao.close()


def buscar_votos_por_partido():
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        sql = """
            SELECT c.partido, COUNT(v.id) AS total_votos
            FROM candidatos c
            LEFT JOIN votos v ON v.candidato_id = c.id AND v.tipo = 'VALIDO'
            GROUP BY c.partido
            ORDER BY total_votos DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao buscar votos por partido:", erro)
        return []

    finally:
        conexao.close()


def buscar_total_votos_urna():
    conexao = conectar()

    if not conexao:
        return 0

    try:
        cursor = conexao.cursor()
        cursor.execute("SELECT COUNT(*) FROM votos")
        return cursor.fetchone()[0]

    except Exception as erro:
        print("Erro ao buscar total de votos:", erro)
        return 0

    finally:
        conexao.close()


def listar_protocolos():
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT protocolo, data_voto FROM votos ORDER BY protocolo")
        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao listar protocolos:", erro)
        return []

    finally:
        conexao.close()