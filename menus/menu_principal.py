from menus.gerenciamento import menu_gerenciamento
from menus.votacao import menu_votacao

def menu_principal():
    opcao = ""

    while opcao != "0":
        print("\n=== MENU PRINCIPAL ===")
        print("1 - Gerenciamento")
        print("2 - Votação")
        print("0 - Sair")

        opcao = input("Escolha: ")

        if opcao == "1":
            menu_gerenciamento()
        elif opcao == "2":
            menu_votacao()
        elif opcao == "0":
            print("Saindo...")
        else:
            print("Opção inválida")