import random
import string

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


def cpf_para_vetor(cpf):
    return [int(d) for d in cpf]


def multiplicar_bloco(bloco):
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE[0][0]*bloco[0] + CHAVE[0][1]*bloco[1] + CHAVE[0][2]*bloco[2]) % 26
    resultado[1] = (CHAVE[1][0]*bloco[0] + CHAVE[1][1]*bloco[1] + CHAVE[1][2]*bloco[2]) % 26
    resultado[2] = (CHAVE[2][0]*bloco[0] + CHAVE[2][1]*bloco[1] + CHAVE[2][2]*bloco[2]) % 26
    return resultado


def multiplicar_bloco_inverso(bloco):
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE_INVERSA[0][0]*bloco[0] + CHAVE_INVERSA[0][1]*bloco[1] + CHAVE_INVERSA[0][2]*bloco[2]) % 26
    resultado[1] = (CHAVE_INVERSA[1][0]*bloco[0] + CHAVE_INVERSA[1][1]*bloco[1] + CHAVE_INVERSA[1][2]*bloco[2]) % 26
    resultado[2] = (CHAVE_INVERSA[2][0]*bloco[0] + CHAVE_INVERSA[2][1]*bloco[1] + CHAVE_INVERSA[2][2]*bloco[2]) % 26
    return resultado


def criptografar_cpf(cpf):
    vetor = cpf_para_vetor(cpf)
    vetor = vetor + [0]
    cifrado = []

    for i in range(0, 12, 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco(bloco)
        cifrado = cifrado + resultado

    return ''.join(chr(ord('A') + n) for n in cifrado)


def descriptografar_cpf(cifrado):
    vetor = [ord(c) - ord('A') for c in cifrado]
    original = []

    for i in range(0, 12, 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco_inverso(bloco)
        original = original + resultado

    return ''.join(str(n) for n in original[:11])


def gerar_chave_acesso(nome):
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
    texto = texto.upper()
    vetor = []

    for c in texto:
        if c.isdigit():
            vetor.append(int(c) + 16)
        elif c.isalpha():
            vetor.append(ord(c) - ord('A'))

    while len(vetor) % 3 != 0:
        vetor.append(0)

    cifrado = []
    for i in range(0, len(vetor), 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco(bloco)
        cifrado = cifrado + resultado

    return ''.join(chr(ord('A') + n) for n in cifrado)


def criptografar_chave(chave):
    return criptografar_texto(chave)


def gerar_protocolo(numero_candidato):
    letras = random.choices(string.ascii_uppercase, k=2)
    letras = letras[0] + letras[1]

    digitos = ''
    for i in range(5):
        digitos = digitos + str(random.randint(0, 9))

    if numero_candidato:
        numero_fmt = str(numero_candidato).zfill(2)
    else:
        numero_fmt = "00"

    return "V" + letras + "26" + numero_fmt + digitos


def criptografar_protocolo(protocolo):
    return criptografar_texto(protocolo)