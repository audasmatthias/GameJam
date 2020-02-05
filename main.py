import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


def draw_player_compass(surf, x, y, xT, yT):
#    pg.draw.line(surf, (255,0,0),(900,700),(925,725))

    pg.draw.circle(surf, (255,255,255), (900,700), 50, 1)
    pg.draw.circle(surf, (255,255,255), (900,700), 5, 1)


    if(xT >= x+20 and yT >= y+20):
        pg.draw.line(surf, (255,0,0),(900,700),(925,725))
    elif(xT >= x+20 and yT <= y-20):
        pg.draw.line(surf, (255,0,0),(900,700),(925,675))
    elif(xT <= x-20 and yT <= y-20):
        pg.draw.line(surf, (255,0,0),(900,700),(875,675))
    elif(xT <= x-20 and yT >= y+20):
        pg.draw.line(surf, (255,0,0),(900,700),(875,725))
    else:
        if((xT <= x+20 and xT >= x) or (xT >= x-20 and xT < x)):
            if(yT >= y):
                #fleche vers le bas
                pg.draw.line(surf, (255,0,0),(900,700),(900,740))
            else:
                #fleche vers le haut
                pg.draw.line(surf, (255,0,0),(900,700),(900,660))
        elif((yT <= y+20 and yT >= y) or (yT >= y-20 and yT < y)):
            if(xT <= x):
                #vers la droite
                pg.draw.line(surf, (255,0,0),(900,700),(860,700))
            else:
                #vers la gauche
                pg.draw.line(surf, (255,0,0),(900,700),(940,700))
        else:
            pg.draw.line(surf, (255,0,0),(875,675),(925,725))
            pg.draw.line(surf, (255,0,0),(875,725),(925,675))

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'maps')
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        #self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        #self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.item_img = pg.image.load(path.join(img_folder, ITEM_IMAGE)).convert_alpha()

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        self.items = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'treasure':
                Item(self, obj_center)

            #int = random.randint(1,3)
            #if int == 1:
            #    if tile_object.name == 'treasure1':
            #       Item(self, obj_center)
            #if int == 2:
            #   if tile_object.name == 'treasure2':
            #        Item(self, obj_center)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        # player hits item
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            hit.kill()
            self.player.health -= 10
        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            #self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # mobs hits island
        hits = pg.sprite.groupcollide(self.mobs, self.walls, False, False)
        for hit in hits:
            hit.health -= WALL_DAMAGE
            hit.vel = vec(0,0)
            hit.pos -= vec(WALL_KNOCKBACK, 0)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            #hit.health -= BULLET_DAMAGE
            hit.vel = vec(0, 0)
            hit.pos -= vec(BULLET_KNOCKBACK, 0).rotate(-hit.rot)

<<<<<<< HEAD
        if not self.mobs:
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                if tile_object.name == 'mob':
                    Mob(self, obj_center.x, obj_center.y)
=======
>>>>>>> 71d06f6e8b482d3402b7372ece4c98a32e553146
    # def draw_grid(self):
    #    for x in range(0, WIDTH, TILESIZE):
    #        pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
    #    for y in range(0, HEIGHT, TILESIZE):
    #        pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        # self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_compass(self.screen, self.player.pos.x, self.player.pos.y, 500, 500)
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
<<<<<<< HEAD
=======
                if event.key == pg.K_k:
>>>>>>> 71d06f6e8b482d3402b7372ece4c98a32e553146
                    print(self.player.pos.x)
                    print(self.player.pos.y)

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
