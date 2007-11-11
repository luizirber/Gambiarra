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

from os.path import abspath

class Penguin(Thing):
    def __init__(self, initialPosition=None, editable=True):
        super(Penguin, self).__init__(
             pygame.image.load(abspath("../data/images/penguin.png")),
             editable, pygame.mixer.Sound(abspath("../data/snd/penguin.wav")),
             initialPosition, elasticity = 100, mobility = True,
             gravity = 5)
        self.speed=[5,0]
