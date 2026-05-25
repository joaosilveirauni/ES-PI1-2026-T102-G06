from menus.submenu.sistemavotacao import submenu_votacao
from menus.submenu.resultados import resultados
from menus.submenu.auditoria import auditoria

votacao_iniciada = False
votacao_encerrada = False

def menu_votacao():
    global votacao_iniciada, votacao_encerrada
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== VOTAÇÃO ===")
            print("1 - Abrir votação")
            print("2 - Resultados")
            print("3 - Auditoria")
            print("4 - Encerrar votação")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "0":
                print("Voltando ao menu principal...")
                return

            elif opcao == "1":
                if votacao_encerrada:
                    print("A votação deste turno já foi encerrada!")
                else:
                    print("Sistema de votação aberto!")
                    votacao_iniciada = True
                    submenu_votacao()


            elif opcao == "2":
                if votacao_iniciada and not votacao_encerrada:
                    print("Atenção: A votação está em andamento. Encerre-a para ver os resultados!")
                elif not votacao_iniciada and not votacao_encerrada:
                    print("A votação ainda não foi aberta hoje!")
                else:
                    resultados()

            elif opcao == "3":
                auditoria()
            
            elif opcao == "4":
                if not votacao_iniciada:
                    print("Não é possível encerrar uma votação que não foi aberta!")
                else:
                    votacao_encerrada = True
                    votacao_iniciada = False
                    print("VOTAÇÃO ENCERRADA! Resultados liberados na Opção 2.")

            else:
                print("Opção Inválida!")

    except:
        print("Opção Inválida!")