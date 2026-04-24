def menu_votacao():
    opcao = ""

    while opcao != "0":
        print("\n=== VOTAÇÃO ===")
        print("1 - Abrir votação")
        print("2 - Resultados")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "0":
            return