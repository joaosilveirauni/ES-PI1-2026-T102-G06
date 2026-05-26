
from services.criptografia import (
    criptografar_cpf,
    descriptografa_cpf,    
    criptografar_chave
)


def cadastrar_eleitor(nome, cpf, titulo, is_mesario):
    """
    Cadastra um novo eleitor no banco.
    - Criptografa o CPF antes de salvar.
    - Gera e criptografa a chave de acesso.
    - Retorna a chave ORIGINAL para exibir ao usuário (apenas uma vez).
    - Retorna None se houver erro (ex: CPF ou título duplicado).
    """
    conexao = conectar()

    if not conexao:
        return None

    try:
        # Criptografa o CPF para armazenar de forma segura
        cpf_criptografado = criptografar_cpf(cpf)

        # Gera a chave de acesso a partir do nome do eleitor
        chave_original = gerar_chave_acesso(nome)

        # Criptografa a chave antes de salvar no banco
        chave_criptografada = criptografar_chave(chave_original)

        cursor = conexao.cursor()
        sql = """
            INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso, is_mesario)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (nome, cpf_criptografado, titulo, chave_criptografada, is_mesario))
        conexao.commit()

        # Retorna a chave original — ela só aparece neste momento
        return chave_original

    except Exception as erro:
        print("Erro ao cadastrar eleitor:", erro)
        return None

    finally:
        conexao.close()



def listar_eleitores():
    """
    Retorna todos os eleitores cadastrados.
    O CPF não é incluído na listagem por segurança (dado sensível).
    """
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)

        # Não seleciona o CPF — dado sensível não deve aparecer na listagem geral
        cursor.execute("""
            SELECT id, nome, titulo_eleitor, is_mesario, ja_votou
            FROM eleitores
            ORDER BY nome
        """)

        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao listar eleitores:", erro)
        return []

    finally:
        conexao.close()


def buscar_eleitor_por_titulo(titulo):
    """
    Busca um eleitor pelo número do título eleitoral.
    Retorna o dicionário com os dados do eleitor ou None se não encontrado.
    """
    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nome, titulo_eleitor, is_mesario, ja_votou FROM eleitores WHERE titulo_eleitor = %s",
            (titulo,)
        )
        return cursor.fetchone()

    except Exception as erro:
        print("Erro ao buscar eleitor por titulo:", erro)
        return None

    finally:
        conexao.close()


def buscar_eleitor_por_cpf(cpf):
    """
    Busca um eleitor pelo CPF.
    O CPF informado é criptografado antes da consulta,
    pois no banco ele também está criptografado.
    """
    conexao = conectar()

    if not conexao:
        return None

    try:
        cpf_criptografado = criptografar_cpf(cpf)

        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, nome, titulo_eleitor, is_mesario, ja_votou FROM eleitores WHERE cpf = %s",
            (cpf_criptografado,)
        )
        return cursor.fetchone()

    except Exception as erro:
        print("Erro ao buscar eleitor por CPF:", erro)
        return None

    finally:
        conexao.close()


def editar_eleitor(titulo_atual, novo_nome, novo_cpf, novo_titulo, cpf_foi_alterado):
    """
    Atualiza os dados de um eleitor existente.

    PARÂMETRO NOVO: cpf_foi_alterado (True ou False)
    - Se True:  o novo_cpf é um CPF limpo (vindo do usuário) → criptografar antes de salvar.
    - Se False: o novo_cpf já está criptografado (veio do banco sem alteração) → salvar direto.

    Isso evita o bug de criptografar o CPF duas vezes.
    """
    conexao = conectar()

    if not conexao:
        return False

    try:
        # Só criptografa se o CPF foi de fato alterado pelo usuário
        if cpf_foi_alterado:
            cpf_para_salvar = criptografar_cpf(novo_cpf)
        else:
            cpf_para_salvar = novo_cpf  # Já está criptografado, usa como está

        cursor = conexao.cursor()
        sql = """
            UPDATE eleitores
            SET nome = %s, cpf = %s, titulo_eleitor = %s
            WHERE titulo_eleitor = %s
        """
        cursor.execute(sql, (novo_nome, cpf_para_salvar, novo_titulo, titulo_atual))
        conexao.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as erro:
        print("Erro ao editar eleitor:", erro)
        return False

    finally:
        conexao.close()


def remover_eleitor(titulo):
    """
    Remove um eleitor do banco pelo título eleitoral.
    Retorna True se removido com sucesso, False caso contrário.
    """
    conexao = conectar()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM eleitores WHERE titulo_eleitor = %s", (titulo,))
        conexao.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as erro:
        print("Erro ao remover eleitor:", erro)
        return False

    finally:
        conexao.close()


def autenticar_eleitor(titulo, primeiros_digitos, chave_acesso):
    """
    Autentica um eleitor verificando três informações:
      1. Título eleitoral (busca no banco)
      2. 4 primeiros dígitos do CPF (descriptografa o CPF salvo para comparar)
      3. Chave de acesso (criptografa a fornecida e compara com a salva)

    Retorna o dicionário do eleitor se autenticado, ou None se falhar.
    """
    # Validação básica: os 4 dígitos devem ser numéricos
    if not primeiros_digitos.isdigit() or len(primeiros_digitos) != 4:
        print("Os 4 primeiros digitos do CPF devem ser numericos.")
        return None

    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor(dictionary=True)

        # Busca o eleitor pelo título
        cursor.execute("SELECT * FROM eleitores WHERE titulo_eleitor = %s", (titulo,))
        eleitor = cursor.fetchone()

        if not eleitor:
            return None

        # ── Verificação 1: 4 primeiros dígitos do CPF ──
        # O CPF está criptografado no banco, então descriptografamos para comparar
        cpf_descriptografado = descriptografar_cpf(eleitor["cpf"])

        if cpf_descriptografado[:4] != primeiros_digitos:
            return None

        # ── Verificação 2: Chave de acesso ──
        # Criptografamos a chave fornecida e comparamos com a que está no banco
        chave_criptografada = criptografar_chave(chave_acesso)

        if chave_criptografada != eleitor["chave_acesso"]:
            return None

        # Autenticação bem-sucedida
        return eleitor

    except Exception as erro:
        print("Erro na autenticacao:", erro)
        return None

    finally:
        conexao.close()




def marcar_como_votou(eleitor_id):
    """
    Marca o eleitor como 'ja_votou = TRUE' no banco.
    Chamado imediatamente após a confirmação do voto.
    Retorna True se atualizado com sucesso, False caso contrário.
    """
    conexao = conectar()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "UPDATE eleitores SET ja_votou = TRUE WHERE id = %s",
            (eleitor_id,)
        )
        conexao.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False

    except Exception as erro:
        print("Erro ao marcar eleitor como votou:", erro)
        return False

    finally:
        conexao.close()