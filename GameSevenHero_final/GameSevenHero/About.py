import pygame
from Beans import *

"""          关于            """

def gameAbout():
    size = width, height = 480, 600
    screen = pygame.display.set_mode(size)  # 显示窗口
    bgimg = pygame.transform.scale(pygame.image.load('./img/about.png'), (width, height))

    bgimgRect = bgimg.get_rect()
    GameState = 'Running'
    clock = pygame.time.Clock()
    choice = False
    # 子菜单
    menuitem = ['back']
    gameMenu = Menu(img = 'button.png')
    for i in range(len(menuitem)):
        rect = gameMenu.img[0].get_rect()
        rect.x = 100
        rect.y = 0 + i * rect.h
        gameMenu.addItem(menuitem[i], rect)

    while GameState != 'Over':
        clock.tick(60)
        for event in pygame.event.get():  # 遍历所有事件
            if event.type == pygame.QUIT:
                pygame.quit()
                GameState = 'Over'
            if event.type == MOUSEBUTTONDOWN:
                down = 1
            elif event.type == MOUSEBUTTONUP and down == 1:
                down = 0
                choice = gameMenu.getId(pygame.mouse.get_pos())
            else:
                choice = False
        # Game loop
        if GameState != 'Over':
            pos = pygame.mouse.get_pos()
            gameMenu.getId(pos)
            # logic
            if choice != False:
                if choice == 'back':
                    GameState = 'Over'
            # paint
            screen.blit(bgimg, bgimgRect)
            gameMenu.paint(screen)
            pygame.display.flip()