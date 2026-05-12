from menus.submenu.sistemavotacao import submenu_votacao
from menus.submenu.resultados import resultados
from menus.submenu.auditoria import auditoria

def menu_votacao():
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== VOTAÇÃO ===")
            print("1 - Abrir votação")
            print("2 - Resultados")
            print("3 - Auditoria")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "0":
                print("Voltando ao menu principal...")
                return

            elif opcao == "1":
                print("Sistema de votação aberto!")
                submenu_votacao()

            elif opcao == "2":
                resultados()

            elif opcao == "3":
                auditoria()

            else:
                print("Opção Inválida!")

    except:
        print("Opção Inválida!")