#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# Copyright (C) 2007 by ULPM: Alexandre Yukio Harano
#                             Fábio Cassarotti Parronchi Navarro
#                             Gabriel Geraldo França Marcondes
#                             Luiz Carlos Irber Júnior
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import os
import sys
from os.path import abspath

import pygame
from pygame.locals import *
import levels as Levels

from command import Play, Help, Quit
from gamemenu import GameMenu

from objects.animals import *
from objects.elastica import Elastica
from objects.esteira import Esteira
from objects.target import Target
from objects.wall import *

def check_collision(sprite_list, wall_list):
    new_objects = pygame.sprite.RenderPlain()
    for obj in sprite_list:
        obj.remove(sprite_list)
        obj.add(new_objects)

        for s in sprite_list:
            """hitbox = obj.rect.inflate(5,5)
            if hitbox.colliderect(s.rect):
                if obj.rect.left < s.rect.right:
                    aux = obj.speed[0]
                    obj.speed[0]=s.speed[0]
                    s.speed[0]=aux
                    obj.rect.left = s.rect.right-1
                if obj.rect.left > s.rect.right :
                    aux = obj.speed[0]
                    obj.speed[0]=s.speed[0]
                    s.speed[0]=aux
                    obj.rect.right = srect.left-1
                if obj.rect.bottom > s.rect.top:
                    aux = obj.speed[1]
                    obj.speed[1]=s.speed[1]
                    s.speed[1]=aux
                    obj.rect.bottom = s.rect.top-1
                if obj.rect.top < s.rect.bottom:
                    aux = obj.speed[1]
                    obj.speed[1]=s.speed[1]
                    s.speed[1]=aux
                    obj.rect.top = s.rect.bottom+1
            """
            #TODO: verifica colisao de objetos dinamicos
            pass

        for w in wall_list:
#            hitbox = obj.rect.inflate(-5,-5)
#            if hitbox.colliderect(w.rect):
            if obj.rect.colliderect(w.rect):
                obj.play()
                w.play()
                if isinstance(w, DownWall):
                    if obj.rect.bottom > w.rect.top:
                       obj.rect.bottom = w.rect.top - 5
                       if isinstance(obj,Penguin):
                            obj.speed[1] = 0
                       else:
                            obj.speed[1] *= -0.75*obj.elasticity/100
                #1. a**n + b**n = c**n ?
                if isinstance(w, UpWall):
                    if obj.rect.top <= w.rect.bottom:
                        obj.rect.top = w.rect.bottom + 5
                        obj.speed[1] *= -0.95*obj.elasticity/100

                if isinstance(w, LeftWall):
                    if obj.rect.left <= w.rect.right:
                        obj.rect.left = w.rect.right + 5
                        obj.speed[0] *= -0.95*obj.elasticity/100

                if isinstance(w, RightWall):
                    if obj.rect.right >= w.rect.left:
                        obj.rect.right = w.rect.left - 5
                        obj.speed[0] *= -0.95*obj.elasticity/100

                if isinstance(w, Esteira):
                     if (obj.rect.bottom >= w.rect.top and obj.speed[1] > 0):
                        obj.rect.bottom = w.rect.top - 5
                        obj.speed[0] = w.sentido*15
                        if isinstance(obj,Penguin):
                             obj.speed[1] = 0
                        else:
                             obj.speed[1] *= -0.75*obj.elasticity/100

                if isinstance(w, Elastica):
                     if (obj.rect.bottom >= w.rect.top and obj.speed[1] > 0):
                        obj.rect.bottom = w.rect.top - 1
                     elif (obj.rect.top <= w.rect.bottom):
                        obj.rect.top = w.rect.bottom + 1
                     obj.speed[1] *= -0.99

                if isinstance(w, Target):
                    pass

            if isinstance(w,DownWall) :
                if obj.rect.bottom >= w.rect.top:
                    obj.rect.bottom = w.rect.top - 5
                    obj.speed[1] *= -0.75*obj.elasticity/100
            if isinstance(w,UpWall) :
                if obj.rect.top <= w.rect.bottom:
                    obj.rect.top = w.rect.bottom + 5
                    obj.speed[1] *= -0.95*obj.elasticity/100
            if isinstance(w,LeftWall) :
                if obj.rect.left <= w.rect.right:
                    obj.rect.left = w.rect.right + 5
                    obj.speed[0] *= -0.95*obj.elasticity/100
            if isinstance(w,RightWall) :
                if obj.rect.right >= w.rect.left:
                    obj.rect.right = w.rect.left - 5
                    obj.speed[0] *= -0.95*obj.elasticity/100

    return new_objects


class Game(object):
    # controle do jogo
    fps = 30
    playing = None
    running = None
    clock = None
    level = 0
    levels = []
    selected_element = None
    _showed_help = None
    count = None
    play_sounds = None

    # elementos do jogo
    screen = None
    menu = None
    congrats = None
    congratsSnd = None

    def __init__(self, play_sounds=True):
        pygame.init()
        self.play_sounds = play_sounds
        if self.play_sounds:
            pygame.mixer.init()
        self.screen = pygame.display.set_mode((1200,900)) #omitindo flags
        pygame.display.flip()
        self.running = True
        self.playing = False
        pygame.display.set_caption("Gambiarra")
        self.clock = pygame.time.Clock()
        self.levels = Levels.init_levels()
        self.menu = GameMenu()
        self.congrats = pygame.image.load("../data/images/fim_fase.png")
        if self.play_sounds:
            self.congratsSnd = pygame.mixer.Sound(abspath("../data/snd/Congrats.wav"))
        self._showed_help = False
        self.count = 0

    def run(self):
        #inicia o loop
        self.main_loop()

    def event_handler(self):
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                self.mouse_event( pygame.mouse.get_pos() )

    def update_screen(self, fps):
        #update dos elementos da tela
        if self.playing:

            # executa a simulacao
            objs = check_collision(self.levels[self.level].simulator.objects,
                                self.levels[self.level].simulator.staticObjs)
            self.levels[self.level].simulator.objects = objs
            for obj in self.levels[self.level].simulator.objects:
                #obj eh um objeto na tela
                if obj.mobility:
                    newpos = obj.rect.move((obj.speed[0],obj.speed[1]))
                    obj.rect = newpos
                    if not(isinstance(obj,Penguin)):
                        obj.speed[0] *= 0.99
                    if obj.speed[1] <= obj.rect[3]*0.04 and obj.speed[1] > 0:
                        obj.speed[1] = 0
                    obj.speed[1] += obj.gravity
        else:
            if self.selected_element:
                if self.selected_element.editable:
                    self.selected_element.rect.center = pygame.mouse.get_pos()

    def mouse_event(self, mousePos):
        if not self.selected_element:
            collided = False
            mouseMove = (0,0)
            mouseMove = pygame.mouse.get_rel()

            for element in self.levels[self.level].simulator.objects:
                if element.rect.collidepoint(mousePos):
                    collided = True
                    self.selected_element = element
                    break

            if not self.selected_element:
                for element in self.levels[self.level].simulator.staticObjs:
                    if element.rect.collidepoint(mousePos):
                        collided = True
                        self.selected_element = element

                        if isinstance(element,Esteira) and element.editable:
                            self.count += 1
                        if self.count == 1:
                            element.sentido=-element.sentido
                            self.count = 0
                        break

            if not self.selected_element: #se nao encontrou no for anterior
                for element in self.levels[self.level].objbar.objects:
                    if element.rect.collidepoint(mousePos):
                        collided = True
                        element.remove(self.levels[self.level].objbar.objects)
                        self.levels[self.level].simulator.add(element)
                        self.selected_element = element
                        break

            if not self.selected_element: #se nao encontrou no for anterior
                for element in self.levels[self.level].cmdbar.commands:
                    if element.rect.collidepoint(mousePos):
                        if isinstance(element, Play):
                            element.image = pygame.transform.flip(element.image,
                                                                  True, False)
                            self.playing = not self.playing
                            if not self.playing:
                                for element in self.levels[self.level].simulator.objects:
                                    element.speed = [0,0]
                                    element.rect.topleft = element.initialPosition
                        elif isinstance(element, Help):
                            self.levels[self.level].show_help(self.screen)
                        elif isinstance(element, Quit):
                            sys.exit()
                        break

        else:
            if self.selected_element.editable and not self.playing:
                mouseMove = pygame.mouse.get_rel()
                if mouseMove != (0,0):
                    self.count -= 1
                self.selected_element.rect.center = pygame.mouse.get_pos()
                #self.selected_element.rect = self.selected_element.rect.move(mouseMove)
                self.selected_element.initialPosition = self.selected_element.rect.topleft
            self.selected_element = None

    def show_congratulations(self):
        if self.play_sounds:
            pygame.mixer.stop()
            self.congratsSnd.play()

        self.screen.blit(self.congrats, (600 - self.congrats.get_width()/2,
                                         450 - self.congrats.get_height()/2) )
        pygame.display.flip()

        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    return

    def main_loop(self):
        self.menu.run()
        while self.running and self.level < len(self.levels):
            while not self.levels[self.level].goal_reached():
                self.event_handler()
                self.clock.tick(self.fps)
                self.update_screen(self.fps)
                self.levels[self.level].draw()

                if not self._showed_help:
                    self.levels[self.level].show_help(self.screen)
                    self._showed_help = True

                pygame.display.flip()

            self.playing = False
            self._showed_help = False
            self.level += 1
            self.show_congratulations()
            if (len(self.levels) == self.level) :
                self.running = False

def main():
    game = Game(play_sounds=False)
    game.run()

if __name__ == "__main__":
    main()
