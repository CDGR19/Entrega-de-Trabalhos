#Base de Dados

#Equipamentos da Sala de Aula
lista_de_materiais = [
    "mesa1",
    "mesa1",
    "mesa1",
    "cadeira1",
    "cadeira1",
    "cadeira1",
    "armario_de_arrumacao"
    "computadore1",
    "computadore1",
    "computadore1",
    "monitore1",
    "monitore1",
    "monitore1",
    "teclado1",
    "teclado1",
    "teclado1",
    "rato1",
    "rato1",
    "rato1",
    "quadro_interativo",
    "quadro_de_escrita"
]

materiais = {
    "mesa1": {
        "tamanho": {
            "comprimento": 80,
            "altura": 65,
            "largura": 40
        },
        "tampo_da_mesa": {
            "tipo": "madeira",
            "cor": "folha_branca"
        },
        "estrutura": {
            "tipo": "ferro",
            "cor": "cinza_escuro"
        }
    },
    "cadeira1": {
        "tamanho": {
            "comprimento": 25,
            "altura": 30,
            "largura": 25
        },
        "tampo_da_cadeira": {
            "tipo": "plastico",
            "cor": "cinza_claro"
        },
        "estrutura": {
            "tipo": "ferro",
            "cor": "cinza_escuro"
        }
    },
    "armario_de_arrumacao": {
        "tamanho": {
            "comprimento": 700,
            "altura": 100,
            "largura": 60
        },
        "tampo_do_armario": {
            "tipo": "madeira",
            "cor": "folha_branca"
        },
        "estrutura": {
            "tipo": "madeira",
            "cor": "cinza_escuro"
        }
    },
    "computador1": {
        "tamanho": {
            "comprimento": 50,
            "altura": 15,
            "largura": 50
        },
        "estrutura": {
            "tipo": ["metal", "plastico"],
            "cor": "cinza_escuro"
        },
        "especificacoes": {
            "processador": "i7",
            "sistema_operativo": "windows10"
        }
    },
    "monitor1": {
        "tamanho": {
            "comprimento": 50,
            "altura": 15,
            "largura": 50
        },
        "estrutura": {
            "tipo": "metal",
            "cor": "cinza_escuro"
        },
        "especificacoes": {
            "ecra": "15'",
            "sistema_operativo": "windows10"
        }
    }
}