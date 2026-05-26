
from db.conexao import conectar
from services.criptografia import (
    criptografar_cpf,
    descriptografar_cpf,
    gerar_chave_acesso,
    criptografar_chave
)
 

def cadastrar_eleitor(nome, cpf, titulo, is_mesario):
  
 
    if not conexao:
        return None
 
    try:
     
        cpf_criptografado = criptografar_cpf(cpf)
 
       
        chave_original = gerar_chave_acesso(nome)
 
        
        chave_criptografada = criptografar_chave(chave_original)
 
        cursor = conexao.cursor()
        sql = """
            INSERT INTO eleitores (nome, cpf, titulo_eleitor, chave_acesso, is_mesario)
            VALUES (%s, %s, %s, %s, %s)
        """
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