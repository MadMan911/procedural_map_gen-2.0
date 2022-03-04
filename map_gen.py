import time

import pygame as p
from pygame.locals import *
import random


#
# def prost(n):
#     k = 0
#     for i in range(2, round(n**0.5)+3):
#         if i != n and n % i == 0:
#             k += 1
#     if k == 0:
#         return 1
#     else:
#         return 0
def near_water(cells, i, j):
    # границ нет, то есть идешь вправо -> появляешься слева
    for y in range(-1, 2):
        for x in range(-1, 2):
            if cells[(i + y) % len(cells)][(j + x) % len(cells[0])] <= 0.2:
                return 1
    return 0

def near_full_grass(cells, i, j):
    # границ нет, то есть идешь вправо -> появляешься слева
    count = 0
    for y in range(-1, 2):
        for x in range(-1, 2):
            if cells[(i + y) % len(cells)][(j + x) % len(cells[0])] <= 0.2:
                count += 1
    if count == 4:
        return 1
    else:
        return 0

# степенью контролируем высоту клеток
stepen = 2
# разрешение
w, h = 600,600 # w и h должны делиться на 12
# политра цветов
WHITE = (255,255,255)
BLACK = (0,0,0)
GRASS1 = (63,155,11)
GRASS2 = (55,160,10)
GRASS3 = (65,150,20)
GRASS4 = (60,155,20)
GRASS5 = (63,163,5)
mass_grass = [GRASS1,GRASS2,GRASS3,GRASS4,GRASS5]
SAND = (252,222,124)
SNOW = (252,247,247)
WATER1 = (47,155,254)
WATER2 = (46,160,255)
WATER3 = (40,155,255)
WATER4 = (57,140,250)
WATER5 = (47,155,255)
mass_water = [WATER1,WATER2,WATER3,WATER4,WATER5]
DEEPWATER = (0,31,143)
# размер клетки
a = 10 # tiles должны быть маленького размера для большей дeтализации

# разложение на простые множители разрешения
deli = []
for i in range(2, (w//a)//2 + 1):
    if w % i == 0:
        deli.append(i)

# print(deli)
# шум Перлина, делаем для большого количества простых делителей
cells = []
for i in range(h//a):
    cells.append([])
    for j in range(w//a):
        cells[i].append(0)

# d = []
# d.append(deli[0])
# d.append(deli[1])
# d.append(deli[2])
# d.append(deli[3])
# d.append(deli[4])
# d.append(deli[-2])
# d.append(deli[-1])
#
# deli = []
# for i in range(len(d)):
#     deli.append(d[i])

count = 0
for ind in range(len(deli)):
    c = 0
    randl = []
    randch = random.choice(deli)
    for i in range(w//a):
        if c%randch == 0:
            randl = []
            for _ in range((w//a)//(w//a//randch)):
                r = random.randrange(0, 100) / 100
                for _ in range((h//a) // randch):
                    randl.append(r)

        c += 1
        for j in range(len(randl)):
            cells[i][j] += randl[j]
    count += 1

for i in range(len(cells)):
    for j in range(len(cells[i])):
        cells[i][j] /= count
        cells[i][j] = cells[i][j]**stepen



# создаем поле
root = p.display.set_mode((w, h))

# основная логика
while True:
    time.sleep(0.3)
    # заполняем поле белым
    root.fill(SAND)
    # проверяем на закрытие проги, чтобы шиндоус не думал, что она не отвечает
    for i in p.event.get():
        if i.type == QUIT:
            quit()


    for i in range(len(cells)):
        for j in range(len(cells[i])):
            h = cells[i][j]
            # if h <= 0.05 and not (0.25 < cells[i%len(cells)][(j-1)%len(cells[i])] and 0.25 < cells[i%len(cells)][(j+1)%len(cells[i])] and 0.25 <cells[(i-1)%len(cells)][j%len(cells[i])] and 0.25 <cells[(i+1)%len(cells)][j%len(cells[i])]):
            #     p.draw.rect(root, DEEPWATER,[j * a, i * a, a, a])
            if h <= 0.2:  # 0.05 <
                p.draw.rect(root, random.choice(mass_water), [j * a, i * a, a, a])
            # elif 0.2 < h <= 0.21 and not (near_full_grass(cells, i, j)) and near_water(cells, i, j):
            #     p.draw.rect(root, SAND, [j * a, i * a, a, a])
            elif 0.21 < h <= 0.7 and not near_water(cells, i, j):
                p.draw.rect(root, GRASS1, [j * a, i * a, a, a])
            elif 0.22 < h <= 0.7:
                p.draw.rect(root, SAND, [j * a, i * a, a, a])
            elif 0.9 < h:
                p.draw.rect(root, WHITE, [j * a, i * a, a, a])

    p.display.update()
