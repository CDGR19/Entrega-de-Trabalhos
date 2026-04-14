# ciclo principal
while True:

    # dados de entrada
    humidade_solo1 = False
    humidade_solo2 = True

    # processamento
    if not (humidade_solo1 and humidade_solo2):
        ligar_sistema_rega = True
    else:
        ligar_sistema_rega = False