from services.eleitor import autenticar_eleitor
from services.candidato import buscar_candidato_por_numero
from menus.votacao import zerar_votos, registrar_voto
from services.criptografia import criptografar_chave
from services.logs import log_abertura, log_acesso_negado, log_voto_duplo, log_voto_sucesso, log_encerramento


def pedir_credenciais():
    titulo = input("Titulo de Eleitor: ")
    primeiros_digitos = input("4 primeiros digitos do CPF: ")
    chave = input("Chave de Acesso: ")
    return titulo, primeiros_digitos, chave


def autenticar_mesario():
    titulo, primeiros_digitos, chave = pedir_credenciais()
    eleitor = autenticar_eleitor(titulo, primeiros_digitos, chave)

    if not eleitor:
        log_acesso_negado("Dados invalidos na autenticacao do mesario")
        print("Dados invalidos! Acesso negado.")
        return None

    if not eleitor["is_mesario"]:
        log_acesso_negado("Eleitor sem perfil de mesario tentou abrir/encerrar votacao")
        print("Este eleitor nao possui perfil de mesario!")
        return None

    return eleitor


def menu_votacao():
    print("\n========================================")
    print("        MODULO DE VOTACAO              ")
    print("========================================")
    print("\nPara abrir a votacao, o mesario deve se identificar.")

    mesario = autenticar_mesario()

    if not mesario:
        return

    print("\n Realizando Zeresima... ")
    sucesso, candidatos = zerar_votos()

    if not sucesso:
        print("Erro ao realizar a Zeresima. Votacao nao pode ser aberta.")
        return

    print("\n ZERESIMA CONCLUIDA ")
    print("-" * 50)
    for c in candidatos:
        print("Candidato:", c["nome"], "| Numero:", c["numero"], "| Votos: 0")
    print("-" * 50)
    print("Urna vazia confirmada. Votacao iniciada.")

    log_abertura()

    menu_urna()


def menu_urna():
    opcao = ""

    while True:
        print("\n URNA ELETRONICA ")
        print("1 - Votar")
        print("2 - Encerrar Sistema de Votacao")

        opcao = input("Escolha: ")

        if opcao == "1":
            fluxo_votacao()
        elif opcao == "2":
            encerrado = fluxo_encerramento()
            if encerrado:
                return
        else:
            print("Opcao invalida!")


def fluxo_votacao():
    print("\n IDENTIFICACAO DO ELEITOR ")
    titulo, primeiros_digitos, chave = pedir_credenciais()

    eleitor = autenticar_eleitor(titulo, primeiros_digitos, chave)

    if not eleitor:
        log_acesso_negado("Dados invalidos na identificacao do eleitor")
        print("Dados invalidos! Acesso negado.")
        return

    if eleitor["ja_votou"]:
        log_voto_duplo(titulo)
        print("Este eleitor ja realizou seu voto!")
        return

    _coletar_voto(eleitor)


def _coletar_voto(eleitor):
    while True:
        print("\n VOTACAO ")
        numero = input("Digite o numero do candidato (ou 0 para voto nulo): ")

        if not numero.isdigit():
            print("Numero invalido! Digite apenas numeros.")
            continue

        numero = int(numero)

        if numero == 0:
            confirmacao = input("Voto NULO. Confirmar? (s/n): ")
            if confirmacao.lower() == "s":
                _confirmar_voto(eleitor["id"], None, 0, "NULO")
                return
            else:
                continue

        candidato = buscar_candidato_por_numero(numero)

        if not candidato:
            print("\nNenhum candidato encontrado com este numero.")
            confirmacao = input("Deseja confirmar mesmo assim? O voto sera registrado como NULO. (s/n): ")
            if confirmacao.lower() == "s":
                _confirmar_voto(eleitor["id"], None, numero, "NULO")
                return
            else:
                continue

        print("\nCandidato encontrado:")
        print("Nome:    ", candidato["nome"])
        print("Numero:  ", candidato["numero"])
        print("Partido: ", candidato["partido"])

        confirmacao = input("\nConfirmar voto neste candidato? (s/n): ")

        if confirmacao.lower() == "s":
            _confirmar_voto(eleitor["id"], candidato["id"], candidato["numero"], "VALIDO")
            return
        else:
            print("Voto nao confirmado. Tente novamente.")


def _confirmar_voto(eleitor_id, candidato_id, numero_candidato, tipo):
    protocolo = registrar_voto(eleitor_id, candidato_id, numero_candidato, tipo)

    if protocolo:
        log_voto_sucesso()
        if tipo == "NULO":
            print("\nVoto NULO registrado com sucesso!")
        else:
            print("\nVoto registrado com sucesso!")
        print("========================================")
        print("Protocolo:", protocolo)
        print("========================================")
        print("Guarde este protocolo como comprovante.")
    else:
        print("\nErro ao registrar o voto. Chame o suporte.")


def fluxo_encerramento():
    print("\n ENCERRAMENTO DA VOTACAO ")
    print("O mesario deve se identificar para encerrar.")

    mesario = autenticar_mesario()

    if not mesario:
        return False

    confirmacao = input("\nDeseja realmente encerrar a votacao? (s/n): ")

    if confirmacao.lower() != "s":
        print("Encerramento cancelado.")
        return False

    print("\nPor seguranca, digite sua chave de acesso novamente:")
    chave_confirmacao = input("Chave de Acesso: ")

    if criptografar_chave(chave_confirmacao) != mesario["chave_acesso"]:
        print("Chave invalida! Encerramento cancelado.")
        return False

    log_encerramento()
    print("\nVotacao encerrada com sucesso!")
    return True