from menus.gerenciamento import menu_gerenciamento
from menus.votacao import menu_votacao

def menu_principal():
    opcao = ""

    while opcao != "0":
        try:
            print("\n=== MENU PRINCIPAL ===")
            print("1 - Votar")
            print("2 - Gerenciar")
            print("0 - Sair")

            opcao = input("Escolha: ")

            if opcao == "1":
                menu_votacao()
            elif opcao == "2":
                menu_gerenciamento()
            elif opcao == "0":
                print("Saindo...")
            else:
                print("Opção Inválida!")
        except:
            print("Opção Inválida!")
