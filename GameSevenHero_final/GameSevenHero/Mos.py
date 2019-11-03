# -*- coding: utf-8 -*-
# @Project: GameSevenHero+怪物
# @File  : Mos.py
# @Group ：Hello World
# @Author: Joker
# @Motto ：Talk is cheap, show me the code.
# @Date  : 2019/10/23 9:23
import pygame,random
from Utils import *
from pygame.locals import *
import random
WIDTH = 320
HEIGHT = 480
fps=300

#创建一个Clock对象，用于操作时间
fclock=pygame.time.Clock()
"""怪物类"""
class Monester(pygame.sprite.Sprite):
    _rate = 100
    images = []
    def __init__(self,img,width,height,number,type):
        """
        :param img: 角色图片
        :param width: 帧宽
        :param height: 帧高
        :param number: 帧数
        """
        "-----------------  角色图像属性    -------------------"
        self.order = 0 #order :当前帧
        self.speed = [1, 1]
        pygame.sprite.Sprite.__init__(self)
        self.number = number  #帧数
        self.type=type
        self.lineNum = 3
        if len(self.images) == 0:
            self.images = load_image(img, width, number,height)    #将原图片切割为number帧
        self.image = self.images[self.order]
        x = random.randrange(0,WIDTH-width)
        y = random.randrange(height, HEIGHT-height)
        self.rect = Rect(x, y, width,height )
        self.passed_time = 0                                        #帧更新频率控制
        "-----------------  角色动作属性    -------------------"
        self.dirc = 'left'                     #移动方向
        self.state = 'run'                    #运动状态
        self.death = False                      #是否死亡
        self.xSpeed = 0
        self.ySpeed = 0
        self.speed = 3

    def update(self, passed_time):
        if self.death == False:
            if self.state == 'run':
                self.passed_time += passed_time
                self.order = int( (self.passed_time / self._rate) % self.lineNum)
                if self.dirc == 'left':
                    self.order += self.lineNum
                elif self.dirc == 'right':
                    self.order += self.lineNum*2
                elif self.dirc == 'back':
                    self.order += self.lineNum*3
                if self.order == 0 and self.passed_time > self._rate:
                    self.passed_time = 0
            else:
                self.order = 2
                if self.dirc == 'left':
                    self.order += self.lineNum
                elif self.dirc == 'right':
                    self.order += self.lineNum*2
                elif self.dirc == 'back':
                    self.order += self.lineNum*3
            self.image = self.images[self.order]
        else:
            self.passed_time += passed_time
            if self.passed_time >= self._rate * 100:
                self.death = False
                self.passed_time = 0
                self.speed = 2

    def stopMove(self):
        self.xSpeed = 0
        self.ySpeed = 0
        self.state = 'stand'
    def moveSpr(self,screen):
        """
        最后修改时间：2019.10.23  8:41   增加参数screen
        :param screen: 传入surface对象，精灵移动不超出此范围
        :return:
        """
        if self.type!='dead':
            self.Ai()
        if self.state=='run':
            if self.dirc == 'left': #and
                self.xSpeed = -self.speed
            if self.dirc == 'right':
                self.xSpeed = self.speed
            if self.dirc == 'back':
                if self.type == 'dead':
                    self.ySpeed = -self.speed
                else:
                    self.ySpeed = -self.speed//self.speed
            if self.dirc == 'front':
                if self.type == 'dead':
                    self.ySpeed = self.speed
                else:
                    self.ySpeed = self.speed//self.speed
            if self.rect.left + self.xSpeed >= 0 and self.rect.right + self.xSpeed <= screen.get_rect().w:
                self.rect = self.rect.move([self.xSpeed, 0])
            if self.rect.top + self.ySpeed >= 0 and self.rect.bottom + self.ySpeed <= screen.get_rect().h:
                self.rect = self.rect.move([0, self.ySpeed])
    def paint(self,screen):
        if self.death==False:
            screen.blit(self.image, self.rect)
    def Ai(self):
        x = random.randrange(0, 1000)
        if x%200 == 0 or self.dirc in [ 'front','back']:
            self.dirc = random.choice(['left', 'right'])
        elif x%430 ==0 :
            self.dirc = random.choice([ 'front','back'])
        if self.rect.x<5:
            self.dirc = 'right'
        elif self.rect.x+self.rect.w>475:
            self.dirc = 'left'

    @classmethod
    def createMos(cls,death,blind,slow):
        monester = []
        for i in range(death):
            a = cls('death.png', 34, 34, 12, "dead")
            a.speed = random.randrange(1, 4)
            a.state = 'stand'
            monester.append(a)
        for i in range(blind):
            a = cls('blind.png', 34, 34, 12, "blind")
            a.speed = 2
            monester.append(a)
        for i in range(slow):
            a = cls('slow.png', 66, 66, 12, "slow")
            a.speed = 3
            monester.append(a)
            #monester.append(cls('slow2.png', 66, 66, 12, "slow"))
        return  monester
    def stateCopy(self,player):
        if self.type == 'dead':
            self.state = player.state
            self.dirc = player.dirc
            if player.death == True:
                self.stopMove()
    def attack(self):
        res = {}
        if self.type=='dead':
            res['death']=True
        if self.type == 'slow':
            self.speed = 4
            res['slow'] = 1
        if self.type == 'blind':
            res['blind'] = -1
        return res
