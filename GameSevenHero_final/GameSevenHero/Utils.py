#coding = utf-8
import pygame
from pygame.locals import *
import  os
MAIN_DIR = os.path.split(os.path.abspath(__file__))[0]

"""         加载指定图片       """
def load_image(file, width=None ,number=None,sub_height=None):
    file = os.path.join(MAIN_DIR, './img', file)
    try:
        surface = pygame.image.load(file).convert_alpha()
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    if width == None:
        return surface
    res = []
    x = 0
    y = 0
    #print('width:%d totalwidth:%d height:%d number:%d'%(width,surface.get_rect().w,sub_height,number))
    for i in range(number):
        if (x)* width >= surface.get_rect().w:
            y+=1
            x=0
        if  width == surface.get_rect().w :
            y=0
        #print('x,y:%d,%d'%(x,y))
        res.append(surface.subsurface(Rect((x * width,y * sub_height), (width, sub_height))))
        x+=1
    return res
