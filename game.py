import pygame
import sys
import time
import math

pygame.init()







player_speed = 10
#player and enemy and coin classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 25
        self.height = 25
        self.speed = player_speed
        self.image = pygame.image.load(r"images\studenthead.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (50, 50)
        self.imagedown = self.image.copy()
        self.imageup = self.image.copy()
        self.imageup = pygame.transform.rotate(self.imageup, 180)
        self.imageright = self.image.copy()
        self.imageright = pygame.transform.rotate(self.imageright, 90)
        self.imageleft = self.image.copy()
        self.imageleft = pygame.transform.rotate(self.imageleft, -90)
        
    
    def update(self):


        pressed_key = pygame.key.get_pressed()

        next_rect = self.rect.copy()  
        directionx = 0
        directiony = 0
        
        if pressed_key[pygame.K_LEFT]:
            self.image = self.imageleft.copy()
            if self.rect.bottomleft[0] > 0:
                directionx = -1
        if pressed_key[pygame.K_RIGHT]:
            self.image = self.imageright.copy()
            if self.rect.bottomright[0] < width_screen:
                directionx = 1
        if pressed_key[pygame.K_UP]:
            self.image = self.imageup.copy()
            if self.rect.top > 0:
                directiony = -1
        if pressed_key[pygame.K_DOWN]:
            self.image = self.imagedown.copy()
            if self.rect.bottom < height_screen:
                directiony = 1
        
        
        #normalize the diagonal movement
        if directionx != 0 and directiony != 0:
            directionx = round(directionx * (0.5**0.5), 3)
            directiony = round(directiony * (0.5**0.5), 3)

        next_rect1 = next_rect.copy()

        next_rect1.move_ip(directionx*self.speed, directiony*self.speed)
        if next_rect1.collidelist(walls.wall_rect_list) == -1:      
            next_rect.move_ip(directionx*self.speed, directiony*self.speed)
        else:
            directionx /= 2
            directiony /= 2
            next_rect1.move_ip(-directionx*self.speed, -directiony*self.speed)
            if next_rect1.collidelist(walls.wall_rect_list) == -1:      
                next_rect.move_ip(directionx*self.speed, directiony*self.speed)
        
        
        self.rect = next_rect.copy()
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)


    #collision function to detect if player has died or not    
    def collision(self, rect1):
        self.collide = self.rect.colliderect(rect1)
        return self.collide



class Enemy(pygame.sprite.Sprite):
    def __init__(self, type=None, speed=None, color=None, spawnpoint=None):
        super().__init__()
        self.width = 20
        self.height = 20

        if color == None:
            color = (230, 90, 50)
        self.color = color
        if type == None:
            type = 1
        self.type = type
        if speed == None:
            speed = 7
        if spawnpoint == None:
            spawnpoint = (300, 300)
        self.spawnpoint = spawnpoint
        self.speed = speed
        
        self.ogspeed = speed
        self.last_dx = 0
        self.last_dy = 0


        if self.type == 1:
            self.image = pygame.image.load(r"images\teacherhead.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect()
            self.rect.topleft = spawnpoint

        elif self.type == 2:
            self.image = pygame.image.load(r"images\teacher1head.png")
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect()
            self.rect.topleft = spawnpoint
        
        elif self.type == 3:
            self.image = pygame.image.load(r"images\onay.png")
            self.image = pygame.transform.scale(self.image, (round(self.image.get_width()/2), self.image.get_height()/2))
            self.rect = self.image.get_rect()
            self.rect.topleft = spawnpoint

        self.imageog = self.image.copy()
        self.last_position = self.rect.topleft
    
    def update(self, player_rect, walls):
        
        if self.type == 1:
            dx, dy = self.type1(player_rect, walls)
        elif self.type == 2:
            dx, dy = self.type2(player_rect, walls)
        elif self.type == 3:
            dx, dy = self.type3(player_rect, walls)
        
        degree = 0
        if self.type != 3:
            if (dx > 0.5) and dy > 0.5:
                degree = 45
            elif (dx < -0.5) and dy > 0.5:
                degree = -45
            elif (dx < -0.5) and dy > 0.5:
                degree = 90-45
            elif (dx > 0.5) and dy > 0.5:
                degree = 90+45
            elif (dx < -0.5) and dy < -0.5:
                degree = 180+45
            elif (dx > 0.5) and dy < -0.5:
                degree = 180-45

            if (dx < 0.5 and dx > -0.5) and dy < -0.5:
                degree = 180
            elif dx > 0.5 and (dy < 0.5 and dy > -0.5):
                degree = 90
            elif dx < -0.5 and (dy < 0.5 and dy > -0.5):
                degree = -90
            elif (dx > -0.5 and dx < 0.5) and dy > 0.5:
                degree = 0

        self.imagerotated = self.imageog.copy()
        self.imagerotated = pygame.transform.rotate(self.imagerotated, degree)


        self.image = self.imagerotated.copy()
        # Move towards the player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed


        self.last_dx = dx
        self.last_dy = dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def check_player(self, player_rect):
        
        dx = player_rect.centerx - self.rect.centerx
        dy = player_rect.centery - self.rect.centery
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        dx = dx / distance
        dy = dy / distance

        return dx, dy

    #chase player directly
    def type1(self, player_rect, walls):
        dx, dy = self.check_player(player_rect)
        
        # Check for obstacles in the way
        if self.check_obstacle_collision(walls):
            # Rotate vector by 90 degrees to avoid obstacle
            dx, dy = -dy, dx

        return dx, dy

    #walk trhough walls
    def type2(self, player_rect, walls):
        dx, dy = self.check_player(player_rect)

        # Check for obstacles in the way
        if self.check_obstacle_collision(walls):
            # If the enemy is stuck on the left or right side of the wall, allow movement in the vertical direction
            if self.last_dx != 0:
                dy = dy if dy == 0 else dy / abs(dy)
                dx = 0
            # If the enemy is stuck at the top or bottom of the wall, allow movement in the horizontal direction
            elif self.last_dy != 0:
                dx = dx if dx == 0 else dx / abs(dx)
                dy = 0
        
        return dx, dy
    

    #runaway player
    def type3(self, player_rect, walls):
        dx, dy = self.check_player(player_rect)
    
        
        
        # Check all possible directions of movement
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        max_distance = 0
        best_direction = None

        for direction in directions:
            # Calculate the next position
            next_x = self.rect.centerx + direction[0] * self.speed
            next_y = self.rect.centery + direction[1] * self.speed

            # Check if the next position is valid (not colliding with walls)
            next_rect = pygame.Rect(next_x - self.width // 2, next_y - self.height // 2, self.width, self.height)
            if not self.check_obstacle_collision(walls, next_rect):
                # Calculate the distance to the player from the next position
                next_distance = ((next_x - player_rect.centerx) ** 2 + (next_y - player_rect.centery) ** 2) ** 0.5
                # If this direction leads to a farther position from the player, update the best direction
                if next_distance > max_distance and (next_x, next_y) != self.last_position:
                    max_distance = next_distance
                    best_direction = direction

        # Move in the best direction
        if best_direction:
            dx = best_direction[0]
            dy = best_direction[1]
            self.last_position = self.rect.topleft
        
        return dx, dy


    #def type4(self):
    #

    def check_obstacle_collision(self, walls, next_rect=None):
        # Check if the enemy collides with any walls after moving
        if next_rect == None:
            next_rect = self.rect.copy()
        for wall in walls:
            if next_rect.colliderect(wall):
                return True
        return False
    
    def dissapear(self):
        self.rect.move_ip(-2000, -2000)
        self.speed = 0

    def revive(self):
        self.__init__(self.type, self.ogspeed, self.color, self.spawnpoint)


class Walls(pygame.sprite.Sprite):
    def __init__(self, wall_list, rect_list, type=None):
        super().__init__()
        self.wall_rect_list = []
        self.wall_coor_list = []
        #if type == None:
        #    type = "wall"
        #self.type = type
        for wall_coor in wall_list:
            self.wall_coor_list.append(wall_coor)
        for wall_rect in rect_list:
            self.wall_rect_list.append(wall_rect)
    
    def draw(self, surface):
        for wall in self.wall_rect_list:
            pygame.draw.rect(surface, BLACK, wall)
    

#COLORS
BLACK = (30, 30, 30)
BLUE = (50, 30, 240)
RED = (255, 30, 30)
GREEN = (30, 240, 30)


#screen parameters
width_screen = 700
height_screen = 750
screen = pygame.display.set_mode((width_screen, height_screen))
FPS = 30
framespersecond = pygame.time.Clock()
pygame.display.set_caption("Oops There Goes The Retake")

musictrack = "none"

#passed level screen
def levelwin(surface, level):


    surface.fill(GREEN)

    #gameover text in the center
    font = pygame.font.SysFont("centrury", 50)
    text = font.render(" YOU PASSED LEVEL {0} ".format(level), True, BLACK)
    recttext = (surface.get_width()/2-text.get_width()/2, surface.get_height()/2)
    surface.blit(text, recttext)

    pygame.mixer_music.stop()
    pygame.mixer_music.unload()   
    pygame.mixer_music.load(r"music\gamejamwinlvl.mp3") 
    pygame.mixer_music.play(3) 
    musictrack = "win"

    pygame.display.update()
    # Wait for spacebar press to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return True
                
    
#gameover screen
def gameover(surface):


    surface.fill(RED)

    #gameover text in the center
    font = pygame.font.SysFont("centrury", 50)
    text = font.render(" OOPS THERE GOES THE RETAKE ", True, BLACK)
    recttext = (surface.get_width()/2-text.get_width()/2, surface.get_height()/2)
    surface.blit(text, recttext)

    pygame.mixer_music.stop()
    pygame.mixer_music.unload()   
    pygame.mixer_music.load(r"music\gamejamloose.mp3") 
    pygame.mixer_music.play(3) 
    musictrack = "loose"

    pygame.display.update()
    # Wait for spacebar press to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                    return True
                
    
#creating player and enemy
player1 = Player()


enemy1 = Enemy(1, 7, (250, 160, 40), (600, 600))
enemy2 = Enemy(3, 9, (240, 160, 100), (280, 300))
enemy3 = Enemy(2, 4, (255, 50, 20), (50, 500))
enem_list = [enemy1, enemy2, enemy3]
for enem in enem_list:
    enem.__init__(enem.type, enem.speed, enem.color, enem.spawnpoint)

enemy1.dissapear()
enemy2.dissapear()
enemy3.dissapear()

def main_menu(player1, enem_list):

    #background music
    pygame.mixer_music.stop()
    pygame.mixer_music.unload()
    pygame.mixer_music.load(r"music\gamejam1menu.mp3")
    pygame.mixer_music.play(-1)
    musictrack = "menu"
    
    #creating player 
    player1.__init__()
    player1.speed = player_speed


    bg = pygame.image.load(r"images\background1.png")
    bg = pygame.transform.scale(bg, (700, 750))
    
    while True:

        screen.blit(bg, (0,0))

        # Draw menu options

        font = pygame.font.Font(None, 36)
        level1_text = font.render("Level 1", True, (255, 255, 255))
        level2_text = font.render("Level 2", True, (255, 255, 255))
        level3_text = font.render("Level 3", True, (255, 255, 255))

        rect1 = level1_text.get_rect(topleft = (300, 300))
        rect2 = level2_text.get_rect(topleft = (300, 350))
        rect3 = level3_text.get_rect(topleft = (300, 400))
        


        pygame.draw.rect(screen, (50, 20, 50), rect1)
        pygame.draw.rect(screen, (50, 20, 50), rect2)
        pygame.draw.rect(screen, (50, 20, 50), rect3)
        screen.blit(level1_text, rect1.topleft)
        screen.blit(level2_text, rect2.topleft)
        screen.blit(level3_text, rect3.topleft)

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Check if user clicked on any of the level options
                if rect1.collidepoint(event.pos):
                    for i in range(0, 1):
                        enem_list[i].revive()
                    if musictrack == "menu":
                        pygame.mixer_music.stop()
                        pygame.mixer_music.unload
                        pygame.mixer_music.load(r"music\gamejamlvl1.mp3") 
                        pygame.mixer_music.play(-1)
                        musictrack = "lvl1"  
                    
                    return 1
                
                        
                elif rect2.collidepoint(event.pos):
                    for i in range(0, 2):
                        enem_list[i].revive()
                    if musictrack == "menu":
                        pygame.mixer_music.stop()
                        pygame.mixer_music.unload
                        pygame.mixer_music.load(r"music\gamejamlvl2.mp3") 
                        pygame.mixer_music.play(-1)
                        musictrack = "lvl2" 
                    # Start level 2
                    return 2
                elif rect3.collidepoint(event.pos):
                    for i in range(0, 3):
                        enem_list[i].revive()
                    if musictrack == "menu":
                        pygame.mixer_music.stop()
                        pygame.mixer_music.unload
                        pygame.mixer_music.load(r"music\gamejamlvl3.mp3") 
                        pygame.mixer_music.play(-1)
                        musictrack = "lvl3" 
                    # Start level 3
                    return 3

        pygame.display.update()

#drawing counter of coins
def counter(surface, string, pos=None):
    font = pygame.font.SysFont("centrury", 30)
    text = font.render(string, True, BLUE, (255, 255, 255))
    if pos == None:
        pos = (width_screen-text.get_width(), 0)
    recttext = text.get_rect(topleft = pos)
    pygame.draw.rect(surface, (255, 255, 255), recttext, 2)
    surface.blit(text, recttext)

# Initialize game variables and objects

# Start with the main menu
selected_level = main_menu(player1, enem_list)
pygame.mixer_music.set_volume(0.5)





#data (sizes and coordinates) for walls
Kazybekwall1 = [(150, 10), (width_screen-260, 250)]
Kazybekwall2 = [(10, 140), (270, 120)]
Kazybekwall3 = [(150, 10), (120, 250)]
Kazybekwall4 = [(150, 10), (120, 350)]
#Kazybekwall5 = [(170, 20), (270, 350)]
Kazybekwall6 = [(150, 10), (width_screen-260, 350)]
Kazybekwall7 = [(10, 140), (width_screen-270, 120)]
Kazybekwall8 = [(60, 10), (270, 110)]
Kazybekwall9 = [(60, 10), (width_screen-320, 110)]

AbilayWall1 = [(10, 60), (120, 0)]
AbilayWall1_2 = [(10, 140), (120, 110)]
AbilayWall2 = [(10, 300), (120, 350)]

#AbilayWall3 = [(10, 110), (220, 250)]
#AbilayWall4 = [(10, 110), (270, 250)]

PanfilWall1 = [(10, 60), (width_screen-120, 0)]
PanfilWall1_2 = [(10, 140), (width_screen-120, 110)]
PanfilWall2 = [(10, 300), (width_screen-120, 350)]
#PanfilWall3 = [(10, 110), (270+170, 250)]
#PanfilWall4 = [(10, 110), (270+170+50, 250)]

Indphall1 =[(10, 70), (260, 360)]
Indphall2 =[(10, 70), (width_screen-260, 360)]
Indphall3 =[(10, 70), (260, 580)]
Indphall4 =[(10, 70), (width_screen-260, 580)]
Indphall5 =[(40, 10), (290, 400)]
Indphall6 =[(40, 10), (width_screen-320, 400)]
Indphall7 =[(40, 10), (290, 600)]
Indphall8 =[(40, 10), (width_screen-320, 600)]
Indphall9 =[(10, 110), (240, 450)]
Indphall10 =[(10, 110), (width_screen-240, 450)]
Indm1 =[(10, 10), (280, 410)] 
Indm2 =[(10, 10), (270, 420)] 
Indm3 =[(10, 10), (260, 430)] 
Indm4 =[(10, 10), (250, 440)]

Indm5 =[(10, 10), (280, 590)]
Indm6 =[(10, 10), (270, 580)]
Indm7 =[(10, 10), (260, 570)]
Indm8 =[(10, 10), (250, 560)]

Indm9 =[(10, 10), (420, 410)]
Indm10 =[(10, 10), (430, 420)]
Indm11 =[(10, 10), (440, 430)]
Indm12 =[(10, 10), (450, 440)] 

Indm13 =[(10, 10), (450, 560)]
Indm14 =[(10, 10), (440, 570)]
Indm15 =[(10, 10), (430, 580)]
Indm16 =[(10, 10), (420, 590)]

TolebiWall1 = [(140, 10), (120, 640)]
TolebiWall2 = [(140, 10), (width_screen-250, 640)]
#TolebiWall3 = [(100, 10), (270, 640)]

wallsrect = []
wallssize = [TolebiWall1[0], TolebiWall2[0],  Kazybekwall1[0], Kazybekwall2[0], Kazybekwall3[0], Kazybekwall4[0],  Kazybekwall6[0], Kazybekwall7[0], Kazybekwall8[0], Kazybekwall9[0], AbilayWall2[0], AbilayWall1[0], AbilayWall1_2[0],  PanfilWall2[0], PanfilWall1[0], PanfilWall1_2[0], Indphall1[0], Indphall2[0], Indphall3[0], Indphall4[0], Indphall5[0], Indphall6[0], Indphall7[0], Indphall8[0], Indphall9[0], Indphall10[0], Indm1[0], Indm2[0], Indm3[0], Indm4[0], Indm5[0], Indm6[0], Indm7[0], Indm8[0], Indm9[0], Indm10[0], Indm11[0], Indm12[0], Indm13[0], Indm14[0], Indm15[0], Indm16[0], (10, height_screen), (10, height_screen), (width_screen, 10), (width_screen, 10)]
wallscoor = [TolebiWall1[1], TolebiWall2[1],  Kazybekwall1[1], Kazybekwall2[1], Kazybekwall3[1], Kazybekwall4[1],  Kazybekwall6[1], Kazybekwall7[1], Kazybekwall8[1], Kazybekwall9[1],AbilayWall2[1], AbilayWall1[1], AbilayWall1_2[1], PanfilWall2[1], PanfilWall1[1], PanfilWall1_2[1], Indphall1[1], Indphall2[1], Indphall3[1], Indphall4[1], Indphall5[1], Indphall6[1], Indphall7[1], Indphall8[1], Indphall9[1], Indphall10[1], Indm1[1], Indm2[1], Indm3[1], Indm4[1], Indm5[1], Indm6[1], Indm7[1], Indm8[1], Indm9[1], Indm10[1], Indm11[1], Indm12[1], Indm13[1], Indm14[1], Indm15[1], Indm16[1], (0, 0), (width_screen-10, 0), (0, height_screen-10), (0, 0)]
for i in range(len(wallscoor)):
    wallsrect.append(pygame.rect.Rect(wallscoor[i][0], wallscoor[i][1], wallssize[i][0], wallssize[i][1]))
walls = Walls(
    wallscoor,
    wallsrect
)


start_time = time.time()
end_time = time.time()
currenttime = round(start_time-end_time)+30

ratscore = 0
passedlevels = [0, 1, 1]


#win screen
def gamewinscreen(screen, passedlevels, enem_list):
    for lvl in passedlevels:

        if lvl != 1:
            return 0
    
    winscreen = pygame.image.load(r"images\IMG_5291.JPG")
    winscreen = pygame.transform.scale(winscreen, (winscreen.get_width()/2, winscreen.get_height()/2))
    screen.blit(winscreen, (0, 0))

    pygame.mixer_music.stop()
    pygame.mixer_music.unload
    pygame.mixer_music.load(r"music\gamejamwin.mp3") 
    pygame.mixer_music.play(1)
    player1.speed = 0
    for enem in enem_list:
        enem.dissapear()
        enem.speed=0
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    time.sleep(15)
    pygame.quit()
    sys.exit()
            
    

mapimage = pygame.image.load(r"images\kbtumap.png")
mapimage = pygame.transform.scale(mapimage, (700, 750))

        
while True:
    screen.blit(mapimage, (0, 0))
    if selected_level == 1:
        currenttime = round(start_time-end_time)+31
        # Code to start level 1
        




        player1.update()
        enemy1.update(player1.rect, walls.wall_rect_list)
        #enemy2.update(player1.rect, walls.wall_rect_list)
        enemy3.update(player1.rect, walls.wall_rect_list)

        player1.draw(screen)
        enemy1.draw(screen)
        #enemy2.draw(screen)
        enemy3.draw(screen)
        walls.draw(screen)
    

        if currenttime <= 27:
            passedlevels[0] = 1
            gamewinscreen(screen, passedlevels, enem_list)
            if levelwin(screen, 1):
                player1.speed = 0
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                selected_level = main_menu(player1, enem_list)

    
    elif selected_level == 2:
        ratend = 10
        currenttime = round(start_time-end_time)+60
        
        # Code to start level 2
            





        player1.update()
        enemy1.update(player1.rect, walls.wall_rect_list)
        enemy2.update(player1.rect, walls.wall_rect_list)
        enemy3.update(player1.rect, walls.wall_rect_list)

        player1.draw(screen)
        enemy1.draw(screen)
        enemy2.draw(screen)
        enemy3.draw(screen)
        walls.draw(screen)

        counter(screen, " ONAY! score: {0}/{1}".format(ratscore, ratend))
        
        if currenttime <= 0:
            if gameover(screen):
                player1.speed = 0
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                selected_level = main_menu(player1, enem_list)
        elif ratscore >= ratend and currenttime > 0:
            passedlevels[1] = 1
            gamewinscreen(screen, passedlevels, enem_list)
            if levelwin(screen, 2):
                ratscore = 0
                player1.speed = 0
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                selected_level = main_menu(player1, enem_list)

    
    if selected_level == 3:
        ratend = 20
        currenttime = round(start_time-end_time)+120
        # Code to start level 3
            





        player1.update()
        enemy1.update(player1.rect, walls.wall_rect_list)
        enemy2.update(player1.rect, walls.wall_rect_list)
        enemy3.update(player1.rect, walls.wall_rect_list)

        player1.draw(screen)
        enemy1.draw(screen)
        enemy2.draw(screen)
        enemy3.draw(screen)
        walls.draw(screen)
        
        counter(screen, " ONAY! score: {0}/{1}".format(ratscore, ratend))
        if currenttime <= 0:
            if gameover(screen):
                player1.speed = 0
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                selected_level = main_menu(player1, enem_list)
        elif ratscore >= ratend and currenttime > 0:
            passedlevels[2] = 1
            gamewinscreen(screen, passedlevels, enem_list)
            if levelwin(screen, 3):
                ratscore = 0
                player1.speed = 0
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                selected_level = main_menu(player1, enem_list)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                ratscore = 0
                selected_level = main_menu(player1, enem_list)
    #check if enemy is touching the player
    for enem in enem_list:
        if player1.collision(enem) and enem.type != 3:
            
            if gameover(screen):
                player1.speed = 0
                ratscore = 0
                for enem in enem_list:
                    enem.dissapear()
                start_time = time.time()
                selected_level = main_menu(player1, enem_list)
        
        elif player1.collision(enem) and enem.type == 3:
            ratscore += 1
            enem.dissapear()
            enem.revive()

    
            
    end_time = time.time()
    counter(screen, " time left: {0}".format(currenttime),  (0, 0))
    pygame.display.update()    
    framespersecond.tick(FPS)