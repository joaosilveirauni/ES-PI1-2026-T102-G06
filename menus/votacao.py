from menus.submenu.sistemavotacao import submenu_votacao
from menus.submenu.resultados import resultados
from menus.submenu.auditoria import auditoria

def menu_votacao():
    opcao = ""
    
    try:
        while opcao != "0":
            print("\n=== VOTAÇÃO ===")
            print("1 - Abrir votação")
            print("2 - Ver Resultados")
            print("0 - Voltar")
            
            opcao = input("Escolha: ")
            
            if opcao == "0":
                return
            elif opcao == "1":
                submenu_votacao()
            elif opcao == "2":
                resultados()
            else:
                print("Opção Inválida!")
    except:
        print("Opção Inválida!")
