import mysql.connector

def conectar():
    try:
        conexao = mysql.connector.connect(
            host="BD-ACD",
            user="BD250226110",
            password="Abhrg5",
            database="BD250226110"
        )
        return conexao
    except Exception as e:
        print(f"\n[ERRO] Não foi possível conectar ao banco: {e}")
        print("Verifique se a VPN está ativa!")
        return None