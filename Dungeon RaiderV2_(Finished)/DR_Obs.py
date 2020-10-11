#for classes
import pygame
import random
import DR_Funcs
import math

class Player:
#this is the player character

    #contrsuctor
    def __init__(self,X,Y):
        self.speed=6
        self.playerImg=pygame.image.load('idle_1.png')
        self.moving_left=False
        self.moving_right=False
        self.moving_up=False
        self.moving_down=False
        self.player_rect= pygame.Rect(X,Y,22,22)
        self.Player_Hit=0
        self.Player_hit_timer=0

        pass

    def render(self,screen,x,y,anim_clock):

        if self.moving_left==False and self.moving_right==False and self.moving_up==False and self.moving_down==False:
            if anim_clock<=3:
                self.playerImg=pygame.image.load('idle_1.png')
            elif anim_clock<= 6:
                self.playerImg=pygame.image.load('idle_2.png')
            elif anim_clock<=9:
                self.playerImg=pygame.image.load('idle_3.png')
            elif anim_clock<=12:
                self.playerImg=pygame.image.load('idle_4.png')

        else:
            if anim_clock<=3:
                self.playerImg=pygame.image.load('walk_1.png')
            elif anim_clock<= 6:
                self.playerImg=pygame.image.load('walk_2.png')
            elif anim_clock<=9:
                self.playerImg=pygame.image.load('walk_3.png')


        if self.Player_Hit==1:
            if int(self.Player_hit_timer%2)==0:
                screen.blit(self.playerImg, (x,y))
        else:
            screen.blit(self.playerImg, (x,y))



    def move(self,k,tiles,screen,anim_clock):
        if k[1]==1:
            self.player_rect.x-=self.speed
            self.moving_left=True
        else:
            self.moving_left=False

        if k[3]==1:
            self.player_rect.x+=self.speed
            self.moving_right=True
        else:
            self.moving_right=False

        hit_list = DR_Funcs.collision_test(self.player_rect,tiles)
        for tile in hit_list:
            if self.moving_right== True:
                self.player_rect.right = tile.left

            elif self.moving_left==True:
                self.player_rect.left = tile.right


        if k[0]==1:
            self.player_rect.y-=self.speed
            self.moving_up=True
        else:
            self.moving_up=False
        if k[2]==1:
            self.player_rect.y+=self.speed
            self.moving_down=True
        else:
            self.moving_down=False

        hit_list = DR_Funcs.collision_test(self.player_rect,tiles)
        for tile in hit_list:
            if self.moving_down==True:
                self.player_rect.bottom = tile.top

            elif self.moving_up==True:
                self.player_rect.top = tile.bottom

        self.render(screen,self.player_rect.x,self.player_rect.y,anim_clock)
        return

class Coin():

    def __init__(self,X,Y):
        self.PosX=X
        self.PosY=Y
        self.CoinImg=pygame.image.load('coin.png')
        self.coin_rect= pygame.Rect(X,Y,16,16)
        pass

    def render(self,screen):
        screen.blit(self.CoinImg, (self.PosX,self.PosY))
        pass

    def SoundFX(self):
        ding=pygame.mixer.Sound('Pickup_Coin.wav')
        ding.play()
        pass


class tile():
    tiles=['floor_tile.png','box_front.png','box_front.png','box_front.png','box_front.png','box_front.png','Ghost_Spawn.png']

    def __init__(self,tile,X,Y):
        self.WallImg=pygame.image.load(self.tiles[tile])
        self.X=X
        self.Y=Y

    def render(self,screen):

        screen.blit(self.WallImg, (self.X,self.Y))
        pass

class ghost():

    def __init__(self,X,Y):
        self.speed=4
        self.ghost_HB= pygame.Rect(X,Y,25,25)
        self.sprite=pygame.image.load('ghost.png')
        self.direction='up'
        self.last_legal=['']
        self.float_timer=0
        pass


    def render(self,screen):
        screen.blit(self.sprite, (self.ghost_HB.x,self.ghost_HB.y+5*math.sin(self.float_timer)))
        #print(math.sin(self.ghost_HB.y))
        pass

    def move(self,tile_set):
        legal_moves = DR_Funcs.collision_ghost(self.ghost_HB,tile_set)
        new=len(legal_moves)
        old=len(self.last_legal)
        FIDDY=[0,1]
        if legal_moves.count(self.direction)==0:
            self.direction=random.choice(legal_moves)

        elif old!=new:
            half=random.choice(FIDDY)
            if half==1:
                self.direction=random.choice(legal_moves)

        if self.direction=='right':
            self.ghost_HB.x+=self.speed
        if self.direction=='left':
            self.ghost_HB.x-=self.speed
        if self.direction=='up':
            self.ghost_HB.y-=self.speed
        if self.direction=='down':
            self.ghost_HB.y+=self.speed


        self.last_legal=legal_moves
        pass


    pass

class heart():

    def __init__(self,X,Y):
        self.heartX=X
        self.heartY=Y
        self.heartIMG= pygame.image.load('full_heart.png')
        self.full=1

    def render(self,display):
        display.blit(self.heartIMG,(self.heartX,self.heartY))
        if self.full==0:
            self.heartIMG=pygame.image.load('empty_heart.png')
            display.blit(self.heartIMG,(self.heartX,self.heartY))
        #yeet
