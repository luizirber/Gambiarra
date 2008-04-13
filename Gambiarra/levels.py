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

import os

import simplejson as json

from objects import *

from command import *

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

        for obj in objects.values():
            if obj.mobility:
                obj.add(self.objects)
            else:
                self.staticObjs.append(obj)

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
        if obj.mobility:
            obj.add(self.objects)
        else:
            self.staticObjs.append(obj)

class ObjectBar(object):
    """ This widget contains the objects available for the problem. """

    def __init__(self, objects):
        self.background = pygame.Surface((1000, 130))
        self.background.fill([0,255,0])   #TODO: achar uma cor melhor =D
        self.objects = pygame.sprite.RenderPlain(objects.values())

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
    return load_levels()

def load_levels():
    level_dir = os.path.join('data', 'levels')
    files = os.listdir(level_dir)
    levels = []
    for level_file in sorted(f for f in files if f.split(".")[-1] == "level"):
        fp = open(os.path.join(level_dir, level_file))
        try:
            level = json.load(fp)
        except ValueError, e:
            print level_file, "-> invalid json file: ", e
            fp.close()
        else:
            lvl = load_level(level, level_dir, level_file)
            if lvl:
                levels.append(lvl)

    return levels

def load_level(level, level_dir, level_name):
    objs = {}
    for obj in level["placed"]:
        try:
            klass = globals()[obj["type"]]
        except KeyError, e:
            print level_name, "-> Invalid type for object:", e
            return None

        o = klass( ( int(obj["xpos"]), int(obj["ypos"]) ), editable=False)
        objs[obj["name"]] = o

    toadd = {}
    for obj in level["available"]:
        try:
            klass = globals()[obj["type"]]
        except KeyError, e:
            print level_name, "-> Invalid type for object:", e
            return None

        try:
            toadd[obj["name"]] = klass()
        except KeyError, e:
            print level_name, "-> Object name not available"

    goals = []
    for goal in level["goals"]:
        try:
            proj = objs[ goal[0] ]
            target = objs[ goal[1] ]
        except KeyError:
            print level_name, "-> Object not available:", e
            return None
        goals.append( (proj, target) )

    img_file = os.path.join(level_dir, level['help'])
    if os.path.isfile(img_file):
        help_image = pygame.image.load(img_file)
    else:
        print level_name, "-> Invalid help file:", level['help']
        return None

    return Level(objs, toadd, goals, help_image)

