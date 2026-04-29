### - Criar uma estrutura de dados com componentes de um quadro elétrico à escolha.
# Mencionar as especificações dos componentes.
quadro = {
    "corte_geral" : {
        "In" : 32,
    },
    "diferencial_300ma" : {
        "In" : 25,
    },
    "diferencial_30ma" : {
        "In" : 25,
    },
    "disjuntor_unipolar" : {
        "In" : 20,
    },
    "disuntor_unipolar" : {
        "In" : 16,
    },
    "disjuntor_unipolar" : {
        "In" : 10,
    },
    "barramentos" : {
        "neutro" : "cobre",
        "terra" : "cobre"
    },
    "barra_de_cobre" : {
        "12mod"
    },
    "ponteiras" : {
        "10mm",
        "6mm",
        "4mm",
        "2,5mm",
        "1,5"
    },
    "caixa_de_quadro" : {
        "tipo_de_instalacao" : "embutir",
        "tipo_de_mateterial" : "plástico",
        "tipo_de_calha_din" : "metálico",
        "numero_modulos" : 24,
    },
    "seccao_condutores" : {
        "tipo_cabo" : "H07V-U",
        "alimentacao" : "10mm²",
        "forno_ou_placa" : "6mm²",
        "iluminacao" : "1.5mm²",
        "tomadas" : "2.5mm²"
    }
}

lampadas = {
    "potencia" : 40,
    "tensao" : 230,
    "quantidade" : 3
}

import minhas_funcoes

corrente_de_cada_lampada = lampadas["potencia"] / lampadas["tensao"]
print(corrente_de_cada_lampada)
corrente_de_cada_lampada = minhas_funcoes.calcular_corrente(lampadas["potencia"], lampadas["tensao"])
print(corrente_de_cada_lampada)

corrente_de_todas_as_lampadas = corrente_de_cada_lampada * lampadas["quantidade"]
corrente_de_todas_as_lampadas

minhas_funcoes.selecionar_disjuntor(corrente_de_todas_as_lampadas)