import datetime
import os
import csv
import random  
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

posicaoX = 5
posicaoY = 5
nome = ""
parede = " 🟦"
comida = " ▫ "
fantasma = " 👻"
cereja = "🍒"
pacman_atual = None
pontos = 0
status = None
velocidade = 550
cabecalho = ["Nome", "Pontos", "Duracao", "Status"]
lista = []
fantasmas_info = {}  
width = 660
height = 660

matriz = [
    [" 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"],
    [" 🟦"," 👻"," ▫ "," ▫ ","🍒"," 🟦"," ▫ "," ▫ "," ▫ "," 👻"," 🟦"],
    [" 🟦"," ▫ "," 🟦"," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," 🟦"," ▫ "," 🟦"],
    [" 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"],
    [" 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"," ▫ "," 🟦"],
    [" "," ▫ "," ▫ "," ▫ "," ▫ ","   "," ▫ "," ▫ "," ▫ "," ▫ "," "],
    [" 🟦"," ▫ "," 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"," ▫ "," 🟦"],
    [" 🟦"," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," ▫ "," 🟦"],
    [" 🟦"," ▫ "," 🟦"," ▫ "," ▫ "," 🟦"," ▫ "," ▫ "," 🟦"," ▫ "," 🟦"],
    [" 🟦"," 👻"," ▫ "," ▫ "," ▫ "," 🟦","🍒"," ▫ "," ▫ "," 👻"," 🟦"],
    [" 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"," 🟦"]
]


def ler_csv():
    if os.path.exists("lista.csv"):
        with open('lista.csv', mode='r') as arq:
            csvfile = csv.DictReader(arq)
            for linha in csvfile:
                lista.append(linha)

def salva_csv():
    fim_partida = datetime.datetime.now()
    duracao = fim_partida - inicio_partida
    with open('lista.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=cabecalho)
        writer.writeheader()
        writer.writerows(lista)
        writer.writerow({'Nome': nome.get(), 'Pontos': pontos, "Duracao": str(duracao).split(".")[0], "Status": status})

def tabela(posicao_pacman_X, posicao_pacman_Y):
    canvas.delete("all")
    for linha in range(len(matriz)):
        for coluna in range(len(matriz[linha])):
            cofx = tamanhox * coluna
            cofy = tamanhoy * linha
            if status != "Perdeu" and linha == posicao_pacman_X and coluna == posicao_pacman_Y:
                caractere = pacman_atual
                canvas.create_image(cofx, cofy, image=pacman_atual, anchor="nw")
            else:
                caractere = matriz[linha][coluna]
                if caractere == fantasma:
                    canvas.create_image(cofx, cofy, image=fantasmapng, anchor="nw")
                elif caractere == parede:
                    canvas.create_image(cofx, cofy, image=paredepng, anchor="nw")
                elif caractere == comida:
                    canvas.create_image(cofx, cofy, image=comidapng, anchor="nw")
                elif caractere == cereja:
                    canvas.create_image(cofx, cofy, image=cerejapng, anchor="nw")
    if status != "Venceu":
        ganhou()

def colisao(linha, coluna):
    if matriz[linha][coluna] == parede:
        return 1
    if matriz[linha][coluna] == comida:
        return 2
    if matriz[linha][coluna] == fantasma:
        return 3
    if matriz[linha][coluna] == cereja:
        return 4
    return 0

def perdeu():
    global status
    status = "Perdeu"
    tabela(posicaoX, posicaoY)
    salva_csv()
    messagebox.showinfo("Fim de jogo", f"Você perdeu!\nPontuação final: {pontos}")
    exit()

def comeu():
    global pontos, velocidade
    if tipo_colisao == 2:
        matriz[posicaoX][posicaoY] = "   "
        pontos += 15
        pontuacao_label.config(text=f"Pontos: {pontos}")
    elif tipo_colisao == 4:
        matriz[posicaoX][posicaoY] = "   "
        pontos += 35
        pontuacao_label.config(text=f"Pontos: {pontos}")
        velocidade = 1100
        janela.after(4000, restaura_velocidade)

def restaura_velocidade():
    global velocidade
    velocidade = 550
    
def ganhou():
    global status
    if pontos >= 1000 and status != "Venceu":
        status = "Venceu"
        salva_csv()
        messagebox.showinfo("Parabéns!", f"Você venceu!\nPontuação final: {pontos}")
        exit()

def mover_fantasmas():
    global fantasmas_info

    direcoes_possiveis = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    novas_posicoes = {}
    novas_infos = {}

    #fantasmas_posicoes = list(fantasmas_info.keys()) if fantasmas_info else []

    if not fantasmas_info:
        for linha in range(len(matriz)):
            for coluna in range(len(matriz[linha])):
                if matriz[linha][coluna] == fantasma:
                    fantasmas_info[(linha, coluna)] = comida


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
                        perdeu()

                    matriz[linha_atual][coluna_atual] = conteudo_anterior
                    novas_infos[(nova_linha, nova_coluna)] = matriz[nova_linha][nova_coluna]
                    novas_posicoes[(nova_linha, nova_coluna)] = fantasma
                    break
                elif nova_linha == posicaoX and nova_coluna == posicaoY:
                    perdeu()
        else:
            novas_posicoes[(linha_atual, coluna_atual)] = fantasma
            novas_infos[(linha_atual, coluna_atual)] = conteudo_anterior

    fantasmas_info = novas_infos
    for (linha, coluna), simbolo in novas_posicoes.items():
        matriz[linha][coluna] = simbolo

def setas(tecla):
    global posicaoX, posicaoY, tipo_colisao, pacman_atual
    deslocamento_linha = 0
    deslocamento_coluna = 0

    if tecla.keysym == "Up":
        deslocamento_linha = -1
        pacman_atual = pacman_cimapng
    elif tecla.keysym == "Down":
        deslocamento_linha = 1
        pacman_atual = pacman_baixopng
    elif tecla.keysym == "Left":
        deslocamento_coluna = -1
        pacman_atual = pacman_esqpng
    elif tecla.keysym == "Right":
        deslocamento_coluna = 1
        pacman_atual = pacman_dirpng
    elif tecla.keysym == "Escape":
        exit()
    else:
        return
    
    nova_posicaoX = posicaoX + deslocamento_linha
    nova_posicaoY = posicaoY + deslocamento_coluna
    
    if nova_posicaoX == 5 and nova_posicaoY < 0:
        nova_posicaoY = 10
    elif nova_posicaoX == 5 and nova_posicaoY > 10:
        nova_posicaoY = 0

    tipo_colisao = colisao(nova_posicaoX, nova_posicaoY)

    if tipo_colisao == 0:
        posicaoX = nova_posicaoX
        posicaoY = nova_posicaoY
    elif tipo_colisao == 2 or tipo_colisao == 4:
        posicaoX = nova_posicaoX
        posicaoY = nova_posicaoY
        comeu()
    elif tipo_colisao == 3:
        posicaoX = nova_posicaoX
        posicaoY = nova_posicaoY
        perdeu()
    tabela(posicaoX, posicaoY)
    
def exibir_ranking():
    vencedores = [jogador for jogador in lista if jogador["Status"] == "Venceu"]
    vencedores_ordenados = sorted(vencedores, key=lambda grupo: grupo['Duracao'])[:10]

    if not vencedores_ordenados:
        messagebox.showinfo("Ranking", "Nenhum jogador venceu ainda.")
        return

    ranking_texto = "🏆 Top 10 Jogadores Vencedores (Menor Tempo):\n\n"
    for num, jogador in enumerate(vencedores_ordenados, start=1):
        ranking_texto += f"{num}. {jogador['Nome']} - {jogador['Pontos']} pts - {jogador['Duracao']}\n"

    messagebox.showinfo("Ranking", ranking_texto)

def exibir_instrucoes():
    texto = '''
    Instruções do Jogo:\n\n
        - Use as teclas de seta (↑ ↓ ← →) para mover o Pac-Man.\n
        - Colete todas as comidas para vencer.\n
        - Colete as comidas especiais para desacelerar os fantasmas durante 4s.\n
        - Evite os fantasmas, se colidir com um, você perde.\n
        - Cada comida vale 15 pontos.\n
        - Cada comida especial vale 35 pontos.
        - Pontuação máxima: 970 pontos.\n
        - Pressione ESC para sair a qualquer momento.
    '''
    messagebox.showinfo("Instruções", texto)

def iniciar_jogo():
    global inicio_partida
    if not nome.get().strip():
        messagebox.showwarning("Nome obrigatório", "Por favor, digite seu nome antes de começar.")
        return
    inicio_partida = datetime.datetime.now()
    frame_menu.pack_forget()
    frame_superior.pack()
    pontuacao_label.pack()
    canvas.pack()
    tabela(posicaoX, posicaoY)
    janela.bind("<KeyPress>", setas)
    loop_fantasmas()
    
def menu():
    global frame_menu, nome, botao_iniciar, botao_ranking, botao_instrucoes
    ler_csv()
    frame_menu = tk.Frame(janela)
    frame_menu.pack(padx=15)

    titulo = tk.Label(frame_menu, text="PAC-MAN", font=("Arial", 20, "bold"))
    titulo.pack(pady=10)

    label_nome = tk.Label(frame_menu, text="Digite seu nome:", font=("Arial", 14))
    label_nome.pack(pady=(20, 5))

    nome = tk.Entry(frame_menu, font=("Arial", 14), justify="center")
    nome.pack(pady=(0, 20))

    botao_iniciar = tk.Button(frame_menu, text="▶ Iniciar Jogo", font=("Arial", 14), width=20, command=iniciar_jogo)
    botao_iniciar.pack(pady=10)

    botao_ranking = tk.Button(frame_menu, text="🏆 Ver Ranking", font=("Arial", 14), width=20, command=exibir_ranking)
    botao_ranking.pack(pady=10)

    botao_instrucoes = tk.Button(frame_menu, text="📜 Instruções", font=("Arial", 14), width=20, command=exibir_instrucoes)
    botao_instrucoes.pack(pady=10)

    frame_superior.pack_forget()
    pontuacao_label.pack_forget()
    canvas.pack_forget()

def exibir_janela():
    global janela, frame_superior, pontuacao_label, canvas
    global fantasmapng, pacman_atual, comidapng, paredepng, cerejapng, pacman_cimapng, pacman_baixopng, pacman_dirpng, pacman_esqpng
    global tamanhox, tamanhoy
    
    janela = tk.Tk()
    janela.title("PAC-MAN")

    frame_superior = tk.Frame(janela)
    frame_superior.pack()

    pontuacao_label = tk.Label(janela, text=f"Pontos: {pontos}", font=("Arial", 22))
    pontuacao_label.pack()

    canvas = tk.Canvas(janela, width=width, height=height, bg="black")
    canvas.pack()

    tamanhox = int(width / 11)
    tamanhoy = int(height / 11)
    fantasmapng = ImageTk.PhotoImage(Image.open("img/fantasma.png").resize((tamanhox,tamanhoy)))
    pacman_cimapng = ImageTk.PhotoImage(Image.open("img/pacmanc.png").resize((tamanhox,tamanhoy)))
    pacman_baixopng = ImageTk.PhotoImage(Image.open("img/pacmanb.png").resize((tamanhox,tamanhoy)))
    pacman_esqpng = ImageTk.PhotoImage(Image.open("img/pacmane.png").resize((tamanhox,tamanhoy)))
    pacman_dirpng = ImageTk.PhotoImage(Image.open("img/pacmand.png").resize((tamanhox,tamanhoy)))
    comidapng = ImageTk.PhotoImage(Image.open("img/food.png").resize((tamanhox,tamanhoy)))
    paredepng = ImageTk.PhotoImage(Image.open("img/parede.png").resize((tamanhox,tamanhoy)))
    cerejapng = ImageTk.PhotoImage(Image.open("img/cereja.png").resize((tamanhox,tamanhoy)))
    
    pacman_atual = pacman_dirpng
      
def loop_fantasmas():
    mover_fantasmas()
    tabela(posicaoX, posicaoY)
    if status == None :
        janela.after(velocidade, loop_fantasmas)

exibir_janela()
menu()
janela.mainloop()