def validar_cpf(cpf):
    cpf = cpf.replace(".", "").replace("-", "")
 
    if len(cpf) != 11:
        return False
 
    if cpf == cpf[0] * 11:
        return False
 
    try:
        for i in range(11):
            int(cpf[i])
    except:
        return False
 
    soma = 0
 
    soma = soma + int(cpf[0]) * 10
    soma = soma + int(cpf[1]) * 9
    soma = soma + int(cpf[2]) * 8
    soma = soma + int(cpf[3]) * 7
    soma = soma + int(cpf[4]) * 6
    soma = soma + int(cpf[5]) * 5
    soma = soma + int(cpf[6]) * 4
    soma = soma + int(cpf[7]) * 3
    soma = soma + int(cpf[8]) * 2

    resto = soma % 11
 
    if resto < 2:
        primeiro_dv = 0
    else:
        primeiro_dv = 11 - resto
 
    if primeiro_dv != int(cpf[9]):
        return False
 
    soma = 0
 
    soma = soma + int(cpf[0]) * 11
    soma = soma + int(cpf[1]) * 10
    soma = soma + int(cpf[2]) * 9
    soma = soma + int(cpf[3]) * 8
    soma = soma + int(cpf[4]) * 7
    soma = soma + int(cpf[5]) * 6
    soma = soma + int(cpf[6]) * 5
    soma = soma + int(cpf[7]) * 4
    soma = soma + int(cpf[8]) * 3
    soma = soma + int(cpf[9]) * 2
 
    resto = soma % 11
 
    if resto < 2:
        segundo_dv = 0
    else:
        segundo_dv = 11 - resto
 
    if segundo_dv != int(cpf[10]):
        return False
 
    return True
 
 
def pedir_cpf():
    cpf = input("Digite o CPF: ")
    cpf = cpf.replace(".", "").replace("-", "")
 
    while not validar_cpf(cpf):
        print("❌ CPF inválido! Tente novamente.")
        cpf = input("Digite o CPF: ")
        cpf = cpf.replace(".", "").replace("-", "")

    return cpf
 
def validar_titulo(titulo):
    if len(titulo) != 12:
        return False
 
    try:
        for i in range(12):
            int(titulo[i])
    except:
        return False
 
    sequencial = titulo[0:8]
    uf = int(titulo[8:10])
 
    if uf < 1 or uf > 28:
        return False
 
    if uf == 1 or uf == 2:
        e_sp_ou_mg = True
    else:
        e_sp_ou_mg = False
 
    soma = 0
 
    soma = soma + int(sequencial[0]) * 2
    soma = soma + int(sequencial[1]) * 3
    soma = soma + int(sequencial[2]) * 4
    soma = soma + int(sequencial[3]) * 5
    soma = soma + int(sequencial[4]) * 6
    soma = soma + int(sequencial[5]) * 7
    soma = soma + int(sequencial[6]) * 8
    soma = soma + int(sequencial[7]) * 9
 
    resto = soma % 11
 
    if resto == 0 and e_sp_ou_mg:
        primeiro_dv = 1
    elif resto == 0 or resto == 10:
        primeiro_dv = 0
    else:
        primeiro_dv = resto
 
    if primeiro_dv != int(titulo[10]):
        return False

    soma = 0
 
    soma = soma + int(titulo[8]) * 7
    soma = soma + int(titulo[9]) * 8
    soma = soma + primeiro_dv   * 9
 
    resto = soma % 11
 
    if resto == 0 and e_sp_ou_mg:
        segundo_dv = 1
    elif resto == 0 or resto == 10:
        segundo_dv = 0
    else:
        segundo_dv = resto
 
    if segundo_dv != int(titulo[11]):
        return False
 
    return True
 
 
def pedir_titulo():
    titulo = input("Digite o Título de Eleitor (12 dígitos): ")
 
    while not validar_titulo(titulo):
        print("❌ Título inválido! Tente novamente.")
        titulo = input("Digite o Título de Eleitor (12 dígitos): ")
 
    return titulo