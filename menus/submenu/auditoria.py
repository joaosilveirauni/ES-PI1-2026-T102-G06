# Esse é o auditoria.py do submenu, diferente do auditoria.py dos serviços

from services.auditoria import listar_ocorrencias

def auditoria():
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== AUDITORIA DA VOTAÇÃO ===")
            print("1 - Exibir Logs de Ocorrência")
            print("2 - Exibir Protocolos de Votação")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                logs = listar_ocorrencias()
                print("\n=== HISTÓRICO DE OCORRÊNCIAS ===")
                
                if logs:
                    for log in logs:
                        print(f"[{log['data_hora']}] {log['mensagem']}")
                        
                else:
                    print("Nenhum registro encontrado no banco.")
            
            elif opcao == "0":
                return
    except Exception as e:
        print(f"Erro ao carregar auditoria: {e}")
