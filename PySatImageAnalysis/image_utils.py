# -*- coding: utf-8 -*-
from random import randint

def generate_random_box(size,min_box_size,max_box_size):
    minx = randint(0,size - min_box_size-1)
    maxx = randint(minx+min_box_size,minx+min(randint(min_box_size,max_box_size),size-1))
    miny = randint(0,size - min_box_size-1)
    maxy = randint(miny+min_box_size,miny+min(randint(min_box_size,max_box_size),size-1))
    return [minx,miny,maxx,maxy]

