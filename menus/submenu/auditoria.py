from services.auditoria import listar_ocorrencias

def auditoria():
    while True:
        print("\n=== AUDITORIA DA VOTAÇÃO ===")
        print("1 - Exibir Logs de Ocorrência")
        print("0 - Voltar")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            try:
                logs = listar_ocorrencias()
                print("\n=== HISTÓRICO DE OCORRÊNCIAS ===")
                if logs:
                    for log in logs:
                        print(f"[{log['data_hora']}] {log['mensagem']}")
                else:
                    print("Nenhum registro encontrado.")
            except Exception as e:
                print(f"Erro ao carregar logs: {e}")

        elif opcao == "0":
            return

        else:
            print("Opção inválida! Digite 0 ou 1.")
