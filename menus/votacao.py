from datetime import datetime
from db.conexao import conectar
from services.criptografia import (
    descriptografar_protocolo,
    gerar_protocolo,
    criptografar_protocolo
)
from services.auditoria import registrar_ocorrencia
import os

def menu_votacao():
    """
    Exibe o menu do modulo de votacao.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    opcao = ""

    os.system('cls')
    try:
        while opcao != "0":
            print("\n=== MODULO DE VOTAÇÃO ===")
            print("1 - Abrir Sistema de Votação")
            print("2 - Auditoria da Votação")
            print("3 - Resultados da Votação")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                from menus.submenu.sistemavotacao import abrir_sistema_votacao
                abrir_sistema_votacao()
            elif opcao == "2":
                from menus.submenu.auditoria import auditoria
                auditoria()
            elif opcao == "3":
                from menus.submenu.resultados import resultados
                resultados()
            elif opcao == "0":
                return
            else:
                print("Opcao invalida!")
    except Exception as erro:
        print("Erro no modulo de votacao:", erro)


def zerar_votos():
    """
    Executa a rotina zerar_votos.
    
    Args:
        Nenhum.
    
    Returns:
        tuple: Resultado da funcao.
    """
    conexao = conectar()

    if not conexao:
        return False, []

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM votos")
        cursor.execute("UPDATE eleitores SET ja_votou = FALSE")
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
        conexao.rollback()
        print("Erro ao zerar votos:", erro)
        return False, []

    finally:
        conexao.close()


def registrar_voto(eleitor_id, candidato_id, numero_candidato, tipo):
    """
    Executa a rotina registrar_voto.
    
    Args:
        eleitor_id (int): Valor usado pela funcao.
        candidato_id (int): Valor usado pela funcao.
        numero_candidato (int): Valor usado pela funcao.
        tipo (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor()

        cursor.execute("SELECT ja_votou FROM eleitores WHERE id = %s", (eleitor_id,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Eleitor nao encontrado no banco.")
            registrar_ocorrencia("ALERTA: Tentativa de acesso negado")
            return None

        if resultado[0]:
            print("Eleitor ja votou! Voto nao registrado.")
            registrar_ocorrencia("ALERTA: Tentativa de voto duplo")
            return None

        protocolo_original = gerar_protocolo(numero_candidato)
        protocolo_criptografado = criptografar_protocolo(protocolo_original)
        data_voto = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute(
            "INSERT INTO votos (eleitor_id, candidato_id, tipo, protocolo, data_voto) VALUES (%s, %s, %s, %s, %s)",
            (eleitor_id, candidato_id, tipo, protocolo_criptografado, data_voto)
        )

        cursor.execute(
            "UPDATE eleitores SET ja_votou = TRUE WHERE id = %s",
            (eleitor_id,)
        )

        conexao.commit()

        registrar_ocorrencia("SUCESSO: Voto realizado com sucesso")

        return protocolo_original

    except Exception as erro:
        conexao.rollback()
        print("Erro ao registrar voto:", erro)
        return None

    finally:
        conexao.close()


def buscar_resultado():
    """
    Executa a rotina buscar_resultado.
    
    Args:
        Nenhum.
    
    Returns:
        list: Resultado da funcao.
    """
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
    """
    Executa a rotina buscar_votos_nulos.
    
    Args:
        Nenhum.
    
    Returns:
        int: Resultado da funcao.
    """
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
    """
    Executa a rotina buscar_estatisticas.
    
    Args:
        Nenhum.
    
    Returns:
        tuple: Resultado da funcao.
    """
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
    """
    Executa a rotina buscar_votos_por_partido.
    
    Args:
        Nenhum.
    
    Returns:
        list: Resultado da funcao.
    """
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
            ORDER BY c.partido
        """
        cursor.execute(sql)
        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao buscar votos por partido:", erro)
        return []

    finally:
        conexao.close()


def buscar_total_votos_urna():
    """
    Executa a rotina buscar_total_votos_urna.
    
    Args:
        Nenhum.
    
    Returns:
        int: Resultado da funcao.
    """
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
    """
    Executa a rotina listar_protocolos.
    
    Args:
        Nenhum.
    
    Returns:
        list: Resultado da funcao.
    """
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT protocolo, data_voto FROM votos")
        dados = cursor.fetchall()

        protocolos = []
        for item in dados:
            protocolo = {}
            protocolo["protocolo"] = descriptografar_protocolo(item["protocolo"])
            protocolo["data_voto"] = item["data_voto"]
            protocolos.append(protocolo)

        protocolos.sort(key=lambda item: item["protocolo"])
        return protocolos

    except Exception as erro:
        print("Erro ao listar protocolos:", erro)
        return []

    finally:
        conexao.close()
