# dinoRun
import pygame
import os
import random

pygame.init()

ASSETS = './studyPyGame/Assets/'
SCREEN_WIDTH = 1100 # 게임 윈도우 넓이 1100으로 변수화
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, 600))
icon = pygame.image.load('./studyPyGame/dinoRun2.png')
pygame.display.set_icon(icon)
# 배경이미지 로드
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png')) # Assets 폴더의 Other 폴더에서 Track.png 가져오는 것
# 공룡이미지 로드
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'), 
           pygame.image.load(f'./studyPyGame/Assets/Dino/DinoRun2.png')]    # 경로는 이렇게 적어도 됨
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'), 
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')   # jump는 이미지가 하나기 때문에 배열처리하면 오류남
# 구름 이미지
CLOUD = pygame.image.load(f'{ASSETS}Other/Cloud.png')
# 익룡 이미지
BIRD = [pygame.image.load(f'{ASSETS}Bird/Bird1.png'), 
        pygame.image.load(f'{ASSETS}Bird/Bird2.png')]
# 선인장 이미지 / 애니메이션 위한거 아님 그냥 선인장 종류 세개씩 
LARGE_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/LargeCactus1.png'), 
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/LargeCactus3.png')]
SMALL_CACTUS = [pygame.image.load(f'{ASSETS}Cactus/SmallCactus1.png'), 
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus2.png'),
                pygame.image.load(f'{ASSETS}Cactus/SmallCactus3.png')]

class Dino: # 공룡 클래스
    X_POS = 80; Y_POS = 310 # 공룡 기본 위치값
    Y_POS_DUCK = 340    # duck 할때 이미지 크기 변경
    JUMP_VEL = 9.0  # 점프 속도

    def __init__(self) -> None:
        self.run_image = RUNNING; self.duck_image = DUCKING; self.jump_image = JUMPING
        # 공룡 상태 초기화 => 기본적으로 run 은 True, duck과 jump는 false 상태임
        self.dino_run = True; self.dino_duck = False; self.dino_jump = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL   # 점프 초기값 9.0
        self.image = self.run_image[0]  # Dinorun1 이 처음 이미지 되는 것
        self.dino_rect = self.image.get_rect()  # 이미지 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS


    def update(self, userInput) -> None:
        if self.dino_run:
            self.run()
        elif self.dino_duck:
            self.duck()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10: self.step_index = 0   # 애니메이션 스텝
        
        if userInput[pygame.K_UP] and not self.dino_jump:   # 점프하면
            self.dino_run = False
            self.dino_duck = False
            self.dino_jump = True
            self.dino_rect.y = self.Y_POS   # 이걸로 초기화 안해주면 공룡 하늘로 날아감

        elif userInput[pygame.K_DOWN] and not self.dino_jump: # 수구리
            self.dino_run = False
            self.dino_duck = True
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):   # 런
            self.dino_run = True
            self.dino_duck = False
            self.dino_jump = False

    def run(self):
        self.image = self.run_image[self.step_index // 5]   # 10 0, 1
        self.dino_rect = self.image.get_rect()  # 이미지 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1 
   
    def duck(self):
        self.image = self.duck_image[self.step_index // 5]   # 10 0, 1
        self.dino_rect = self.image.get_rect()  # 이미지 사각형 정보
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK  # 이미지 높이 작으니까 변경해주는 것 
        self.step_index += 1 
   
    def jump(self):
        self.image = self.jump_image
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:  # -9.0 되면 점프 중단
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL


    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))

class Cloud:    # 구름 클래스
    def __init__(self) -> None: # 클래스 만들때 생성자 초기화는 필수임!!!!! pass 적어놓더라도 클래스 만들면 무조건 초기화부터 하기
        self.x = SCREEN_WIDTH + random.randint(300, 500)
        self.y = random.randint(50, 100)    # 윈도우 높이의 50~100 사이에만 구름 넣겠다는 것
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self) -> None:
        self.x -= game_speed
        if self.x < -self.width:    # x 축 화면 밖으로 벗어나면 
            self.x = SCREEN_WIDTH + random.randint(1300, 2000)  # 구름을 멀리 보내서 다음 구름 보이기 까지 시간차 두게 하는 것
            self.y = random.randint(50, 100)

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image, (self.x, self.y))

class Obstacle: # 익룡이랑 선인장은 장애물이기 때문에 관련 처리할 부모 클래스를 먼저 만들어 주는 것
    def __init__(self, image, type) -> None:
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH 

    def update(self) -> None:
        self.rect.x -= game_speed
        if self.rect.x <= -self.rect.width:  # 왼쪽 화면 밖으로 벗어나면
            obstacles.pop()  # 장애물 리스트에 하나 꺼내오기

    def draw(self, SCREEN) -> None:
        SCREEN.blit(self.image[self.type], self.rect)

class Bird(Obstacle):   # 장애물 클래스를 상속받음
    def __init__(self, image) -> None:
        self.type = 0 # 새는 0 
        super().__init__(image, self.type)
        self.rect.y = 250
        self.index = 0  # 새 이미지 2개이기 때문에 0번 인덱스 값의 이미지로 먼저 시작한다는 것

    def draw(self, SCREEN) -> None: # draw 재정의
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index // 5], self.rect)
        self.index += 1

class LargeCactus(Obstacle): # 장애물 클래스 상속받는 큰선인장 클래스
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2)    # 큰 선인장 이미지 세개 중에 하나 고르는 것
        super().__init__(image, self.type)
        self.rect.y = 300

class SmallCactus(Obstacle): # 장애물 클래스 상속받는 작은선인장 클래스
    def __init__(self, image) -> None:
        self.type = random.randint(0, 2)    # 작은 선인장 이미지 세개 중에 하나 고르는 것
        super().__init__(image, self.type)
        self.rect.y = 325

def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles
    x_pos_bg = 0
    y_pos_bg = 380  # 배경화면의 위치
    points = 0  # 게임점수
    run = True
    clock = pygame.time.Clock()
    dino = Dino()   # 공룡객체
    cloud = Cloud() # 구름객체
    game_speed = 14
    obstacles = []

    font = pygame.font.Font(f'{ASSETS}NanumGothicBold.ttf', 20)

    def score():
        global points, game_speed
        points += 1
        if points % 100 == 0:   # 점수가 100점 단위로 올라가면
            game_speed += 1 # 게임 속도 증가
        
        txtScore = font.render(f'SCORE : {points}', True, (83,83,83))  # True는 antialias 에 대한 것.. 그림 확대할 때 픽셀 깨져보이는 현상에 대한건데 글씨 부드러워 보이도록 True 하는 것임
        txtRect = txtScore.get_rect()
        txtRect.center = (1000, 40)
        SCREEN.blit(txtScore, txtRect)



    def background():   # 함수 안의 함수.. main 함수 안에서만 사용하는 함수 만드는 것
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))   # 0, 380에 먼저 그리는 것
        SCREEN.blit(BG, (image_width+x_pos_bg, y_pos_bg))   # 2404+0, 380에 그림그림.. 2404는 배경에 들어갈 파일의 크기임
        # update랑 draw 동시에
        if x_pos_bg <= -image_width:
            x_pos_bg = 0

        x_pos_bg -= game_speed



    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255))  # 배경 흰색
        userInput = pygame.key.get_pressed()

        background()
        score()

        cloud.draw(SCREEN)  # 구름 애니메이션
        cloud.update()  
        # 구름 부분이 공룡 부분 밑에 적으면 구름이 공룡 앞으로 지나가게 됨 _ 구름부분 먼저 적고 공룡 부분 적어서 공룡이 앞으로 가게 하는 것

        dino.draw(SCREEN)  # 공룡을 화면에 그려주는 것
        dino.update(userInput)  # input에따른 동작

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:   # 작은선인장
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:   # 큰선인장
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2: # 익룡
                obstacles.append(Bird(BIRD)) # Bird 클래스로 BIRD 이미지 받아서 쓴다는 것
        
        for obs in obstacles:
            obs.draw(SCREEN)
            obs.update()
            if dino.dino_rect.colliderect(obs.rect): # 충돌감지.. Collision Detection
                pygame.draw.rect(SCREEN, (255, 0, 0), dino.dino_rect, 3)

        
        clock.tick(30)  # 30 기본.. 수가 커질수록 공룡 움직임 빨라짐
        pygame.display.update() # 초당 30번 update 수행

if __name__ == '__main__':
    main()