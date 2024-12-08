import pygame
import random
import math
#constants
Screenwidth=1270
Screenheight=680
plwidth=200
plheight=20
plcolor=(100,100,100)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
BLUE=(0,0,200)
BLACK=(0,0,0)
SPEED_THRESHOLD = 5
pygame.mixer.init()
# Load sound effects
banana_sound = pygame.mixer.Sound('pop.mp3')
watermelon_sound = pygame.mixer.Sound('pop.mp3')
strawberry_sound = pygame.mixer.Sound('pop.mp3')
# Load crash sound effect
crash_sound = pygame.mixer.Sound('crash.mp3')

# Load background music
pygame.mixer.music.load('wee.mp3')



class Monkey(pygame.sprite.Sprite):
     
    def __init__(self,x,y):#here i will pass the value of x and y to spawn it on display
        super().__init__()
        self.x=x
        self.y=y
        self.a=0.2
        self.g=0.1 
        self.vely=0
        self.velx=0
        self.banana=100
        self.strawB=100
        self.coco=150
        self.pts=0
        self.fuel=2
        self.missionpassed=True
        self.image = pygame.image.load('Monkey_sprite.png').convert_alpha()  # Load sprite image
        self.rect = self.image.get_rect(center=(x, y))
        self.font = pygame.font.SysFont(None, 24)
         

    def update(self):
        self.fuel-=0.001
         
        self.fuel = max(0, self.fuel)
        self.vely+=self.g
        self.rect.y+=self.vely
        if self.rect.left < 0 or self.rect.right > Screenwidth or self.rect.top < 0 or self.rect.bottom > Screenheight:
            game_over = True
    def thrust(self):
        if self.fuel > 0:
            self.fuel=self.fuel-0.01
            self.vely-=self.a
            self.rect.y+=self.a
        
    def left(self):
        if self.fuel > 0:
            x=x-1
            self.fuel-=0.01
    def right(self):
        if self.fuel > 0:
            self.x=self.x+1
            self.fuel-=0.01
     
    def draw_fuel_text(self, screen):
        fuel_text = self.font.render("Fuel: {:.1f}".format(self.fuel), True, GREEN)
        screen.blit(fuel_text, (10,10))
    
    def fruitpts(self):
        pass 

    def ptssys(self):
        if self.missionpassed:
            self.pts=self.pts+self.fuel


class Fruit(pygame.sprite.Sprite):
    def __init__(self, x, y,file):
        super().__init__()
        self.image = pygame.image.load(file).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))    
        
              
class LandingPlatform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('lander.png').convert_alpha()  # Load the image file
        self.rect = self.image.get_rect(topleft=(x, y))



class SpecialFruit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('coconut.png').convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

    def collect(self, monkey):
        monkey.fuel += 1  # Increase fuel by 3 units when collected
        if monkey.fuel  > 2:
            monkey.fuel = 2

 
def main():
    pygame.init()
    screen = pygame.display.set_mode((Screenwidth ,Screenheight ))
    pygame.display.set_caption("Monkey Lander")
    clock = pygame.time.Clock()

    background_image = pygame.image.load('Background.png').convert()
    

    monkey = Monkey(Screenwidth // 2, 50)
    all_sprites = pygame.sprite.Group(monkey)
    fruits = pygame.sprite.Group()
    
    fruit1 = Fruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200),'banana.png')
    fruits.add(fruit1)
    all_sprites.add(fruit1)
    fruit2 = Fruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200),'watermelon.png')
    fruits.add(fruit2)
    all_sprites.add(fruit2)
    fruit3 = Fruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200),'Straw berry.png')
    fruits.add(fruit3)
    all_sprites.add(fruit3)
    fruit4 = SpecialFruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200) )
    fruits.add(fruit4)
    all_sprites.add(fruit4)

    score = 0
    landing_platform_created =False
    game_over = False
        
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
             
                 
                    

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            monkey.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            monkey.rect.x += 5
        if keys[pygame.K_UP]:
            monkey.thrust()   

        fruits_collected = pygame.sprite.spritecollide(monkey, fruits, True)
        for fruit in fruits_collected:
            if isinstance(fruit, SpecialFruit):
                fruit.collect(monkey)
            else:
                if fruit == fruit1:
                    banana_sound.play()  # Play banana collection sound
                elif fruit == fruit2:
                    watermelon_sound.play()  # Play watermelon collection sound
                elif fruit == fruit3:
                    strawberry_sound.play()  # Play strawberry collection sound
        score +=len(fruits_collected)
        if pygame.sprite.collide_rect(monkey, fruit4):
            fruit4.collect(monkey)
            all_sprites.remove( fruit4)

        if len(fruits) == 0 and not landing_platform_created:
            landing_platform = LandingPlatform( random.randint(600, Screenwidth-200) ,random.randint(550, Screenheight-100))
            all_sprites.add(landing_platform)
            landing_platform_created = True 
        
        
        #  Check if monkey is above the platform             
        if landing_platform_created == True and pygame.sprite.collide_rect(monkey, landing_platform):
            if monkey.rect.bottom <= landing_platform.rect.top + 5 and \
               abs(monkey.rect.centerx - landing_platform.rect.centerx) < 25:
                speed = math.sqrt(monkey.vely ** 2)
                if speed > SPEED_THRESHOLD:
                    game_over = True
                    # pygame.time.wait(2000)
                else:
                    pygame.mixer.music.load('wee.mp3')
                    pygame.mixer.music.play()
                    font = pygame.font.Font(None, 72)
                    text = font.render("Congrats moving to next level", True, BLUE)
                    screen.blit(text, (Screenwidth // 2 - text.get_width() // 2, Screenheight // 2 - text.get_height() // 2))
                    pygame.display.flip()
                    pygame.time.wait(2000)

                # Reset game elements to initial state
                    monkey.rect.x = random.randint(0, Screenwidth// 2) 
                    monkey.rect.y = random.randint(0, Screenheight// 2)
                    monkey.vely = 0
                    landing_platform_created = False 
                    landing_platform.kill()
             
                    for fruit in fruits.sprites():
                       fruit.kill()
                    fruit1 = Fruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200),'banana.png')
                    fruits.add(fruit1)
                    all_sprites.add(fruit1)
                    fruit2 = Fruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200),'watermelon.png')
                    fruits.add(fruit2)
                    all_sprites.add(fruit2)
                    fruit3 = Fruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200),'Straw berry.png')
                    fruits.add(fruit3)
                    all_sprites.add(fruit3)
                    fruit4 = SpecialFruit(random.randint(200, Screenwidth-200), random.randint(200, Screenheight-200) )
                    fruits.add(fruit4)
                    all_sprites.add(fruit4)


        if landing_platform_created == True and((monkey.rect.left < landing_platform.rect.right and monkey.rect.right > landing_platform.rect.left) \
                and monkey.rect.bottom > landing_platform.rect.top):
            game_over = True
            crash_sound.play()
            pygame.time.wait(2000)
        if monkey.rect.left < -200 or monkey.rect.right > Screenwidth+200 or monkey.rect.top <-200 or monkey.rect.bottom > Screenheight+200:
            game_over = True
            crash_sound.play()
            pygame.time.wait(2000)
                
        all_sprites.update()

        # Draw background image
        screen.blit(background_image, (0, 0))

         
        all_sprites.draw(screen)
         
        monkey.draw_fuel_text(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render("Score: " + str(score), True, GREEN)
        screen.blit(text, (10, 70))
        
        
        pygame.display.flip()
        clock.tick(60)

         # Game over code
     
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (Screenwidth // 2 - text.get_width() // 2, Screenheight // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)
    if __name__ == "__main__":
        main()
if __name__ == "__main__":
    main()