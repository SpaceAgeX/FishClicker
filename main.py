import pygame
import random
import text
import button
import factoryManager
import animSprite
import upgrades
import effects
from pygame.locals import *

 
pygame.init()

#Set Pygame Variables
WIDTH = 1100
HEIGHT = 700
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

#Effects
ClickEffectImage = pygame.image.load('Assets/ClickEffect.png').convert_alpha()

decorations = [None, PalmTreeImage, RockImage]
decorationOffsets = [0, 48, 24]


#Factories
FishingRodImage = pygame.image.load('Assets/Rod.png').convert_alpha()
FishingNetImage = pygame.image.load('Assets/Net.png').convert_alpha()
FishingBoatImage = pygame.image.load('Assets/Boat.png').convert_alpha()

factories = [None, FishingRodImage, FishingNetImage, FishingBoatImage]
factoryOffsets = [(0,0), (57, 66), (36, 36), (0, 30)]

#Buttons
RodButtonImage = pygame.image.load('Assets/RodButton.png').convert()
NetButtonImage = pygame.image.load('Assets/NetButton.png').convert()
BoatButtonImage = pygame.image.load('Assets/BoatButton.png').convert()

#Upgrade Buttons 
ClickUpgradeImage = pygame.image.load('Assets/ClickX2Button.png').convert()
RodUpgradeImage = pygame.image.load('Assets/RodX2Button.png').convert()
NetUpgradeImage = pygame.image.load('Assets/NetX2Button.png').convert()
BoatUpgradeImage = pygame.image.load('Assets/BoatX2Button.png').convert()
UpgradeLockImage = pygame.image.load('Assets/Lock.png').convert()


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
            if row_nb == 7:
                Map.factories[row_nb].append(factory)
            else:
                Map.factories[row_nb].append(0)

            map_data[row_nb].append(map_data[row_nb][0])



#Main Fuction
def main():


    running = True
    

    # Game View Port
    clickRect = Rect(190, 80, WIDTH-400, HEIGHT-200)

    #UI Rects
    UIRectL = Rect(0, 0, 190, HEIGHT-120)
    UIRectT = Rect(0, 0, WIDTH, 80)
    UIRectR = Rect(WIDTH-210, 0, 210, HEIGHT-120)
    UIRectB = Rect(0, HEIGHT-120, WIDTH, 120)

    # Init Map
    Map.updateMap((0,0))


    # Game Variables 
    clicks = 0
    cameraPos = (0,0)


     #Factory Managers
    fishingClicks = factoryManager.Factory(0, 1, 10, False)
    fishingRods = factoryManager.Factory(0, 1, 10)
    fishingNets = factoryManager.Factory(0, 10, 100)
    fishingBoats = factoryManager.Factory(0, 100, 1000)
    factoryManagers = [fishingClicks, fishingRods, fishingNets, fishingBoats]

    # UI Init
    fpsDisplay = text.Text((255, 255, 255), (0,0))
    ClickDisplay = text.Text((255, 255, 255), (WIDTH,0))
    FishPerSecondDisplay = text.Text((255, 255, 255), (WIDTH, 0))


    ClicksDisplay = text.Text((255,255,255), (WIDTH/2, 0), 20)

    RodButton = button.Button(WIDTH - (RodButtonImage.get_width()) - 140, 100, RodButtonImage, 1.2, text.ToolTip(RodButtonImage.get_rect, (150, 75), (47, 77, 47), "This is a Tool Tip"), fishingRods)
    RodPriceDisplay = text.Text((255,255,255), (WIDTH, 0), 20)
    NetButton = button.Button(WIDTH - (NetButtonImage.get_width()) - 140, RodButton.rect.topleft[1] + RodButtonImage.get_height() + 40, NetButtonImage, 1.2, text.ToolTip(RodButtonImage.get_rect, (150, 75),  (47, 77, 47), "This is a Tool Tip"), fishingNets)
    NetPriceDisplay = text.Text((255,255,255), (WIDTH, 0), 20)
    BoatButton = button.Button(WIDTH - (BoatButtonImage.get_width()) - 140, NetButton.rect.topleft[1] + NetButtonImage.get_height() + 40, BoatButtonImage, 1.2, text.ToolTip(RodButtonImage.get_rect, (150, 75),  (47, 77, 47), "This is a Tool Tip"), fishingBoats)
    BoatPriceDisplay = text.Text((255,255,255), (WIDTH, 0), 20)

   



    #Upgrades Init
    upgradesUI = upgrades.Upgrades((27, 80), (3, 3), [ClickUpgradeImage, RodUpgradeImage, NetUpgradeImage, BoatUpgradeImage])
    upgradesLock = upgrades.Lock(UpgradeLockImage)

    currentUpgrades = (False, 0, 0)
    while running:

        clock.tick(60)
        surface.fill((0,0,0))

        Map.updateMap(cameraPos)
        effects.Click.draw(surface, pygame.mouse.get_pos(), ClickEffectImage)

        #Draw Frame
        pygame.draw.rect(surface, (20, 35 , 58), clickRect, 5)
        pygame.draw.rect(surface, (0, 0, 0), UIRectL)
        pygame.draw.rect(surface, (0, 0, 0), UIRectT)
        pygame.draw.rect(surface, (0, 0, 0), UIRectR)
        pygame.draw.rect(surface, (0, 0, 0), UIRectB)

        #UI
        fpsDisplay.renderText(str(int(clock.get_fps())),surface, (0,0))
        ClickDisplay.renderText(str(int(clicks))+" Fish Caught", surface, (WIDTH - ClickDisplay.text.get_width()- 5, 0))
        FishPerSecondDisplay.renderText(str(int((fishingRods.rate*fishingRods.count)+(fishingNets.rate*fishingNets.count) + (fishingBoats.rate*fishingBoats.count))) + " Fish per second", surface, (WIDTH - FishPerSecondDisplay.text.get_width()- 5,ClickDisplay.text.get_height()+2))
        RodPriceDisplay.renderText(str(fishingRods.price),surface, (WIDTH  - RodPriceDisplay.text.get_width()- 5, RodButton.rect.topleft[1]))
        NetPriceDisplay.renderText(str(fishingNets.price),surface, (WIDTH  - NetPriceDisplay.text.get_width()- 5, NetButton.rect.topleft[1]))
        BoatPriceDisplay.renderText(str(fishingBoats.price),surface, (WIDTH - BoatPriceDisplay.text.get_width() - 5, BoatButton.rect.topleft[1]))
        ClicksDisplay.renderText("Fish Per Click: " + str(int(fishingClicks.rate)),surface, ((WIDTH/2) - ClicksDisplay.text.get_width(), 5))




        #Upgrades 
        
        if not upgradesLock.unlocked:
            

            if int(upgrades.UpgradeData.upgradesUnlock) <= int(clicks):
                if upgradesLock.draw(surface, 0):
                    clicks -= upgrades.UpgradeData.upgradesUnlock
                    upgradesLock.unlocked = True
            else:
                upgradesLock.draw(surface, int(upgrades.UpgradeData.upgradesUnlock - clicks))
            
        else:
            currentUpgrades = currentUpgrades
            if currentUpgrades[0]:
                if clicks >= upgrades.UpgradeData.upgradePriceMult[currentUpgrades[2]]*factoryManagers[currentUpgrades[1]].price:
                    factoryManagers[currentUpgrades[1]].rate *= upgrades.UpgradeData.upgradeValue[currentUpgrades[2]]
                    clicks -= upgrades.UpgradeData.upgradePriceMult[currentUpgrades[2]]*factoryManagers[currentUpgrades[1]].price
                    upgrades.UpgradeData.upgradesUnlock = pow(upgrades.UpgradeData.upgradesUnlock, 1.05)

                    if not factoryManagers[currentUpgrades[1]].duplicable:
                        factoryManagers[currentUpgrades[1]].price *= 2
                    for x in upgrades.UpgradeData.upgradePriceMult:
                        x += 0.5
                    upgradesUI.refresh()
                    upgradesLock.unlocked = False
                    print(upgradesLock.unlocked)
            currentUpgrades = upgradesUI.draw(surface, [fishingClicks.price,fishingRods.price,fishingNets.price,fishingBoats.price])
                
        
            
        
            
        


        
        #Buttons
        if BoatButton.draw(surface, fishingBoats) and clicks >= fishingBoats.price:
            fishingBoats.count += 1
            clicks -= fishingBoats.price
            fishingBoats.price *= 1.15
            fishingBoats.price = int(fishingBoats.price)
            Map.add_column(3)

        if NetButton.draw(surface, fishingNets) and clicks >= fishingNets.price:
            fishingNets.count += 1
            clicks -= fishingNets.price
            fishingNets.price *= 1.15
            fishingNets.price = int(fishingNets.price)
            Map.add_column(2)

        
            

        if RodButton.draw(surface, fishingRods) and clicks >= fishingRods.price:
            fishingRods.count += 1
            clicks -= fishingRods.price
            fishingRods.price *= 1.15
            fishingRods.price = int(fishingRods.price)
            Map.add_column(1)
            
        
            

        clicks += ((fishingRods.rate*fishingRods.count)+(fishingNets.rate*fishingNets.count) + (fishingBoats.rate*fishingBoats.count))/60
        


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
                    effects.Click.add(ClickEffectImage)
                    clicks += 1*fishingClicks.rate
            


    

        #Update Screen
        pygame.display.update()
        

    pygame.quit()


#Initiate the Game
if __name__ == "__main__":
    main()
       