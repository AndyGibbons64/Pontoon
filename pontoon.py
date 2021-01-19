import pygame
import time
import random
 
pygame.init()
 
display_width = 1200
display_height = 800
 
black = (0,0,0)
white = (255,255,255)
bright_red = (255,0,0)
red = (200, 0, 0)
bright_green = (0, 255, 0)
green = (0, 200, 0)
bg_colour = (0,120,0)
 
block_color = (53,115,255)

hand = [None, None, None, None, None]
dealer = [None, None, None, None, None]

in_game = False
player_stuck = False
player_total = 0
dealer_total = 0
player_bust = False
dealer_bust = False

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Pontoon by Andy G')
clock = pygame.time.Clock()

deck=[(1,'images/ace_of_clubs.png'), (1,'images/ace_of_hearts.png'), (1,'images/ace_of_spades.png'), (1,'images/ace_of_diamonds.png'),
      (2,'images/2_of_clubs.png'), (2,'images/2_of_hearts.png'), (2,'images/2_of_spades.png'), (2,'images/2_of_diamonds.png'),
      (3,'images/3_of_clubs.png'), (3,'images/3_of_hearts.png'), (3,'images/3_of_spades.png'), (3,'images/3_of_diamonds.png'),
	  (4,'images/4_of_clubs.png'), (4,'images/4_of_hearts.png'), (4,'images/4_of_spades.png'), (4,'images/4_of_diamonds.png'),
	  (5,'images/5_of_clubs.png'), (5,'images/5_of_hearts.png'), (5,'images/5_of_spades.png'), (5,'images/5_of_diamonds.png'),
	  (6,'images/6_of_clubs.png'), (6,'images/6_of_hearts.png'), (6,'images/6_of_spades.png'), (6,'images/6_of_diamonds.png'),
	  (7,'images/7_of_clubs.png'), (7,'images/7_of_hearts.png'), (7,'images/7_of_spades.png'), (7,'images/7_of_diamonds.png'),
	  (8,'images/8_of_clubs.png'), (8,'images/8_of_hearts.png'), (8,'images/8_of_spades.png'), (8,'images/8_of_diamonds.png'),
	  (9,'images/9_of_clubs.png'), (9,'images/9_of_hearts.png'), (9,'images/9_of_spades.png'), (9,'images/9_of_diamonds.png'),
	  (10,'images/10_of_clubs.png'), (10,'images/10_of_hearts.png'), (10,'images/10_of_spades.png'), (10,'images/10_of_diamonds.png'),
      (10,'images/jack_of_clubs.png'), (10,'images/jack_of_hearts.png'), (10,'images/jack_of_spades.png'), (10,'images/jack_of_diamonds.png'),
      (10,'images/queen_of_clubs.png'), (10,'images/queen_of_hearts.png'), (10,'images/queen_of_spades.png'), (10,'images/queen_of_diamonds.png'),
      (10,'images/king_of_clubs.png'), (10,'images/king_of_hearts.png'), (10,'images/king_of_spades.png'), (10,'images/king_of_diamonds.png')]

current_deck = deck.copy()

def deal():

    #only deal if not already in a game and player has not stuck
    global in_game
    global player_stuck

    if in_game != True and player_stuck != True:	
        #generate a random number to select next card
        next_card = random.randrange(0, len(current_deck))
        #first card for player
        card_image = current_deck[next_card]
        image = pygame.image.load(card_image[1])
        image = pygame.transform.scale(image, (100, 150))
        hand[0] = image
        current_deck.pop(next_card)
        #first card for dealer
        card_image = current_deck[next_card]
        image = pygame.image.load(card_image[1])
        image = pygame.transform.scale(image, (100, 150))
        dealer[0] = image
        current_deck.pop(next_card)
        #second card for player
        next_card = random.randrange(0, len(current_deck))
        card_image = current_deck[next_card]
        image = pygame.image.load(card_image[1])
        image = pygame.transform.scale(image, (100, 150))
        hand[1] = image
        current_deck.pop(next_card)
        in_game = True
        print(len(current_deck))

def twist():

    #only twist if in a game
    global in_game
    global player_stuck

    if in_game == True and player_stuck != True:
        i=0
        while i < 5:
            if hand[i] == None:
                next_card = random.randrange(0, len(current_deck))
                card_image = current_deck[next_card]
                image = pygame.image.load(card_image[1])
                image = pygame.transform.scale(image, (100, 150))
                hand[i] = image
                current_deck.pop(next_card)
                break
            i+=1	
        print(len(current_deck))

def stick():

    #only stick if in a game
    global in_game
    global player_stuck

    if in_game == True:
        player_stuck = True
        i=0
        while i < 5:
            if dealer[i] == None:
                next_card = random.randrange(0, len(current_deck))
                card_image = current_deck[next_card]
                image = pygame.image.load(card_image[1])
                image = pygame.transform.scale(image, (100, 150))
                dealer[i] = image
                current_deck.pop(next_card)
                break
            i+=1	
        print(len(current_deck))
        dealerBust()
        playerBust()

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()
 
def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
 
    game_loop()
    
def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    #print(click)
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            #print(action)
            action()    
            pygame.event.wait(pygame.MOUSEBUTTONUP)    
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))
        
    smallText = pygame.font.SysFont("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)
 
def playerBust():
    global player_bust

    mediumText = pygame.font.SysFont("freesansbold.ttf",70)
    textSurf, textRect = text_objects("You bust!", mediumText)
    textRect.center = (600,480)
    gameDisplay.blit(textSurf, textRect)
    player_bust = True

def dealerBust():
    global dealer_bust
    
    mediumText = pygame.font.SysFont("freesansbold.ttf",70)
    textSurf, textRect = text_objects("Dealer bust!", mediumText)
    textRect.center = (600,50)
    gameDisplay.blit(textSurf, textRect)
    dealer_bust = True

def playerWon():
    global player_won

    mediumText = pygame.font.SysFont("freesansbold.ttf",70)
    textSurf, textRect = text_objects("You Won!", mediumText)
    textRect.center = (600,480)
    gameDisplay.blit(textSurf, textRect)
    player_won = True

def dealerWon():
    global dealer_won
    
    mediumText = pygame.font.SysFont("freesansbold.ttf",70)
    textSurf, textRect = text_objects("Dealer Won!", mediumText)
    textRect.center = (600,50)
    gameDisplay.blit(textSurf, textRect)
    dealer_won = True

def quitgame ():
    pygame.quit()
    quit()    

def game_loop():

    gameExit = False
 
    while not gameExit:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(bg_colour)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects("Pontoon!", largeText)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        mediumText = pygame.font.Font('freesansbold.ttf',70)
        TextSurf, TextRect = text_objects("Dealer", mediumText)
        TextRect.center = (180,200)
        gameDisplay.blit(TextSurf, TextRect)        

        TextSurf, TextRect = text_objects("You", mediumText)
        TextRect.center = (220,600)
        gameDisplay.blit(TextSurf, TextRect)

        button("Deal",430,750,50,25,green,bright_green,deal)
        button("Twist",530,750,50,25,green,bright_green,twist) 
        button("Stick",630,750,50,25,green,bright_green,stick)
        button("Quit",730,750,50,25,green,bright_green,quitgame)

        playerWon()
        dealerBust()

        index = 0
        card_x = [330, 440, 550, 660, 770]
        for x in hand:
            if x != None:
                rect = x.get_rect()
                rect.x = card_x[index]
                rect.y = 550
                gameDisplay.blit(x, rect)
                index += 1
        index = 0
        card_x = [330, 440, 550, 660, 770]
        for x in dealer:
            if x != None:
                rect = x.get_rect()
                rect.x = card_x[index]
                rect.y = 100
                gameDisplay.blit(x, rect)
                index += 1
        pygame.display.update()

game_loop()
pygame.quit()
quit()