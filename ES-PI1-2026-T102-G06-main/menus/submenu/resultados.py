def resultados():
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== RESULTADOS DA VOTAÇÃO ===")
            print("1 - Boletim de Urna")
            print("2 - Estatística de Comparecimento")
            print("3 - Votos por Partido")
            print("4 - Validação de Integridade")
            print("0 - Voltar")

            opcao = input("Escolha: ")
    except:
        print("Opção Inválida!")