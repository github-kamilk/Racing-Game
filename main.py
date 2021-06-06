import pygame, time, sys, random
from pygame.locals import *
from pygame import mixer
import pygame_menu

pygame.init()
black = (0, 0, 0)
red = (255, 0, 0)
window = pygame.display.set_mode((700, 750))
window.fill(black)
pygame.display.set_caption("Racing Game")

def set_difficulty(value, difficulty):
    # Do the job here !
    pass

def start_the_game():
    FPS = 30
    framesPerSec = pygame.time.Clock()

    speed = 5

    SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.get_surface().get_size()

    mixer.init()
    mixer.music.load("data/crash.mp3")
    mixer.music.set_volume(0.0)

    obstaclesPositons = [95, 270, 445]
    coinsPositons = [178, 353, 528]
    collected = False

    class Coins(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("data/scaledCoin.png")
            self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            self.rect = self.surface.get_rect(center=(random.choice(coinsPositons), random.randint(-800, 0)))

        def move(self, collected):
            self.rect.move_ip(0, speed)
            if (self.rect.bottom > SCREEN_HEIGHT) or collected:
                self.rect.center = (random.choice(coinsPositons), random.randint(-800, 0))

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    class Obstacle(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("data/scaledBlock.png")
            self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            self.rect = self.surface.get_rect(topleft=(random.choice(obstaclesPositons), random.randint(-800, 0)))

        def move(self, score):
            self.rect.move_ip(0, speed)
            if self.rect.bottom > SCREEN_HEIGHT:
                self.rect.topleft = (random.choice(obstaclesPositons), random.randint(-800, 0))
                score += 1
            return score

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.image.load("data/scaledFerrari.png")
            self.surface = pygame.Surface((self.image.get_width(), self.image.get_height()))
            self.rect = self.surface.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 80))

        def draw(self, surface):
            surface.blit(self.image, self.rect)

        def update(self):
            pressedKeys = pygame.key.get_pressed()

            if self.rect.left > 80:
                if pressedKeys[K_LEFT]:
                    self.rect.move_ip(-8, 0)

            if self.rect.right < SCREEN_WIDTH - 80:
                if pressedKeys[K_RIGHT]:
                    self.rect.move_ip(8, 0)

    class Background():
        def __init__(self):
            self.backgroundImage = pygame.image.load("data/scaledBackground.png")
            self.rectangleBGimage = self.backgroundImage.get_rect()

            self.bgY1 = 0
            self.bgX1 = 0

            self.bgY2 = -self.rectangleBGimage.height
            self.bgX2 = 0

            self.moveSpeed = speed

        def update(self):
            self.bgY1 += self.moveSpeed
            self.bgY2 += self.moveSpeed

            if self.bgY1 > self.rectangleBGimage.height:
                self.bgY1 = -self.rectangleBGimage.height

            if self.bgY2 > self.rectangleBGimage.height:
                self.bgY2 = -self.rectangleBGimage.height

        def render(self):
            window.blit(self.backgroundImage, (self.bgX1, self.bgY1))
            window.blit(self.backgroundImage, (self.bgX2, self.bgY2))

    def fuellHeight(fuell, collectedCoin):
        if collectedCoin:
            if fuell >= 5:
                fuell -= 15
            else:
                fuell = 0

        if fuell >= 105:
            pygame.quit()
            sys.exit()

        fuell += 0.2

        return fuell

    background = Background()

    # Zwieksz predkosc co 3s
    # INCREASE_SPEED = pygame.USEREVENT + 1
    # pygame.time.set_timer(INCREASE_SPEED, 3000)

    P1 = Player()
    playerGroup = pygame.sprite.Group()
    playerGroup.add(P1)

    coinsGroup = pygame.sprite.Group()
    coinsGroup.add(Coins())
    coinsGroup.add(Coins())

    obstacleGroup = pygame.sprite.Group()
    obstacleGroup.add(Obstacle())
    obstacleGroup.add(Obstacle())
    obstacleGroup.add(Obstacle())

    fuellImage = pygame.image.load("data/scaledFuell.png")

    font = pygame.font.SysFont("Verdana", 60)
    gameOver = font.render("Game Over!", True, red)

    score = 0
    fuell = 0

    while True:
        background.update()
        background.render()

        window.blit(fuellImage, (620, 0))
        pygame.draw.rect(window, red, (SCREEN_WIDTH - 28, 8 + fuell, 20, 105 - fuell))
        pygame.draw.rect(window, black, (SCREEN_WIDTH - 28, 8, 20, fuell))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            # if event.type == INCREASE_SPEED:
            #     speed += 0.5

        if pygame.sprite.spritecollideany(P1, obstacleGroup):
            window.fill(black)
            window.blit(gameOver, (150, 150))
            pygame.display.update()
            mixer.music.play()
            # time.sleep(4)
            #pygame.quit()
            #sys.exit()
            mainMenu()

        for obstacle in obstacleGroup:
            score = obstacle.move(score)
            obstacle.draw(window)

        for coins in coinsGroup:
            coins.move(collected)
            if pygame.sprite.spritecollideany(coins, playerGroup):
                collected = True
                coins.move(collected)
                window.blit(coins.image, coins.rect)
                fuell = fuellHeight(fuell, True)
                collected = False
            coins.draw(window)

        scoreRender = font.render("Score: " + str(score), True, red)
        window.blit(scoreRender, (0, 0))
        P1.update()
        P1.draw(window)
        fuell = fuellHeight(fuell, False)
        pygame.display.update()
        framesPerSec.tick(FPS)

#-----------------------------------------------------------------------
# MENU
#-----------------------------------------------------------------------


font = pygame_menu.font.FONT_8BIT

myimage = pygame_menu.baseimage.BaseImage(
    image_path=("data/scaledMenu.png"),
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY
)

mytheme = pygame_menu.themes.THEME_DARK.copy()
mytheme.widget_font = font
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
mytheme.widget_alignment = pygame_menu.locals.ALIGN_CENTER
mytheme.background_color = myimage



def mainMenu():
    menu = pygame_menu.Menu(750, 700, 'Welcome',
                            theme=mytheme)
    menu.add.button('Play', start_the_game)
    menu.add.text_input('Name ', default='Player 1')
    menu.add.selector('Difficulty ', [('Hard', 1), ('Medium', 2), ('Easy', 3)], onchange=set_difficulty)
    menu.add.button('How to play', howToPlay)
    menu.add.button('High scores', highScores)
    menu.add.button('Autors', about)
    menu.add.button('Quit', pygame_menu.events.EXIT)

    menu.mainloop(window)

def howToPlay():
    menu = pygame_menu.Menu(750, 700, 'How to play',
                            theme=mytheme)
    description= 'Collect coins\navoid obstacles\n'\
                'Press LEFT RIGHT to move your car\n'\
                'Remember about fuell'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Back', mainMenu)
    menu.mainloop(window)

def highScores():
    menu = pygame_menu.Menu(750, 700, 'High Scores',
                            theme=mytheme)
    description= 'Collect coins\navoid obstacles\n'\
                'Press LEFT RIGHT to move your car\n'\
                'Remember about fuell'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Back', mainMenu)
    menu.mainloop(window)

def about():
    menu = pygame_menu.Menu(750, 700, 'Autors',
                            theme=mytheme)
    description= 'Kamil Kowalski \n Matematyka stosowana I rok\n Programowanie'

    menu.add.label(description, max_char=-1, font_size=20)
    menu.add.button('Back', mainMenu)
    menu.mainloop(window)

mainMenu()