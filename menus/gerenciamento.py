from services.eleitor import listar_eleitores, cadastrar_eleitor, buscar_eleitor_por_titulo

def menu_gerenciamento():
    opcao = ""

    while opcao != "0":
        print("\n=== GERENCIAMENTO ===")
        print("1 - Cadastrar Eleitor")
        print("2 - Listar Eleitores")
        print("3 - Buscar Eleitor")
        print("0 - Voltar")

        opcao = input("Escolha: ")

        if opcao == "1":
            print("\n--- CADASTRO DE ELEITOR ---")
            nome = input("Nome completo: ")
            cpf = input("CPF (apenas números): ")
            titulo = input("Título de Eleitor: ")
            chave = input("Chave de Acesso (senha): ")

            sucesso = cadastrar_eleitor(nome, cpf, titulo, chave)
            
            if sucesso:
                print("Eleitor cadastrado com sucesso!")
            else:
                print("Erro ao cadastrar. Verifique se o CPF ou título já existe.")

        elif opcao == "2":
            eleitores = listar_eleitores()

            print("\n--- LISTA DE ELEITORES ---")
            if not eleitores:
                print("Nenhum eleitor encontrado.")
            else:
                for e in eleitores:
                    print(f"Nome: {e['nome']} | Título: {e['titulo_eleitor']}")

        elif opcao == "3":
            print("\n--- BUSCA DE ELEITOR ---")
            titulo_busca = input("Digite o Título de Eleitor: ")
            
            eleitor = buscar_eleitor_por_titulo(titulo_busca)
            
            if eleitor:
                print(f"Eleitor Encontrado:")
                print(f"Nome: {eleitor['nome']}")
                print(f"CPF: {eleitor['cpf']}")
                print(f"Já votou? {'Sim' if eleitor['ja_votou'] else 'Não'}")
                # fazer lógica de verificar se ja votou ou não
            else:
                print("Eleitor não encontrado com este título.")

        elif opcao == "0":
            return

        else:
            print("Opção inválida!")
