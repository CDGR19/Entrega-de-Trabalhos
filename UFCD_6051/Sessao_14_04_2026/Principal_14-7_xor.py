# ciclo principal
while True:

    # dados de entrada
    interruptor_A = False
    interruptor_B = True

    # processamento
    if (not interruptor_A and interruptor_B) or (interruptor_A and not interruptor_B):
        ligar_luz = True
    else:
        ligar_luz = False

    if interruptor_A ^ interruptor_B:
        ligar_luz = True
    else:
        ligar_luz = False