# ciclo principal

while True:
    # dados de entrada
    sensor_de_humidade = 5
    temporizador = 75 # horas
    cacto = 1

    # processamento
    if sensor_de_humidade < 10 and temporizador >72 and cacto == 1:
        Ligar_rega = True
    else:
        Ligar_rega = False