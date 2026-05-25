from services.criptografia import criptografar_cpf, descriptografa_cpf
from db.conexao import conectar
import random
from db.conexao import conectar


def gerar_chave_acesso(nome):
    prefixo = ""
    contador = 0

    for letra in nome.upper():
        if letra.isalpha() and contador < 3:
            prefixo = prefixo + letra
            contador = contador + 1

    while len(prefixo) < 3:
        prefixo = prefixo + "X"

    sufixo = "".join(str(random.randint(0, 9)) for _ in range(5))

    return prefixo + sufixo


def listar_eleitores():
    conexao = conectar()
    if not conexao:
        return []

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT nome, cpf, titulo_eleitor, is_mesario, ja_votou FROM eleitores"
        )
        dados = cursor.fetchall()
        return dados
    except Exception as erro:
        print("Erro ao listar eleitores:", erro)
        return []
    finally:
        if conexao:
            conexao.close()


def cadastrar_eleitor(nome, cpf, titulo, is_mesario):
    if buscar_eleitor_por_cpf(cpf) or buscar_eleitor_por_titulo(titulo):
        print("Erro: Já existe um eleitor cadastrado com este CPF ou Título.")
        return None

    conexao = conectar()
    if not conexao:
        return None

    chave = gerar_chave_acesso(nome)
    cpf_cifrado = criptografar_cpf(cpf)
    cpf_cifrado = ''.join(str(n) for n in cpf_cifrado) # Converte a lista para uma string
    cpf_cifrado = ''.join(str(n) for n in cpf_cifrado)
    print(f"CPF cifrado: {cpf_cifrado} | Tamanho: {len(cpf_cifrado)}")  # linha 53

    try:
        cursor = conexao.cursor()
        sql = "INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso, is_mesario) VALUES (%s, %s, %s, %s, %s)"
        valores = (nome, cpf_cifrado, titulo, chave, is_mesario)
        cursor.execute(sql, valores)
        conexao.commit()
        return chave
    except Exception as erro:
        print("Falha no cadastro:", erro)
        return None
    finally:
        if conexao:
            conexao.close()


def buscar_eleitor_por_titulo(titulo):
    conexao = conectar()
    if not conexao:
        return None

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute(
            "SELECT * FROM eleitores WHERE titulo_eleitor = %s", (titulo,)
        )
        resultado = cursor.fetchone()
        return resultado
    except Exception as erro:
        print("Erro na busca por título:", erro)
        return None
    finally:
        if conexao:
            conexao.close()


def buscar_eleitor_por_cpf(cpf):
    conexao = conectar()
    if not conexao:
        return None

    cpf_cifrado = criptografar_cpf(cpf)
    cpf_cifrado = ''.join(str(n) for n in cpf_cifrado) # Converte a lista para uma string

    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM eleitores WHERE cpf = %s", (cpf_cifrado,))
        resultado = cursor.fetchone()
        return resultado
    except Exception as erro:
        print("Erro na busca por CPF:", erro)
        return None
    finally:
        if conexao:
            conexao.close()


def editar_eleitor(titulo_atual, novo_nome, novo_cpf, novo_titulo):
    conexao = conectar()
    if not conexao:
        return False

    nova_chave = gerar_chave_acesso(novo_nome)

    try:
        cursor = conexao.cursor()
        sql = "UPDATE eleitores SET nome = %s, cpf = %s, titulo_eleitor = %s, chave_acesso = %s WHERE titulo_eleitor = %s"
        valores = (novo_nome, novo_cpf, novo_titulo, nova_chave, titulo_atual)
        cursor.execute(sql, valores)
        conexao.commit()

        return cursor.rowcount > 0
    except Exception as erro:
        print("Erro ao editar eleitor:", erro)
        return False
    finally:
        if conexao:
            conexao.close()


def remover_eleitor(titulo):
    conexao = conectar()
    if not conexao:
        return False

    try:
        cursor = conexao.cursor()
        cursor.execute(
            "DELETE FROM eleitores WHERE titulo_eleitor = %s", (titulo,)
        )
        conexao.commit()

        return cursor.rowcount > 0
    except Exception as erro:
        print("Erro ao remover eleitor:", erro)
        return False
    finally:
        if conexao:
            conexao.close()


def autenticar_eleitor(titulo, primeiros_digitos_cpf, chave_digitada):
    eleitor = buscar_eleitor_por_titulo(titulo)

    if not eleitor:
        return None
    
    # descriptografa o CPF do banco para comparar
    cpf_original = descriptografa_cpf([int(d) for d in eleitor["cpf"]])

    if not cpf_original.startswith(primeiros_digitos_cpf):
        return None

    if eleitor["chave_acesso"].strip() != chave_digitada.strip().upper():
        return None
    

    return eleitor
