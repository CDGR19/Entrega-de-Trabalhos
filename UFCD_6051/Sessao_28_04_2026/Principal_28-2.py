import tkinter

raiz = tkinter.Tk()

texto = tkinter.Entry()
texto.pack()

def ligar_lampada_0():
    print ("Olá")

def ligar_lampada_1():
    print ("Testar")

# Criar o Botão
botao0 = tkinter.Button(text="0", command=ligar_lampada_0)
botao1 = tkinter.Button(text="1", command=ligar_lampada_1)
botao2 = tkinter.Button(text="2")
botao3 = tkinter.Button(text="3")
botao4 = tkinter.Button(text="4")
botao5 = tkinter.Button(text="5")
botao6 = tkinter.Button(text="6")
botao7 = tkinter.Button(text="7")
botao8 = tkinter.Button(text="8")
botao9 = tkinter.Button(text="9")

# Envia-lo para o Interface
botao0.pack()
botao1.pack()
botao2.pack()
botao3.pack()
botao4.pack()
botao5.pack()
botao6.pack()
botao7.pack()
botao8.pack()
botao9.pack()

# Arrancar com o Interface
raiz.mainloop()