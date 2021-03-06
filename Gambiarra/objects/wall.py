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

from things import Thing

class LeftWall(Thing):
    def __init__(self, initial_pos=(0, 0), editable=False):
        image = pygame.Surface( (15, 770) )
        image.fill( (255, 255, 255) )
        Thing.__init__(self,
           image, editable, None,
           initial_pos, elasticity = 100, mobility = False,
           gravity = 10)

    def collide(self, obj):
        if obj.rect.colliderect(self.rect):
            if obj.rect.left <= self.rect.right:
                obj.rect.left = self.rect.right + 5
            obj.speed[0] *= -0.95*obj.elasticity/100
            return True
        return False

class RightWall(Thing):
    def __init__(self, initial_pos=(1185, 0), editable=False):
        image = pygame.Surface( (15, 770) )
        image.fill( (255, 255, 255) )
        Thing.__init__(self,
           image, editable, None,
           initial_pos, elasticity = 100, mobility = False, gravity = 10)

    def collide(self, obj):
        if obj.rect.colliderect(self.rect):
            if obj.rect.right >= self.rect.left:
                obj.rect.right = self.rect.left - 5
            obj.speed[0] *= -0.95*obj.elasticity/100
            return True
        return False

class UpWall(Thing):
    def __init__(self, initial_pos = (15, 0), editable=False):
        image = pygame.Surface( (1770, 15) )
        image.fill( (255, 255, 255) )
        Thing.__init__(self,
            image, editable, None,
            initial_pos, elasticity = 100, mobility = False,
            gravity = 10)

    def collide(self, obj):
        if obj.rect.colliderect(self.rect):
            if obj.rect.top <= self.rect.bottom:
                obj.rect.top = self.rect.bottom + 5
            obj.speed[1] *= -0.95*obj.elasticity/100
            return True
        return False

class DownWall(Thing):
    def __init__(self, initial_pos = (15, 755), editable=False):
        image = pygame.Surface( (1770, 15) )
        image.fill( (255, 255, 255) )
        Thing.__init__(self,
            image, editable, None,
            initial_pos, elasticity = 100, mobility = False,
            gravity = 10)

    def collide(self, obj):
        if obj.rect.colliderect(self.rect):
            if obj.rect.bottom > self.rect.top:
                obj.rect.bottom = self.rect.top - 5
            obj.speed[1] *= -0.75*obj.elasticity/100
            return True
        return False
