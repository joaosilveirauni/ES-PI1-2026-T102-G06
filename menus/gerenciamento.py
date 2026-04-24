from services.eleitor import listar_eleitores

def menu_gerenciamento():
    opcao = ""

    while opcao != "0":
        print("\n=== GERENCIAMENTO ===")
        print("1 - Cadastrar Eleitor")
        print("2 - Listar Eleitores")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "2":
            eleitores = listar_eleitores()

            print("\n--- LISTA DE ELEITORES ---")
            for e in eleitores:
                print(f"Nome: {e['nome']} | Título: {e['titulo_eleitor']}")

        elif opcao == "0":
            return