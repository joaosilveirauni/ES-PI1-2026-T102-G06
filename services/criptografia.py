def cpf_para_vetor(cpf): # Transforma a string do cpf em uma lista de inteiros de 11 digitos
    return [int(d) for d in cpf]

def adicionar_padding(vetor):
    """
    Transforma a lista do cpf em uma lista com 12 dígitos, pois trabalharemos com matriz 3x3
    11 não é divisível por 3, portanto optamos por adicionar um 0 ao final do vetor
    """
    
    vetor.append(0)
    return vetor

vetor = cpf_para_vetor("12345678900")
print(adicionar_padding(vetor))