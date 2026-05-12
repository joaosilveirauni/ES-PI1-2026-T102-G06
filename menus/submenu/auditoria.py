def auditoria():
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== AUDITORIA DA VOTAÇÃO ===")
            print("1 - Exibir Logs de Ocorrência")
            print("2 - Exibit Protocolos de Votação")
            print("0 - Voltar")

            opcao = input("Escolha: ")
    except:
        print("Opção Inválida!")