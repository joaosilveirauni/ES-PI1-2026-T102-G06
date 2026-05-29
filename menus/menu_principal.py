from menus.gerenciamento import menu_gerenciamento
from menus.votacao import menu_votacao
import os

def menu_principal():
    """
    Exibe o menu principal do sistema.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    opcao = ""
    
    os.system('cls')
    while opcao != "0":
        try:
            print("\n=== MENU PRINCIPAL ===")
            print("1 - Votacao")
            print("2 - Gerenciamento")
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
