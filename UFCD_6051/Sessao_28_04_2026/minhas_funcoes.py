def calcular_corrente(potencia, tensao):
    corrente = potencia / tensao
    return corrente

def selecionar_disjuntor(valor):
    if valor <6:
        print("C6")
    elif valor >=6 and valor <10:
        print("C10")
    elif valor >=10 and valor <16:
        print("C16")
    elif valor >=16 and valor <20:
        print("C20")
    elif valor >=20 and valor <25:
        print("C25")