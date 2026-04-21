# operações com IVA

# IVA
valorIVA = 1.23
valorsemIVA = 15

valor_com_IVA = valorsemIVA * valorIVA
print(valor_com_IVA)

IVA_Continental = 23
preco_sem_iva = 100
preco_com_iva = 1.23 * preco_sem_iva
preco_com_iva = (1 + IVA_Continental / 100) * preco_sem_iva
print(preco_com_iva)