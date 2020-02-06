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

#compass
def draw_player_compass(surf, x, y, xT, yT):
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

    #to draw text
    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        snd_folder = path.join(game_folder, 'snd')
        map_folder = path.join(game_folder, 'maps')
        music_folder = path.join(game_folder, 'music')
        self.map = TiledMap(path.join(map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.item_img = pg.image.load(path.join(img_folder, ITEM_IMG)).convert_alpha()
        self.menu_img = pg.image.load(path.join(img_folder, MENU_IMG)).convert_alpha()
        self.go_img = pg.image.load(path.join(img_folder, GAMEOVER_IMG)).convert_alpha()
        self.hud_font = path.join(img_folder, 'OLD.ttf')
        self.credits_img = pg.image.load(path.join(img_folder, CREDIT_IMG)).convert_alpha()
        #Sounds
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))

        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
             self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            if tile_object.name == 'mob':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'treasure':
                self.treasure = Item(self, obj_center)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.paused = False
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0  # fix for Python 2.x
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        #game over ?
        if self.player.health <= 0:
            pg.mixer.music.stop()
            self.playing = False
            #self.effects_sounds['gameover'].play()
        # player hits item (lol)
        if collide_hit_rect(self.player,self.treasure):
            self.effects_sounds['treasure'].play()
            numTresor = random.randint(0,20)
            if numTresor == 0:
                xTresor = 500
                yTresor = 500
            elif numTresor == 1:
                xTresor = 607
                yTresor = 2975
            elif numTresor == 2:
                xTresor = 114
                yTresor = 2573
            elif numTresor == 3:
                xTresor = 327
                yTresor = 1997
            elif numTresor == 4:
                xTresor = 213
                yTresor = 1487
            elif numTresor == 5:
                xTresor = 259
                yTresor = 891
            elif numTresor == 6:
                xTresor = 1198
                yTresor = 735
            elif numTresor == 7:
                xTresor = 970
                yTresor = 940
            elif numTresor == 8:
                xTresor = 1461
                yTresor = 1246
            elif numTresor == 9:
                xTresor = 1186
                yTresor = 1648
            elif numTresor == 10:
                xTresor = 708
                yTresor = 1797
            elif numTresor == 11:
                xTresor = 1221
                yTresor = 2476
            elif numTresor == 12:
                xTresor = 2001
                yTresor = 2173
            elif numTresor == 13:
                xTresor = 2587
                yTresor = 1655
            elif numTresor == 14:
                xTresor = 3043
                yTresor = 1263
            elif numTresor == 15:
                xTresor = 2345
                yTresor = 714
            elif numTresor == 16:
                xTresor = 2277
                yTresor = 2408
            elif numTresor == 17:
                xTresor = 3046
                yTresor = 2797
            elif numTresor == 18:
                xTresor = 1748
                yTresor = 1592
            elif numTresor == 19:
                xTresor = 2400
                yTresor = 1344
            elif numTresor == 20:
                xTresor = 2495
                yTresor = 750
            self.player.score += 1
            self.treasure.rect.center = vec(xTresor,yTresor)

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            hit.vel = vec(0, 0)
        if hits:
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
            self.effects_sounds['sharkbite'].set_volume(0.1)
            self.effects_sounds['sharkbite'].play()

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

        # all mobs dead
        if not self.mobs:
            for tile_object in self.map.tmxdata.objects:
                obj_center = vec(tile_object.x + tile_object.width / 2, tile_object.y + tile_object.height / 2)
                if tile_object.name == 'mob':
                    Mob(self, obj_center.x, obj_center.y)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, RED, self.camera.apply_rect(wall.rect), 1)

        # HUD functions
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
        draw_player_compass(self.screen, self.player.pos.x, self.player.pos.y, self.treasure.rect.center[0],self.treasure.rect.center[1])
        self.draw_text('Score : {}'.format(self.player.score), self.hud_font, 30,  WHITE, WIDTH-10, 10, align="ne")

        if self.paused:
            self.draw_text("PAUSED", self.hud_font, 105, BLACK, WIDTH/2, HEIGHT/2, align="center")
        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.paused = not self.paused
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                    print(self.player.pos.x)
                    print(self.player.pos.y)

    def show_start_screen(self):
        self.screen.blit(self.menu_img, (0,0))
        pg.display.flip()
        self.wait_for_click()
        pg.mixer.music.set_volume(0.8)
        pg.mixer.music.play(loops =-1)
    def show_go_screen(self):
        self.screen.blit(self.go_img, (0,0))
        self.draw_text('{}'.format(self.player.score), self.hud_font, 100, RED, WIDTH/2, HEIGHT/ 2, align="center")
        #self.draw_text("Press a key to start", self.hud_font, 75, WHITE,
                       #WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def wait_for_click(self):
        pg.event.wait()
        waiting = True
        while waiting:
            posit = pg.mouse.get_pos()
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if(((296 <= posit[0]) and (posit[0] <= 723)) and ((207<=posit[1]) and (posit[1]<=277))):
                    pg.draw.rect(self.screen, (255,0,0), (296, 207, 427, 70), 2)
                    pg.display.flip()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        waiting = False
                elif(((296 <= posit[0]) and (posit[0] <= 723)) and ((342<=posit[1]) and (posit[1]<=412))):
                    pg.draw.rect(self.screen, (255,0,0), (296, 342, 427, 70), 2)
                    pg.display.flip()
                    #if event.type == pg.MOUSEBUTTONDOWN:
                        #règles du jeu
                elif(((294 <= posit[0]) and (posit[0] <= 721)) and ((478<=posit[1]) and (posit[1]<=548))):
                    pg.draw.rect(self.screen, (255,0,0), (294, 478, 427, 70), 2)
                    pg.display.flip()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        self.show_credit_screen()
                elif(((293 <= posit[0]) and (posit[0] <= 720)) and ((615<=posit[1]) and (posit[1]<=685))):
                    pg.draw.rect(self.screen, (255,0,0), (293, 615, 427, 70), 2)
                    pg.display.flip()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        waiting = False
                        self.quit()
                else:
                    pg.draw.rect(self.screen, (255,255,255), (296, 207, 427, 70), 2)
                    pg.draw.rect(self.screen, (255,255,255), (296, 342, 427, 70), 2)
                    pg.draw.rect(self.screen, (255,255,255), (294, 478, 427, 70), 2)
                    pg.draw.rect(self.screen, (255,255,255), (293, 615, 427, 70), 2)
                    pg.display.flip()
                    if event.type == pg.MOUSEBUTTONDOWN:
                        print(posit[0])
                        print(posit[1])

    def show_credit_screen(self):
        self.screen.blit(self.credits_img, (0,0))
        pg.display.flip()
        self.wait_for_key()
        self.show_start_screen()
# create the game object
g = Game()
while True:
    g.new()
    g.show_start_screen()
    g.run()
    g.show_go_screen()
