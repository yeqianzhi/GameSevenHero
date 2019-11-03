import pygame
from pygame.locals import *
from Beans import *
from Utils import *
import random
from os import path

########## buff类 #################
class BuffSprites(MySprit):
    # 加载盾牌、闪电图片
    img_dir = path.join(path.dirname(__file__), 'img')
    powerup_images = {}
    powerup_images['bulletset'] = pygame.image.load(path.join(img_dir, 'bulletset.png'))
    powerup_images['pause'] = pygame.image.load(path.join(img_dir, 'pause.png'))
    powerup_images['mine'] = pygame.transform.scale(pygame.image.load(path.join(img_dir, 'mine.png')), (30, 30))

    def __init__(self, img, width, height, number,  lineNum = 3, state = 'stand'):
        super().__init__(img, width, height, number, lineNum=3, state='stand')
        ########################################################
        self.type = random.choice(['bulletset', 'pause', 'mine'])
        self.image = self.powerup_images[self.type]
        #######################################################
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 480)
        if self.type == 'mine':
            self.rect.y = random.randrange(200, 400)
        else:
            self.rect.y = random.randrange(0, 10)
        self.speedy = random.randrange(1, 3)

    def update(self, passed_time):
        self.rect.y += self.speedy
        self.passed_time += passed_time
        if (self.rect.top > 568 + 10) or (self.rect.left < -25) or (self.rect.right > 320 + 20):
            if self.passed_time >= self._rate * 100:
                self.rect.x = random.randrange(0, 320 - self.rect.width)
                self.rect.y = random.randrange(-200, -40)
                self.speedy = random.randrange(1, 2)
        if self.rect.top > 568:
            self.kill()










        
    