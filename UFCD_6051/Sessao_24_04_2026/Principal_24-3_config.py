config = {
    "produtos" : {
        "café longo" : {
            "preco" : "0.5",
            "tem_palheta" : True,
            "nivel_acucar" : 2,
            "tem_copo" : True,
            "botao_cafe_longo": "periferico_2"
        },
        "café comprido" : {
            "preco" : "0.5",
        },
        "chá" : {
            "preco" : "0.2",
        },
        "cappucino" : {
            "preco" : "0.6",
        }
    }
}

config["produtos"]
config["produtos"]["cha"]
preco_do_cha = config["produtos"]["cha"]["preco"]

config["produtos"]["cafe longo"]["nivel_de_acucar"] += 1

config_da_maquina = {
    "velocidade"
}

botao_cafe_longo = config["produtos"]["cafe longo"]["botao_cafe_longo"]

#ciclo principal
while True:
    #dados de entrada
    velocidade_da_maquina = config_da_maquina["velocidade"]

    #processamento
    if botao_cafe_longo and dinheiro_certo:
        if config["produtos"]["cafe longo"]["tem_copo"]:
            colocar_copo ()
        else:
            nao_colocar_copo()
        
        if botao_tirar_acucar :
            if config["produtos"]["cafe longo"]["nive_de_acucar"] > 0:
                config["produtos"]["cafe longo"]["nive_de_acucar"] -= 1


def colocar_copo():
    """Código para pedir à máquina para tirar copo"""
    print("Tirar copo")