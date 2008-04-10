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

import pygame
from pygame.locals import *

import sys

import simplejson as json

from objects.balls import *
from objects.animals import *
from objects.elastica import *
from objects.esteira import *
from objects.target import *
from objects.wall import *

from command import *

def _is_static(obj):
    # FIXME: we need to define a way of saying that an object is static, this
    # "if" is repulsive! =D
    if (isinstance(obj, Target) or isinstance(obj, Esteira)
        or isinstance(obj, Elastica)):
        return True

class SimulationView(object):
    """ This widget holds the objects being simulated. """
    running = None
    background = None
    objects = None

    def __init__(self, objects):
        self.running = False
        self.background = pygame.Surface((1200, 770))
        self.background.fill([99,157,237])
        self.objects = pygame.sprite.RenderPlain()
        self.staticObjs = []

        for obj in objects:
            if _is_static(obj):
                self.staticObjs.append(obj)
            else:
                obj.add(self.objects)

        self.staticObjs.append(LeftWall())
        self.staticObjs.append(RightWall())
        self.staticObjs.append(UpWall())
        self.staticObjs.append(DownWall())

    def draw(self, pos = None):
        screen = pygame.display.get_surface()
        if pos:
            screen.blit(self.background, (pos[0], pos[1]), pos)
        else:
            screen.blit(self.background, (0, 0))

        for obj in self.staticObjs:
            obj.draw(screen, obj.rect)

        for item in self.objects:
            item.draw(screen, item.rect.topleft)

    def add(self, obj):
        if _is_static(obj):
            self.staticObjs.append(obj)
        else:
            obj.add(self.objects)

class ObjectBar(object):
    """ This widget contains the objects available for the problem. """

    def __init__(self, objects):
        self.background = pygame.Surface((1000, 130))
        self.background.fill([0,255,0])   #TODO: achar uma cor melhor =D
        self.objects = pygame.sprite.RenderPlain(objects)

    def draw(self, pos = None):
        screen = pygame.display.get_surface()
        if pos:
            screen.blit(self.background, (pos[0], 770 + pos[1]), pos)
        else:
            screen.blit(self.background, (0, 770))

        objpos = [15, 785]
        for item in self.objects:
            item.rect.topleft = objpos
            item.draw(screen, item.rect.topleft )
            objpos[0] += item.image.get_width() + 15

    def update(self):
        pass

class CommandBar(object):
    """ This widget contains the commands: play, help, and quit. KISS! =D """

    def __init__(self):
        self.background = pygame.Surface((200, 130))
        self.width, self.height = self.background.get_size()
        self.background.fill([0,0,255])   #TODO: achar uma cor melhor =D
        self.commands = [ Play(), Help(), Quit() ]

    def draw(self, pos=None):
        screen = pygame.display.get_surface()
        if pos:
            screen.blit(self.background, (1000 + pos[0], 770 + pos[1]), pos)
        else:
            screen.blit(self.background, (1000, 770))

        objpos = [1015, 810]
        for cmd in self.commands:
            cmd.rect.topleft = objpos
            cmd.draw(screen, cmd.rect.topleft )
            objpos[0] += cmd.image.get_width() + 15

    def update(self):
        pass

class Level(object):
    """This widget contains the objects in the scenario and their positions
    on the screen"""
    objects = None

    def __init__(self, objInPlace, objToAdd, goals, helpImage):
        self.simulator = SimulationView(objInPlace)
        self.objbar = ObjectBar(objToAdd)
        self.cmdbar = CommandBar()
        self.goals = goals
        self.helpImage = helpImage

    def goal_reached(self):
        for obj, goal in self.goals:
            if not obj.rect.collidepoint(goal.rect.center):
                return False
        return True

    def draw(self):
        self.simulator.draw()
        self.objbar.draw()
        self.cmdbar.draw()

    def show_help(self, screen):
        screen.blit(self.helpImage, (600 - self.helpImage.get_width()/2,
                                     450 - self.helpImage.get_height()/2) )
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN:
                    return

def init_levels():
    #FIXME: fazer de um jeito menos lusitano
    #Sample levels
    level1ObjInPlace = [ SoccerBall((200,300),editable=False),
                         Esteira((300,500), editable=False),
                         Target((1000,600), editable=False)]
    level1ObjToAdd = [ Penguin() ]
    level1Goal = level1ObjInPlace[-1]
    level1ToGoal = level1ObjInPlace[0]
    level1HelpImage = pygame.image.load("data/images/obj-level1.png")

    level2ObjInPlace = [ Penguin((300,500),editable=False),
                         Target((500,600), editable=False)]
    level2ObjToAdd = [ Esteira() ]
    level2Goal = level2ObjInPlace[-1]
    level2ToGoal = level2ObjInPlace[0]
    level2HelpImage = pygame.image.load("data/images/obj-level2.png")

    level3ObjInPlace = [ BowlingBall((20,20), editable=False),
                         Esteira((10, 300),editable=False),
                         Target((1100, 20), editable=False)]
    level3ObjToAdd = [ Elastica(), Elastica()]
    level3Goal = level3ObjInPlace[-1]
    level3ToGoal = level3ObjInPlace[0]
    level3HelpImage = pygame.image.load("data/images/obj-level3.png")

    level4ObjInPlace = [ BowlingBall((20,20), editable=False),
                         SoccerBall((800, 300), editable=False),
                         Target((900, 90), editable=False),
                         Target((100, 550), editable=False)]
    level4ObjToAdd = [ Esteira(), Esteira(), Esteira()]
    level4Goal1 = level4ObjInPlace[-2]
    level4ToGoal1 = level4ObjInPlace[0]
    level4Goal2 = level4ObjInPlace[-1]
    level4ToGoal2 = level4ObjInPlace[1]
    level4HelpImage = pygame.image.load("data/images/obj-level4.png")

    level5ObjInPlace = [ BowlingBall((1000,300), editable=False),
                         Esteira((1000,500), editable=False),
                         Target((1100, 650), editable=False)]
    level5ObjToAdd = [ Esteira(), Esteira()]
    level5Goal = level5ObjInPlace[-1]
    level5ToGoal = level5ObjInPlace[0]
    level5HelpImage = pygame.image.load("data/images/obj-level5.png")

    level6ObjInPlace = [ BeachBall((800,50),editable = False),
                         Elastica((800,400),editable = False),
                         Elastica((900,200),editable = False),
                         Target((1070,650),editable = False)]
    level6ObjToAdd = [ Esteira(), Esteira() ]
    level6Goal = level6ObjInPlace[-1]
    level6ToGoal = level6ObjInPlace[0]
    level6HelpImage = pygame.image.load("data/images/obj-level6.png")

    level1 = Level( level1ObjInPlace,
                    level1ObjToAdd,
                    [(level1Goal, level1ToGoal)],
                    level1HelpImage)

    level2 = Level( level2ObjInPlace,
                    level2ObjToAdd,
                    [(level2Goal, level2ToGoal)],
                    level2HelpImage)

    level3 = Level( level3ObjInPlace,
                    level3ObjToAdd,
                    [(level3Goal,level3ToGoal)],
                    level3HelpImage)

    level4 = Level( level4ObjInPlace,
                    level4ObjToAdd,
                    [(level4Goal1, level4ToGoal1),
                     (level4Goal2, level4ToGoal2)],
                    level4HelpImage)

    level5 = Level( level5ObjInPlace,
                    level5ObjToAdd,
                    [(level5Goal, level5ToGoal)],
                    level5HelpImage)

    level6 = Level( level6ObjInPlace,
                    level6ObjToAdd,
                    [(level6Goal, level6ToGoal)],
                    level6HelpImage)

    return [level1, level2, level3, level4, level5, level6]

def load_levels():
    pass
