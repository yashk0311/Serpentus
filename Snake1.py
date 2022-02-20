import pygame
import time
import random
from pygame import mixer

# screen
width = 800
height = 448
size = (width, height)
screen = pygame.display.set_mode(size)

#colors
red = pygame.Color("red")
black= pygame.Color("black")
green=(0,180,0)
dark_green=(0,255,0)
white=(255,255,255)
blue=(0,0,255)
light_red=(100,0,0)
dark_red=(255,0,0)
light_blue=(0,0,100)
dark_blue=(0,0,255)
bgm='./Sounds/bgm.wav'


class Snake():
    # snake body is represented as
    # [Tail, n-1th part, n-2th part,............2nd turn, 1st turn, Head]
    # For every movement, a new element is added at the and which becomes the head
    # and current tail is removed and the first element becomes the new tail    

    speed = 0.33

    def __init__(self):
        self.colour = "red"
        self.head = [(width+32)/2, (height+32)/2]     
        self.tail = [(width)/2, (height+32)/2]      
        self.body = [self.tail, self.head]  
        self.x_inc = 0
        self.y_inc = 0
        self.prev_dir = None

    @staticmethod
    def pos(b, a):    # Position of b wrt a   a,b are lists of the form [x,y]
        if(a == b):
            return 's'
        elif(b[0] == a[0]):
            if(b[1] < a[1]):
                return 'u'
            elif(b[1] > a[1]):
                return 'd'
        elif(b[1] == a[1]):
            if(b[0] > a[0]):
                return 'r'
            elif(b[0] < a[0]):
                return 'l'

    def movement(self, event):   # Identifies key inputs and changes x_inc and y_inc
        if(game.pause==False):
            if event.key == pygame.K_LEFT:
                if(self.prev_dir!='r'):
                    self.x_inc = -16
                    self.y_inc = 0
                    self.prev_dir='l'

            elif event.key == pygame.K_RIGHT:
                if(self.prev_dir!='l'):
                    self.x_inc = 16
                    self.y_inc = 0
                    self.prev_dir='r'

            elif event.key == pygame.K_UP:
                if(self.prev_dir!='d'):
                    self.y_inc = -16
                    self.x_inc = 0
                    self.prev_dir='u'

            elif event.key == pygame.K_DOWN:
                if(self.prev_dir!='u'):
                    self.y_inc = 16
                    self.x_inc = 0
                    self.prev_dir='d'

    def move_one_step(self):  # moves the sname by one step depending on x_inc and y_inc
        snake=self.body
        if(self.x_inc != 0 or self.y_inc != 0):
            time.sleep(1/(self.speed*100))
            # Head
            snake.append([snake[-1][0]+self.x_inc, snake[-1][1]+self.y_inc])
            # Tail
            snake.pop(0)

    def add_new(self):    # Increases the length of the snake
        snake=self.body
        if(self.pos(snake[1], snake[0]) == 'r'):
            snake.insert(0, [snake[0][0]-16, snake[0][1]])
        elif(self.pos(snake[1], snake[0]) == 'l'):
            snake.insert(0, [snake[0][0]+16, snake[0][1]])
        elif(self.pos(snake[1], snake[0]) == 'u'):
            snake.insert(0, [snake[0][0], snake[0][1]+16])
        elif(self.pos(snake[1], snake[0]) == 'd'):
            snake.insert(0, [snake[0][0], snake[0][1]-16])
        return snake


    def boundary(self):  # Snake emerges from opposite side if it goes out of the boundary
        snake=self.body
        if(game.borders==False):
            for point in snake:
                if point[0] >= width:
                    point[0] = 0
                elif(point[0] <= -16):
                    point[0] = width-16
                if point[1] >= height:
                    point[1] = 0
                elif(point[1] <= -16):
                    point[1] = height-16
        else:
            for point in snake:
                if(point[0]>=width or point[0]<= -16 or point[1]>=height or point[1]<=-16):
                    game.over()

    def change_color(self,score):
        if(score.total<30):
            self.colour=light_red
        elif(score.total<60):
            self.colour=light_blue
        elif(score.total<90):
            self.colour=dark_red
        else:
            self.colour=dark_blue

    def display(self):  # Displays the snake on the screen
        snake=self.body

        for i in snake:
            coordinates = [i[0], i[1]]
            pygame.draw.rect(screen,self.colour, pygame.Rect(i[0], i[1], 16, 16))
        return coordinates

    def death(self):
        count=0
        for i in range(len(self.body)-1):
            if(self.body[-1]==self.body[i]):
                count+=1

        if(count!=0 and len(self.body)>3):
            game.over()


class Score():

    def __init__(self):
        self.total=0

    def update_score(self):
        if (food.respawn() == 1):
            self.total += 1
        elif (food.respawn() == 2):
            self.total += 2
        elif (food.respawn() == 3):
            self.total += 3
        elif (food.respawn() == 4):
            self.total += 10

    def display(self):
        self.font = pygame.font.Font('./Fonts/FreeSansBold.ttf', 20)
        self.text=self.font.render('Score '+str(self.total), True, (0, 255, 0), (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = (50, 10)
        screen.blit(self.text, self.textRect)

    def HighScore(self):
        if(game.borders == False):
            # opening file which stores highscores
            with open('./High_Scores/Without_borders.txt', 'r') as f:
                try:
                    highscore = int(f.read())
                except:
                    highscore = 0

            # writing new highscore into file
            if (self.total >= highscore):
                highscore = self.total
                with open('./High_Scores/Without_borders.txt', 'w') as f:
                    f.write(str(highscore))

            return highscore

        else:
            # opening file which stores highscores
            with open('./High_Scores/With_borders.txt', 'r') as f:
                try:
                    highscore = int(f.read())
                except:
                    highscore = 0

            # writing new highscore into file
            if (self.total >= highscore):
                highscore = self.total
                with open('./High_Scores/With_borders.txt', 'w') as f:
                    f.write(str(highscore))

            return highscore


class Food():
    # loading food images
    apple = pygame.image.load('./Images/apple.png')
    plum = pygame.image.load('./Images/plum.png')
    oranges = pygame.image.load('./Images/orange.png')
    strawberry = pygame.image.load('./Images/strawberry.png')

    def __init__(self):
        self.food_position=None
        self.food_spawn=False

    def respawn(self):
        if self.food_spawn is False:  # When a food is taken it will respawn randomly
            # implementing different foods with different probabilities of occuring. fruit with lower points has a higher chance of occuring
            self.weighted_list = random.choices([1, 2, 3, 4], weights=(40, 30, 20, 10), k=1)  
            self.n = self.weighted_list[0]
            self.food_position = [random.randint( 1, width/16 - 1) *16 , random.randint(1, height/16 - 1) *16 ]
            while (self.food_position in snake.add_new()):
                self.food_position = [random.randint(1, width / 16 - 1) * 16, random.randint(1, height / 16 - 1) * 16]
            self.food_spawn = True  # It will set the food to True again, to keep the cycle
        return self.n

    def eat(self,snake,score):
        if snake.body[-1] == self.food_position :
            eat_sound=mixer.Sound('./Sounds/eat.wav')
            eat_sound.play()
            score.update_score()
            snake.add_new()
            self.food_spawn = False  # It removes the food from the board
            
    def display(self): # Displays the food images on the screen
        if (self.n == 1):
            screen.blit(Food.apple, (self.food_position))
        elif (self.n == 2):
            screen.blit(Food.oranges, (self.food_position))
        elif (self.n == 3):
            screen.blit(Food.plum, (self.food_position))
        elif (self.n == 4):
            screen.blit(Food.strawberry, (self.food_position))


class Menu():
    @staticmethod
    def heading(str):
        f=pygame.font.Font('./Fonts/Chopsic-K6Dp.ttf',80)
        headin=f.render(str,True,(255,55,155))
        screen.blit(headin,(100,-10))

    
    
        
    @staticmethod
    def button(msg,x,y,w,h,ic,ac,action=None):
        global borders
        mouse=pygame.mouse.get_pos()
        click=pygame.mouse.get_pressed()

        if x+w>mouse[0]>x and y+h>mouse[1]>y:
            pygame.draw.rect(screen, ac,(x,y,w,h))
            if click[0] and action!= None:
                if (action=="play"):
                    game.play()
                elif (action=="speed"):
                    Menu.speed()
                elif (action=="slow"):
                    Snake.speed = 0.25
                    Menu.main()
                elif (action=="medium"):
                    Snake.speed = 0.33
                    Menu.main()
                elif (action=="fast"):
                    Snake.speed = 0.43
                    Menu.main()
                elif (action=="back"):
                    Menu.main()

                elif (action=="modes"):
                    Menu.modes()

                elif (action=="with borders"):
                    game.borders=True
                    Menu.main()

                elif (action=="without borders"):
                    game.borders=False
                    Menu.main()

                elif (action=="pause"):
                    game.pause=True

                elif (action=="resume"):
                    game.pause=False

                elif(action=="bgm"):
                    Menu.bgmusic()

                elif (action=="funky"):
                    bgm='./Sounds/bgm.wav'
                    mixer.music.load(bgm)
                    mixer.music.play(-1)
                    Menu.main()

                elif (action=="calm"):
                    bgm='./Sounds/bgm3.wav'
                    mixer.music.load(bgm)
                    mixer.music.play(-1)
                    Menu.main()

                elif (action=="hcore"):
                    bgm='./Sounds/bgm2.wav'
                    mixer.music.load(bgm)
                    mixer.music.play(-1)
                    Menu.main()

                elif(action=="menu"):
                    game.pause=False
                    Menu.main()

                elif (action=="quit"):
                    pygame.quit()
                    quit()
        else:
            pygame.draw.rect(screen, ic,(x,y,w,h))
        
        textg=pygame.font.Font('./Fonts/Chango-Regular.ttf', 20)
        textsurf=textg.render(msg,True,red)
        textrect=textsurf.get_rect()
        textrect.center=((x+(w/2)), (y+(h/2)))
        screen.blit(textsurf,textrect)

    @staticmethod
    def main():

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            bg=pygame.image.load('./Images/bg2.png')
            screen.blit(bg,(0,0))
            Menu.heading("SERPENTUS")

            Menu.button("Play",405,150,70,35,white,dark_green,"play")
            Menu.button("Modes",390,200,100,35,white,dark_green,"modes")
            Menu.button("Speed",390,250,100,35,white,dark_green,"speed")
            Menu.button("Music",405,300,70,35,white,dark_green,"bgm")
            Menu.button("Quit",405,350,70,35,white,dark_green,"quit")
            
            pygame.display.update()

    
    @staticmethod
    def bgmusic():
        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            bg=pygame.image.load('./Images/bg2.png')
            screen.blit(bg,(0,0))
            Menu.heading("         MUSIC")

            if(bgm=='./Sounds/bgm.wav'):
                Menu.button("Funky",140,100,85,35,white,dark_green,"funky")
                Menu.button("Calm",240,100,70,35,white,dark_green,"calm")
                Menu.button("Hardcore",330,100,130,35,white,dark_green,"hcore")
            
            if(bgm=='./Sounds/bgm2.wav'):
                Menu.button("Funky",140,100,85,35,white,dark_green,"funky")
                Menu.button("Calm",240,100,70,35,white,dark_green,"calm")
                Menu.button("Hardcore",330,100,130,35,white,dark_green,"hcore")
            
            if(bgm=='./Sounds/bgm3.wav'):
                Menu.button("Funky",140,100,85,35,white,dark_green,"funky")
                Menu.button("Calm",240,100,70,35,white,dark_green,"calm")
                Menu.button("Hardcore",330,100,130,35,white,dark_green,"hcore")
            
            Menu.button("Back",490,100,70,35,white,dark_green,"back")
            

            pygame.display.update()


    @staticmethod
    def speed():

        while True:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()

            bg=pygame.image.load('./Images/bg2.png')
            screen.blit(bg,(0,0))
            Menu.heading("                    SPEED")

            if(Snake.speed==0.25):
                Menu.button("Slow",520,150,70,35,dark_green,dark_green,"slow")
                Menu.button("Medium",500,200,120,35,white,dark_green,"medium")
                Menu.button("Fast",520,250,70,35,white,dark_green,"fast")
            elif(Snake.speed==0.33):
                Menu.button("Slow",520,150,70,35,white,dark_green,"slow")
                Menu.button("Medium",500,200,120,35,dark_green,dark_green,"medium")
                Menu.button("Fast",520,250,70,35,white,dark_green,"fast")
            elif(Snake.speed==0.43):
                Menu.button("Slow",520,150,70,35,white,dark_green,"slow")
                Menu.button("Medium",500,200,120,35,white,dark_green,"medium")
                Menu.button("Fast",520,250,70,35,dark_green,dark_green,"fast")

            Menu.button("Back",520,300,70,35,white,dark_green,"back")
            
            pygame.display.update()

    @staticmethod
    def modes():
        
        while True:
            global boundary
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    quit()
            bg=pygame.image.load('./Images/bg2.png')
            screen.blit(bg,(0,0))
            Menu.heading("MODES")

            if(game.borders==True):
                Menu.button("With borders",150,150,200,35,dark_green,dark_green,"with borders")
                Menu.button("Without borders",125,200,250,35,white,dark_green,"without borders") 
            else:
                Menu.button("With borders",150,150,200,35,white,dark_green,"with borders")
                Menu.button("Without borders",125,200,250,35,dark_green,dark_green,"without borders")
            Menu.button("Back",200,250,75,35,white,dark_green,"back")
            pygame.display.update()


class game():
    borders=False
    pause=False

    pygame.display.set_caption("SERPENTUS")
    icon=pygame.image.load("anaconda.png")
    pygame.display.set_icon(icon)

    @staticmethod
    def begin():
        pygame.init()
        mixer.music.load(bgm)
        mixer.music.play(-1)
        Menu.main()

    @staticmethod
    def play():
        global snake
        global score
        global food
        snake = Snake()
        food = Food()
        score = Score()
        run = True
        while run:
                
            bgg=pygame.image.load('./Images/grass.jpg')
            screen.blit(bgg,(0,0))
            # screen.fill(white)

            game.Pause()

            score.display()
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    quit()
                elif event.type == pygame.KEYDOWN:
                    snake.movement(event)

            snake.change_color(score)    
            snake.move_one_step()

            snake.boundary()
                
            food.eat(snake,score)
            food.respawn()
            food.display()
                
            score.display()
                
            snake.display()
            snake.death()

            pygame.display.update()

    @staticmethod
    def Pause():
        if(game.pause==False):
            Menu.button("Pause",width-100,0,100,20,white,dark_green,"pause")
            
        if(game.pause==True):
            Menu.button("Resume",width-220,0,120,25,white,dark_green,"resume")
            Menu.button("Menu",width-350,0,80,25,white,dark_green,"menu")
            snake.x_inc=0
            snake.y_inc=0

    def over():
        mixer.music.pause()
        go_sound=mixer.Sound("./Sounds/go.wav")
        go_sound.play()
        over=pygame.font.Font('./Fonts/valianttimesexpand.ttf',80)
        overt=over.render('GAME OVER',True,(220,20,60))
        screen.blit(overt,(250,180))
        h_score = pygame.font.Font('./Fonts/valianttimes3d.ttf', 80)
        h_score1 = h_score.render('HIGH SCORE: ' + str(score.HighScore()), True, (0, 0, 255))
        screen.blit(h_score1, (50, 50))
        pygame.display.update()
        time.sleep(3)
        mixer.music.play(-1)
        Menu.main()

if(__name__ == '__main__'):
    game.begin()