#for functions
import pygame
import DR_Obs
import math
import random


def Map():                           #
    Tile_Set=[  [2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,1],
                [2,0,0,0,0,0,0,0,0,0,5,0,0,0,0,0,0,0,0,0,1],
                [2,0,5,5,0,5,5,5,5,0,5,0,5,5,5,5,0,5,5,0,1],
                [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [2,0,5,5,0,5,5,0,5,5,5,5,5,0,5,5,0,5,5,0,1],
                [2,0,0,0,0,5,5,0,0,0,5,0,0,0,5,5,0,0,0,0,1],
                [2,5,5,5,0,5,5,5,5,0,5,0,5,5,5,5,0,5,5,5,1],
                [2,5,5,5,0,5,5,0,0,0,0,0,0,0,5,5,0,5,5,5,1],
                [2,5,5,5,0,3,3,0,5,5,5,5,5,0,3,3,0,5,5,5,1],
                [2,5,5,5,0,0,0,0,3,3,3,3,3,0,0,0,0,5,5,5,1],
                [3,3,3,3,0,5,5,0,0,0,0,0,0,0,5,5,0,3,3,3,3],    #mid
                [5,0,0,0,0,0,0,0,5,5,0,5,5,0,0,0,0,0,0,0,5],
                [2,5,5,5,0,5,5,0,3,3,3,3,3,0,5,5,0,5,5,5,1],
                [2,5,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,5,1],
                [2,5,5,5,0,5,5,0,5,5,5,5,5,0,5,5,0,5,5,5,1],
                [2,3,5,5,0,0,0,0,0,0,0,0,0,0,0,0,0,5,5,3,1],
                [2,0,3,3,0,5,5,0,5,0,5,0,5,0,5,5,0,3,3,0,1],
                [2,0,0,0,0,5,5,0,0,0,5,0,0,0,5,5,0,0,0,0,1],
                [2,0,5,5,0,3,3,0,5,5,3,5,5,0,3,3,0,5,5,0,1],
                [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3],
                ]

    return Tile_Set


def Map_Gen(Tile_Set):
    Map=[]
    tile_rects=[]
    y=0
    for j in range(21): # number of rows
        row=[]
        x=0
        for i in range(21):#columns in row
            new_tile= DR_Obs.tile(Tile_Set[j][i],x*32,y*32)
            row.append(new_tile)
            if Tile_Set[j][i] != 0:
                tile_rects.append(pygame.Rect(x*32,y*32,32,32))
            x+=1
        y+=1
        Map.append(row)


    return Map , tile_rects


def Render_Map(Map,screen):

    for j in range(21):

        for i in range(21):
            tile=Map[j][i]
            tile.render(screen)

    pass

def collision_playerhit(player_HB,ghost_HB):
    hit=0
    if player_HB.colliderect(ghost_HB):
        hit=1
    return hit


def collision_test(rect,tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def collision_ghost(rect,tiles):
    moves = ['right','left','up','down']

    for tile in tiles:
        rect.x+=5
        if rect.colliderect(tile):
            try:
                moves.remove('right')
            except ValueError:
                pass

        rect.x-=10
        if rect.colliderect(tile):
            try:
                moves.remove('left')
            except ValueError:
                pass

        rect.x+=5

        rect.y+=5
        if rect.colliderect(tile):
            try:
                moves.remove('down')
            except ValueError:
                pass
        rect.y-=10
        if rect.colliderect(tile):
            try:
                moves.remove('up')
            except ValueError:
                pass
        rect.y+=5
    return moves

def collision_test_coins(rect,coins):
    hit_list = []
    for coin in coins:
        if rect.colliderect(coin.coin_rect):
            hit_list.append(coin)
    return hit_list

def load_coins(tile_set):
    y=0
    coins=[]
    for j in range(21): # number of rows
        x=0
        for i in range(21):#columns in row
            if tile_set[j][i] == 0:
                new_coin = DR_Obs.Coin(x*32+8,y*32+8)
                coins.append(new_coin)

            x+=1
        y+=1
    return coins

def render_coins(coins,screen):
    for coin in coins:
        coin.render(screen)
    pass

def grab_coin(player,coins,score,screen):

    hit_list =collision_test_coins(player.player_rect,coins)

    for coin in hit_list:
        coin.SoundFX()

        for coin in coins:

            for dead in hit_list:

                if dead.PosX== coin.PosX and dead.PosY== coin.PosY:
                    coins.remove(coin)
                    score+=1

            pass

    return coins, score

def win(coins,tile_set,player):
    if len(coins)==0:
        coins=load_coins(tile_set)
        player.player_rect.x=336
        player.player_rect.y=336
        return coins
    return coins

def scoring(x,y,font,display,score):
    score_val= font.render("Score: "+str(score),True,(255,255,255))
    display.blit(score_val,(x,y))
    pass

def player_hit(player,ghost,Player_HP,Player_HP_val):
    WasHit= collision_playerhit(player.player_rect,ghost.ghost_HB)

    if WasHit==0:
        return Player_HP_val

    else:
        try:
            Player_HP[Player_HP_val-1].full=0
            Player_HP_val-=1
            player_hit=pygame.mixer.Sound('player_hit.wav')
            player_hit.play()
        except IndexError:
            pass

    return Player_HP_val













#yeet
