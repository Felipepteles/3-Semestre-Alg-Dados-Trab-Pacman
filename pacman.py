from pynput import keyboard
from pynput.keyboard import Key
import datetime
import os
import csv


posicaoX = 5
posicaoY = 5
parede = "@"
comida = "."
fantasma = "#"
pacman = "*"
pontos = 0
nome = input("Insira o seu nome: ")
data = datetime.datetime.now()
status = False
cabecalho = ["Nome", "Pontos", "Data", "Status"]
lista = []

matriz = [
  ["@","@","@","@","@","@","@","@","@","@","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@",".",".",".",".",".",".",".",".",".","@"],
  ["@","@","@","@","@","@","@","@","@","@","@"]
]


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

def tabela(X, Y):
  os.system("cls")
  print(f"Pontos: {pontos}")
  for i, linha in enumerate(matriz):
    for j, coluna in enumerate(linha):
      if j == Y and i == X:
        print(pacman, end="")
      else:
        print(coluna, end="")
    print("\n") 
  ganhou()
    
def colisao(X, Y):
  if matriz[X][Y] == parede:
    return 1
  if matriz[X][Y] == comida:
    return 2
  if matriz[X][Y] == fantasma:
    return 3
  else:
    return 0
  
def morreu():
  print("Morreu otario")
  salva()
  exit()
  
def comeu():
  matriz[posicaoX][posicaoY] = " "
  
  
def ganhou():
  global status
  if pontos == 1080:
    print("Voce ganhou")
    print(f"Pontuação final: {pontos}")
    status = True
    salva()
    exit()
        
   
def setas(tecla):
  global posicaoX
  global posicaoY
  global pontos
  
  if tecla == Key.up:
    colisaoFuturo = colisao(posicaoX - 1, posicaoY)
    if colisaoFuturo == 0:
      posicaoX = posicaoX - 1
    elif colisaoFuturo == 2:
      pontos += 15
      posicaoX = posicaoX - 1
      comeu()
    elif colisaoFuturo == 3:
      morreu()
    tabela(posicaoX, posicaoY)
    
    
  elif tecla == Key.left:
    colisaoFuturo = colisao(posicaoX, posicaoY - 1)
    if colisaoFuturo == 0:
      posicaoY = posicaoY - 1
    elif colisaoFuturo == 2:
      pontos += 15
      posicaoY = posicaoY - 1
      comeu()
    elif colisaoFuturo == 3:
      morreu()
    tabela(posicaoX, posicaoY)
    
  elif tecla == Key.right:
    colisaoFuturo = colisao(posicaoX, posicaoY + 1)
    if colisaoFuturo == 0:
      posicaoY = posicaoY + 1
    elif colisaoFuturo == 2:
      pontos += 15
      posicaoY = posicaoY + 1
      comeu()
    elif colisaoFuturo == 3:
      morreu()
    tabela(posicaoX, posicaoY)
    
  elif tecla == Key.down:
    colisaoFuturo =colisao(posicaoX + 1, posicaoY)
    if colisaoFuturo == 0:
      posicaoX = posicaoX + 1
    elif colisaoFuturo == 2:
      pontos += 15
      posicaoX = posicaoX + 1
      comeu()
    elif colisaoFuturo == 3:
      morreu()
    tabela(posicaoX, posicaoY)
    
  elif tecla == Key.esc:
    exit()
        
tabela(posicaoX, posicaoY)
with keyboard.Listener(on_release=setas) as listener:
  listener.join()