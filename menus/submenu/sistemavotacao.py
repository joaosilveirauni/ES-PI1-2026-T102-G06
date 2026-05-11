from services.auditoria import registrar_ocorrencia

def submenu_votacao():
    opcao = ""
    
    try:
        while opcao != "2":
            print("\n=== VOTAÇÃO ===")
            print("1 - Votar")
            print("2 - Encerrar Sistema de Votação")
            
            opcao = input("Escolha: ")
            
    except:
        print("Opção Inválida!")
        status_votacao = False
    
