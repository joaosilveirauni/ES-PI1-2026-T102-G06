from menus.votacao import listar_protocolos
from services.auditoria import exibir_ocorrencias


def auditoria():
    """
    Exibe o menu de auditoria da votacao.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== AUDITORIA DA VOTAÇÃO ===")
            print("1 - Exibir Logs de Ocorrências ")
            print("2 - Exibir Protocolos de Votação")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                exibir_ocorrencias()
            elif opcao == "2":
                protocolos = listar_protocolos()

                print("\n=== PROTOCOLOS DE VOTACAO ===")

                if not protocolos:
                    print("Nenhum protocolo encontrado.")
                else:
                    for item in protocolos:
                        print("Protocolo:", item["protocolo"], "| Data:", item["data_voto"])
            elif opcao == "0":
                return
            else:
                print("Opção Inválida!")
    except Exception as erro:
        print("Erro na auditoria:", erro)
