from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import sys
#import random
import time
from math import cos, sin
w=900
h=700
loop=True
count=0
text=0
move_limit=17
time_limit=12

###########################################
player_x=627  #Initial start position
player_y=277
radius = 22  # radius

goal_x1,goal_y1,goal_x2,goal_y2=510,310,550,350
############################################
start_time = time.time()
paused_time = 0
paused = False

RETRY_BUTTON_LOCATION = (20, h - 50)
PAUSE_BUTTON_LOCATION = (w/2, h - 50)
EXIT_BUTTON_LOCATION = (w - 50, h - 50)

# draw functions
def draw_retry_button(x, y, color = (0.0, 1.0, 0.0)):
   draw_line(x, y, x + 20, y - 20, color)
   draw_line(x, y, x + 20, y + 20, color)
   draw_line(x, y, x + 50, y, color)


def draw_pause_button(x, y, color = (1.0, 0.0, 1.0)):
   draw_line(x + 10, y + 20, x + 10, y - 20, color)
   draw_line(x - 10, y + 20, x - 10, y - 20, color)


def draw_play_button(x, y, color = (1.0, 0.0, 1.0)):
   draw_line(x - 10, y + 20, x - 10, y - 20, color)
   draw_line(x - 10, y + 20, x + 10, y, color)
   draw_line(x - 10, y - 20, x + 10, y, color)


def draw_exit(x, y, color = (1.0, 0.0, 0.0)):
   draw_line(x - 20, y + 20, x + 20, y - 20, color)
   draw_line(x - 20, y - 20, x + 20, y + 20, color)


# MidPoint Line Drawing Algorithm
def draw_points(x, y, color = (1, 1, 1), size=2):
   glColor3fv(color)
   glPointSize(size)
   glBegin(GL_POINTS)
   glVertex2f(x,y)
   glEnd()


def to_zone0(zone, x, y):
   if zone == 0: return (x,y)
   elif zone == 1: return (y,x)
   elif zone == 2: return (y,-x)
   elif zone == 3: return (-x,y)
   elif zone == 4: return (-x,-y)
   elif zone == 5: return (-y,-x)
   elif zone == 6: return (-y,x)
   elif zone == 7: return (x,-y)
   else: raise ValueError("Zone must be in [0, 7]")


def to_zoneM(zone, x, y):
   if zone == 0: return (x,y)
   elif zone == 1: return (y,x)
   elif zone == 2: return (-y,x)
   elif zone == 3: return (-x,y)
   elif zone == 4: return (-x,-y)
   elif zone == 5: return (-y,-x)
   elif zone == 6: return (y,-x)
   elif zone == 7: return (x,-y)
   else: raise ValueError("Zone must be in [0, 7]")


def find_zone(x1,y1,x2,y2):
   dx = x2 - x1
   dy = y2 - y1
   if abs(dx) > abs(dy):
       if dx>=0 and dy>=0: return 0
       elif dx>=0 and dy<=0: return 7
       elif dx<=0 and dy>=0: return 3
       elif dx<=0 and dy<=0: return 4
   else :
       if dx>=0 and dy>=0: return 1
       elif dx<=0 and dy>=0: return 2
       elif dx<=0 and dy<=0: return 5
       elif dx>=0 and dy<=0: return 6


def draw_line(x1, y1, x2, y2, color):
   zone = find_zone(x1,y1,x2,y2)
   x1,y1 = to_zone0(zone, x1, y1)
   x2,y2 = to_zone0(zone, x2, y2)
  
   dx = x2 - x1
   dy = y2 - y1
  
   d = 2*dy - dx
   incrE = 2*dy
   incrNE = 2*(dy - dx)

   x = x1
   y = y1
   x0, y0 = to_zoneM(zone, x, y)
  
   draw_points(x0, y0, color)
   while x < x2:
       if d <= 0:
           d = d + incrE
           x = x + 1
       else:
           d = d + incrNE
           x = x + 1
           y = y + 1
       x0, y0 = to_zoneM(zone, x, y)
      
       draw_points(x0, y0, color)
       
    #######################################################
    
# MidPoint Circle Drawing Algorithm

def convert_zone(x, y, zone):
    if zone == 0:
        return x, y
    if zone == 1:
        return y, x
    if zone == 2:
        return -y, x
    if zone == 3:
        return -x, y
    if zone == 4:
        return -x, -y
    if zone == 5:
        return -y, -x
    if zone == 6:
        return y, -x
    if zone == 7:
        return x, -y

def midPointCircleAlgorithm(radius, center_x, center_y, color):
    # Initial d
    d = 1 - radius
    x = 0
    y = radius

    while x < y:
        for i in range(8):
            x_, y_ = convert_zone(x, y, i)
            draw_points(x_ + center_x, y_ + center_y, color, 4)

        if d < 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * x - 2 * y + 5
            x += 1
            y -= 1
       
    #######################################################
    
def map(i,j):
    glColor3f(0.5, 0.5, 0.5) 
    glBegin(GL_QUADS)
    glVertex2f(10+(i*40), 25+(j*40))  # Bottom-left vertex
    glVertex2f(45+(i*40), 25+(j*40))   # Bottom-right vertex
    glVertex2f(45+(i*40), 60+(j*40))    # Top-right vertex
    glVertex2f(10+(i*40), 60+(j*40))   # Top-left vertex 
    glEnd() 
    
    
    
def draw_base(i,j):
    glColor3f(0.5, 0.5, 0.5) 
    glBegin(GL_QUADS)
    glVertex2f(410+(i*50), 60+(j*50))  # Bottom-left vertex
    glVertex2f(450+(i*50), 60+(j*50))   # Bottom-right vertex
    glVertex2f(450+(i*50), 100+(j*50))    # Top-right vertex
    glVertex2f(410+(i*50), 100+(j*50))   # Top-left vertex 
    glEnd() 
    
    glColor3f(0.45, 0.4, 0.4) 
    glBegin(GL_QUADS)
    glVertex2f(405+(i*50), 55+(j*50))  # Bottom-left vertex
    glVertex2f(410+(i*50), 60+(j*50))   # Bottom-right vertex
    glVertex2f(410+(i*50), 100+(j*50))    # Top-right vertex
    glVertex2f(405+(i*50), 95+(j*50)) # Top-left vertex 
    glEnd()    
    glColor3f(0.45, 0.4, 0.4) 
    glBegin(GL_QUADS)
    glVertex2f(405+(i*50), 55+(j*50))  # Bottom-left vertex
    glVertex2f(445+(i*50), 55+(j*50))   # Bottom-right vertex
    glVertex2f(450+(i*50), 60+(j*50))    # Top-right vertex
    glVertex2f(410+(i*50), 60+(j*50))   # Top-left vertex 
    glEnd() 
        
        
def boarder(i,j):
    color=(1,.3,.3)
    glColor3f(.9,.1,.1)
    glBegin(GL_QUADS)
    glVertex2f(410+(i*50), 60+(j*50))  # Bottom-left vertex
    glVertex2f(450+(i*50), 60+(j*50))   # Bottom-right vertex
    glVertex2f(460+(i*50), 70+(j*50))    # Top-right vertex
    glVertex2f(420+(i*50), 70+(j*50))   # Top-left vertex 
    glEnd() 

    glColor3f(1,0,0)
    glBegin(GL_QUADS)
    glVertex2f(420+(i*50), 70+(j*50))  # Bottom-left vertex
    glVertex2f(460+(i*50), 70+(j*50))   # Bottom-right vertex
    glVertex2f(460+(i*50), 110+(j*50))    # Top-right vertex
    glVertex2f(420+(i*50), 110+(j*50))   # Top-left vertex 
    glEnd() 
    glColor3f(.9,.1,.1)     
    glBegin(GL_QUADS)
    glVertex2f(410+(i*50), 100+(j*50))  # Bottom-left vertex
    glVertex2f(410+(i*50), 60+(j*50))   # Bottom-right vertex
    glVertex2f(420+(i*50), 70+(j*50))    # Top-right vertex
    glVertex2f(420+(i*50), 110+(j*50))   # Top-left vertex 
    glEnd() 
    draw_line(410+(i*50), 60+(j*50), 450+(i*50), 60+(j*50), color)
    draw_line(460+(i*50), 70+(j*50), 450+(i*50), 60+(j*50), color)
    draw_line(410+(i*50), 60+(j*50), 420+(i*50), 70+(j*50), color)
    draw_line(420+(i*50), 70+(j*50), 460+(i*50), 70+(j*50), color)
    
    draw_line(420+(i*50), 70+(j*50), 460+(i*50), 70+(j*50), color)
    draw_line(460+(i*50), 70+(j*50), 460+(i*50), 110+(j*50), color)
    draw_line(420+(i*50), 110+(j*50), 460+(i*50), 110+(j*50), color)
    draw_line(420+(i*50), 110+(j*50), 420+(i*50), 70+(j*50), color)

    draw_line(410+(i*50), 100+(j*50), 410+(i*50), 60+(j*50), color)
    draw_line(420+(i*50), 70+(j*50), 410+(i*50), 60+(j*50), color)
    draw_line(420+(i*50), 110+(j*50), 420+(i*50), 70+(j*50), color)
    draw_line(420+(i*50), 110+(j*50), 410+(i*50), 100+(j*50), color)    
def goal():
    color=(1,1,0.4)
    draw_line(510, 210, 550, 210, color)
    draw_line(550, 210, 550, 250, color)
    draw_line(510, 250, 550, 250, color)
    draw_line(510, 210, 510, 250, color)
    draw_line(510, 210, 550, 250, color)
    draw_line(510, 250, 550, 210, color)
    
    #map
    glColor3f(1,1,0) 
    glBegin(GL_QUADS)
    glVertex2f(10+(2*40), 25+(3*40))  # Bottom-left vertex
    glVertex2f(45+(2*40), 25+(3*40))   # Bottom-right vertex
    glVertex2f(45+(2*40), 60+(3*40))    # Top-right vertex
    glVertex2f(10+(2*40), 60+(3*40))   # Top-left vertex 
    glEnd() 
    
    glColor3f(0,1,0) 
    glBegin(GL_QUADS)
    glVertex2f(10+(2*40), 25+(5*40))  # Bottom-left vertex
    glVertex2f(45+(2*40), 25+(5*40))   # Bottom-right vertex
    glVertex2f(45+(2*40), 60+(5*40))    # Top-right vertex
    glVertex2f(10+(2*40), 60+(5*40))   # Top-left vertex 
    glEnd() 

    draw_filled_circle(187,202,18)

def draw_filled_box(x1, y1, x2, y2, color=(0, 0, 0)):
    #Square Circumference using midpoint line drawing algorithm
    draw_line(x1, y1, x1, y2, color)
    draw_line(x1, y2, x2, y2, color)  
    draw_line(x2, y2, x2, y1, color)  
    draw_line(x2, y1, x1, y1, color) 
    
    #xolor
    color=(0, 1, 0)
    glColor3fv(color)
    glBegin(GL_QUADS)
    glVertex2f(x1, y1) 
    glVertex2f(x2, y1) 
    glVertex2f(x2, y2) 
    glVertex2f(x1, y2) 
    glEnd()

def draw_filled_circle(player_x,player_y,radius):

    color=(0, 0, 1)

    midPointCircleAlgorithm(radius, player_x, player_y, color)
    glColor3f(0.0, 0.0, 1.0)  # Blue color for the filled circle
    glBegin(GL_POLYGON)
    num_segments = 100  # Increase or decrease for smoother or fewer segments
    for i in range(num_segments):
        theta = 2.0 * 3.1415926 * i / num_segments
        x = radius * cos(theta) + player_x  # Adjust the center x-coordinate
        y = radius * sin(theta) + player_y  # Adjust the center y-coordinate
        glVertex2f(x, y)
    glEnd()
    
##################################################################
        
def draw_timer(x, y, elapsed_time, color=(0, 0, 0)):
    global paused, loop
    if paused:
        text_color = (1, 0, 0)  # Red when paused
    else:
        text_color = (0, 0, 0)  # black when running

    glColor3fv(text_color)
    glRasterPos2f(x-5, y - 10)
    text = f"Timer: {elapsed_time:.2f}s"

    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))  # Changed font style and increased size


def display():
    global move_limit, text,count,loop,start_time, paused_time, paused,player_x,player_y,radius,goal_x1,goal_y1,goal_x2,goal_y2

    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, w, 0, h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()    

    for j in range(8):
        for i in range(8):
            draw_base(i,j)
            

    for i in range(8):
        for j in range(8):            
            if i==0 and j!=0 and j!=1 and j!=7:
                boarder(i,j)
                map(i,j)
            elif i==1 and j!=3 and j!=4 and j!=5 and j!=7:
                boarder(i,j)
                map(i,j)
            elif i==2 and j!=1 and j!=2 and j!=3 and j!=5:
                boarder(i,j)
                map(i,j)
            elif i==3 and j!=1 and j!=3 and j!=4 and j!=5 and j!=6:
                boarder(i,j)
                map(i,j)
            elif i==4 and j!=1 and j!=2 and j!=3 and j!=4 and j!=6:
                boarder(i,j)
                map(i,j)
            elif i==5 and j!=2 and j!=4 and j!=5 and j!=6:
                boarder(i,j)
                map(i,j)
            elif i==6 and j!=0 and j!=2 and j!=3 and j!=4:
                boarder(i,j)
                map(i,j)
            elif i==7 and j!=0 and j!=6 and j!=7:
                boarder(i,j)
                map(i,j)
    goal()
    draw_retry_button(RETRY_BUTTON_LOCATION[0], RETRY_BUTTON_LOCATION[1])
    draw_exit(EXIT_BUTTON_LOCATION[0], EXIT_BUTTON_LOCATION[1])

    # Draw the timer just under the pause button
    draw_timer(PAUSE_BUTTON_LOCATION[0] - 50, PAUSE_BUTTON_LOCATION[1] - 50, paused_time)

    if not paused:
        draw_pause_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    else:
        draw_play_button(PAUSE_BUTTON_LOCATION[0], PAUSE_BUTTON_LOCATION[1])
    draw_filled_circle(player_x,player_y,radius)
    draw_filled_box(goal_x1,goal_y1,goal_x2,goal_y2)
    
    if loop==True:
        if 510<player_x<550 and 210<player_y<250:
            print("WIN🎉") 
            loop=False  
            text=1
            
        elif count>=move_limit  or paused_time>time_limit: #LIMIT (17 is lowest 2 extra move given)
            print("GAME OVER")
            loop=False
            text=2
            
    if text!=0:
        paused=True #game over ba jitle timer/game pause
        text_show(text)
        
    glColor3f(0,0,0)
    glRasterPos2f(100, 580)
    t=f"Move Left:{move_limit-count}"
    for char in t:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))
    glutSwapBuffers()
       
def text_show(a):
    glColor3f(1,0,0)
    glRasterPos2f(350, 500)
    if a==1:
        text="WINNER!!!"
    elif a==2:
        text="GAME OVER!!!"
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_TIMES_ROMAN_24, ord(char))

def update_timer(value):
    global start_time, paused_time, paused

    if start_time is not None and not paused:
        elapsed_time = time.time() - start_time
        paused_time = elapsed_time

    glutPostRedisplay()
    glutTimerFunc(100, update_timer, 0)


def keyboard(key, x, y):
    global text,start_time, paused_time, paused,loop,player_x,player_y,radius,goal_x1,goal_x2,goal_y1,goal_y2,count

    if key == b' ' and loop==True:
        if not paused:
            paused = True
            print("Pause")
        else:
            start_time = time.time() - paused_time
            paused = False
            print("Resumed")
    elif key== b'R' or key== b"r":
            start_time=time.time()
            # paused_time = 0
            print("Play again")
            text=0
            paused = False 
            loop=True
            player_x=627 
            player_y=277
            radius = 22 
            goal_x1,goal_y1,goal_x2,goal_y2=510,310,550,350
            count=0
            update_timer(1) #reset timer
            display()
            glutPostRedisplay()

        
def keyboard_special_keys(key, _, __):
    global count,loop,paused,goal_x1,goal_y1,goal_x2,goal_y2,player_x,player_y,radius

    if not paused and loop==True and count<move_limit:
        if key == GLUT_KEY_LEFT:
            if 250<=goal_y2<=350 and goal_x2==500:
                pass
            elif goal_y2==400 and goal_x2==600:
                pass
            elif goal_x2==550 and 150<=goal_y2<=200:
                pass
            elif (goal_x2==700 and goal_y2==350) or (goal_x2==600 and goal_y2==300) or (goal_x2==650 and goal_y2==200) or (goal_x2==750 and goal_y2==250):
                pass
            elif  (goal_x1-40<player_x and goal_y1<player_y<goal_y2) and (((360<player_y<400 or 260<player_y<300) and player_x-40<550) or (210<player_y<250 and player_x-40<450) or (160<player_y<200 and player_x-40<600)):
                pass 
            else:
                count+=1
                if goal_x1>player_x and goal_x1<player_x+40 and goal_x2<player_x+80 and goal_y2>player_y>goal_y1:
                    player_x-=50
                    draw_filled_circle(player_x,player_y,radius)
                    
                goal_x1 -= 50
                goal_x2 -= 50
                draw_filled_box(goal_x1,goal_y1,goal_x2,goal_y2)
        elif key == GLUT_KEY_RIGHT: 
            if goal_x2==700 and 350<=goal_y2<=400:
                pass
            elif goal_x2==750 and 200<=goal_y2<=300:
                pass
            elif goal_x2==650 and goal_y2<=150:
                pass
            elif (goal_x2==550 and goal_y2==200) or (goal_x2==500 and goal_y2==300) or (goal_x2==600 and goal_y2==350) or (goal_x2==650 and goal_y2==250):
                pass
            elif  (goal_x2+40>player_x and goal_y1<player_y<goal_y2) and ((310<player_y<350 and player_x+40>610) or (260<player_y<300 and player_x+40>760) or (210<player_y<250 and player_x+40>660) or (110<player_y<150 and player_x+40>660)):
                pass 
            else:
                count+=1
                if goal_x2<player_x and goal_x1>player_x-80 and goal_x2>player_x-40 and goal_y2>player_y>goal_y1:
                    player_x+=50
                    draw_filled_circle(player_x,player_y,radius)
                goal_x1 += 50
                goal_x2 += 50
                draw_filled_box(goal_x1,goal_y1,goal_x2,goal_y2)
        elif key == GLUT_KEY_DOWN:
            if goal_x2==500 and goal_y2==250:
                pass
            elif 550<=goal_x2<=650 and goal_y2==150:
                pass
            elif 700<=goal_x2<=750 and goal_y2==200:
                pass
            elif (goal_x2==650 and goal_y2==400) or (goal_x2==550 and goal_y2==350) or (goal_x2==700 and goal_y2==300) or (goal_x2==600 and goal_y2==250):
                pass
            elif  (goal_y1-40<player_y and goal_x1<player_x<goal_x2) and ((460<player_x<500 and player_y-40<200) or (620<player_x<650 and player_y-40<100) or (550<player_x<600 and player_y-40<210) or (650<player_x<700 and player_y-40<250)):
                pass    
            else:
                count+=1
                if goal_y1>player_y and goal_y1<player_y+40<goal_y2 and goal_x2>player_x>goal_x1:
                    player_y-=50
                    draw_filled_circle(player_x,player_y,radius)
                goal_y1 -= 50
                goal_y2 -= 50
                draw_filled_box(goal_x1,goal_y1,goal_x2,goal_y2)
        elif key == GLUT_KEY_UP:
            if (500<=goal_x2<=550 and goal_y2==350): 
                pass
            elif  (goal_y2+40>player_y and goal_x1<player_x<goal_x2) and ((560<player_x<600 and player_y+40>400) or (710<player_x<750 and player_y+40>300) or (610<player_x<650 and player_y+40>300) or (510<player_x<550 and player_y+40>250)):
                pass    
            elif (goal_y2==400 and 600<=goal_x2<=700):
                pass
            elif (goal_x2==750 and goal_y2==300):
                pass  
            elif (goal_x2==600 and goal_y2==150) or (goal_x2==700 and goal_y2==200) or (goal_x2==650 and goal_y2==300) or (goal_x2==550 and goal_y2==250):
                pass
            else:
                count+=1
                if goal_y2<player_y and goal_y1<player_y-40<goal_y2 and goal_x2>player_x>goal_x1:
                    player_y+=50
                    draw_filled_circle(player_x,player_y,radius)
                goal_y1 += 50
                goal_y2 += 50
                draw_filled_box(goal_x1,goal_y1,goal_x2,goal_y2)

        glutPostRedisplay()

def mouseListener(button, state, x, y):
    global text,count,loop, paused,start_time,player_x,player_y,radius,goal_x1,goal_y1,goal_x2,goal_y2
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        if (20< x < 72 and 47 < y < 71):
            print("Play again")
            text=0
            paused = False 
            loop=True
            start_time=time.time() 
            player_x=627 
            player_y=277
            radius = 22 
            goal_x1,goal_y1,goal_x2,goal_y2=510,310,550,350
            count=0
            update_timer(1)
            display()
            glutPostRedisplay()
            
        elif 438 < x < 461 and 29 < y < 72 and loop==True:
            if not paused:
                paused = True
                print("Pause")
            else:
                start_time = time.time() - paused_time
                paused = False
                print("Resume")
        elif 831 < x < 872 and 33 < y < 70:
            print("Goodbye")
            glutLeaveMainLoop()
                      

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(w, h)
glutCreateWindow(b"Box Quest")
glClearColor(.9, .9, .9, 1.0)
gluOrtho2D(0, w, 0, h)
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutMouseFunc(mouseListener)
glutSpecialFunc(keyboard_special_keys)
glutTimerFunc(100, update_timer, 0)
glutMainLoop()