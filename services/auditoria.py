from datetime import datetime


LOG_PATH = "logs_ocorrencias.txt"


def registrar_ocorrencia(mensagem):
    """
    Executa a rotina registrar_ocorrencia.
    
    Args:
        mensagem (str): Valor usado pela funcao.
    
    Returns:
        bool: Resultado da funcao.
    """
    horario = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    linha = f"[{horario}] {mensagem}"

    try:
        with open(LOG_PATH, "a", encoding="utf-8") as arquivo:
            arquivo.write(linha + "\n")
        return True
    except Exception as erro:
        print("Falha ao registrar log:", erro)
        return False


def listar_ocorrencias():
    """
    Executa a rotina listar_ocorrencias.
    
    Args:
        Nenhum.
    
    Returns:
        list: Resultado da funcao.
    """
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as arquivo:
            return arquivo.readlines()
    except FileNotFoundError:
        return []
    except Exception as erro:
        print("Erro ao ler logs:", erro)
        return []


def exibir_ocorrencias():
    """
    Executa a rotina exibir_ocorrencias.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    ocorrencias = listar_ocorrencias()

    if not ocorrencias:
        print("\nNenhuma ocorrência encontrada.")
        return

    print("\n===== LOGS DE OCORRÊNCIAS =====")

    for linha in ocorrencias:
        print(linha.strip())
