import cv2
import numpy as np
import math


#python snake game with comments and clock
import pygame
import time
import random
#iniatialize
pygame.init()


gestured_click=0;

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('snake game')

#condition check
#clock setting
clock = pygame.time.Clock()
#text showwing
font = pygame.font.SysFont(None, 25)
def message_to_screen(msg,color):
    screen_text = font.render(msg, True, color)
    gameDisplay.blit(screen_text, [400,300]) #showing image or text on screen and also in the middle of screen 800/2=400
gameExit = False

#variables

lead_x = 300
lead_y = 300
lead_x_change = 0
lead_y_change = 0
snakeList = []
snakeLen = 1 #leangth of the snake
random_foodx = round(random.randrange(0,700)/10.0)*10#random range from zero display width
random_foody = round(random.randrange(0,600)/10.0)*10#rounding so that properly overlaps
def snake(snakeList):
    for xny in snakeList:
        pygame.draw.rect(gameDisplay, black, [xny[0], xny[1], 10, 10])#liist of snakes for getting fat and extraxting x and y
#loop for events


click_flag=0
resetclick_flag=0

shape_select=1
b_col=255
g_col=255
r_col=255

pq=0

cap = cv2.VideoCapture(1)


#black_img=np.zeros((380,506,3), np.uint8)
#erase_img=np.zeros((380,506,3), np.uint8)

black_img=cv2.imread('yash1.png')
erase_img=cv2.imread('yash1.png')

line_testimg=cv2.imread('yash1.png')
yash=cv2.imread('yash1.png')

draw_lineflag=0
draw_resetlineflag=0


while(not gameExit):




        #######show full image with rectangle
        ret, im = cap.read()
        im=cv2.flip(im,1)
        #cv2.rectangle(im,(500,500),(50,50),(255,0,0),2)
        #cv2.imshow('imagesource',im)
        #cv2.waitKey(0)
        ###########

        ##### crop the rectangle###
        cropped_img = cv2.resize(im,(800,600))

        #cv2.imshow(' cropped_img',cropped_img)
        #cv2.waitKey(2)
        ######
        
        ####Find and draw counters in the cropped image##
        imgray=cv2.cvtColor(cropped_img,cv2.COLOR_BGR2GRAY)
        #cv2.imshow('imagegray',imgray)
        #cv2.waitKey(2)
        ret,thresh1 = cv2.threshold(imgray,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
        cv2.imshow('thresholded',thresh1)
        cv2.waitKey(2)
        image,contours, hierarchy = cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        ########
        if len(contours)==0:
            continue
        ##### detecting defects and finding number of defects
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        hull2 = cv2.convexHull(cnt,returnPoints = False)
        defects = cv2.convexityDefects(cnt,hull2)
        count_defects = 0

        
        for i in range(defects.shape[0]):
                        s,e,f,d = defects[i,0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        far = tuple(cnt[f][0])
                        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
                        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
                        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)
                        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
                        if angle <= 90:
                                count_defects += 1
      
        #print count_defects

        #######################

        
        ####deciding points
        cnt = max(contours, key = lambda x: cv2.contourArea(x))
        hull = cv2.convexHull(cnt)
        
        x=hull.shape[0]  #x nnumber of points in the contour
        y=hull.shape[1] # y dont know what it is actually
        z=hull.shape[2] #z is used to define coordinates of the points in the contour
        
        corro_c=0
        minb=700
        
        for i in range(0,x):
                c=hull[i][0][0]
                b=hull[i][0][1]
        
                if b<minb:
                        minb=b
                        corro_c=c
                        '''
                        #new coordimate
                        new_minb=minb
                        new_corro_c=corro_c-134

                        new_minb=new_minb*2
                        new_corro_c=new_corro_c*2
                        '''
    ########	#################################################
        cv2.circle(cropped_img,(corro_c,minb),5,(b_col,g_col,r_col),-1)
        cv2.rectangle(cropped_img,(200,0),(400,200),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(400,0),(600,200),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(600,0),(800,200),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(200,200),(400,400),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(400,200),(600,400),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(600,200),(800,400),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(200,400),(400,600),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(400,400),(600,600),(b_col,g_col,r_col),0)
        cv2.rectangle(cropped_img,(600,400),(800,600),(b_col,g_col,r_col),0)

        cv2.imshow('cropped_img',cropped_img)

        print minb
 
        print corro_c
        if minb>200 and minb<400 and corro_c>200 and corro_c<400:
             lead_x_change = -10
             lead_y_change = 0 #so that does not move diagonally
             print 'Yash'
        if minb>200 and minb<400 and corro_c>600 and corro_c<800:
             lead_x_change = 10
             lead_y_change = 0 #so that does not move diagonally
             print 'Yash'
        if minb>0 and minb<200 and corro_c>400 and corro_c<600:
             lead_x_change = 0
             lead_y_change = -10 #so that does not move diagonally
             print 'Yash'
        if minb>400 and minb<600 and corro_c>400 and corro_c<600:
             lead_x_change = 0
             lead_y_change = 10 #so that does not move diagonally
             print 'Yash'


     
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                '''
                if event.key == pygame.K_LEFT:
                    lead_x_change = -10
                    lead_y_change = 0 #so that does not move diagonally
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = 10
                    lead_y_change = 0
                elif event.key == pygame.K_UP:
                    lead_y_change = -10
                    lead_x_change = 0
                elif event.key == pygame.K_DOWN:
                    lead_y_change = 10
                    lead_x_change = 0
                '''
                print minb
                sleep(2)
                print corro_c
                sleep(2)
                if minb>200 and minb<400 and corro_c>200 and corro_c<400:
                    lead_x_change = -10
                    lead_y_change = 0 #so that does not move diagonally
                '''
                elif 200<minb & minb<400 & 200<corro_c & corro_c<400:
                    lead_x_change = 10
                    lead_y_change = 0
                elif 200<minb & minb<400 & 200<corro_c & corro_c<400:
                    lead_y_change = -10
                    lead_x_change = 0
                elif 200<minb & minb<400 & 200<corro_c & corro_c<400:
                    lead_y_change = 10
                    lead_x_change = 0

                '''
            #without this key up the rect will keep on moving and moving and, also it wont go diagonally also, you can make x change zero when changing y change in if statements to stop diagonal movements       
            #if event.type == pygame.KEYUP:
            #    if event.key == pygame.K_LEFT or event.key == pygame.K_DOWN or event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
            #        lead_y_change = 0
            #        lead_x_change = 0
        #creating boundaries for 800 rows and 600 columns
        #if lead_x >= 800 or lead_x < 0 or lead_y >= 600 or lead_y < 0:
        #    gameExit = True
        lead_x += lead_x_change
        lead_y += lead_y_change
        gameDisplay.fill(white)
        pygame.draw.rect(gameDisplay, red, [random_foodx,random_foody, 10, 10])#food for snake
        
        snakeHead = []
        snakeHead.append(lead_x)
        snakeHead.append(lead_y)
        snakeList.append(snakeHead)
        if len(snakeList) > snakeLen:
            del snakeList[0] # len is for length and head cuts off tail increases
        snake(snakeList)#snake itself
        #without update it will paint the whole path black
        pygame.display.update()
        if lead_x == random_foodx and lead_y == random_foody:
            print ("you")
            random_foodx = round(random.randrange(0,700)/10.0)*10#random range from zero display width
            random_foody = round(random.randrange(0,600)/10.0)*10#calling the function again
            snakeLen += 1
        #clock is for frames per second without it moving rect will go out of the screen as laptop is very fast so to control the movement 15 frames per second
        clock.tick(15)
                    
message_to_screen("you lose , looser",red)
time.sleep(2)
pygame.display.update() #you have to update the display whenevr display changes
time.sleep(10)
pygame.quit()
quit()              
        



                
