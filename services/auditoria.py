from db.conexao import conectar

def registrar_ocorrencia(mensagem):
    conexao = conectar()
    if not conexao:
        print(f"\n[AUDITORIA - LOG]: {mensagem}")
        return False

    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO auditoria (mensagem, data_hora) VALUES (%s, NOW())"
        cursor.execute(sql, (mensagem,))
        conexao.commit()
        return True
    except Exception as erro:
        print(f"Falha ao registrar auditoria: {erro}")
        return False
    finally:
        if conexao:
            conexao.close()


def listar_ocorrencias():
    conexao = conectar()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT mensagem, data_hora FROM auditoria ORDER BY data_hora DESC")
        return cursor.fetchall()
    except Exception as erro:
        print(f"Erro ao ler auditoria: {erro}")
        return []
    finally:
        if conexao:
            conexao.close()

def exibir_ocorrencias():
    ocorrencias = listar_ocorrencias()

    if not ocorrencias:
        print("\nNenhuma ocorrência encontrada.")
        return

    print("\n===== LOG DE AUDITORIA =====")

    for i, item in enumerate(ocorrencias, start=1):
        data = item.get("data_hora")
        mensagem = item.get("mensagem")

        print(f"\n[{i}] {data}")
        print(f"Mensagem: {mensagem}")

    print("\n===== FIM DO LOG =====\n")

#def listar_protocolos():
#    conexao = conectar()
#
#    if not conexao:
#        return []
#
#    try:
#        cursor = conexao.cursor(dictionary=True)
#
#        sql = """
#        SELECT id, eleitor_id, candidato_id, tipo, data_voto
#        FROM votos
#        ORDER BY data_voto DESC
#        """
#
#        cursor.execute(sql)
#        return cursor.fetchall()
#
#    except Exception as erro:
#        print(f"Erro ao listar protocolos: {erro}")
#        return []
#    finally:
#        if conexao:
#            conexao.close()
