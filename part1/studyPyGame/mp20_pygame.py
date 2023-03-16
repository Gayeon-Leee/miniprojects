# Python Game - PyGame  Game Framework
# pip install pygame
import pygame

pygame.init() # 1(중요도). 게임 초기화 --- 필수!!!
width = 500; height = 500

win = pygame.display.set_mode((width, height))   # 윈도우 500x500 으로 만드는것.. 튜플이라 괄호 한 번 더 쓴것
pygame.display.set_caption('게임만들기')
icon = pygame.image.load('./studyPyGame/game.png')
pygame.display.set_icon(icon)

# object 설정
x = 250
y = 250  # 전체 사이즈 500 이므로 정중앙
radius = 10
vel_x = 10
vel_y = 10
jump = False


run = True

# GUI 는 내부적으로 while True 가 계속 되는 상태라고 볼 수 있음.. 사용자가 버튼을 클릭하거나 하는 등의 시그널을 감지해야하기 때문!
# game은 GUI랑 다르게 while True을 사용자가 제어해줘야하는 것! 
while run:
    win.fill((0,0,0))   # 윈도우 전체 배경을 
    pygame.draw.circle(win, (255,255,255), (x, y), radius)  # circle(장소 - win, 색상 - 흰색(255,255,255), 위치 - (x, y), 반지름 - radius)

    # 이벤트 = 시그널
    for event in pygame.event.get():    # 2(중요도). 이벤트 받기.. 게임초기화 다음으로 중요함!!
        if event.type == pygame.QUIT:
            run = False

    # 객체이동
    userInput = pygame.key.get_pressed()
    if userInput[pygame.K_LEFT] and x > 10: 
        x -= vel_x  # 왼쪽으로 10씩 이동
    if userInput[pygame.K_RIGHT] and x < width - 10:
        x += vel_x  # 오른쪽으로 10씩 이동
    # if userInput[pygame.K_UP] and y > 10:
    #     y -= vel_x
    # if userInput[pygame.K_DOWN] and y < height - 10:
    #     y += vel_x        

    # 객체점프
    if jump == False and userInput[pygame.K_SPACE]:
        jump = True
    if jump == True:
        y -= vel_y * 3
        vel_y -= 1
        if vel_y < -10:
            jump = False
            vel_y = 10

    pygame.time.delay(10)    
    pygame.display.update() # 3(중요도). 화면 업데이트(전환)