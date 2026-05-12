import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Jujyo9",
            database="ladpy"
        )
        return conexao
    except Exception as e:
        print(f"\n[ERRO] Não foi possível conectar ao banco: {e}")
        print("Verifique se o MySQL está rodando!")
        return None