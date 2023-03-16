# dinoRun
import pygame
import os

pygame.init()

ASSETS = './studyPyGame/Assets/'
SCREEN = pygame.display.set_mode((1100, 600))
icon = pygame.image.load('./studyPyGame/dinoRun2.png')
pygame.display.set_icon(icon)
# 배경이미지 로드
BG = pygame.image.load(os.path.join(f'{ASSETS}Other', 'Track.png')) # Assets 폴더의 Other 폴더에서 Track.png 가져오는 것
# 공룡이미지 로드
RUNNING = [pygame.image.load(f'{ASSETS}Dino/DinoRun1.png'), 
           pygame.image.load(f'./studyPyGame/Assets/Dino/DinoRun2.png')]    # 경로는 이렇게 적어도 됨
DUCKING = [pygame.image.load(f'{ASSETS}Dino/DinoDuck1.png'), 
           pygame.image.load(f'{ASSETS}Dino/DinoDuck2.png')]
JUMPING = pygame.image.load(f'{ASSETS}Dino/DinoJump.png')

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


def main():
    run = True
    clock = pygame.time.Clock()
    dino = Dino()


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        SCREEN.fill((255,255,255))  # 배경 흰색
        userInput = pygame.key.get_pressed()

        dino.draw(SCREEN)  # 공룡을 화면에 그려주는 것
        dino.update(userInput)  # input에따른 동작
        
        clock.tick(30)
        pygame.display.update() # 초당 30번 update 수행

if __name__ == '__main__':
    main()