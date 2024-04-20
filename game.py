import pygame
import sys
from queue import PriorityQueue

pygame.init()







player_speed = 10
#player and enemy and coin classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = 10
        self.height = 20
        self.speed = player_speed
        self.rect = pygame.rect.Rect(50, 50, self.width, self.height)
        
    
    def update(self):


        pressed_key = pygame.key.get_pressed()

        next_rect = self.rect.copy()     
        
        if pressed_key[pygame.K_LEFT]:
            if self.rect.bottomleft[0] > 0:
                next_rect.move_ip(-self.speed, 0)
        if pressed_key[pygame.K_RIGHT]:
            if self.rect.bottomright[0] < width_screen:
                next_rect.move_ip(self.speed, 0)
        if pressed_key[pygame.K_UP]:
            if self.rect.top > 0:
                next_rect.move_ip(0, -self.speed)
        if pressed_key[pygame.K_DOWN]:
            if self.rect.bottom < height_screen:
                next_rect.move_ip(0, self.speed)
        

        if next_rect.collidelist(walls.wall_rect_list) == -1:      
            self.rect = next_rect.copy()

    def draw(self, surface):
        pygame.draw.rect(surface, (20, 30, 120), self.rect)


    #collision function to detect if player has died or not    
    def collision(self, rect1):
        self.collide = self.rect.colliderect(rect1)
        return self.collide



class Enemy(pygame.sprite.Sprite):
    def __init__(self, type=None, speed=None, color=None):
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
        self.speed = speed
        self.rect = pygame.rect.Rect(250, 250, self.width, self.width)
        self.last_dx = 0
        self.last_dy = 0
        self.last_position = self.rect.topleft
    
    def update(self, player_rect, walls):
        
        if self.type == 1:
            dx, dy = self.type1(player_rect, walls)
        elif self.type == 2:
            dx, dy = self.type2(player_rect, walls)
        elif self.type == 3:
            dx, dy = self.type3(player_rect, walls)
            
            

        # Move towards the player
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        self.last_dx = dx
        self.last_dy = dy

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

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
RED = (255, 30, 30)


#screen parameters
width_screen = 700
height_screen = 750
screen = pygame.display.set_mode((width_screen, height_screen))
FPS = 30
framespersecond = pygame.time.Clock()
pygame.display.set_caption("Oops There Goes The Retake")


#creating player and enemy
player1 = Player()
enemy1 = Enemy(1, 7, (250, 160, 40))
enemy2 = Enemy(2, 4)
enemy3 = Enemy(3, 10, (240, 160, 100))

enem_list = [enemy1, enemy2, enemy3]

#gameover screen
def gameover(surface):


    surface.fill(RED)

    #gameover text in the center
    font = pygame.font.SysFont("centrury", 50)
    text = font.render(" OOPS THERE GOES THE RETAKE ", True, BLACK)
    recttext = (surface.get_width()/2-text.get_width()/2, surface.get_height()/2)
    surface.blit(text, recttext)

    pygame.display.update()
    # Wait for spacebar press to restart
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                
    

musictrack = "none"

def main_menu():

    #background music
    pygame.mixer_music.stop()
    pygame.mixer_music.unload()
    pygame.mixer_music.load(r"music\gamejam1menu.mp3")
    pygame.mixer_music.play(-1)
    musictrack = "menu"
    
    #creating player and enemy
    player1.__init__()
    player1.speed = player_speed
    enemy1.__init__(1, 7, (250, 160, 40))
    enemy2.__init__(2, 4)
    enemy3.__init__(3, 10, (240, 160, 100))
        

    while True:


        screen.fill((255, 255, 255))  # Fill the screen with white

        # Draw menu options
        title_font = pygame.font.Font(None, 50)
        title_text = title_font.render("Oops There Goes The Retake", True, (0, 0, 0))
        screen.blit(title_text, (140, 50))

        font = pygame.font.Font(None, 36)
        level1_text = font.render("Level 1", True, (0, 0, 0))
        level2_text = font.render("Level 2", True, (0, 0, 0))
        level3_text = font.render("Level 3", True, (0, 0, 0))

        rect1 = level1_text.get_rect(topleft = (300, 200))
        rect2 = level2_text.get_rect(topleft = (300, 250))
        rect3 = level3_text.get_rect(topleft = (300, 300))

        screen.blit(level1_text, (300, 200))
        screen.blit(level2_text, (300, 250))
        screen.blit(level3_text, (300, 300))

        # Check for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                # Check if user clicked on any of the level options
                if rect1.collidepoint(event.pos):
                    if musictrack == "menu":
                        pygame.mixer_music.stop()
                        pygame.mixer_music.unload
                        pygame.mixer_music.load(r"music\gamejamlvl1.mp3") 
                        pygame.mixer_music.play(-1)
                        musictrack = "lvl1"  
                    return 1
                
                        
                elif rect2.collidepoint(event.pos):
                    if musictrack == "menu":
                        pygame.mixer_music.stop()
                        pygame.mixer_music.unload
                        pygame.mixer_music.load(r"music\gamejamlvl2.mp3") 
                        pygame.mixer_music.play(-1)
                        musictrack = "lvl2" 
                    # Start level 2
                    return 2
                elif rect3.collidepoint(event.pos):
                    # Start level 3
                    return 3

        pygame.display.update()

# Initialize game variables and objects

# Start with the main menu
selected_level = main_menu()
pygame.mixer_music.set_volume(0.5)



#data (sizes and coordinates) for walls
Kazybekwall1 = [(100, 10), (width_screen-210, 250)]
Kazybekwall2 = [(170, 10), (270, 250)]
Kazybekwall3 = [(100, 10), (120, 250)]
Kazybekwall4 = [(100, 10), (120, 350)]
Kazybekwall5 = [(170, 10), (270, 350)]
Kazybekwall6 = [(100, 10), (width_screen-210, 350)]

AbilayWall1 = [(10, 250), (120, 0)]
AbilayWall2 = [(10, 300), (120, 350)]
AbilayWall3 = [(10, 110), (220, 250)]
AbilayWall4 = [(10, 110), (270, 250)]

PanfilWall1 = [(10, 250), (width_screen-120, 0)]
PanfilWall2 = [(10, 300), (width_screen-120, 350)]
PanfilWall3 = [(10, 110), (270+170, 250)]
PanfilWall4 = [(10, 110), (270+170+50, 250)]

TolebiWall1 = [(100, 10), (120, 640)]
TolebiWall2 = [(170, 10), (270, 640)]
TolebiWall3 = [(100, 10), (width_screen-210, 640)]

wallsrect = []
wallssize = [TolebiWall1[0], TolebiWall2[0], TolebiWall3[0], Kazybekwall1[0], Kazybekwall2[0], Kazybekwall3[0], Kazybekwall4[0], Kazybekwall5[0], Kazybekwall6[0], AbilayWall4[0], AbilayWall3[0], AbilayWall2[0], AbilayWall1[0], PanfilWall4[0], PanfilWall3[0], PanfilWall2[0], PanfilWall1[0], (10, height_screen), (10, height_screen), (width_screen, 10), (width_screen, 10)]
wallscoor = [TolebiWall1[1], TolebiWall2[1], TolebiWall3[1], Kazybekwall1[1], Kazybekwall2[1], Kazybekwall3[1], Kazybekwall4[1], Kazybekwall5[1], Kazybekwall6[1], AbilayWall4[1], AbilayWall3[1], AbilayWall2[1], AbilayWall1[1], PanfilWall4[1], PanfilWall3[1], PanfilWall2[1], PanfilWall1[1], (0, 0), (width_screen-10, 0), (0, height_screen-10), (0, 0)]
for i in range(len(wallscoor)):
    wallsrect.append(pygame.rect.Rect(wallscoor[i][0], wallscoor[i][1], wallssize[i][0], wallssize[i][1]))
walls = Walls(
    wallscoor,
    wallsrect
)

        

while True:
    if selected_level == 1:
        # Code to start level 1
        


        screen.fill((255,255,255))




        player1.update()
        #enemy1.update(player1.rect, walls.wall_rect_list)
        #enemy2.update(player1.rect, walls.wall_rect_list)
        enemy3.update(player1.rect, walls.wall_rect_list)

        player1.draw(screen)
        #enemy1.draw(screen)
        #enemy2.draw(screen)
        enemy3.draw(screen)
        walls.draw(screen)
    
    
    elif selected_level == 2:
        # Code to start level 2
            

        screen.fill((255,255,255))




        player1.update()
        enemy1.update(player1.rect, walls.wall_rect_list)
        #enemy2.update(player1.rect, walls.wall_rect_list)
        enemy3.update(player1.rect, walls.wall_rect_list)

        player1.draw(screen)
        enemy1.draw(screen)
        #enemy2.draw(screen)
        enemy3.draw(screen)
        walls.draw(screen)

    
    if selected_level == 3:
        # Code to start level 3
            

        screen.fill((255,255,255))




        player1.update()
        enemy1.update(player1.rect, walls.wall_rect_list)
        enemy2.update(player1.rect, walls.wall_rect_list)
        enemy3.update(player1.rect, walls.wall_rect_list)

        player1.draw(screen)
        enemy1.draw(screen)
        enemy2.draw(screen)
        enemy3.draw(screen)
        walls.draw(screen)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                selected_level = main_menu()
    #check if enemy is touching the player
    for enem in enem_list:
        if player1.collision(enem):
            
            if gameover(screen):
                player1.speed = 0
                pygame.mixer_music.stop()
                pygame.mixer_music.unload()    
                selected_level = main_menu()

    pygame.display.update()    
    framespersecond.tick(FPS)
