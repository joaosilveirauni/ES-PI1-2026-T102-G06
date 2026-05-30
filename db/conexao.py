import mysql.connector

def conectar():
    """
    Executa a rotina conectar.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    try:
        conexao = mysql.connector.connect(
            host="BD-ACD",
            user="BD250226117",
            password="Jujyo9",
            database="BD250226117"
        )
        return conexao
    except Exception as e:
        print(f"\n[ERRO] Não foi possível conectar ao banco: {e}")
        print("Verifique se o MySQL está rodando!")
        return None
