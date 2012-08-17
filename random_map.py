# Copyright 2012 Andreev Alexander <carzil@yandex.ru>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.

import random
import sys

INF = float("inf")
WALL_HEIGHT = (20, INF)
HEAL_HEIGHT = (5, 19)
SPIKES_HEIGHT = (-INF, -1)
MAP_POW2 = 5

class DiamondSquare():
    def __init__(self, pow_2, r, mi, ma):
        self._x = 1 << pow_2
        self._y = 1 << pow_2
        self._r = r
        self._min_iv = mi
        self._max_iv = ma
        self._world = {}

    def generate(self):
        self._init_step()
        l = (0, 0)
        r = (self._x, 0)
        l2 = (0, self._y)
        r2 = (self._x, self._y)

        lenght = self._get_length(l, r)
        center = (l[0] + lenght / 2, l[1] + lenght / 2)
        up_middle = (l[0] + lenght / 2, l[1])
        left_middle = (l[0], l[1] + lenght / 2)
        right_middle = (r[0], r[1] + lenght / 2)
        down_middle = (l2[0] + lenght / 2, l2[1])

        self._square_step(l, r, l2, r2)
        return self._world

    def _init_step(self):
        self._world[(0, 0)] = random.randint(self._min_iv, self._max_iv)
        self._world[(0, self._x)] = random.randint(self._min_iv, self._max_iv)
        self._world[(self._y, 0)] = random.randint(self._min_iv, self._max_iv)
        self._world[(self._y, self._x)] = random.randint(self._min_iv, self._max_iv)

    def _random_height(self, s, num, lenght):
        average = s / num
        random_offset = random.uniform(-(self._r * lenght), self._r * lenght)
        return average + random_offset

    def _get_length(self, point1, point2):
        return abs(point1[0] - point2[0])

    def _square_step(self, l, r, l2, r2):
        if self._check(l, r, l2, r2):
            return

        lenght = self._get_length(l, r)
        lenght_div_2 = lenght / 2

        center = (l[0] + lenght_div_2, l[1] + lenght_div_2)
        self._world[center] = self._random_height(
            self._world[l] + self._world[r] + self._world[l2] + self._world[r2],
            4,
            lenght
        )
        self._diamond_step(l, r, l2, r2)

    def _check(self, l, r, l2, r2):
        lenght = self._get_length(l, r)
        return lenght < 1

    def _diamond_step(self, l, r, l2, r2):
        lenght = self._get_length(l, r)
        lenght_div_2 = lenght / 2

        center = (l[0] + lenght_div_2, l[1] + lenght_div_2)
        up_middle = (l[0] + lenght_div_2, l[1])
        left_middle = (l[0], l[1] + lenght_div_2)
        right_middle = (r[0], r[1] + lenght_div_2)
        down_middle = (l2[0] + lenght_div_2, l2[1])

        res = l[1] - lenght_div_2
        up_middle_extra_point = self._world.get((center[0], res), 0)

        res = l2[1] + lenght_div_2
        down_middle_extra_point = self._world.get((center[0], res), 0)

        res = r[0] + lenght_div_2
        right_middle_extra_point = self._world.get((res, center[1]), 0)

        res = l[0] - lenght_div_2
        left_middle_extra_point = self._world.get((res, center[1]), 0)

        self._world[up_middle] = self._random_height(
            self._world[l] + self._world[r] + self._world[center] + up_middle_extra_point, 4, lenght
        )

        self._world[left_middle] = self._random_height(
            self._world[l] + self._world[l2] + self._world[center] + left_middle_extra_point, 4, lenght
        )

        self._world[right_middle] = self._random_height(
            self._world[r] + self._world[r2] + self._world[center] + right_middle_extra_point, 4, lenght
        )

        self._world[down_middle] = self._random_height(
            self._world[l2] + self._world[r2] + self._world[center] + down_middle_extra_point, 4, lenght
        )

        self._square_step(l, up_middle, left_middle, center)
        self._square_step(up_middle, r, center, right_middle)
        self._square_step(left_middle, center, l2, down_middle)
        self._square_step(center, right_middle, down_middle, r2)

def get_entity_by_height(height):
    if height >= WALL_HEIGHT[0] and height <= WALL_HEIGHT[1]:
        return "*"
    elif height >= HEAL_HEIGHT[0] and height <= HEAL_HEIGHT[1]:
        return "+"
    elif height >= SPIKES_HEIGHT[0] and height <= SPIKES_HEIGHT[1]:
        return "#"
    else:
        return "."

def transfrom_to_matrix(world, x, y):
    w = [[0 for _ in range(x)] for _ in range(y)]
    for i in range(y):
        for j in range(x):
            height = world[(i, j)]
            w[i][j] = get_entity_by_height(height)
    return w

world = DiamondSquare(MAP_POW2, 3, -3, 21).generate()
world = transfrom_to_matrix(world, 2 ** MAP_POW2, 2 ** MAP_POW2)

print("\n".join(map(lambda x: " ".join(map(str, x)), world)))

