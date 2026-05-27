from db.conexao import conectar
from services.criptografia import (
    criptografar_cpf,
    descriptografar_cpf,
    gerar_chave_acesso,
    criptografar_chave
)


def cadastrar_eleitor(nome, cpf, titulo, is_mesario):
    conexao = conectar()

    if not conexao:
        return None

    try:
        cpf_criptografado = criptografar_cpf(cpf)
        chave_original = gerar_chave_acesso(nome)
        chave_criptografada = criptografar_chave(chave_original)

        cursor = conexao.cursor()
        sql = "INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso, is_mesario) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (nome, cpf_criptografado, titulo, chave_criptografada, is_mesario))
        conexao.commit()

        return chave_original

    except Exception as erro:
        print("Erro ao cadastrar eleitor:", erro)
        return None

    finally:
        conexao.close()


def listar_eleitores():
    conexao = conectar()

    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT id, nome, titulo_eleitor, is_mesario, ja_votou FROM eleitores ORDER BY nome")
        return cursor.fetchall()

    except Exception as erro:
        print("Erro ao listar eleitores:", erro)
        return []

    finally:
        conexao.close()


def buscar_eleitor_por_titulo(titulo):
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
    conexao = conectar()

    if not conexao:
        return False

    try:
        if cpf_foi_alterado:
            cpf_para_salvar = criptografar_cpf(novo_cpf)
        else:
            cpf_para_salvar = novo_cpf

        cursor = conexao.cursor()
        sql = "UPDATE eleitores SET nome = %s, cpf = %s, titulo_eleitor = %s WHERE titulo_eleitor = %s"
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
    if not primeiros_digitos.isdigit() or len(primeiros_digitos) != 4:
        print("Os 4 primeiros digitos do CPF devem ser numericos.")
        return None

    conexao = conectar()

    if not conexao:
        return None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eleitores WHERE titulo_eleitor = %s", (titulo,))
        eleitor = cursor.fetchone()

        if not eleitor:
            return None

        cpf_descriptografado = descriptografar_cpf(eleitor["cpf"])

        if cpf_descriptografado[:4] != primeiros_digitos:
            return None

        chave_criptografada = criptografar_chave(chave_acesso)

        if chave_criptografada != eleitor["chave_acesso"]:
            return None

        return eleitor

    except Exception as erro:
        print("Erro na autenticacao:", erro)
        return None

    finally:
        conexao.close()


def marcar_como_votou(eleitor_id):
    conexao = conectar()

    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute("UPDATE eleitores SET ja_votou = TRUE WHERE id = %s", (eleitor_id,))
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