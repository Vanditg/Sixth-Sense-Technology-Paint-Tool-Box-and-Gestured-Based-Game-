import cv2
import numpy as np
import math
from time import sleep

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


while(cap.isOpened()):

        #######show full image with rectangle
        ret, im = cap.read()
        im=cv2.flip(im,1)
        #cv2.rectangle(im,(500,500),(50,50),(255,0,0),2)
        #cv2.imshow('imagesource',im)
        #cv2.waitKey(0)
        ###########

        ##### crop the rectangle###
        cropped_img = im
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

        ##### detecting defects and finding number of defects
	if len(contours)==0:
		continue
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
      
        print count_defects

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

                        #new coordimate
                        new_minb=minb
                        new_corro_c=corro_c-134

                        new_minb=new_minb*2
                        new_corro_c=new_corro_c*2
########	#################################################

        
        
        #####assigning colour corrosponding to any defect
        if count_defects >3:
                if resetclick_flag==0:
                        click_flag=click_flag^1
                        resetclick_flag=1
        else:
                resetclick_flag=0
        
        

        if click_flag == 1:
                #####color selection
                if (new_corro_c>715) & (new_corro_c<798):
                        if (new_minb>61) & (new_minb<188):
                                b_col=255
                                g_col=0
                                r_col=0
                        elif (new_minb>188) & (new_minb<360):
                                b_col=0
                                g_col=255
                                r_col=255
                        elif (new_minb>360) & (new_minb<519):
                                b_col=0
                                g_col=0
                                r_col=255
                draw_lineflag=1
                pq=0
                        

                
                ##selecting shape
                if (new_corro_c>3) & (new_corro_c<106):
                        if (new_minb>57) & (new_minb<165):
                                shape_select=1
                        elif (new_minb>165) & (new_minb<291):
                                shape_select=2
                        elif (new_minb>291) & (new_minb<430):
                                shape_select=3
                        elif (new_minb>430) & (new_minb<570):
                                shape_select=4
                        


                
        else:
                b_col=255
                g_col=255
                r_col=255
                draw_lineflag=0
                draw_resetlineflag = 0
                if pq==0:
                        yash=cv2.addWeighted(line_testimg,0.5,line_testimg,0.5,0)
                        pq=1

                
        ######################

        cv2.circle(cropped_img,(corro_c,minb),5,(b_col,g_col,r_col),-1)
        cv2.imshow('dot',cropped_img)
        cv2.waitKey(10)

        
        #######drawing dot
        if shape_select==3:		
                cv2.circle(line_testimg,(new_corro_c,new_minb),5,(b_col,g_col,r_col),-1)
                cv2.imshow('line',line_testimg)
                cv2.waitKey(10)

        ########line drawing
        elif shape_select==1:	
                line_testimg=cv2.addWeighted(yash,0.5,yash,0.5,0)
                if draw_lineflag == 1:
                        if draw_resetlineflag == 0:
                                startb=new_minb
                                startc=new_corro_c
                                draw_resetlineflag=1
                        cv2.line(line_testimg,(startc,startb),(new_corro_c,new_minb),(b_col,g_col,r_col),5)
                cv2.circle(line_testimg,(new_corro_c,new_minb),5,(b_col,g_col,r_col),-1)
                cv2.imshow('line',line_testimg)
                cv2.waitKey(10)
        ####eraser
        elif shape_select==2:
                if (new_minb>67) & (new_minb<560) & (new_corro_c>116) & (new_corro_c<706) :
                        cv2.circle(line_testimg,(new_corro_c,new_minb),20,(0,0,0),-1)
                        cv2.imshow('line',line_testimg)
                        cv2.waitKey(10)

        #######rectangledrawing	
        elif shape_select==4:
                line_testimg=cv2.addWeighted(yash,0.5,yash,0.5,0)
                if draw_lineflag == 1:
                        if draw_resetlineflag == 0:
                                print "yash"
                                startb=new_minb
                                startc=new_corro_c
                                draw_resetlineflag=1
                        cv2.rectangle(line_testimg,(startc,startb),(new_corro_c,new_minb),(b_col,g_col,r_col),0)
                        cv2.circle(line_testimg,(new_corro_c,new_minb),5,(b_col,g_col,r_col),-1)
        cv2.imshow('line',line_testimg)
        cv2.waitKey(10)

                
                
        



                
