from pynput import keyboard
from pynput.keyboard import Key
import datetime
import os
import csv
import random  
import tkinter as tk

posicaoX = 5
posicaoY = 5
parede = " 🟦"
comida = " ▫ "
fantasma = " 👻"
pacman = " © "
pontos = 0
nome = input("Insira o seu nome: ")
data = datetime.datetime.now()
status = "Morreu"
cabecalho = ["Nome", "Pontos", "Data", "Status"]
lista = []

matriz = [
    [" 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"],
    [" 🟦"," 👻"," ▫ "," ▫ "," ▫ "," 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"],
    [" 🟦"," ▫ "," 🟦"," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," 🟦"," ▫ "," 🟦"],
    [" 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"],
    [" 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"],
    [" 🟦"," ▫ "," ▫ "," ▫ "," ▫ ","   "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"],
    [" 🟦"," ▫ "," 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"," ▫ "," 🟦"],
    [" 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"],
    [" 🟦"," 🟦"," 🟦"," ▫ "," ▫ "," 🟦"," ▫ "," ▫ "," 🟦"," 🟦"," 🟦"],
    [" 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"," ▫ "," ▫ "," ▫ "," 👻"," 🟦"],
    [" 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"]
]

fantasmas_info = {}  

janela = tk.Tk()
janela.title("PAC-MAN")
texto = tk.Text(janela)


if os.path.exists("lista.csv"):
    with open('lista.csv', mode='r') as arq:
        csvfile = csv.DictReader(arq)
        for linha in csvfile:
            lista.append(linha)

def salva():
    with open('lista.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(lista)
        writer.writerow({'Nome': nome, 'Pontos': pontos, "Data": data, "Status": status})

def tabela(posicao_pacman_X, posicao_pacman_Y):
    texto_matriz = ""
    os.system("cls" if os.name == "nt" else "clear")
    print(f"Pontos: {pontos}")
    for linha in range(len(matriz)):
        for coluna in range(len(matriz[linha])):
            if linha == posicao_pacman_X and coluna == posicao_pacman_Y:
                print(pacman, end="")
                texto_matriz += pacman
            else:
                print(matriz[linha][coluna], end="")
                texto_matriz += matriz[linha][coluna]
        print()
        texto_matriz += "\n"
        
    ganhou()
    texto.delete("0.0", tk.END)
    texto.insert(tk.END, texto_matriz)
    texto.pack()

def colisao(linha, coluna):
    if matriz[linha][coluna] == parede:
        return 1
    if matriz[linha][coluna] == comida:
        return 2
    if matriz[linha][coluna] == fantasma:
        return 3
    return 0

def morreu():
    print("Morreu otário")
    salva()
    exit()

def comeu():
    global pontos
    matriz[posicaoX][posicaoY] = "   "
    pontos += 15

def ganhou():
    global status
    if pontos == 900:
        print("Você ganhou!")
        print(f"Pontuação final: {pontos}")
        status = "Venceu"
        salva()
        exit()

def mover_fantasmas():
    global fantasmas_info

    direcoes_possiveis = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    novas_posicoes = {}
    novas_infos = {}

    fantasmas_posicoes = list(fantasmas_info.keys()) if fantasmas_info else []

    if not fantasmas_info:
        for linha in range(len(matriz)):
            for coluna in range(len(matriz[linha])):
                if matriz[linha][coluna] == fantasma:
                    fantasmas_info[(linha, coluna)] = comida if comida == matriz[linha][coluna] else "   "

    for (linha_atual, coluna_atual) in list(fantasmas_info.keys()):
        conteudo_anterior = fantasmas_info[(linha_atual, coluna_atual)]
        random.shuffle(direcoes_possiveis)

        for deslocamento_linha, deslocamento_coluna in direcoes_possiveis:
            nova_linha = linha_atual + deslocamento_linha
            nova_coluna = coluna_atual + deslocamento_coluna

            if (0 <= nova_linha < len(matriz) and 0 <= nova_coluna < len(matriz[0])):
                destino = matriz[nova_linha][nova_coluna]
                destino_vazio = destino in ["   ", comida]
                destino_ocupado = (nova_linha, nova_coluna) in novas_posicoes

                if destino_vazio and not destino_ocupado:
                    if nova_linha == posicaoX and nova_coluna == posicaoY:
                        morreu()

                    matriz[linha_atual][coluna_atual] = conteudo_anterior
                    novas_infos[(nova_linha, nova_coluna)] = matriz[nova_linha][nova_coluna]
                    novas_posicoes[(nova_linha, nova_coluna)] = fantasma
                    break
                elif nova_linha == posicaoX and nova_coluna == posicaoY:
                    morreu()
        else:
            novas_posicoes[(linha_atual, coluna_atual)] = fantasma
            novas_infos[(linha_atual, coluna_atual)] = conteudo_anterior

    fantasmas_info = novas_infos
    for (linha, coluna), simbolo in novas_posicoes.items():
        matriz[linha][coluna] = simbolo

def setas(tecla):
    global posicaoX, posicaoY
    deslocamento_linha = 0
    deslocamento_coluna = 0

    if tecla.keysym == "Up":
        deslocamento_linha = -1
    elif tecla.keysym == "Down":
        deslocamento_linha = 1
    elif tecla.keysym == "Left":
        deslocamento_coluna = -1
    elif tecla.keysym == "Right":
        deslocamento_coluna = 1
    elif tecla.keysym == "Escape":
        exit()
    else:
        return

    nova_posicaoX = posicaoX + deslocamento_linha
    nova_posicaoY = posicaoY + deslocamento_coluna

    tipo_colisao = colisao(nova_posicaoX, nova_posicaoY)

    if tipo_colisao == 0:
        posicaoX = nova_posicaoX
        posicaoY = nova_posicaoY
    elif tipo_colisao == 2:
        posicaoX = nova_posicaoX
        posicaoY = nova_posicaoY
        comeu()
    elif tipo_colisao == 3:
        morreu()

    mover_fantasmas()
    tabela(posicaoX, posicaoY)

tabela(posicaoX, posicaoY)
janela.bind("<KeyPress>", setas)
janela.mainloop()
with keyboard.Listener(on_release=setas) as listener:
    listener.join()
