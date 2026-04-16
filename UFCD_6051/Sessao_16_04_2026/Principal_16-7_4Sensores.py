# ciclo principal

while True:
    # dados de entrada
    sensor_de_luz_1 = 15
    sensor_de_luz_2 = 13
    sensor_de_luz_3 = 11
    sensor_de_luz_4 = 9

    # processamento
    if sensor_de_luz_1 <= 10 or sensor_de_luz_2 <= 10 or sensor_de_luz_3 <= 10 or sensor_de_luz_4 <= 10:
        ligar_lampadas = True
    else:
        ligar_lampadas = False