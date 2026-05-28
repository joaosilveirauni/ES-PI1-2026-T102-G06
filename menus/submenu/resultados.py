from menus.votacao import (
    buscar_resultado,
    buscar_votos_nulos,
    buscar_estatisticas,
    buscar_votos_por_partido,
    buscar_total_votos_urna
)


def resultados():
    opcao = ""

    try:
        while opcao != "0":
            print("\n=== RELATORIOS E RESULTADOS DA VOTACAO ===")
            print("1 - Boletim de Urna")
            print("2 - Estatistica de Comparecimento")
            print("3 - Votos por Partido")
            print("4 - Validacao de Integridade")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "0":
                print("Voltando ao menu de votacao...")
                return

            elif opcao == "1":
                print("\n" + "="*30)
                print("       BOLETIM DE URNA       ")
                print("="*30)

                votos_candidatos = buscar_resultado()
                nulos = buscar_votos_nulos()

                print("\n--- VOTOS DOS CANDIDATOS ---")
                if not votos_candidatos:
                    print("Nenhum voto registrado para candidatos.")
                else:
                    vencedor = votos_candidatos[0]
                    for candidato in votos_candidatos:
                        print("Candidato:", candidato["nome"], "| Votos:", candidato["total_votos"])
                        if candidato["total_votos"] > vencedor["total_votos"]:
                            vencedor = candidato

                print("\n--- VOTOS ESPECIAIS ---")
                print("Votos Nulos:", nulos)
                print("="*30)

                if votos_candidatos and vencedor["total_votos"] > 0:
                    print("\n*** VENCEDOR ***")
                    print("Nome:    ", vencedor["nome"])
                    print("Numero:  ", vencedor["numero"])
                    print("Partido: ", vencedor["partido"])
                    print("Votos:   ", vencedor["total_votos"])
                    print("="*30)

            elif opcao == "2":
                print("\n" + "="*30)
                print("     ESTATISTICA DE COMPARECIMENTO")
                print("="*30)

                votaram, total = buscar_estatisticas()

                if total == 0:
                    print("Nenhum eleitor cadastrado no sistema.")
                else:
                    faltaram = total - votaram
                    pct_comparecimento = (votaram / total) * 100
                    pct_abstencao = (faltaram / total) * 100

                    print("Total de Eleitores Aptos:    ", total)
                    print("Total de Comparecimento:     ", votaram, "-", round(pct_comparecimento, 2), "%")
                    print("Total de Abstencao (Faltas): ", faltaram, "-", round(pct_abstencao, 2), "%")
                print("="*30)

            elif opcao == "3":
                print("\n" + "="*30)
                print("          VOTOS POR PARTIDO          ")
                print("="*30)

                votos_partido = buscar_votos_por_partido()

                if not votos_partido:
                    print("Nenhum voto registrado para os partidos.")
                else:
                    for p in votos_partido:
                        print("Partido:", p["partido"], "| Total de Votos:", p["total_votos"])
                print("="*30)

            elif opcao == "4":
                print("\n" + "="*30)
                print("       VALIDACAO DE INTEGRIDADE      ")
                print("="*30)

                votaram, _ = buscar_estatisticas()
                votos_urna = buscar_total_votos_urna()

                print("Total de Eleitores com status Ja Votou:", votaram)
                print("Total de Votos registrados na Urna:    ", votos_urna)

                if votaram == votos_urna:
                    print("\n[OK] STATUS: INTEGRO")
                    print("O numero de votos condiz com o numero de eleitores.")
                else:
                    print("\n[X] STATUS: DIVERGENCIA ENCONTRADA")
                    print("Os numeros nao conferem. E necessaria auditoria.")
                print("="*30)

            else:
                print("Opcao Invalida!")

    except Exception as e:
        print("Erro no sistema de resultados:", e)
