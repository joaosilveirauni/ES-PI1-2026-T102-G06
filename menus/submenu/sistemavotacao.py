status_votacao = False

def submenu_votacao():
    global status_votacao

    opcao = ""
    status_votacao = True

    try:
        while opcao != "2" and status_votacao:

            print("\n=== SISTEMA DE VOTAÇÃO ===")
            print("1 - Votar")
            print("2 - Encerrar Sistema de Votação")

            opcao = input("Escolha: ")

            if opcao == "1":

                if status_votacao:
                    print("Voto realizado com sucesso!")
                else:
                    print("A votação está encerrada!")

            elif opcao == "2":
                status_votacao = False
                print("Sistema de votação encerrado!")

            else:
                print("Opção Inválida!")

    except:
        print("Opção Inválida!!")
        
