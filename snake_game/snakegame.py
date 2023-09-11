# snakes 
import pygame
import random
import os
pygame.init()
white=(255,255,255)
red=(255,0,0)
black=(0,0,0)
screen_width=900
screen_height=600
display_screen= pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption(" Snake Game ")
pygame.display.update()


clock=pygame.time.Clock()#TO KEEP TRACK OF TIME(UPDATE FRAME PER SECOND)

font=pygame.font.SysFont(None,55)

def text_screen(text,color,x,y):
    screen_text=font.render(text,True,color)
    display_screen.blit(screen_text,[x,y])

def plot_snake(display_screen,color,snake_list,snake_size):
    for x,y in snake_list:
        pygame.draw.rect(display_screen,color,[x,y,snake_size,snake_size])

def  welcome():
    exit_game=False
    while not exit_game:
        display_screen.fill((100,100,160))
        text_screen(" Snake Game ",black,330,240)
        
        text_screen("Press Space Bar To Play",black,232,290)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game=True
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    game_loop()
        pygame.display.update()
        clock.tick(60)

def game_loop():
    exit_game=False
    game_over=False
    snake_size=10
    snake_x=45
    snake_y=45
    food_x=random.randint(20,screen_width/2)
    food_y=random.randint(30,screen_height/2)
    FPS=60
    velocity_x=0
    velocity_y=0
    init_velocity=4
    snake_list=[]
    snake_length=1 
    score=0
    level = 1
    required_score = 50
    currentDirection = "hehe";
    #to check if highscore file exist or not
    if (not os.path.exists("highscore.txt")):
        with open("highscore.txt","w") as f :
            f.write("0")

    with open("highscore.txt","r") as f :
        highscore=f.read()
    
    while not exit_game:
        if game_over:
            with open("highscore.txt","w") as f :
                f.write(str(highscore))
            display_screen.fill((100,100,160))
            text_screen("Your score:"+str(score),black,300,250)
            text_screen("Game Over! Press Enter To Continue",black,160,300)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game=True
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RETURN:
                        welcome()
        else:
            for event in pygame.event.get():
                

                if event.type == pygame.QUIT:
                    exit_game=True
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT and currentDirection != "left":
                        velocity_x=init_velocity
                        velocity_y=0
                        currentDirection = "right"
                        
                    if event.key==pygame.K_LEFT and currentDirection != "right": 
                        velocity_x=-init_velocity
                        velocity_y=0
                        currentDirection = "left"
                        

                    if event.key==pygame.K_UP and currentDirection != "down":
                        velocity_y=-init_velocity
                        velocity_x=0 
                        currentDirection = "up"
                        
                    if event.key==pygame.K_DOWN and currentDirection != "up":
                        velocity_y=init_velocity
                        velocity_x=0
                        currentDirection = "down"
                        
            snake_x=snake_x+velocity_x
            snake_y=snake_y+velocity_y
            if abs(snake_x-food_x)<15 and abs(snake_y-food_y)<15:
                score=score+10
                snake_length=snake_length+5
                food_x=random.randint(0,screen_width/2)
                food_y=random.randint(30,screen_height/2)  
                snake_length=snake_length+5 
                if score>int(highscore):
                    highscore=score
            if score >= required_score:
                level = level + 1
                required_score = required_score +required_score
                FPS = FPS + 10
                init_velocity+=0.5

            display_screen.fill(white)
            text_screen("Score:"+str(score)+"      Highscore: "+str(highscore)+"      Level:"+str(level),red,5,5)
            pygame.draw.rect(display_screen,red,[food_x,food_y,20,20])
            head=[]
            head.append(snake_x)
            head.append(snake_y)
            snake_list.append(head)
            # pygame.draw.rect(display_screen,black,[snake_x,snake_y,snake_size,snake_size])

            if len(snake_list)>snake_length:
                del snake_list[0]


            
                
            plot_snake(display_screen,black,snake_list,snake_size)
            if head in snake_list[:-1]:
                game_over=True

            if snake_x<0 or snake_x>screen_width or snake_y<0 or snake_y>screen_height:
                game_over=True

        pygame.display.update()
        clock.tick(FPS)#TO UPDATE THE CLOCK(HOW MANY  frame passed in MILISECOND )  
    pygame.quit()
    quit( )
welcome()

