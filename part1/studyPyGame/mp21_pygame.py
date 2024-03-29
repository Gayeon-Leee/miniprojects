import pygame

pygame.init()
win = pygame.display.set_mode((1000, 500))

bg_img = pygame.image.load('./studyPyGame/Assets/Background.png')
BG = pygame.transform.scale(bg_img, (1000, 500))    # 원래 이미지 사이즈 800x400 인데 1000x500으로 변경
pygame.display.set_caption('게임만들기')
icon = pygame.image.load('./studyPyGame/game.png')
pygame.display.set_icon(icon)

width = 1000
loop = 0
run = True
while run:
    win.fill((0,0,0))
   
    # 이벤트 = 시그널
    for event in pygame.event.get():    # 2(중요도). 이벤트 받기.. 게임초기화 다음으로 중요함!!
        if event.type == pygame.QUIT:
            run = False
    
    # 배경
    win.blit(BG, (loop,0))
    win.blit(BG, (width + loop, 0))
    if loop == -width:  # -1000
        win.blit(BG, (width + loop, 0))
        loop = 0

    loop -= 1

    pygame.display.update()