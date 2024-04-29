import pygame
import random
import text
import timeWait
import button
import factoryManager
import animSprite
from pygame.locals import *

 
pygame.init()

#Set Pygame Variables
WIDTH = 1000
HEIGHT = 600
surface = pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF)   
pygame.display.set_caption('ISO')
clock = pygame.time.Clock()
 
# Array For Holding Map Data
map_data = [
[0],
[0],
[0],
[0],
[0],
[1],
[2],
[2],
[2],
[2]
]   

#Load Images
 
#Tiles
WaterSync = animSprite.AnimSync(0, 0)
WaterImage = animSprite.AnimSprite(pygame.image.load('Assets/Water.png').convert_alpha(), 1)

SandSync = animSprite.AnimSync(0, 0)
SandImage = animSprite.AnimSprite(pygame.image.load('Assets/Sand.png').convert_alpha(), 1)

WavesSync = animSprite.AnimSync(1, 4)
SandLastImage = animSprite.AnimSprite(pygame.image.load('Assets/SandLast.png').convert_alpha(), 4)

TileSyncs = [SandSync, WavesSync, WaterSync]
tiles = [SandImage, SandLastImage ,WaterImage]

#Decorations
PalmTreeImage = pygame.image.load('Assets/PalmTree.png').convert_alpha()
RockImage = pygame.image.load('Assets/Rock.png').convert_alpha()

decorations = [None, PalmTreeImage, RockImage]
decorationOffsets = [0, 48, 24]


#Factories
FishingRodImage = pygame.image.load('Assets/Rod.png').convert_alpha()
FishingNetImage = pygame.image.load('Assets/Net.png').convert_alpha()

factories = [None, FishingRodImage, FishingNetImage]
factoryOffsets = [(0,0), (25, 50), (4, 20)]

#Buttons
RodButtonImage = pygame.image.load('Assets/RodButton.png').convert()
NetButtonImage = pygame.image.load('Assets/NetButton.png').convert()
 
# Tile Variables
TILEWIDTH = 64  #holds the tile width and height
TILEHEIGHT = 64
TILEHEIGHT_HALF = TILEHEIGHT /2
TILEWIDTH_HALF = TILEWIDTH /2


#Map Class
class Map():

    # Decorations data
    decorations = [
    [random.randint(0,2)],
    [random.randint(0,2)],
    [random.randint(0,2)],
    [random.randint(0,2)],
    [random.randint(0,2)],
    [0],
    [0],
    [0],
    [0],
    [0]
    ]
    #Factory Data
    factories = [
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0],
    [0]
    ]

    #Coordinates To Iso
    def toIso(cart_x, cart_y): 
        iso_x = (cart_x - cart_y) 
        iso_y = (cart_x + cart_y)/2
        return (iso_x, iso_y)

    #Update Fuction Loops Through Array and Places Tiles
    def updateMap(cameraPos):
        #Offsets
        offsetDecorations = 0
        offsetFactories = (0, 0)
        tileFrame = 0
        #For Loop Through Array
        for row_nb, row in enumerate(map_data):
            for col_nb, tile in enumerate(row):
                
                tileImage = tiles[tile]
                tileFrame = TileSyncs[tile]

                #Draw Decorations

                decorationImage = decorations[Map.decorations[row_nb][col_nb]]
                offsetDecorations = decorationOffsets[Map.decorations[row_nb][col_nb]]

                
                #Draw Factories
                
                factoryImage = factories[Map.factories[row_nb][col_nb]]
                offsetFactories = factoryOffsets[Map.factories[row_nb][col_nb]]
                

                #Find Coordinates
                cart_x = row_nb * TILEWIDTH_HALF
                cart_y = col_nb * TILEHEIGHT_HALF  
                #Get Center
                centered_x = (surface.get_rect().centerx-20) + Map.toIso(cart_x, cart_y)[0]
                centered_y = (surface.get_rect().centery-40)/2 + Map.toIso(cart_x, cart_y)[1]

                tileImage.draw((centered_x-cameraPos[0], centered_y-cameraPos[1]), surface, tileFrame.frame)

                # Draw Decorations
                if decorationImage != None:
                    surface.blit(decorationImage, (centered_x-cameraPos[0], centered_y-offsetDecorations-cameraPos[1]))
                if factoryImage != None:
                    surface.blit(factoryImage, (centered_x-offsetFactories[0]-cameraPos[0], centered_y-offsetFactories[1]-cameraPos[1]))

                
                WavesSync.update()

    #Add a new column with a factory
    def add_column(factory):
        #Loop through array
        for row_nb, row in enumerate(map_data):

            #Set Decorations
            if not row_nb > 4:
                Map.decorations[row_nb].append(random.randint(0,2))
            else:
                Map.decorations[row_nb].append(0)

            #Set factories
            if row_nb == 6:
                Map.factories[row_nb].append(factory)
            else:
                Map.factories[row_nb].append(0)

            map_data[row_nb].append(map_data[row_nb][0])



#Main Fuction
def main():


    running = True
    

    # Game View Port
    clickRect = Rect(150, 80, WIDTH-300, HEIGHT-140)

    #UI Rects
    UIRectL = Rect(0, 0, 150, HEIGHT-60)
    UIRectT = Rect(0, 0, WIDTH, 80)
    UIRectR = Rect(WIDTH- 150, 0, 150, HEIGHT-60)
    UIRectB = Rect(0, HEIGHT-60, WIDTH, 60)

    # Init Map
    Map.updateMap((0,0))


    # Game Variables 
    clicks = 1000

    cameraPos = (0,0)


    # UI Init
    fpsDisplay = text.Text((255, 255, 255), (0,0))
    ClickDisplay = text.Text((255, 255, 255), (WIDTH,0))
    FishPerSecondDisplay = text.Text((255, 255, 255), (WIDTH, 0))

    RodButton = button.Button(WIDTH - (RodButtonImage.get_width()*2) - 5, 100, RodButtonImage, 1.2)
    RodPriceDisplay = text.Text((255,255,255), (WIDTH, 0), 20)
    NetButton = button.Button(WIDTH - (NetButtonImage.get_width()*2) - 5,100 + RodButtonImage.get_height() + 40, NetButtonImage, 1.2)
    NetPriceDisplay = text.Text((255,255,255), (WIDTH, 0), 20)

    #Factory Managers
    fishingRods = factoryManager.Factory(0, 1, 10)
    fishingNets = factoryManager.Factory(0, 10, 100)

    #Timer Init
    OneSecWait = timeWait.TimeWait(pygame.time.get_ticks(), 1)

    while running:

        clock.tick(60)
        surface.fill((0,0,0))

        Map.updateMap(cameraPos)

        #Draw Frame
        pygame.draw.rect(surface, (20, 35 , 58), clickRect, 5)
        pygame.draw.rect(surface, (0, 0, 0), UIRectL)
        pygame.draw.rect(surface, (0, 0, 0), UIRectT)
        pygame.draw.rect(surface, (0, 0, 0), UIRectR)
        pygame.draw.rect(surface, (0, 0, 0), UIRectB)

        #UI
        fpsDisplay.renderText(str(int(clock.get_fps())),surface, (0,0))
        ClickDisplay.renderText(str(clicks)+" Fish Caught", surface, (WIDTH  - ClickDisplay.text.get_width()- 5, 0))
        FishPerSecondDisplay.renderText(str((fishingRods.rate*fishingRods.count)+(fishingNets.rate*fishingNets.count)) + " Fish per second", surface, (WIDTH - FishPerSecondDisplay.text.get_width()- 5,ClickDisplay.text.get_height()+2))
        RodPriceDisplay.renderText(str(fishingRods.price),surface, (WIDTH   - RodPriceDisplay.text.get_width()- 5, RodButton.rect.topleft[1]))
        NetPriceDisplay.renderText(str(fishingNets.price),surface, (WIDTH   - NetPriceDisplay.text.get_width()- 5, NetButton.rect.topleft[1]))
        

        
        #Buttons
        if RodButton.draw(surface) and clicks >= fishingRods.price:
            fishingRods.count += 1
            clicks -= fishingRods.price
            fishingRods.price *= 1.125
            fishingRods.price = int(fishingRods.price)
            Map.add_column(1)
            
        if NetButton.draw(surface) and clicks >= fishingNets.price:
            fishingNets.count += 1
            clicks -= fishingNets.price
            fishingNets.price *= 1.125
            fishingNets.price = int(fishingNets.price)
            Map.add_column(2)
            

        #One Sec Update
        if OneSecWait.update(clock):
            clicks += (fishingRods.rate*fishingRods.count)+(fishingNets.rate*fishingNets.count)


        # Get Keys Input
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_UP]:
            cameraPos = (cameraPos[0]+4, cameraPos[1]-2)
        if keys[pygame.K_DOWN]:
            cameraPos = (cameraPos[0]-4, cameraPos[1]+2)   

        # Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and clickRect.collidepoint(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    clicks += 1
            


    

        #Update Screen
        pygame.display.update()
        

    pygame.quit()


#Initiate the Game
if __name__ == "__main__":
    main()
       