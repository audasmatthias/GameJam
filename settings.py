import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Ile Interdite 2.0"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'tileGreen_39.png'

# Boat/player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 280
PLAYER_ROT_SPEED = 200
PLAYER_IMG = 'boat.png'
PLAYER_HIT_RECT = pg.Rect(20, 0, 65, 65)
BARREL_OFFSET = vec(30, 10)
WALL_DAMAGE = 50
WALL_KNOCKBACK = 160
PLAYER_SCORE = 0
# Gun settings
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 500
BULLET_LIFETIME = 1000
BULLET_RATE = 150
KICKBACK = 200
GUN_SPREAD = 5
BULLET_DAMAGE = 10
BULLET_KNOCKBACK = 100
# Mob settings
MOB_IMG = 'mobrequin.png'
MOB_SPEED = 250
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 20
MOB_KNOCKBACK = 20

MENU_IMG = 'menu.png'
SCORE_IMG = 'score.png'
GAMEOVER_IMG = 'gameover.png'
#Items
ITEM_IMG = 'treasure1.png'
ITEM_HIT_RECT = pg.Rect(0, 0, 30, 30)
