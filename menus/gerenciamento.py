from services.eleitor import listar_eleitores, cadastrar_eleitor, buscar_eleitor_por_titulo, buscar_eleitor_por_cpf, editar_eleitor, remover_eleitor
from services.candidato import listar_candidatos, cadastrar_candidato, buscar_candidato_por_numero, editar_candidato, remover_candidato
from services.validacoes import pedir_cpf, pedir_titulo

def menu_gerenciamento():
    opcao = ""

    try:
        while opcao != "0":
            print("\n GERENCIAMENTO ")
            print("1 - Gerenciar Eleitores")
            print("2 - Gerenciar Candidatos")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                menu_eleitores()
            elif opcao == "2":
                menu_candidatos()
            elif opcao == "0":
                return
            else:
                print("Opcao invalida!")
    except:
        print("Opcao Invalida!")

def menu_eleitores():
    opcao = ""

    try:
        while opcao != "0":
            print("\n GERENCIAMENTO DE ELEITORES ")
            print("1 - Cadastrar Eleitor")
            print("2 - Listar Eleitores")
            print("3 - Buscar Eleitor por Titulo")
            print("4 - Buscar Eleitor por CPF")
            print("5 - Editar Eleitor")
            print("6 - Remover Eleitor")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                cadastrar()
            elif opcao == "2":
                listar()
            elif opcao == "3":
                buscar_titulo()
            elif opcao == "4":
                buscar_cpf()
            elif opcao == "5":
                editar()
            elif opcao == "6":
                remover()
            elif opcao == "0":
                return
            else:
                print("Opcao invalida!")
    except:
        print("Opcao Invalida!")


def cadastrar():
    print("\n CADASTRO DE ELEITOR ")
    nome = input("Nome completo: ")
    cpf = pedir_cpf()
    titulo = pedir_titulo()

    resposta = input("Este eleitor e mesario? (s/n): ")

    if resposta.lower() == "s":
        is_mesario = True
    else:
        is_mesario = False

    chave = cadastrar_eleitor(nome, cpf, titulo, is_mesario)

    if chave:
        print("\nEleitor cadastrado com sucesso!")
        print("========================================")
        print("CHAVE DE ACESSO:", chave)
        print("========================================")
        print("Anote esta chave! Ela nao podera ser recuperada.")
    else:
        print("Erro ao cadastrar. Verifique se o CPF ou titulo ja existe.")


def listar():
    eleitores = listar_eleitores()

    print("\n LISTA DE ELEITORES ")

    if not eleitores:
        print("Nenhum eleitor encontrado.")
    else:
        for e in eleitores:
            if e["is_mesario"]:
                mesario = "Sim"
            else:
                mesario = "Nao"

            if e["ja_votou"]:
                votou = "Sim"
            else:
                votou = "Nao"

            print("Nome:", e["nome"], "| Titulo:", e["titulo_eleitor"], "| Mesario:", mesario, "| Ja votou:", votou)


def buscar_titulo():
    print("\n--- BUSCA POR TITULO ---")
    titulo_busca = input("Digite o Titulo de Eleitor: ")
    eleitor = buscar_eleitor_por_titulo(titulo_busca)

    if eleitor:
        exibir_eleitor(eleitor)
    else:
        print("Eleitor nao encontrado.")


def buscar_cpf():
    print("\n BUSCA POR CPF ")
    cpf_busca = pedir_cpf()
    eleitor = buscar_eleitor_por_cpf(cpf_busca)

    if eleitor:
        exibir_eleitor(eleitor)
    else:
        print("Eleitor nao encontrado.")


def exibir_eleitor(eleitor):
    print("\nEleitor encontrado:")
    print("Nome:    ", eleitor["nome"])
    print("CPF:     ", eleitor["cpf"])
    print("Titulo:  ", eleitor["titulo_eleitor"])

    if eleitor["is_mesario"]:
        print("Mesario:  Sim")
    else:
        print("Mesario:  Nao")

    if eleitor["ja_votou"]:
        print("Ja votou: Sim")
    else:
        print("Ja votou: Nao")


def editar():
    print("\n EDITAR ELEITOR ")
    titulo_busca = input("Digite o Titulo do eleitor que deseja editar: ")
    eleitor = buscar_eleitor_por_titulo(titulo_busca)

    if not eleitor:
        print("Eleitor nao encontrado.")
        return

    exibir_eleitor(eleitor)

    print("\nDigite os novos dados (Enter para manter o atual):")

    novo_nome = input("Novo nome [" + eleitor["nome"] + "]: ")
    if novo_nome == "":
        novo_nome = eleitor["nome"]

    novo_cpf = input("Novo CPF [" + eleitor["cpf"] + "]: ")
    if novo_cpf == "":
        novo_cpf = eleitor["cpf"]
    else:
        novo_cpf = pedir_cpf()

    novo_titulo = input("Novo Titulo [" + eleitor["titulo_eleitor"] + "]: ")
    if novo_titulo == "":
        novo_titulo = eleitor["titulo_eleitor"]
    else:
        novo_titulo = pedir_titulo()

    sucesso = editar_eleitor(titulo_busca, novo_nome, novo_cpf, novo_titulo)

    if sucesso:
        print("Eleitor editado com sucesso!")
    else:
        print("Erro ao editar. Verifique se o novo CPF ou titulo ja existe.")


def remover():
    print("\n REMOVER ELEITOR ")
    titulo_busca = input("Digite o Titulo do eleitor que deseja remover: ")
    eleitor = buscar_eleitor_por_titulo(titulo_busca)

    if not eleitor:
        print("Eleitor nao encontrado.")
        return

    exibir_eleitor(eleitor)

    confirmacao = input("\nTem certeza que deseja remover este eleitor? (s/n): ")

    if confirmacao.lower() == "s":
        sucesso = remover_eleitor(titulo_busca)

        if sucesso:
            print("Eleitor removido com sucesso!")
        else:
            print("Erro ao remover eleitor.")
    else:
        print("Remocao cancelada.")


# ── CANDIDATOS ────────────────────────────────────────────────────────────────

def menu_candidatos():
    opcao = ""

    try:
        while opcao != "0":
            print("\n GERENCIAMENTO DE CANDIDATOS")
            print("1 - Cadastrar Candidato")
            print("2 - Listar Candidatos")
            print("3 - Buscar Candidato por Numero")
            print("4 - Editar Candidato")
            print("5 - Remover Candidato")
            print("0 - Voltar")

            opcao = input("Escolha: ")

            if opcao == "1":
                cadastrar_cand()
            elif opcao == "2":
                listar_cand()
            elif opcao == "3":
                buscar_cand()
            elif opcao == "4":
                editar_cand()
            elif opcao == "5":
                remover_cand()
            elif opcao == "0":
                return
            else:
                print("Opcao invalida!")
    except:
        print("Opcao Invalida!")


def cadastrar_cand():
    print("\n CADASTRO DE CANDIDATO ")
    nome = input("Nome do candidato: ")
    partido = input("Partido: ")

    numero = input("Numero de votacao: ")

    while not numero.isdigit():
        print("Numero invalido! Digite apenas numeros.")
        numero = input("Numero de votacao: ")

    numero = int(numero)

    candidato_existente = buscar_candidato_por_numero(numero)

    if candidato_existente:
        print("Ja existe um candidato com este numero!")
        return

    sucesso = cadastrar_candidato(nome, numero, partido)

    if sucesso:
        print("Candidato cadastrado com sucesso!")
    else:
        print("Erro ao cadastrar candidato.")


def listar_cand():
    candidatos = listar_candidatos()

    print("\n LISTA DE CANDIDATOS ")

    if not candidatos:
        print("Nenhum candidato encontrado.")
    else:
        for c in candidatos:
            print("Nome:", c["nome"], "| Numero:", c["numero"], "| Partido:", c["partido"])


def buscar_cand():
    print("\n BUSCA DE CANDIDATO ")
    numero = input("Digite o numero do candidato: ")

    while not numero.isdigit():
        print("Numero invalido! Digite apenas numeros.")
        numero = input("Digite o numero do candidato: ")

    numero = int(numero)
    candidato = buscar_candidato_por_numero(numero)

    if candidato:
        exibir_candidato(candidato)
    else:
        print("Candidato nao encontrado.")


def exibir_candidato(candidato):
    print("\nCandidato encontrado:")
    print("Nome:    ", candidato["nome"])
    print("Numero:  ", candidato["numero"])
    print("Partido: ", candidato["partido"])


def editar_cand():
    print("\n EDITAR CANDIDATO ")
    numero = input("Digite o numero do candidato que deseja editar: ")

    while not numero.isdigit():
        print("Numero invalido! Digite apenas numeros.")
        numero = input("Digite o numero do candidato: ")

    numero = int(numero)
    candidato = buscar_candidato_por_numero(numero)

    if not candidato:
        print("Candidato nao encontrado.")
        return

    exibir_candidato(candidato)

    print("\nDigite os novos dados (Enter para manter o atual):")

    novo_nome = input("Novo nome [" + candidato["nome"] + "]: ")
    if novo_nome == "":
        novo_nome = candidato["nome"]

    novo_partido = input("Novo partido [" + candidato["partido"] + "]: ")
    if novo_partido == "":
        novo_partido = candidato["partido"]

    novo_numero = input("Novo numero [" + str(candidato["numero"]) + "]: ")
    if novo_numero == "":
        novo_numero = candidato["numero"]
    else:
        while not novo_numero.isdigit():
            print("Numero invalido! Digite apenas numeros.")
            novo_numero = input("Novo numero: ")

        novo_numero = int(novo_numero)

        if novo_numero != candidato["numero"]:
            existente = buscar_candidato_por_numero(novo_numero)
            if existente:
                print("Ja existe um candidato com este numero!")
                return

    sucesso = editar_candidato(numero, novo_nome, novo_numero, novo_partido)

    if sucesso:
        print("Candidato editado com sucesso!")
    else:
        print("Erro ao editar candidato.")


def remover_cand():
    print("\n--- REMOVER CANDIDATO ---")
    numero = input("Digite o numero do candidato que deseja remover: ")

    while not numero.isdigit():
        print("Numero invalido! Digite apenas numeros.")
        numero = input("Digite o numero do candidato: ")

    numero = int(numero)
    candidato = buscar_candidato_por_numero(numero)

    if not candidato:
        print("Candidato nao encontrado.")
        return

    exibir_candidato(candidato)

    confirmacao = input("\nTem certeza que deseja remover este candidato? (s/n): ")

    if confirmacao.lower() == "s":
        sucesso = remover_candidato(numero)

        if sucesso:
            print("Candidato removido com sucesso!")
        else:
            print("Erro ao remover candidato.")
    else:
        print("Remocao cancelada.")