# ciclo principal

while True:
    # dados de entrada
    sensor_de_nivel = 35

    # processamento
    if sensor_de_nivel >= 40:
        ativa_desligar_bomba_de_agua = True
    else:
        ativa_desligar_bomba_de_agua = False