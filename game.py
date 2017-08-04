import pygame
import time
import random

pygame.init()

music = "music/bg.mp3"
ate = "music/ate.mp3"
pygame.mixer.init()
pygame.mixer.music.load(music)
pygame.mixer.music.play(-1)

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,155,0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snakes')

icon = pygame.image.load('images/icon.ico')
pygame.display.set_icon(icon)

block_size = 10
fps = 10
AppleThickness = 30

smallfont = pygame.font.SysFont("Calibri",25)
mediumfont = pygame.font.SysFont("Calibri",35)
bigfont = pygame.font.SysFont("Calibri",55)

img = pygame.image.load('images/head.png')
backgroundImage = pygame.image.load('images/bg.jpg')
appleimg = pygame.image.load('images/apple.png')

clock = pygame.time.Clock()

latestDirection = '';
score = 0

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        gameDisplay.blit(backgroundImage, (0, 0))
        message_to_screen("Paused",red,-100,size="big")
        message_to_screen("Press C to continue or Q to quit",black,10)
        pygame.display.update()
        clock.tick(5)

def getScore(score=0):
    text = smallfont.render("Score: "+str(score),True,black)
    gameDisplay.blit(text,[0,0])
    pygame.display.update()


def randAppleGen():
    randAppleX = round(random.randrange(0,display_width-AppleThickness))
    randAppleY = round(random.randrange(0,display_height-AppleThickness))
    return randAppleX,randAppleY

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                if event.key == pygame.K_p:
                    intro = False

        gameDisplay.blit(backgroundImage, (0, 0))
        message_to_screen("SNAKES",green,-100,size="big")
        message_to_screen("Press P to play or Q to Quit",black,10,size="medium")

        pygame.display.update()
        clock.tick(115)

def snake(block_size,snakelist):
    head = pygame.transform.rotate(img,270)
    if latestDirection is 'RIGHT':
        head = pygame.transform.rotate(img,270)
    if latestDirection is 'LEFT':
        head = pygame.transform.rotate(img,90)
    if latestDirection is 'UP':
        head = pygame.transform.rotate(img,0)
    if latestDirection is 'DOWN':
        head = pygame.transform.rotate(img,180)

    gameDisplay.blit(head,(snakelist[-1][0],snakelist[-1][1]))

    for XnY in snakelist[:-1]:
        pygame.draw.rect(gameDisplay,black,[XnY[0],XnY[1],block_size,block_size])

def text_objects(text,color,size):
    if size is "small":
        font = smallfont
    if size is "medium":
        font = mediumfont
    if size is "big":
        font = bigfont
    textSurface = font.render(text,True,color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color,y_displace=0,size="medium"):
    textSurf,textRect = text_objects(msg,color,size)
    # screen_text = font.render(msg,True,color)
    # gameDisplay.blit(screen_text,[display_width/3,display_height/2])
    textRect.center = (display_width/2),(display_height/2)+y_displace
    gameDisplay.blit(textSurf,textRect)

def gameLoop():
    global latestDirection
    global score
    gameExit = False
    gameOver = False
    lead_x = display_width/2
    lead_y = display_height/2
    lead_x_change = 10
    lead_y_change = 0

    snakeList = []
    snakeLength = 3

    randAppleX,randAppleY = randAppleGen()


    while not gameExit:
        while gameOver == True:
            gameDisplay.blit(backgroundImage, (0, 0))
            message_to_screen("Game Over!",red,-50,"big")
            message_to_screen(" Press C to play again or Q to quit",black,50)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
                    gameOver = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if latestDirection is not 'RIGHT':
                        lead_x_change = -block_size
                        lead_y_change = 0
                        latestDirection = 'LEFT'
                elif event.key == pygame.K_RIGHT:
                    if latestDirection is not 'LEFT':
                        lead_x_change = block_size
                        lead_y_change = 0
                        latestDirection = 'RIGHT'
                elif event.key == pygame.K_UP:
                    if latestDirection is not 'DOWN':
                        lead_y_change = -block_size
                        lead_x_change = 0
                        latestDirection = 'UP'

                elif event.key == pygame.K_DOWN:
                    if latestDirection is not 'UP':
                        lead_y_change = block_size
                        lead_x_change = 0
                        latestDirection = 'DOWN'

                elif event.key == pygame.K_p:
                    pause()

        if lead_x >= display_width or lead_x < 0 or lead_y >= display_height or lead_y < 0:
            gameOver = True

        lead_x += lead_x_change
        lead_y += lead_y_change



        gameDisplay.blit(backgroundImage, (0, 0))

        # pygame.draw.rect(gameDisplay,red,[randAppleX,randAppleY,AppleThickness,AppleThickness])
        gameDisplay.blit(appleimg,(randAppleX,randAppleY))

        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)

        if len(snakeList) > snakeLength:
            del snakeList[0]

        for eachSegment in snakeList[:-1]:
            if eachSegment == snakeHead:
                gameOver = True

        snake(block_size,snakeList)

        getScore(score)
        # gameDisplay.fill(red,rect=[lead_x,lead_y,50,50])
        pygame.display.update()
        # if lead_x >= randAppleX and lead_x <= randAppleX+AppleThickness:
        #     if lead_y >= randAppleY and lead_y <= randAppleY+AppleThickness:
        #         randAppleX = round(random.randrange(0,display_width-block_size))#/10.0) * 10.0
        #         randAppleY = round(random.randrange(0,display_height-block_size))#/10.0) * 10.0
        #         snakeLength += 5

        if lead_x >= randAppleX and lead_x <= randAppleX+AppleThickness or lead_x + block_size > randAppleX and lead_x + block_size < randAppleX + AppleThickness:

            if lead_y >= randAppleY and lead_y <= randAppleY+AppleThickness :
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 5
                effect = pygame.mixer.Sound(ate)
                effect.play()
                score += 1
            elif lead_y + block_size > randAppleY and lead_y + block_size < randAppleY + AppleThickness:
                randAppleX,randAppleY = randAppleGen()
                snakeLength += 5
                effect = pygame.mixer.Sound(ate)
                effect.play()
                score += 1


        clock.tick(fps)

    pygame.quit()
    quit()

game_intro()
gameLoop()
