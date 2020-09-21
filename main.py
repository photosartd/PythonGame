import sys
import os

import pygame
import random
import tkinter as tk
from tkinter import messagebox

import constants as con
import snake
import cube
import menu
import draw_something
import db_managing as db

pygame.init()

#size of the frame
width = 500
rows = 20
#font of the text
font = pygame.font.SysFont(None, 30)

def drawGrid(width, rows, frame):
    blockSize = width//rows
    x = 0
    y = 0
    for l in range(rows):
        x += blockSize
        y += blockSize
        #Вертикальные линии
        pygame.draw.line(frame, con.white, (x,0), (x,width))
        #Горизонтальные линии
        pygame.draw.line(frame, con.white, (0,y), (width,y))


def drawFrame(frame):
    global s, snack
    frame.fill(con.black)
    s.draw(frame)
    snack.draw(frame)
    draw_something.draw_text('Score: ' + str(len(s.body)), font, con.blue,
    frame, 27, 27)
    drawGrid(width, rows, frame)
    pygame.display.update()

def generate_random_snack_pos(item):
    positions = item.body
    while True:
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z: z.pos == (x,y), positions))) > 0:
           continue
        else:
            break
    return (x,y)

def check_for_intersect():
    global s
    for x in range(len(s.body)):
        if s.body[x].pos in list(map(lambda z:z.pos, s.body[x+1:])):
            print('Score: ', len(s.body))
            message_box('You lost!', 'Play again...')
            db.insert_result_into_db(len(s.body))
            #Коммитим здесь, так как после полной сессии он не сохраняет(?)
            db.commit_connect()
            s.reset((10,10))
            break

def get_new_snack():
    global s, snack
    if s.body[0].pos == snack.pos:
        s.add_cube()
        snack = cube.Cube(generate_random_snack_pos(s), color=con.green)

def message_box(subject, content):
    #Создание всплывающего окна
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject,content)
    try:
        root.destroy()
    except:
        pass           

def main():
    global s, snack
    #setting size of the frame
    frame = pygame.display.set_mode((width, width))
    #setting snake
    s = snake.Snake(con.red, (10,10))
    snack = cube.Cube(generate_random_snack_pos(s), color=con.green)
    flag = True

    clock = pygame.time.Clock()

    while flag:
        #Чтобы движение происходило не очень быстро
        pygame.time.delay(50)
        #10fps
        clock.tick(10)
        events = s.move()
        get_new_snack()
        check_for_intersect()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menu.start_menu(frame, clock, result=len(s.body))
        drawFrame(frame)
    pass

main()