# coding = utf-8

import pygame
from Utils import *
from pygame.locals import *

"""         精灵类           """
class MySprit(pygame.sprite.Sprite):
    _rate = 100
    images = []
    def __init__(self,img,width,height,number,lineNum = 3,state = 'stand'):
        """
        :param img: 角色图片
        :param width: 帧宽
        :param height: 帧高
        :param number: 帧数
        """
        "-----------------  角色图像属性    -------------------"
        self.order = 0                                              #order :当前帧
        pygame.sprite.Sprite.__init__(self)
        self.number = number                                        #帧数
        self.lineNum = lineNum                                      #原素材每行的帧数
        if len(self.images) == 0:
            self.images = load_image(img, width, number,height)    #将原图片切割为number帧
        self.image = self.images[self.order]
        self.rect = Rect(0, 0, width, height)                       #角色矩形区域
        self.passed_time = 0                                        #帧更新频率控制
        "-----------------  角色动作属性    -------------------"
        self.dirc = 'front'                     #移动方向
        self.state = state                    #运动状态
        self.death = False                      #是否死亡
        self.blood = 3                           #血量
        self.level = 0                           #等级
        self.buff = {'froze':0,'shot':0}  #冰冻能力，射击能力
        self.buffTime = {'froze':0,'shot':0}    #能力时效
        self.reborn = 1000
        self.xSpeed = 0
        self.ySpeed = 0
        self.speed = 3                            #移动速度
        self.playMusic = False
        self.walkMusic =  pygame.mixer.Sound('./music/walk.wav')
        self.getbuffMusic =  pygame.mixer.Sound('./music/getbuff.wav')
        self.shotMusic =  pygame.mixer.Sound('./music/shotmusic.wav')
        self.magicMusic =  pygame.mixer.Sound('./music/magicmusic.wav')
        self.loseMusic =  pygame.mixer.Sound('./music/lose.wav')
    def loopOnce(self,passed_time):
        if self.death == False:
            self.passed_time += passed_time
            self.order = int((self.passed_time / self._rate))
            if self.order >= self.lineNum:
                self.death = True
            if self.order == 0 and self.passed_time > self._rate:
                self.passed_time = 0
            self.image = self.images[self.order]

    def update(self, passed_time):
        """
        2019.10.23 最后修改： 死亡后一段时间再复活
        :param passed_time:
        :return:
        """
        if self.death == True:
            self.passed_time += passed_time
            if self.passed_time >= self.reborn:
                self.death = False
                self.passed_time = 0
        if self.death == False:
            if self.state == 'run':
              #  if self.playMusic:
               #     self.walkMusic.play()
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
                self.walkMusic.stop()
                self.order = 2
                if self.dirc == 'left':
                    self.order += self.lineNum
                elif self.dirc == 'right':
                    self.order += self.lineNum*2
                elif self.dirc == 'back':
                    self.order += self.lineNum*3
            self.image = self.images[self.order]
    def stopMove(self):
        self.xSpeed=0
        self.ySpeed=0
        self.state='stand'
    def moveSpr(self,screen):
        """
        最后修改时间：2019.10.23  8:41   增加参数screen
        :param screen: 传入surface对象，精灵移动不超出此范围
        :return:
        """
        if self.state=='run':
            if self.dirc == 'left':
                self.xSpeed = -self.speed
            if self.dirc == 'right':
                self.xSpeed = self.speed
            if self.dirc == 'back':
                self.ySpeed = -self.speed
            if self.dirc == 'front':
                self.ySpeed = self.speed
            if self.rect.left + self.xSpeed >= 0 and self.rect.right + self.xSpeed <= screen.get_rect().w:
                self.rect = self.rect.move([self.xSpeed, 0])
            if self.rect.top + self.ySpeed >= 0 and self.rect.bottom + self.ySpeed <= screen.get_rect().h:
                self.rect = self.rect.move([0, self.ySpeed])
    def froze(self):
        if self.buff['froze'] != 0:
            self.buff['froze'] -= 1
            froz = MySprit('iceBrust.png',width=96,height=96,number=10)
            froz.lineNum = 5
            froz.state = 'run'
            froz.rect = froz.rect.clamp(self.rect)
            froz.dirc = None
            self.magicMusic.play()
            return froz
        return False
    def shot(self):
        if self.buff['shot'] != 0:
            self.buff['shot'] -= 1
            shot = MySprit('shot.png',width=96,height=96,number=20,lineNum=5)
            shot.lineNum = 5
            shot.state = 'run'
            shot.rect = shot.rect.clamp(self.rect)
            shot.dirc = self.dirc
            self.shotMusic.play()
            return shot
        return False
    def paint(self,screen):
        if self.death!=True:
            screen.blit(self.image, self.rect)
    def getState(self):
        """
        2019.10.23 10:20 最后修改 ：以字典形式返回精灵的状态
        :return: 字典类型，精灵状态，key需要和状态栏的状态项名称一一对应
        """
        res = {}
        res['level'] = str(self.level)
        res['frozen'] = str(self.buff['froze'])
        res['shot'] = str(self.buff['shot'])
        res['bonus'] = '0'
        res['blood'] = str(self.blood)
        return res
    def getBuff(self):
        ""
        "加属性！写这"
        self.getbuffMusic.play()
    def dead(self):
        self.death = True
        self.loseMusic.play()
        if self.blood>=0:
            self.blood-=1
            self.rect.bottom = 600
            self.rect.x = 0
            return 'wait'
        else:
            return 'lose'
    def beAttack(self,dic):
        if self.death == False:
            for i in dic:
                if i == 'death':
                    self.dead()
                if i == 'blind':
                    self.speed = -self.speed
                if i == 'slow':
                    self.speed = 1
    def getOver(self):
        if self.blood == 0:
            return True
        else:
            return False
    def upGrade(self,level):
        self.blood = 3
        self.buff['froze']=0
        self.buff['shot']=0
        self.speed = 3
        self.state = 'stand'
        self.rect.bottom = 600
        self.rect.x = 0
"""         菜单类           """
class Menu:
    def __init__(self,img,back=None):
        self.items = {}  #"文字"：[rect,是否选中]
        image = load_image(img)
        self.img = load_image(img,width=image.get_rect().w,
                              number=2,sub_height=image.get_rect().h//2)   #图片
        self.choseMusic =  pygame.mixer.Sound('./music/choseMenu.wav')
        self.back = None
    def addItem(self,text,rect):
        self.items[text] =[rect,False]
    def getId(self,pos):
        select = False
        for item in self.items:
            if self.items[item][0].collidepoint(pos):
                "播放音乐"
                if self.items[item][1] == False:
                    self.choseMusic.play()
                self.items[item][1] = True
                select =  item
            else:
                self.items[item][1] = False
        return select
    def paint(self,screen):
        """
        2019.10.23 最后修改:增加菜单自带背景的绘制
        :param screen: 应该传入窗口的surface
        :return:
        """
        if self.back != None:
            screen.blit(self.back, self.back.get_rect())
        my_font = pygame.font.SysFont('arial',20)
        for i in self.items:
            if self.items[i][1]:
                text_surface = my_font.render(i,True,(255,150,0))
            else:
                text_surface = my_font.render(i,True,(0,0,0))
            text_rect = text_surface.get_rect().clamp(self.items[i][0])
            text_rect.midtop = self.items[i][0].midtop
            text_rect.centery = self.items[i][0].centery
            screen.blit(self.img[1], self.items[i][0])
            screen.blit(text_surface, text_rect)

"""         状态栏类         """
"""2019.10.23 10:29 新增      """
class StateMenu:
    def __init__(self):
        self.items = {}
    def addItem(self,img,str):
        """
        :param img: string类型，图片名
        :param str: 状态项的名称，绘制时需要和传入的数据名称对应
        :return:
        """
        self.items[str] = load_image(img)
        self.items[str] = pygame.transform.scale(self.items[str], (40, 40))
    def paint(self,screen,state):
        """
        :param screen: 窗口
        :param state: 要绘制的状态数据
        :return:
        """
        my_font = pygame.font.SysFont('arial', 20)
        for j,i in enumerate(self.items):
            text_surface = my_font.render(state[i], True, (255, 255, 255))
            "----------Icon----------"
            rect  = self.items[i].get_rect()
            rect.top =  5
            rect.x = j* (rect.w+20) +2
            "----------Text----------"
            text_rect = text_surface.get_rect().clamp(rect)
            text_rect.x = rect.x + rect.w
            text_rect.centery = rect.centery
            screen.blit(self.items[i],rect)
            screen.blit(text_surface, text_rect)

class PlayerMenu(Menu):
    def __init__(self,img,screen,back=None):
        Menu.__init__(self,img,back)
        self.bgimg = pygame.image.load('./img/bg_aircity.png')
        self.bgimg = pygame.transform.scale(self.bgimg, (screen.get_rect().w, screen.get_rect().h))
        self.bgimgRect = self.bgimg.get_rect()

        self.dcimg = pygame.image.load('./img/menu_dec.png')
        self.dcimg = pygame.transform.scale(self.dcimg, (screen.get_rect().w, screen.get_rect().h//7))
        self.dcimgRect = self.dcimg.get_rect()


    def addItem(self,text,img,width,number,height,screen):
        index = len(self.items)
        sprit = MySprit(img,width=width,number=number,height=height,lineNum=3,state='run')
        img = pygame.transform.scale( sprit.image, (50, 50))
        rect = img.get_rect()
        rect.centerx = (index % 4+1) * (screen.get_rect().w//5)+index//4 *40
        rect.y = index//4 * (screen.get_rect().h//5)+250
        self.items[text] =[rect,False,sprit]
    def anim(self):
        for i in self.items:
            self.items[i][2].update(15)
    def paintText(self,screen,text):
        my_font = pygame.font.SysFont('SimHei', 45)
        text_surface = my_font.render(text, True, (250, 150, 0))
        text_rect = text_surface.get_rect()
        text_rect.y = 20
        text_rect.centerx = screen.get_rect().centerx
        screen.blit(text_surface, text_rect)
    def paint(self,screen,Text):
        screen.blit(self.bgimg, self.bgimgRect)
        if self.back!=None:
            screen.blit(self.back, self.bgimgRect)
        else:
            screen.blit(self.dcimg, self.dcimgRect)
        self.paintText(screen,Text)
        my_font = pygame.font.SysFont('SimHei', 20)
        for i in self.items:
            if self.items[i][1]:
                text_surface = my_font.render(i,True,(255,250,250))
            else:
                text_surface = my_font.render(i,True,(0,0,0))
            text_rect = text_surface.get_rect().clamp(self.items[i][0])
            text_rect.centerx = self.items[i][0].centerx
            text_rect.centery = self.items[i][0].y + self.items[i][0].h*1.1
            img = pygame.transform.scale(self.items[i][2].image, (50, 50))
            screen.blit(img, self.items[i][0])
            screen.blit(text_surface, text_rect)