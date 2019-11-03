# coding = utf-8

import pygame
from pygame.locals import *
from Beans import *
from Utils import *
from Mos import *
from BuffSprit import *
import sys

class GameData:
    _rate = 100
    _passed_time = 100
    def __init__(self,screen,playerImg):
        "       初始化一局游戏        "
        """-----------   背景和游戏时序  ---------------"""
        self.bgimg = pygame.image.load('./img/forest.png')  #游戏背景
        self.bgimg = \
            pygame.transform.scale(self.bgimg,(screen.get_rect().w, screen.get_rect().h))  # 2019.10.23 8:44新增 根据屏幕大小拉伸背景图片
        self.bgimgRect = self.bgimg.get_rect()
        self.GameState = 'Running'                   #游戏状态
        self.clock = pygame.time.Clock()             #设置时钟
        self.choice = False                          #菜单选项
        """--------------  建精灵对象   ---------------"""
        self.rub = MySprit(playerImg, 34, 34, 12)     #玩家
        self.rub.rect.bottom = screen.get_rect().bottom
        self.rub.playMusic = True
        """--------------  建奖励对象   ---------------"""
        self.buff_list = pygame.sprite.Group()
        """--------------  建怪物对象   ---------------"""
        self.sflower = Monester('tu.png', 34, 34, 12, "rub")  # npc
        self.sflower.rect.bottom = 480
        self.sflower.reborn = 10000
        self.monesters = Monester.createMos(1,2,1)
        self.monesters.append(self.sflower)
        """--------------   子弹列表   ---------------"""
        self.player_shot = []                               #子弹列表
        """---------------   子菜单   ---------------"""
        self.menuitem = ['back']                            #子菜单菜单项
        self.gameMenu = Menu(img='button.png')              #子菜单
        self.subimg = pygame.image.load('./img/sub_menu930x105.png')
        self.subimg = pygame.transform.scale(self.subimg, (screen.get_rect().w, 50))
        self.gameMenu.back = self.subimg
        self.gameMenu.img[1] = pygame.transform.scale(self.gameMenu.img[1], (100, 40))

        self.sureMenuItem = ['sure','back']
        self.sureMenu = Menu(img='button.png')  # 子菜单
        self.sureMenu.img[1] = pygame.transform.scale(self.sureMenu.img[1], (100, 40))
        for i in range(len(self.sureMenuItem)):
            rect = self.sureMenu.img[1].get_rect()
            rect.centerx = screen.get_rect().centerx -50+100*i
            rect.top = screen.get_rect().centery+100
            self.sureMenu.addItem(self.sureMenuItem[i], rect)

        for i in range(len(self.menuitem)):
            rect = self.gameMenu.img[1].get_rect()
            rect.x = screen.get_rect().w - rect.w - 5
            rect.y = 0 + i * rect.h
            self.gameMenu.addItem(self.menuitem[i], rect)
        """---------------   状态栏   ---------------"""
        self.stateMenu = StateMenu()                    #状态栏
        self.stateMenu.addItem('Icon_level56x56.png', 'level')
        self.stateMenu.addItem('Icon_frozen56x56.png', 'frozen')
        self.stateMenu.addItem('Icon_shot56x56.png', 'shot')
        self.stateMenu.addItem('Icon_bonus56x56.png', 'bonus')
        self.stateMenu.addItem('Icon_blood44x42.png', 'blood')
        self.down = 0
        """---------------   道具状态   ---------------"""
        self.mine = 0
        self.Frozen = False
        self.FrozenTime = 0

        self.winMusic =  pygame.mixer.Sound('./music/win.wav')
    def CheckEvent(self):
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:
                pygame.quit()
                self.GameState = 'Over'
            if event.type == KEYDOWN:          #键盘
                self.keyBoardEvent(event.key)
            if event.type == KEYUP:
                self.rub.stopMove()
                for i in  self.monesters:
                    if i.type == 'dead':
                        i.stopMove()
            if event.type == MOUSEBUTTONDOWN:   #鼠标
                self.down = 1
            elif event.type == MOUSEBUTTONUP and self.down == 1:
                self.down = 0
                if self.GameState == 'upGrade':
                    self.choice = self.sureMenu.getId(pygame.mouse.get_pos())
                else:
                    self.choice = self.gameMenu.getId(pygame.mouse.get_pos())
            else:
                self.choice = False
    def  Logic(self,screen):
        '''Game Logic  '''
        self.setMenu()          #菜单处理
        self.sprMove(screen)    #移动处理
        self.animLoop(screen)   #动画播放
        self.attack()           #碰撞检测
        self.load_img(1)        #奖励
        if self.rub.getOver():
            self.GameState='Over'
        self.judgeWin()
    def  Paint(self,screen):
        '''Game Paint'''
        screen.blit(self.bgimg, self.bgimgRect)     #背景
       # self.sflower.paint(screen)                  #精灵
        self.rub.paint(screen)
        self.buff_list.draw(screen)       #奖励
        for i in  self.monesters:        #怪物
            i.paint(screen)
        for i in self.player_shot:       #技能
            i.paint(screen)
            if i.death == True:          # 技能只播放一次，播放完就清除
                self.player_shot.remove(i)
        self.gameMenu.paint(screen)
        state = self.rub.getState()
        state['bonus'] = str(self.mine)
        self.stateMenu.paint(screen, state)
        pygame.display.flip()

    def keyBoardEvent(self,key):
        "键盘处理函数"
        if key == K_LEFT or key == K_RIGHT or key == K_UP or key == K_DOWN:
            self.rub.state = 'run'
        if key == K_LEFT:
            self.rub.dirc = 'left'
        elif key == K_RIGHT:
            self.rub.dirc = 'right'
        elif key == K_UP:
            self.rub.dirc = 'back'
        elif key == K_DOWN:
            self.rub.dirc = 'front'
        for i in self.monesters:            # 致死怪复制玩家状态
            i.stateCopy(self.rub)
        if key == K_z:                      # 玩家进行攻击
            if self.rub.buff['froze'] != 0:
                self.Frozen = True          # 设置冰冻状态
                self.FrozenTime += 1000     # 冰冻时间
                self.player_shot.append(self.rub.froze())# 实体
        if key == K_c:
            if self.rub.buff['shot'] != 0:  # 射击
                self.player_shot.append(self.rub.shot())
    def setMenu(self):
        "     菜单处理     "
        pos = pygame.mouse.get_pos()
        self.gameMenu.getId(pos)
        if self.choice != False:
            if self.choice == 'back':
                self.GameState = 'Over'
    def sprMove(self,screen):
        '''     移动    '''
        if self.rub.death == False:     #人物移动控制
            self.rub.moveSpr(screen)
        if self.Frozen!=True:               # 非冰冻状态可以移动
            for i in self.monesters:        # 怪物移动控制
                    i.moveSpr(screen)
        else:                               #冰冻状态处理效果计时
            self.FrozenTime -=10
            if self.FrozenTime<=0:
                self.FrozenTime = 0
                self.Frozen = False

    def animLoop(self,screen):
        "     动画帧切换     "
        self.rub.update(15)          # 玩家动画
        for i in self.monesters:    # 怪物动画
            i.update(10)
        for i in self.player_shot:  # 释放的冰冻技能列表 动画
            i.loopOnce(15)
            if i.dirc!=None:
                i.moveSpr(screen)
        for i in self.buff_list:     #奖励
            i.update(10)

    def attack(self):
        "     攻击和碰撞检测        "
        if self.rub.rect.colliderect(self.sflower.rect) and self.sflower.death == False:
            self.rub.buff['froze'] += 1
            self.rub.buff['shot'] += 1
            self.sflower.death = True
            self.rub.speed = 3      #人物拾取花之后减速效果消除
            self.rub.getBuff()
        '''      怪物和buff碰撞检测   '''
        for i in self.monesters:
            if i.type=='dead' and i.death==False:
                if i.rect.colliderect(self.sflower.rect) and self.sflower.death == False:
                   self.sflower.death = True
                   i.speed = 8

        '''     怪物与人物碰撞检测    '''
        for i in self.monesters:
            if i.death==False and i.rect.colliderect(self.rub.rect) :
                self.rub.beAttack(i.attack())
                if self.mine>0:             #怪物夺取宝物
                    self.mine = 0
            for m in self.player_shot:
                if m.dirc != None:
                    if i.death==False and i.rect.colliderect(m.rect) :
                        i.death =True
        '''     奖励          '''
        hits = pygame.sprite.spritecollide(self.rub, self.buff_list, True)
        for hit in hits:
            if hit.type == 'bulletset':
                self.rub.buff['shot'] += 1
            if hit.type == 'pause':
                self.rub.buff['froze'] += 1
            if hit.type == 'mine':
                self.mine+=1
            self.rub.getBuff()
    '''奖励'''
    def load_img(self, passed_time):
        self._passed_time += passed_time
        if self._passed_time % 150 == 0:
            buff = BuffSprites('pause.png', 30, 30, 1, lineNum=1)
            if buff.type == 'mine':
                buff.speedy=0
            self.buff_list.add(buff)

    def judgeWin(self):
        if self.rub.level == 0 and self.mine == 5:
            self.GameState = 'upGrade'
            self.rub.level += 1
            self.mine = 0
            self.winMusic.play()
        if self.rub.level == 1 and self.mine == 10:
            self.GameState = 'upGrade'
            self.rub.level += 1
            self.mine = 0
            self.winMusic.play()
        if self.rub.level == 2 and self.mine == 15:
            self.GameState = 'upGrade'
            self.rub.level += 1
            self.mine = 0
            self.winMusic.play()
        if self.rub.level == 3 and self.mine==20:
            self.GameState = 'Win'
            self.rub.level += 1
            self.mine = 0
            self.winMusic.play()
    def upGrade(self,screen):
        '''更换关卡'''
        if self.rub.level == 1:
            self.monesters = Monester.createMos(1,3,0) #'''重新生成怪物'''
            self.bgimg = pygame.image.load('./img/bg_cave.png')  # 游戏背景
            self.bgimg = pygame.transform.scale(self.bgimg,(screen.get_rect().w, screen.get_rect().h))
        if self.rub.level == 2:
            self.monesters = Monester.createMos(2,5,1) #'''重新生成怪物'''
            self.bgimg = pygame.image.load('./img/bg_volcano.png')  # 游戏背景
            self.bgimg = pygame.transform.scale(self.bgimg,(screen.get_rect().w, screen.get_rect().h))
        if self.rub.level == 3:
            self.monesters = Monester.createMos(3,3,3) #'''重新生成怪物'''
            self.bgimg = pygame.image.load('./img/bg_ether.png')  # 游戏背景
            self.bgimg = pygame.transform.scale(self.bgimg,(screen.get_rect().w, screen.get_rect().h))
        self.sflower = Monester('tu.png', 34, 34, 12, "rub")  # npc
        self.sflower.rect.bottom = 480
        self.sflower.reborn = 10000
        self.monesters.append(self.sflower)
        self.buff_list.empty()  #'''重新Load奖励'''
        self.rub.upGrade(self.rub.level)
    def Win(self,screen):
        pos = pygame.mouse.get_pos()
        self.sureMenu.getId(pos)
        if self.choice == 'sure':
            if self.GameState == 'upGrade':
                self.GameState = 'Running'
            if self.GameState == 'Win':
                self.GameState = 'Over'
        elif self.choice == 'back':
            self.GameState = 'Over'
        if self.GameState == 'upGrade':
            win_you = pygame.image.load('./img/win_you.png')  # 游戏背景
            win_win = pygame.image.load('./img/win_win.png')  # 游戏背景
            win_text = pygame.image.load('./img/win_text.png')
            win_text.get_rect().midtop = screen.get_rect().midtop
            win_text.get_rect().y = screen.get_rect().bottom
            screen.blit(win_text,(150,320,100,100))
            screen.blit(win_you,(150,250,100,100))
            screen.blit(win_win,(250,250,100,100))
            self.sureMenu.paint(screen)
        elif self.GameState == 'Win':
            final_pic = pygame.image.load('./img/final_pic.png')
            rect = final_pic.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.top = 70
            screen.blit(final_pic,rect)
            if rect.collidepoint(pos):
                final_pic_open = pygame.image.load('./img/final_pic_open.jpg')
                final_pic_open = pygame.transform.scale(final_pic_open, (screen.get_rect().w, screen.get_rect().h))
                screen.blit(final_pic_open,final_pic_open.get_rect() )
        pygame.display.flip()

