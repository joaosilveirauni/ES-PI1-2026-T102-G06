import random

ALFABETO = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

CHAVE = [
    [1, 2, 3],
    [0, 1, 4],
    [5, 6, 0]
]

CHAVE_INVERSA = [
    [2, 18, 5],
    [20, 11, 22],
    [21, 4, 1]
]

CHAVE_INVERSA_TEXTO = [
    [12, 18, 5],
    [20, 21, 32],
    [31, 4, 1]
]


def cpf_para_vetor(cpf):
    """
    Executa a rotina cpf_para_vetor.
    
    Args:
        cpf (str): Valor usado pela funcao.
    
    Returns:
        list: Resultado da funcao.
    """
    return [int(d) for d in cpf]


def multiplicar_bloco(bloco):
    """
    Executa a rotina multiplicar_bloco.
    
    Args:
        bloco (list): Valor usado pela funcao.
    
    Returns:
        list: Resultado da funcao.
    """
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE[0][0]*bloco[0] + CHAVE[0][1]*bloco[1] + CHAVE[0][2]*bloco[2]) % 26
    resultado[1] = (CHAVE[1][0]*bloco[0] + CHAVE[1][1]*bloco[1] + CHAVE[1][2]*bloco[2]) % 26
    resultado[2] = (CHAVE[2][0]*bloco[0] + CHAVE[2][1]*bloco[1] + CHAVE[2][2]*bloco[2]) % 26
    return resultado


def multiplicar_bloco_inverso(bloco):
    """
    Executa a rotina multiplicar_bloco_inverso.
    
    Args:
        bloco (list): Valor usado pela funcao.
    
    Returns:
        list: Resultado da funcao.
    """
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE_INVERSA[0][0]*bloco[0] + CHAVE_INVERSA[0][1]*bloco[1] + CHAVE_INVERSA[0][2]*bloco[2]) % 26
    resultado[1] = (CHAVE_INVERSA[1][0]*bloco[0] + CHAVE_INVERSA[1][1]*bloco[1] + CHAVE_INVERSA[1][2]*bloco[2]) % 26
    resultado[2] = (CHAVE_INVERSA[2][0]*bloco[0] + CHAVE_INVERSA[2][1]*bloco[1] + CHAVE_INVERSA[2][2]*bloco[2]) % 26
    return resultado


def criptografar_cpf(cpf):
    """
    Executa a rotina criptografar_cpf.
    
    Args:
        cpf (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    vetor = cpf_para_vetor(cpf)
    vetor = vetor + [0]
    cifrado = []

    for i in range(0, 12, 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco(bloco)
        cifrado = cifrado + resultado

    return ''.join(chr(ord('A') + n) for n in cifrado)


def descriptografar_cpf(cifrado):
    """
    Executa a rotina descriptografar_cpf.
    
    Args:
        cifrado (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    vetor = [ord(c) - ord('A') for c in cifrado]
    original = []

    for i in range(0, 12, 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco_inverso(bloco)
        original = original + resultado

    return ''.join(str(n) for n in original[:11])


def gerar_chave_acesso(nome):
    """
    Executa a rotina gerar_chave_acesso.
    
    Args:
        nome (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    partes = nome.strip().upper().split()

    primeira = partes[0][:2] if len(partes[0]) >= 2 else partes[0][0] * 2

    if len(partes) >= 2:
        segunda = partes[1][0]
    else:
        segunda = partes[0][0]

    digitos = ''
    for i in range(4):
        digitos = digitos + str(random.randint(0, 9))

    return primeira + segunda + digitos


def criptografar_texto(texto):
    """
    Executa a rotina criptografar_texto.
    
    Args:
        texto (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    texto = texto.upper()
    vetor = []

    for c in texto:
        if c in ALFABETO:
            vetor.append(ALFABETO.index(c))

    while len(vetor) % 3 != 0:
        vetor.append(ALFABETO.index("X"))

    cifrado = []
    for i in range(0, len(vetor), 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco_texto(bloco)
        cifrado = cifrado + resultado

    return ''.join(ALFABETO[n] for n in cifrado)


def multiplicar_bloco_texto(bloco):
    """
    Executa a rotina multiplicar_bloco_texto.
    
    Args:
        bloco (list): Valor usado pela funcao.
    
    Returns:
        list: Resultado da funcao.
    """
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE[0][0]*bloco[0] + CHAVE[0][1]*bloco[1] + CHAVE[0][2]*bloco[2]) % 36
    resultado[1] = (CHAVE[1][0]*bloco[0] + CHAVE[1][1]*bloco[1] + CHAVE[1][2]*bloco[2]) % 36
    resultado[2] = (CHAVE[2][0]*bloco[0] + CHAVE[2][1]*bloco[1] + CHAVE[2][2]*bloco[2]) % 36
    return resultado


def multiplicar_bloco_texto_inverso(bloco):
    """
    Executa a rotina multiplicar_bloco_texto_inverso.
    
    Args:
        bloco (list): Valor usado pela funcao.
    
    Returns:
        list: Resultado da funcao.
    """
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE_INVERSA_TEXTO[0][0]*bloco[0] + CHAVE_INVERSA_TEXTO[0][1]*bloco[1] + CHAVE_INVERSA_TEXTO[0][2]*bloco[2]) % 36
    resultado[1] = (CHAVE_INVERSA_TEXTO[1][0]*bloco[0] + CHAVE_INVERSA_TEXTO[1][1]*bloco[1] + CHAVE_INVERSA_TEXTO[1][2]*bloco[2]) % 36
    resultado[2] = (CHAVE_INVERSA_TEXTO[2][0]*bloco[0] + CHAVE_INVERSA_TEXTO[2][1]*bloco[1] + CHAVE_INVERSA_TEXTO[2][2]*bloco[2]) % 36
    return resultado


def descriptografar_texto(cifrado):
    """
    Executa a rotina descriptografar_texto.
    
    Args:
        cifrado (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    vetor = [ALFABETO.index(c) for c in cifrado]
    original = []

    for i in range(0, len(vetor), 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco_texto_inverso(bloco)
        original = original + resultado

    return ''.join(ALFABETO[n] for n in original).rstrip("X")


def criptografar_chave(chave):
    """
    Executa a rotina criptografar_chave.
    
    Args:
        chave (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    return criptografar_texto(chave)


def gerar_protocolo(numero_candidato):
    """
    Executa a rotina gerar_protocolo.
    
    Args:
        numero_candidato (int): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    letras = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    letras = letras + random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    digitos = ''
    for i in range(5):
        digitos = digitos + str(random.randint(0, 9))

    if numero_candidato:
        numero_fmt = str(numero_candidato).zfill(2)[-2:]
    else:
        numero_fmt = "00"

    return "V" + letras + "26" + numero_fmt + digitos


def criptografar_protocolo(protocolo):
    """
    Executa a rotina criptografar_protocolo.
    
    Args:
        protocolo (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    return criptografar_texto(protocolo)


def descriptografar_protocolo(protocolo):
    """
    Executa a rotina descriptografar_protocolo.
    
    Args:
        protocolo (str): Valor usado pela funcao.
    
    Returns:
        str: Resultado da funcao.
    """
    return descriptografar_texto(protocolo)
