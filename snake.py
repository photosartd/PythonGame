import pygame
import sys
import os
import cube as cb
import menu


class Snake:
    body = []
    _turns = {}

    def __init__(self, color, pos):
        self._color = color
        #Голова змеи
        self._head = cb.Cube(pos)
        #В начало тела
        self.body.append(self._head)
        #Направления движения
        self._dirnx = 0
        self._dirny = 1

    def move(self):
        events = pygame.event.get()
        for event in events:
            #Проверка выхода
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        #Получение нажатий
        keys = pygame.key.get_pressed()
        for key in keys:
            if keys[pygame.K_LEFT]:
                self._dirnx = -1
                self._dirny = 0
                #Для запоминания места, где повернула голова, мы
                #добавляем новый ключ в место, где повернула голова
                #чтобы потом остальные кубы поворачивали там же
                self._turns[self._head.pos[:]] = [self._dirnx, self._dirny]
            elif keys[pygame.K_RIGHT]:
                self._dirnx = 1
                self._dirny = 0
                self._turns[self._head.pos[:]] = [self._dirnx, self._dirny]
            elif keys[pygame.K_UP]:
                self._dirnx = 0
                self._dirny = -1
                self._turns[self._head.pos[:]] = [self._dirnx, self._dirny]
            elif keys[pygame.K_DOWN]:
                self._dirnx = 0
                self._dirny = 1
                self._turns[self._head.pos[:]] = [self._dirnx, self._dirny]

        for i, c in enumerate(self.body):
            #Получение позиции
            p = c.pos[:]
            #Если позиция находится в turns
            if p in self._turns:
                turn = self._turns[p]
                c.move(turn[0], turn[1])
                #Удаление поворота
                if i == len(self.body)-1:
                    self._turns.pop(p)
            else:
                #Для краев поля
                if c.dirnx == -1 and c.pos[0] <= 0: c.pos = (c.rows-1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows-1: c.pos = (0,c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows-1: c.pos = (c.pos[0],0)
                elif c.dirny == -1 and c.pos[1] <= 0: c.pos = (c.pos[0],c.rows-1)
                else: c.move(c.dirnx,c.dirny)
        return events

    def draw(self, frame):
        for i, c in enumerate(self.body):
            if i == 0:
                c.draw(frame, True)
            else:
                c.draw(frame)

    def add_cube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        #Добавление куба в правильную позицию 
        if dx == 1 and dy == 0:
            self.body.append(cb.Cube((tail.pos[0]-1,tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cb.Cube((tail.pos[0]+1,tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cb.Cube((tail.pos[0],tail.pos[1]-1)))
        elif dx == 0 and dy == -1:
            self.body.append(cb.Cube((tail.pos[0],tail.pos[1]+1)))
        
        self.body[-1].dirnx = dx
        self.body[-1].dirny = dy

    def reset(self, pos):
        self._head = cb.Cube(pos)
        self.body = []
        self.body.append(self._head)
        self._turns = {}
        self._dirnx = 0
        self._dirny = 1


