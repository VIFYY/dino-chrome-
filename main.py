import pygame
import os
import random
pygame.init()

# Global Constants
SCREEN_HEIGHT = 600
SCREEN_WIDTH = 1100
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

RUNNING = [pygame.image.load(os.path.join("chrome-dinosaur/Assets/Dino", "DinoRun1.png")),
           pygame.image.load(os.path.join("chrome-dinosaur/Assets/Dino", "DinoRun2.png"))]
JUMPING = pygame.image.load(os.path.join("chrome-dinosaur/Assets/Dino", "DinoJump.png"))
DUCKING = [pygame.image.load(os.path.join("chrome-dinosaur/Assets/Dino", "DinoDuck1.png")),
           pygame.image.load(os.path.join("chrome-dinosaur/Assets/Dino", "DinoDuck2.png"))]

SMALL_CACTUS = [pygame.image.load(os.path.join("chrome-dinosaur/Assets/Cactus", "SmallCactus1.png")),
                pygame.image.load(os.path.join("chrome-dinosaur/Assets/Cactus", "SmallCactus2.png")),
                pygame.image.load(os.path.join("chrome-dinosaur/Assets/Cactus", "SmallCactus3.png"))]
LARGE_CACTUS = [pygame.image.load(os.path.join("chrome-dinosaur/Assets/Cactus", "LargeCactus1.png")),
                pygame.image.load(os.path.join("chrome-dinosaur/Assets/Cactus", "LargeCactus2.png")),
                pygame.image.load(os.path.join("chrome-dinosaur/Assets/Cactus", "LargeCactus3.png"))]

BIRD = [pygame.image.load(os.path.join("chrome-dinosaur/Assets/Bird", "Bird1.png")),
        pygame.image.load(os.path.join("chrome-dinosaur/Assets/Bird", "Bird2.png"))]

CLOUD = pygame.image.load(os.path.join("chrome-dinosaur/Assets/Other", "Cloud.png"))
#Creamos una lista de la imagen Poder para heredar en Obstacle
POWER = [pygame.image.load(os.path.join("chrome-dinosaur/Assets/Other", "pawer.png"))]

BG = pygame.image.load(os.path.join("chrome-dinosaur/Assets/Other", "Track.png"))


class Dinosaur:
    X_POS = 80
    Y_POS = 310
    Y_POS_DUCK = 340
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.dino_fly = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
#Intenta que el dinosario vuele al tocar el orbe el booleano se torna true cuando colisiona 
    def playerFly(self, booleano):
        self.dino_fly = booleano

    def fly(self):
        self.image = self.jump_img
            

    def update(self, userInput):
        if self.dino_duck:
            self.duck()
        if self.dino_run:
            self.run()
        if self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_UP] and not self.dino_jump:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < - self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


class Cloud:
    def __init__(self):
        self.x = SCREEN_WIDTH + random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = CLOUD
        self.width = self.image.get_width()

    def update(self):
        self.x -= game_speed
        if self.x < -self.width:
            self.x = SCREEN_WIDTH + random.randint(2500, 3000)
            self.y = random.randint(50, 100)

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.x, self.y))




class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)
#Se crea la clase Power para que aparezca la imagen
class Power(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 200

## cactus pequeño 
class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 325

##cactus grande
class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = random.randint(0, 2)
        super().__init__(image, self.type)
        self.rect.y = 300

## pajaro 
class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 260
        self.index = 0

    def draw(self, SCREEN):
        if self.index >= 9:
            self.index = 0
        SCREEN.blit(self.image[self.index//5], self.rect)
        self.index += 1


def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, lives_count
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    cloud = Cloud()
    game_speed = 20
    x_pos_bg = 0
    y_pos_bg = 380
    points = 0
    lives_count = 0
    font = pygame.font.Font('freesansbold.ttf', 20)
    obstacles = []
    death_count = 0

    def score():
        global points, game_speed, lives_count
        points += 1

        # Incremento de velocidad multiplos de 100 puntos
        if points % 100 == 0:
            game_speed += 1
        
        # Incremento de vidas multiplos de 500 puntos
        if points % 200 == 0:
            lives_count += 1

        text = font.render("Points: " + str(points), True, (0, 0, 0))
        livesText = font.render("Lives: " + str(lives_count), True, (0, 0, 0))
        textRect = text.get_rect()
        livesRect = livesText.get_rect()
        textRect.center = (1000, 40)
        livesRect.center = (1000, 80)
        SCREEN.blit(text, textRect)
        SCREEN.blit(livesText, livesRect)

    def background():
        global x_pos_bg, y_pos_bg
        image_width = BG.get_width()
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))
        SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
        if x_pos_bg <= -image_width:
            SCREEN.blit(BG, (image_width + x_pos_bg, y_pos_bg))
            x_pos_bg = 0
        x_pos_bg -= game_speed

    def start(run, death_count):
        global lives_count

        colision = False

        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            SCREEN.fill((255, 255, 255))
            userInput = pygame.key.get_pressed()

            player.draw(SCREEN)
            player.update(userInput)

            if len(obstacles) == 0:
                if random.randint(0, 6) == 0 or random.randint(0, 6) == 1:
                    obstacles.append(SmallCactus(SMALL_CACTUS))
                elif random.randint(0, 6) == 2 or random.randint(0, 6) == 3:
                    obstacles.append(LargeCactus(LARGE_CACTUS))
                elif random.randint(0, 6) == 4 or random.randint(0, 6) == 5:
                    obstacles.append(Bird(BIRD))
                    #Si el numero randomda 6 muestra el poder Chance 1/7
                elif random.randint(0, 6) == 6:
                    obstacles.append(Power(POWER))

            for obstacle in obstacles:
                obstacle.draw(SCREEN)
                obstacle.update()
                #Comprueba si el dinosario colisiono con una imagen de poder
                if player.dino_rect.colliderect(obstacle.rect) and obstacle == Power(POWER):
                    player.dino_fly(True)
                    break
                elif player.dino_rect.colliderect(obstacle.rect):
                    colision = True
                    break
                
                if colision == True:
                    lives_count -= 1
                    death_count += 1
                    if lives_count > 0:
                        start(True, death_count)
                    else:
                        menu(death_count, lives_count)

            background()

            cloud.draw(SCREEN)
            cloud.update()

            score()

            clock.tick(30)
            pygame.display.update()

    start(True, death_count)

def menu(death_count, lives_count):

    if (lives_count > 1):
        return lives_count

    global points
    run = True

    while run:
        SCREEN.fill((255, 255, 255))
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Press any Key to Start", True, (0, 0, 0))
        elif death_count > 0 and lives_count <= 0:
            text = font.render("Press any Key to Restart", True, (0, 0, 0))
            score = font.render("Your Score: " + str(points), True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)
        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0, lives_count=1)
