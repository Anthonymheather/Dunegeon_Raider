import pygame
import os
import random
import math
import DR_Funcs
import DR_Obs

#initialize pygame modules
pygame.init()
pygame.font.init()

#change directory to find game files
path = os.getcwd()
os.chdir('C:\Python Files\Dungeon RaiderV1')

#initialize screen
display = pygame.display.set_mode((1000,1000)) #width , height
screen = pygame.Surface((672,672)) # used as the rednering surface

#title and icon
pygame.display.set_caption("Dungeon Raider")
#icon = pygame.image.load('ship_one.png')
#pygame.display.set_icon(icon)

#creates a global game clock
clock = pygame.time.Clock()

#create a player character
player=DR_Obs.Player(322,426)
score=0

Font= pygame.font.Font('freesansbold.ttf',32)

#load ghosts------------------------------------------------------
ghosts=[]
for i in range(4):
    ghosts.append(DR_Obs.ghost(320,356))

#Initialize Tile set---------------------------------------------------------------
Tile_Set= DR_Funcs.Map() #loads mapping for how tiles will be organized in game
Map, tile_rects = DR_Funcs.Map_Gen(Tile_Set) #generetes physical tile map by making list of wall objects
#-----------------------------------------------------------------------------
#load coins---------------
coins= DR_Funcs.load_coins(Tile_Set)
anim_clock=0

#initialize player life---------------------------------------------------
Player_HP_val=3
Player_HP=[]
heartX=700
for i in range(Player_HP_val):
    Player_HP.append(DR_Obs.heart(heartX,80))
    heartX+=60
#-------------------------------------------------
running= True
while running:
    #set game fps
    clock.tick(30)

#EVENTS---------------------------------------------------------------------
    #first get any inputs from player
    for event in pygame.event.get():
        #first event is to allow game to be closed
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                #pause game func
                pass
        #store all key states in list
        keys = pygame.key.get_pressed()
        k=[keys[119],keys[97],keys[115],keys[100]]
#---------------------------------------------------------------------------

#SCREEN ART---------------------------------------------------------------------
    screen.fill((0,0,0))
    #screen.blit(background,(50,100))
#------------------------------------------------------------------------------
#render_Map
    DR_Funcs.Render_Map(Map,screen)
#render coins-------------------------
    DR_Funcs.render_coins(coins,screen)
#render ghosts------------------------------
    for ghost in ghosts:
        ghost.render(screen)

#Movments----------------------------------------------------------------------
    player.move(k,tile_rects,screen,anim_clock) #moves player and handles collision
    #enemy move
    for ghost in ghosts:
        ghost.move(tile_rects)
        Player_HP_val=DR_Funcs.player_hit(player,ghost,Player_HP,Player_HP_val)
#Player ghost contact-----------------------------------------------------------------------


#pickup check------------------------------------------------------------------
    coins, score=DR_Funcs.grab_coin(player,coins,score,screen)
    coins=DR_Funcs.win(coins,Tile_Set,player)

    display.fill((0,100,150))

    for heart in Player_HP:
        heart.render(display)

    DR_Funcs.scoring(64,64,Font,display,score)
    display.blit(pygame.transform.scale(screen,(800,800)),(100,125))
    anim_clock+=1
    if anim_clock==13:
        anim_clock=0
    pygame.display.update()
