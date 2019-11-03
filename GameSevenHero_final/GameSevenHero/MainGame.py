#coding = utf-8
import pygame
from pygame.locals import *
from Beans import *
from Utils import *
from Game import *
from About import *
import sys

pygame.init()  # 初始化
pygame.mixer.init()
pygame.mixer.music.load('./music/bgMusic2.wav')
pygame.mixer.music.set_volume(0.2)

size = width, height = 480, 600
screen = pygame.display.set_mode(size)  # 显示窗口
bgimg = pygame.image.load('./img/forest.png')
bgimgRect = bgimg.get_rect()
title_img = pygame.image.load('./img/title.png')
clock = pygame.time.Clock()  # 设置时钟
player_img = {'彭琪':'player_pq.png','叶倩芝':'player_yqz.png','付康':'player_fk.png'
    , '曾树林': 'player_zsl.png','谭诗龙':'player_tsl.png'
    ,'李名兴':'player_lmx.png','卓秀祥':'player_zxx.png'}
player_say ={'彭琪':'强 不愧是你','叶倩芝':'哼~小样！开挂了','付康':'闯关失败，你已被孤立'
    , '曾树林': '0 error 0 warning','谭诗龙':'牛逼'
    ,'李名兴':'none  named v!','卓秀祥':'你获得了阿里云证书'}
"""         新游戏          """
def newGame():
    "       一局新游戏        "
    GameState = 'chosePlayer'
    down = 0
    choice = 0
    "新建菜单"
    playerMenu = PlayerMenu(screen=screen,img='button.png')
    for i in player_img:
        playerMenu.addItem(i,player_img[i], width=34, height = 34,number = 12, screen=screen)
    "人物选择阶段"
    while GameState == 'chosePlayer':
        clock.tick(60)
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:
                GameState = 'Over'
            elif event.type == MOUSEBUTTONDOWN:
                down = 1
            elif event.type == MOUSEBUTTONUP and down == 1:
                down = 0
                choice = playerMenu.getId(pygame.mouse.get_pos())
                print(choice)
            else:
                choice = False
        "     菜单处理     "
        pos = pygame.mouse.get_pos()
        playerMenu.getId(pos)
        if choice != False:
            if choice == 'back':
                GameState = 'Over'
            else:
                GameState = 'Start'
        else:
            playerMenu.anim()
            playerMenu.paint(screen,'选择人物')
            pygame.display.flip()
    "冒险阶段"
    ourGame  = GameData(screen,player_img[choice])
    choice = False
    while ourGame.GameState != 'Over':
        ourGame.clock.tick(60)
        ourGame.CheckEvent()
        if ourGame.GameState != 'Over':
            if ourGame.GameState == 'upGrade':
                ourGame.upGrade(screen)
                ourGame.Win(screen)
            if  ourGame.GameState == 'Running':
                ourGame.Logic(screen)
                ourGame.Paint(screen)
            if ourGame.GameState == 'Win':
                playerMenu.back = pygame.transform.scale(pygame.image.load('./img/bg_win.png'),
                                                         (screen.get_rect().w,screen.get_rect().h))
                ourGame.Win(screen)
                pos = pygame.mouse.get_pos()
                choice = playerMenu.getId(pos)
                if choice != False:
                    playerMenu.paint(screen,player_say[choice])
                else:
                    playerMenu.paint(screen,'你拿到了证书')
        else:
            return

"""#################    游戏开始    #######################"""
GameState = 'Runing'
"""     菜单初始化        """
menuitem = ['NewGame','About','Exit']
mainMenu = Menu(img='button.png')
for i in range(len(menuitem)):
    rect = mainMenu.img[1].get_rect()
    rect.x = (screen.get_rect().w - mainMenu.img[1].get_rect().w)//2
    rect.y = 200 + i*rect.h
    mainMenu.addItem(menuitem[i],rect)
mainMenubg =  pygame.transform.scale(bgimg,(screen.get_rect().w,screen.get_rect().h))
mainMenu.back = mainMenubg
pygame.mixer.music.play(-1)
while True:
    clock.tick(60)
    ######     Check Event   ######
    for event in pygame.event.get():  # 遍历所有事件
        if event.type == pygame.QUIT:
            GameState = 'Over'
            #pygame.quit()
        elif event.type == MOUSEBUTTONDOWN:
            down = 1
        elif event.type == MOUSEBUTTONUP and down == 1:
            down = 0
            choice = mainMenu.getId(pygame.mouse.get_pos())
            print(choice)
        else:
            choice = False
    if GameState!='Over':
        #####      Logic    ######
        pos = pygame.mouse.get_pos()
        mainMenu.getId(pos)
        if choice != False:
            if choice == 'NewGame':
                newGame()
                choice=False
            if choice == 'Exit':
                GameState = 'Over'
                choice=False
            if choice == 'About':
                gameAbout()
                choice = False
        #####       Paint       ######
        mainMenu.paint(screen)
        screen.blit(title_img,title_img.get_rect())
        pygame.display.flip()
    else:
        pygame.quit()
        sys.exit()