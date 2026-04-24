from db.conexao import conectar

def listar_eleitores():
    conexao = conectar()
    
    if not conexao:
        return []

    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT nome, titulo_eleitor FROM eleitores")

    dados = cursor.fetchall()

    conexao.close()

    return dados