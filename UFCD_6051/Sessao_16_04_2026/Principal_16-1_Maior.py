# ciclo principal

while True:
    # dados de entrada
    sensor_de_pressao = 35

    # processamento
    if sensor_de_pressao > 40:
        ativa_eletrovalvula = True
    else:
        ativa_eletrovalvula = False