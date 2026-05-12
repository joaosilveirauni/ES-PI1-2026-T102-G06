# Esse é o auditoria.py do submenu (menus/submenus/auditoria.py), diferente do auditoria.py dos serviços (services/auditoria.py)
from services.auditoria import listar_ocorrencias

def auditoria():
    opcao = ""

    try:   
        while opcao != "0":
            print("\n=== AUDITORIA DA VOTAÇÃO ===")
            print("1 - Exibir Logs de Ocorrência")
            #print("2 - Exibir Protocolos de Votação")
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

#            elif opcao == "2":
#                print("\n=== PROTOCOLOS DE VOTAÇÃO ===")
#                
#                try:
#                    from services.protocolo import listar_protocolos
#                    protocolos = listar_protocolos()
#
#                    if protocolos:
#                        for p in protocolos:
#                            print(f"[{p['data_hora']}] ID: {p['id_voto']} - Eleitor: {p['eleitor']}")
#                    else:
#                        print("Nenhum protocolo encontrado.")#
#
#                except ImportError:
#                    print("Serviço de protocolos ainda não implementado.")
            
            elif opcao == "0":
                return
    except Exception as e:
        print(f"Erro ao carregar auditoria: {e}")
