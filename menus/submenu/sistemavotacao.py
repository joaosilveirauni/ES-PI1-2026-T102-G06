from services.eleitor import autenticar_eleitor
from services.candidato import buscar_candidato_por_numero
from menus.votacao import zerar_votos, registrar_voto
from services.criptografia import criptografar_chave
from services.auditoria import registrar_ocorrencia


def pedir_credenciais():
    """
    Executa a rotina pedir_credenciais.
    
    Args:
        Nenhum.
    
    Returns:
        tuple: Resultado da funcao.
    """
    titulo = input("Titulo de Eleitor: ")
    primeiros_digitos = input("4 primeiros digitos do CPF: ")
    chave = input("Chave de Acesso: ")
    return titulo, primeiros_digitos, chave


def autenticar_mesario():
    """
    Executa a rotina autenticar_mesario.
    
    Args:
        Nenhum.
    
    Returns:
        dict | None: Resultado da funcao.
    """
    titulo, primeiros_digitos, chave = pedir_credenciais()
    eleitor = autenticar_eleitor(titulo, primeiros_digitos, chave)

    if not eleitor:
        registrar_ocorrencia("ALERTA: Tentativa de acesso negado")
        print("Validacao falhou. Dados invalidos!")
        return None

    if not eleitor["is_mesario"]:
        registrar_ocorrencia("ALERTA: Tentativa de acesso negado")
        print("Validacao falhou. Este eleitor nao possui perfil de mesario!")
        return None

    return eleitor


def abrir_sistema_votacao():
    """
    Abre o sistema de votacao apos validar o mesario.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    print("\n========================================")
    print("        ABRIR SISTEMA DE VOTACAO        ")
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
        print("Candidato:", c["nome"], "| Numero:", c["numero"], "| Partido:", c["partido"], "| Votos: 0")
    print("-" * 50)
    print("Urna vazia confirmada. Votacao iniciada.")

    registrar_ocorrencia("ABERTURA: Votação iniciada com sucesso. Total de votos zerado.")

    menu_urna()


def menu_urna():
    """
    Exibe o menu da urna durante a votacao.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    encerrado = False

    while not encerrado:
        print("\n=== URNA ELETRONICA ===")
        print("1 - Votar")
        print("2 - Encerrar Votação")

        opcao = input("Escolha: ")

        if opcao == "1":
            fluxo_votacao()
        elif opcao == "2":
            encerrado = fluxo_encerramento()
        else:
            print("Opcao invalida!")


def fluxo_votacao():
    """
    Executa a rotina fluxo_votacao.
    
    Args:
        Nenhum.
    
    Returns:
        None: Resultado da funcao.
    """
    print("\n IDENTIFICACAO DO ELEITOR ")
    titulo, primeiros_digitos, chave = pedir_credenciais()

    eleitor = autenticar_eleitor(titulo, primeiros_digitos, chave)

    if not eleitor:
        registrar_ocorrencia("ALERTA: Tentativa de acesso negado")
        print("Dados invalidos! Acesso negado.")
        return

    if eleitor["ja_votou"]:
        registrar_ocorrencia("ALERTA: Tentativa de voto duplo")
        print("Este eleitor ja realizou seu voto!")
        return

    _coletar_voto(eleitor)


def _coletar_voto(eleitor):
    """
    Executa a rotina _coletar_voto.
    
    Args:
        eleitor (dict): Valor usado pela funcao.
    
    Returns:
        None: Resultado da funcao.
    """
    voto_confirmado = False

    while not voto_confirmado:
        print("\n VOTACAO ")
        numero = input("Digite o numero do candidato: ")

        if not numero.isdigit():
            print("Numero invalido! Digite apenas numeros.")
        else:
            numero = int(numero)
            candidato = buscar_candidato_por_numero(numero)

            if candidato:
                print("\nCandidato encontrado:")
                print("Nome:    ", candidato["nome"])
                print("Numero:  ", candidato["numero"])
                print("Partido: ", candidato["partido"])

                confirmacao = input("\nConfirmar voto neste candidato? (s/n): ")

                if confirmacao.lower() == "s":
                    _confirmar_voto(eleitor["id"], candidato["id"], candidato["numero"], "VALIDO")
                    voto_confirmado = True
                else:
                    print("Voto nao confirmado. Digite o numero novamente.")
            else:
                print("\nNenhum candidato encontrado com este numero.")
                confirmacao = input("Deseja confirmar mesmo assim? O voto sera registrado como NULO. (s/n): ")

                if confirmacao.lower() == "s":
                    _confirmar_voto(eleitor["id"], None, numero, "NULO")
                    voto_confirmado = True
                else:
                    print("Voto nao confirmado. Digite o numero novamente.")


def _confirmar_voto(eleitor_id, candidato_id, numero_candidato, tipo):
    """
    Executa a rotina _confirmar_voto.
    
    Args:
        eleitor_id (int): Valor usado pela funcao.
        candidato_id (int): Valor usado pela funcao.
        numero_candidato (int): Valor usado pela funcao.
        tipo (str): Valor usado pela funcao.
    
    Returns:
        None: Resultado da funcao.
    """
    protocolo = registrar_voto(eleitor_id, candidato_id, numero_candidato, tipo)

    if protocolo:
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
    """
    Executa a rotina fluxo_encerramento.
    
    Args:
        Nenhum.
    
    Returns:
        bool: Resultado da funcao.
    """
    print("\n=== ENCERRAMENTO DA VOTACAO ===")
    print("O mesário deve se identificar para encerrar.")

    mesario = autenticar_mesario()

    if not mesario:
        return False

    confirmacao = input("\nDeseja realmente encerrar a votação? (S/N): ")

    if confirmacao.lower() not in ["sim", "s"]:
        print("Encerramento cancelado.")
        return False

    print("\nPor seguranca, digite sua chave de acesso novamente:")
    chave_confirmacao = input("Chave de Acesso: ")

    if criptografar_chave(chave_confirmacao) != mesario["chave_acesso"]:
        registrar_ocorrencia("ALERTA: Tentativa de acesso negado")
        print("Chave invalida! Encerramento cancelado.")
        return False

    registrar_ocorrencia("ENCERRAMENTO: Votação finalizada com sucesso.")
    print("\nVotacao encerrada com sucesso!")
    return True
