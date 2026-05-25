from db.eleitores import listar_resultado_votacao, buscar_votos_brancos_e_nulos

def resultados():
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== RElATÓRIOS E RESULTADOS DA VOTAÇÃO ===")
            print("1 - Boletim de Urna")
            print("2 - Estatística de Comparecimento")
            print("3 - Votos por Partido")
            print("4 - Validação de Integridade")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "0":
                print("Voltando ao menu de votação...")
                return

            elif opcao == "1":
                print("\n" + "="*30)
                print("       BOLETIM DE URNA OBRIGATÓRIO      ")
                print("="*30)
            
                votos_candidatos = listar_resultado_votacao()
                
                print("\n--- VOTOS DOS CANDIDATOS ---")
                if not votos_candidatos:
                    print("Nenhum voto registrado para candidatos.")
                else:
                    for candidato in votos_candidatos:
                        print(f"Candidato: {candidato['nome']} | Votos: {candidato['total_votos']}")
                
                votos_especiais = buscar_votos_brancos_e_nulos()
                
                print("\n--- VOTOS GERAIS ---")
                print(f"Votos Brancos: {votos_especiais['brancos']}")
                print(f"Votos Nulos: {votos_especiais['nulos']}")
                print("="*30)

            elif opcao == "2":
                print("\n[Aviso] Estatísticas de Comparecimento (Funcionalidade em desenvolvimento pelo grupo).")

            elif opcao == "3":
                print("\n[Aviso] Votos por Partido (Funcionalidade em desenvolvimento pelo grupo).")

            elif opcao == "4":
                print("\n[Aviso] Validação de Integridade (Funcionalidade em desenvolvimento pelo grupo).")

            else:
                print("Opção Inválida!")

    except Exception as e:
        print(f"Erro no sistema de resultados: {e}")
        print("Opção Inválida!")
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