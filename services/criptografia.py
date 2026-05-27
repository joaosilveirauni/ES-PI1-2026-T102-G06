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

def cpf_para_vetor(cpf): # Transforma a string do cpf em uma lista de inteiros de 11 digitos
    return [int(d) for d in cpf]



def multiplicar_bloco(bloco):
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE[0][0]*bloco[0] + CHAVE[0][1]*bloco[1] + CHAVE[0][2]*bloco[2]) % 26
    resultado[1] = (CHAVE[1][0]*bloco[0] + CHAVE[1][1]*bloco[1] + CHAVE[1][2]*bloco[2]) % 26
    resultado[2] = (CHAVE[2][0]*bloco[0] + CHAVE[2][1]*bloco[1] + CHAVE[2][2]*bloco[2]) % 26

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


def multiplicar_bloco_inverso(bloco):
    resultado = [0, 0, 0]
    resultado[0] = (CHAVE_INVERSA[0][0]*bloco[0] + CHAVE_INVERSA[0][1]*bloco[1] + CHAVE_INVERSA[0][2]*bloco[2]) % 26
    resultado[1] = (CHAVE_INVERSA[1][0]*bloco[0] + CHAVE_INVERSA[1][1]*bloco[1] + CHAVE_INVERSA[1][2]*bloco[2]) % 26
    resultado[2] = (CHAVE_INVERSA[2][0]*bloco[0] + CHAVE_INVERSA[2][1]*bloco[1] + CHAVE_INVERSA[2][2]*bloco[2]) % 26

    return resultado

def descriptografa_cpf(cifrado):
    vetor = [ord(c) - ord('A') for c in cifrado]
    original =  []

    for i in range(0, 12, 3):
        bloco = cifrado[i:i+3]
        resultado = multiplicar_bloco_inverso(bloco)
        original = original + resultado
    
    return ''.join(str(n) for n in original[:11])

def criptografar_chave(chave):
    
    chave = str(chave).upper()
    
    vetor = [ord(c) % 26 for c in chave]
    
    while len(vetor) % 3 != 0:
        vetor.append(0)
        
    cifrado = []
    
    for i in range(0, len(vetor), 3):
        bloco = vetor[i:i+3]
        resultado = multiplicar_bloco(bloco)
        cifrado = cifrado + resultado
        
    return ''.join(chr(ord('A') + n) for n in cifrado)
