#Paint Project
#Tailai Wang,ICS 3U-07
#December 13th, 2016-December 27th, 2017
#Welcome to Skyrim Paint!
"""Skyrim Paint is an MS Paint recreation with an Elder Scrolls V: Skyrim
Theme. It includes many different tools you can use to create art on your
computer. With many stickers directly from the game, amazing background music
featuring number one hits along with Skyrim Classics, this program is an amazing
purchase if you are a skyrim fan. Create fan art, recreate battles, or even
just doodle in your spare time! All for the low, low, price of a small loan
of a million dollars!"""
#Enjoy this product of hard work! :)
#Make sure to read all comments especially triple quotation marks

"""Major Note: I didn't know how collidepoint could be used on my toolbox
if i set each tool to its own variable until later, so my initial toolbox uses
long if statements while my stamp boxes use collidepoint"""
from pygame import* #all pygame files require this 
from pygame.locals import* #Positions and "tings"
from random import* #shuffle and randint and such things
from math import* #funnily enough i dont think i used this...?
import tkinter as tk #TKINTER stuff for dialog boxes
from tkinter import filedialog
import pygame 
import os #used to center screen

pygame.init() #sound
pygame.mixer.init() #sound
pygame.mixer.pre_init(22050,-16,2,2048) #sound 

root=tk.Tk() #tkinter
root.withdraw()

inf=display.Info() #setting screen to middle, exactly like the example
w,h=inf.current_w,inf.current_h
os.environ['SDL_VIDEO_WINDOW_POS']='25,25'
screen=display.set_mode((w-50,h-50),NOFRAME)
for x in range(0,screen.get_width(),10):
    draw.line(screen,(0,0,255),(x,0),(x,screen.get_height()))
display.flip()

screen=display.set_mode((1200,700))#screen size
loadingScreen=image.load("images/loadingScreen.png")
loadingScreen=transform.scale(loadingScreen,(1200,700))
screen.blit(loadingScreen,(0,0))
display.flip()
#the loading screen sits there until everything loads in
                                 

#########################PRESET VARIABLES########################

tool="pencil" #Defaults 
tool2="eraser"
toolText="" 
description=""
description2=""
description3=""
toolTitleA="Brush" #default tools
toolTitleB="Eraser"
cursor=None #cursor icon in stamps
cursorB=False #cursor boolean in stamps
cSongIndex=0 #First song
paused=False #song boolean
colour=(0,0,0)#Default for colours 
colour2=(111,111,111)
sizeRad=5 #Default radius for circles
points = [] #points for freeform tool

########################ALL DEF FUNCTIONS#########################
"""*NOTE* "c" in functions means colour, r means radius"""
"""In the highligther,pencileraser, brush and eraser functions, there
is a for loop for i in range(1,dist+1). This for loop divides the distance
between (mx,my) and (omx,omy) into even portios, so that you can blit the
appropriate amount of brusheads or draw the appropriate amount of circles"""
def pencil(c): #omx and omy are placeholders
    draw.line(screen,(c),(omx,omy),(mx,my),1)

def brush(r,c):  #adjustable radius using scroll
    bx=mx-omx #x distance
    by=my-omy #y distance
    dist=int(sqrt(bx**2+by**2)) #distance formula, making sure it draws smoothly
    for i in range(1,dist+1):
        #all functions with this for loop divide the dist into even sections 
        dotX1=int(omx+i*bx/dist) #horizontal shift
        dotY1=int(omy+i*by/dist) #vertical shift
        draw.circle(screen,(c),(dotX1,dotY1),r) #centered at dotX1,dotY1

def eraser(r): #adjustable scroll radius
    dx=mx-omx #same as brush
    dy=my-omy
    dist=int(sqrt(dx**2+dy**2)) #distance formula makes sure it draws smoothly
    for i in range(1,dist+1):
        dotX=int(omx+i*dx/dist) #horizontal shift
        dotY=int(omy+i*dy/dist) #vertical shift
        draw.circle(screen,(255,255,255),(dotX,dotY),r)
def pencilEraser(): #alpha surface eraser (gives you eraserhead feel)
    dx=mx-omx #same as brush
    dy=my-omy
    dist=int(sqrt(dx**2+dy**2)) #distance formula
    for i in range(1,dist+1):
        dotX=int(omx+i*dx/dist)#horizontal shift
        dotY=int(omy+i*dy/dist) #vertical shift
        screen.blit(eraserHead,(dotX-18,dotY-15))

def highlighter(): #utilizes alpha surface
    dx=mx-omx
    dy=my-omy
    dist=int(sqrt(dx**2+dy**2))
    if omx!=mx or omy!=my: #detecting mouse movemenet
        if mb[0]==1 or mb[2]==1: #detecting click
            for i in range(1,dist+1): #same as brush and eraser
                dotX=int(omx+i*dx/dist)
                dotY=int(omy+i*dy/dist)
                screen.blit(brushHead,(dotX-18,dotY-15)) #blitting subsurface
    

def spray(r,c): #adjustable radius using scroll
    x=r//2 #variable in for loop
    #speed depends on size of circle 
    for i in range(x): #Makes it faster
        sx=randint(-r,r) #random x in square
        sy=randint(-r,r) #random y in square
        if hypot(sx,sy)<=r: #if it falls on eq'n of circle
            screen.set_at((sx+mx,sy+my),c) #setting


def freeFormShape(c): #draw shapes with your own points
    if leftClick and canvas.collidepoint(mx,my): #one click only
        point=evt.pos #get mx,my of click
        points.append(point) #adds to list
        draw.circle(screen,(c),evt.pos,1) #draws a circle on the spot
    if rightClick and tool2=="freeform": #to join the points together
        if len(points)>1: #only works for 2 or more point
            draw.polygon(screen,c,points,2) #draws polygon to join
            del points[:] #clears list
                    
                

def fill(c): 
    mainColour=screen.get_at((mx,my)) #where the mouse was clicked
    pointList=[(mx,my)] #list of points
    usedPointSet=set() #set of used points: no doubles, no order
    while len(pointList)>0: #runs while length of points is greater than 0
        pixel=pointList.pop() #current pixel is last value in pointList
        if mainColour==screen.get_at(pixel) and pixel not in usedPointSet:
            #if the pixel hasnt been used yet
            screen.set_at(pixel,c) #setting pixel to selected colour
            pointList.append((pixel[0]+1,pixel[1])) #checks every direction
            pointList.append((pixel[0]-1,pixel[1]))
            pointList.append((pixel[0],pixel[1]+1))
            pointList.append((pixel[0],pixel[1]-1))
        usedPointSet.add(pixel) #adding the pixel to usedPointSet

def drawLine(c): #cmx,cmy found in event loop
    screen.blit(shapeBack,(250,125)) #So you can only draw one thing
    draw.line(screen,(c),(cmx,cmy),(mx,my),2)

def drawRect(c): #cmx,cmy found in event loop
    screen.blit(shapeBack,(250,125)) #only draws once
    draw.rect(screen,(c),(cmx,cmy,mx-cmx,my-cmy),2)

def drawFilledRect(c): #same as drawRect(), just with a filled interior
    screen.blit(shapeBack,(250,125))
    draw.rect(screen,(c),(cmx,cmy,mx-cmx,my-cmy),0)

def drawFilledEllipse(c):
    screen.blit(shapeBack,(250,125)) #only draws once
    ellipse2Rect=Rect(cmx,cmy,mx-cmx,my-cmy)
    ellipse2Rect.normalize() #makes it an ellipse
    draw.ellipse(screen,(c),(ellipse2Rect))

def drawEmptyEllipse(c):
    screen.blit(shapeBack,(250,125)) #only draws once
    ellipseRect=Rect(cmx,cmy,mx-cmx,my-cmy) #ellipse is just a rect
    ellipseRect.normalize() #makes it an ellipse: found it on stackoverflow
    if ellipseRect.w<(sizeRad*2) or ellipseRect.h<(sizeRad*2):
        drawFilledEllipse(colour) #call filled function
    else:
        draw.ellipse(screen,(c),(ellipseRect),sizeRad) #unfilled
        
            
def saveToFile(): 
    file=filedialog.asksaveasfilename()#using tkinter
    if file!=None and (".png" or ".jpg" or ".bmp" or ".jpeg" or ".tiff") in file: #invalid file names
        image.save(screen.subsurface(canvas),file) #saving it to file



def loadFile(): #using tkinter dialong to open file, thanks Karl
    #Open any image or saved canvas! 
    openfilename=filedialog.askopenfilename()
    screen.set_clip(canvas) #setting clip
    if openfilename!=None and (".png" or ".jpg" or ".bmp" or ".jpeg" or ".tiff") in openfilename:
        screen.blit(transform.scale(image.load(openfilename),(700,475)),(250,125)) #blitting file to canvas
        screen.set_clip(None) #resetting canvas
         

def resetScreen(): #redraws canvas
    draw.rect(screen,(255,255,255),(250,125,700,475),0)
    del points[:] #clearing possible freeform points 
    
def drawBlackBorder(): #Left-Click Toolbox Border
    for a in range(4): #draws the borders on top half
        draw.line(screen,(0,0,0),(50,125+a*55),(50,175+a*55),2)
        draw.line(screen,(0,0,0),(50,125+a*55),(100,125+a*55),2)
        draw.line(screen,(0,0,0),(110,125+a*55),(160,125+a*55),2)
        draw.line(screen,(0,0,0),(110,125+a*55),(110,175+a*55),2)
    draw.line(screen,(0,0,0),(175,180),(225,180),2) #highlighter lines
    draw.line(screen,(0,0,0),(175,180),(175,230),2)
    draw.line(screen,(0,0,0),(175,235),(175,285),2)#pencilEraser
    draw.line(screen,(0,0,0),(175,235),(225,235),2)
    draw.line(screen,(0,0,0),(175,290),(225,290),2) #free form
    draw.line(screen,(0,0,0),(175,290),(175,340),2)
    draw.line(screen,(0,0,0),(175,60),(225,60),2) #dropper
    draw.line(screen,(0,0,0),(175,60),(175,110),2) 

def drawBlackBorder2(): #Right-Click Toolbox Border
    for b in range(4): #draws the borders on bottom half
        draw.line(screen,(0,0,0),(100,125+b*55),(100,175+b*55),2)
        draw.line(screen,(0,0,0),(50,175+b*55),(100,175+b*55),2)
        draw.line(screen,(0,0,0),(110,175+b*55),(160,175+b*55),2)
        draw.line(screen,(0,0,0),(160,125+b*55),(160,175+b*55),2)
    draw.line(screen,(0,0,0),(225,180),(225,230),2) #highlighter
    draw.line(screen,(0,0,0),(175,230),(225,230),2)
    draw.line(screen,(0,0,0),(175,285),(225,285),2)#pencilEraser
    draw.line(screen,(0,0,0),(225,235),(225,285),2)
    draw.line(screen,(0,0,0),(175,340),(225,340),2) #free form
    draw.line(screen,(0,0,0),(225,290),(225,340),2)
    draw.line(screen,(0,0,0),(175,110),(225,110),2) #dropper
    draw.line(screen,(0,0,0),(225,60),(225,110),2)
        
def drawStampBorder(): #Left-Click Stampbox Border
    for d in range(8): #covers top half of left click stamps
        draw.line(screen,(0,0,0),(270+d*80,610),(345+d*80,610),2)
        draw.line(screen,(0,0,0),(270+d*80,610),(270+d*80,685),2)
        
def drawStampBorder2(): #Right-Click Stampbox Border
    for e in range(8): #covers bottom half of right click stamps
        draw.line(screen,(0,0,0),(270+e*80,685),(345+e*80,685),2)
        draw.line(screen,(0,0,0),(345+e*80,610),(345+e*80,685),2)

        

#########################DRAGON STAMPS##################################
dragon1=image.load("images/dragon1.png") #Just loading, nothing to see
dragon1=transform.scale(dragon1,(135,95))
dragon2=image.load("images/dragon2.png")
dragon2=transform.scale(dragon2,(128,102))
dragon3=image.load("images/dragon3.png")
dragon3=transform.scale(dragon3,(205,200))
dragon4=image.load("images/dragon4.png")
dragon4=transform.scale(dragon4,(150,98))
#########################BEAST STAMPS####################################
beast1=image.load("images/beast1.png") #Just loading,nothing to see
beast1=transform.scale(beast1,(150,66))
beast2=image.load("images/beast2.png")
beast2=transform.scale(beast2,(175,150))
beast3=image.load("images/beast3.png")
beast3=transform.scale(beast3,(180,140))
beast4=image.load("images/Trump.png")
beast4=transform.scale(beast4,(100,100))
question=image.load("images/questionMark.png")
########################LOGO AND BACKGROUND############################
bg=image.load("images/background.jpg") #Mountain Background
screen.blit(bg,(0,0))
cP=image.load("images/colors.jpg") #colour box
screen.blit(cP,(15,535))
draw.rect(screen,(0,0,0),(15,535,225,155),2)
#######################################################################

canvas=Rect(250,125,700,475) #700x475 canvas
draw.rect(screen,(255,255,255),canvas) #drawing pad
stampBack=screen.subsurface(canvas).copy()


font.init() #fonts
algerFont=font.SysFont("Algerian",75) #Title Font
algerFont2=font.SysFont("Algerian",25) #Sub Title Font
algerFont3=font.SysFont("Algerian",11)#description font
algerFont4=font.SysFont("Algerian",15) #Info font
txtPic=algerFont.render("Skyrim Paint",True,(111,111,111)) #title
colText1=algerFont2.render("Colour 1",True,(111,111,111)) 
colText2=algerFont2.render("Colour 2",True,(111,111,111))
screen.blit(txtPic,(357,27)) #blitting to screen

############################STAMP BOXES################################
for w in range (8): 
    draw.rect(screen,(255,255,255),(270+w*80,610,75,75)) #drawing stampboxes
drawStampBorder()
drawStampBorder2()
    
screen.blit(transform.scale(dragon1,(60,60)),(280,615)) #dragon 1
dragon1Rect=Rect(270,610,75,75)
screen.blit(transform.scale(dragon2,(60,60)),(360,615)) #dragon 2
dragon2Rect=Rect(350,610,75,75)
screen.blit(transform.scale(dragon3,(60,60)),(440,615)) #dragon 3
dragon3Rect=Rect(430,610,75,75)
screen.blit(transform.scale(dragon4,(60,60)),(515,615)) #dragon 4
dragon4Rect=Rect(510,610,75,75)
screen.blit(transform.scale(beast1,(60,60)),(600,615))  #beast 1
beast1Rect=Rect(590,610,75,75)
screen.blit(transform.scale(beast2,(60,60)),(680,615))  #beast 2
beast2Rect=Rect(670,610,75,75)
screen.blit(transform.scale(beast3,(60,60)),(755,615))  #beast 3
beast3Rect=Rect(750,610,75,75)
screen.blit(transform.scale(question,(60,60)),(835,615)) #Trump
beast4Rect=Rect(830,610,75,75)
#############################TOOL BOXES###############################
for i in range (4): #Toolbox 
    draw.rect(screen,(255,255,255),(50,i*55+125,50,50)) #8 Tools
    draw.rect(screen,(255,255,255),(110,i*55+125,50,50))
draw.rect(screen,(255,255,255),(175,180,50,50)) #Highlighter
draw.rect(screen,(255,255,255),(175,235,50,50)) #pencilEraser
draw.rect(screen,(255,255,255),(175,60,50,50)) #dropper

penLogo=image.load("images/pencil.png") #pencil logo
penLogo=transform.scale(penLogo,(60,60))
screen.blit(penLogo,(50,120)) 
sprayLogo=image.load("images/spray.png") #spray logo
sprayLogo=transform.scale(sprayLogo,(40,40))
screen.blit(sprayLogo,(55,185))
eraserLogo=image.load("images/eraser.png") #eraser logo
eraserLogo=transform.scale(eraserLogo,(40,40))
screen.blit(eraserLogo,(115,130))
brushLogo=image.load("images/brush.png") #Brush logo
brushLogo=transform.scale(brushLogo,(40,40))
screen.blit(brushLogo,(115,190))
draw.rect(screen,(255,255,255),(178,127,46,47))
buttonLogo=image.load("images/button.png") #button logo
buttonLogo=transform.scale(buttonLogo,(50,50))
screen.blit(buttonLogo,(175,128))
draw.rect(screen,(0,0,0),(175,125,50,50),2) #border of clear button
highlighterLogo=image.load("images/highlighter.png") #highlighter logo
highlighterLogo=transform.scale(highlighterLogo,(40,40))
screen.blit(highlighterLogo,(183,185))
fillBucketLogo=image.load("images/fillBucket.png") #fill bucket logo
fillBucketLogo=transform.scale(fillBucketLogo,(40,40))
screen.blit(fillBucketLogo,(115,295))
pencilEraserLogo=image.load("images/pencilEraser.png")#pencilEraser logo
pencilEraserLogo=transform.scale(pencilEraserLogo,(40,40))
screen.blit(pencilEraserLogo,(180,235))
dropperLogo=image.load("images/dropper.png") #eyeDropper Logo
dropperLogo=transform.scale(dropperLogo,(40,40))
screen.blit(dropperLogo,(180,65))
                       
saveRect=Rect(985,195,70,70) #save logo and rectangle
draw.rect(screen,(255,255,255),(saveRect))
draw.rect(screen,(0,0,0),(saveRect),2)
saveLogo=image.load("images/save.png")
saveLogo=transform.scale(saveLogo,(60,60))
screen.blit(saveLogo,(990,200))
loadRect=Rect(1085,195,70,70) #load logo and rectangle
draw.rect(screen,(255,255,255),(loadRect)) 
draw.rect(screen,(0,0,0),(loadRect),2)
loadLogo=image.load("images/load.png")
loadLogo=transform.scale(loadLogo,(60,60))
screen.blit(loadLogo,(1090,200))


draw.line(screen,(0,0,0),(110,235),(160,285),2) #Line tool

draw.rect(screen,(0,0,0),(53,238,20,20),2) #Unfilled Rect
draw.line(screen,(0,0,0),(100,235),(50,285),2) #Dividing line
draw.rect(screen,(0,0,0),(76,262,20,20)) #Filled Rect

draw.ellipse(screen,(0,0,0),(53,293,25,25),2) #unfilled Ellipse
draw.line(screen,(0,0,0),(50,340),(100,290),2)
draw.ellipse(screen,(0,0,0),(76,312,25,25)) #filled ellipse

undoRect=Rect(50,60,50,50) #undo and redo rectangles, I utilized collidepoint 
redoRect=Rect(110,60,50,50)
undos=[] #lists
undos.append(screen.subsurface(canvas).copy()) #The blank screen
redos=[]
draw.rect(screen,(255,255,255),undoRect) #drawing the physical rectangles
draw.rect(screen,(255,255,255),redoRect)
draw.rect(screen,(0,0,0),(50,60,50,50),2)
draw.rect(screen,(0,0,0),(110,60,50,50),2)
undoLogo=image.load("images/undo.png") #undo logo
undoLogo=transform.scale(undoLogo,(40,40))
screen.blit(undoLogo,(55,64))
redoLogo=image.load("images/redo.png") #redo logo
redoLogo=transform.scale(redoLogo,(40,40))
screen.blit(redoLogo,(115,64))

pauseRect=Rect(965,75,70,70) #Pause Rect and logo
draw.rect(screen,(255,255,255),pauseRect)
pause1Logo=image.load("images/pause1.png")
pause2Logo=image.load("images/pause2.png")
pause1Logo=transform.scale(pause1Logo,(65,65)) #Play 
pause2Logo=transform.scale(pause2Logo,(65,65)) #Pause
screen.blit(pause1Logo,(968,77))
draw.rect(screen,(0,0,0),pauseRect,2)

skipRect=Rect(1040,75,70,70) #skip rect and logo
draw.rect(screen,(255,255,255),skipRect)
skipLogo=image.load("images/next.png")
skipLogo=transform.scale(skipLogo,(60,60))
screen.blit(skipLogo,(1045,80))
draw.rect(screen,(0,0,0),skipRect,2)

backRect=Rect(1115,75,70,70) #Back track trect and logo
draw.rect(screen,(255,255,255),backRect)
backLogo=transform.rotate(skipLogo,180)
screen.blit(backLogo,(1120,80))
draw.rect(screen,(0,0,0),backRect,2)

draw.rect(screen,(255,255,255),(175,290,50,50)) #Draw Polygon rectangle
polyLogo=image.load("images/polygon.png")
polyLogo=transform.scale(polyLogo,(40,40))
screen.blit(polyLogo,(180,295))

draw.line(screen,(255,0,0),(50,125),(100,125),2) #default borders
draw.line(screen,(255,0,0),(50,125),(50,175),2) #pencil and eraser
draw.line(screen,(0,255,0),(110,175),(160,175),2)
draw.line(screen,(0,255,0),(160,125),(160,175),2)

drawBlackBorder()
drawBlackBorder2()
                    

###########################LOAD MUSIC###################################
#youtubetomp3.com :) and my own collection of music
file1="Audio/01_Dragonborn.mp3" #From Elder Scrolls V: Skyrim
file2="Audio/02_Sovngarde.mp3" #From Elder Scrolls V: Skyrim
file3="Audio/03_300.mp3" #300 Violin Orchestra, Jorge Quintero
file4="Audio/04_Aqua_Vitae.mp3" #Aqua Vitae, Future World Music
file5="Audio/05_Heart_Of_Courage.mp3" #Heart of Courage, Two Steps From Hell
file6="Audio/Hans Zimmer - Time.mp3"#Hans Zimmer, Time
file7="Audio/Skyrim Music - Secunda (Night 2).mp3" #From Elder Scrolls V:Skyrim
file8="Audio/01 Lighters (feat. Bruno Mars).mp3" #Lighters, Bad Meets Evil
file9="Audio/02 - Just The Way You Are.mp3"#Just The Way You Are, Bruno Mars
file10="Audio/10-the_weeknd-in_the_night.mp3"#In The Night, The Weeknd



music=[] #adding all music to list
music.append(file1) #^
music.append(file2)#^^
music.append(file3)#^^^
music.append(file4)#^^^^
music.append(file5)#^^^^^
music.append(file6)#^^^^^^
music.append(file7)#^^^^^^^
music.append(file8)#^^^^^^^^
music.append(file9)#^^^^^^^^^
music.append(file10)#^^^^^^^^^

shuffle(music) #shuffling music hehe
cSong=music[0] #current song
pygame.mixer.music.load(cSong) #loading to mixer
pygame.mixer.music.play() #playing music
END_MUSIC_EVENT=pygame.USEREVENT+0 #loops music
pygame.mixer.music.set_endevent(END_MUSIC_EVENT)

##############################SUBSURFACES############################
brushHead=Surface((50,50),SRCALPHA) #Highlighter Subsurface
draw.circle(brushHead,(255,255,0,10),(25,25),10) #drawing on subsurface
eraserHead=Surface((50,50),SRCALPHA) #Pencil eraser subsurface
draw.circle(eraserHead,(255,245,252,5),(25,25),10) #drawing on subsurface
############################# EVENT LOOP################################
running=True
while running:
    leftClick=False #leftClick and rightClick are used to prevent accidental drag
    rightClick=False
    mouseUp=False #used in undo redo
    mouseDown=False #used in undo redo
    for evt in event.get():
        if evt.type==QUIT:
            running=False
        if evt.type==KEYDOWN:
            if evt.key==K_ESCAPE:
                running=False #shuts program on ESC
        if evt.type==MOUSEBUTTONDOWN:
            mouseDown=True #undoredo
            shapeBack=screen.subsurface(canvas).copy() #Shape tools and undoredo
            if 250<=mx<=950 and 125<=my<=600: 
                cmx,cmy=mx,my #cmx,cmy used for shapes
            if evt.button==1:
                leftClick=True #Only true for one click
            if evt.button==3:
                rightClick=True #Only true for one click
            if evt.button==4: #Scrolling Up
                if sizeRad>1:
                    sizeRad-=1 #decreases radius
            if evt.button==5: #scrolling Down
                if sizeRad<100:
                    sizeRad+=1 #increases radius
        if evt.type==MOUSEBUTTONUP: #when mouse is lifted
            back1=screen.subsurface(canvas).copy()#used for undo redo
            mouseUp=True #undo redo
#---------------------------------------------------------------------
    mx,my=mouse.get_pos() #getting positions
    mb   =mouse.get_pressed() #getting pressed
#--------------------------------SET CANVAS----------------------------
    if canvas.collidepoint(mx,my) and mb[0]==1: #setting the canvas clip
        screen.set_clip(canvas) 
#-------------------------Picking colours (Left & Right)-----------------
    if 15<=mx<=241 and 535<=my<=691 and (leftClick or rightClick):
        if mb[0]==1:
            colour=screen.get_at((mx,my))  #picking left click colour
        if mb[2]==1:
            colour2=screen.get_at((mx,my)) #picking right click colour
#----------------------------Tool Selection----------------------------
    ###READ MAJOR NOTE AT THE TOP
    """The first if statement checks if the mouse is on the button,
    the next two if statements check if and how its being clicked.
    After being clicked, the necessary tool and border changes are made,
    then new highlights are drawn"""
    if 175<=mx<=225 and 130<=my<=180 and leftClick: #Clear screen
        resetScreen()
    if saveRect.collidepoint(mx,my) and leftClick: #save to file
        saveToFile()
    if loadRect.collidepoint(mx,my) and leftClick: #load file/image
        loadFile()
    if 955<=mx<=1255 and 30<=my<=50 and leftClick: #Open Music
        openMusic=filedialog.askopenfilename()
        if openMusic!=None and (".mp3" or ".mp4") in openMusic:
            cSong=openMusic
            pygame.mixer.music.load(cSong)
            pygame.mixer.music.play()

    if 50<=mx<=100 and 125<=my<=175:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="pencil"
            toolTitleA="Pencil"
            draw.line(screen,(255,0,0),(50,125),(100,125),2) #setting highlight
            draw.line(screen,(255,0,0),(50,125),(50,175),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="pencil"
            toolTitleB="Pencil"
            draw.line(screen,(0,255,0),(50,175),(100,175),2)
            draw.line(screen,(0,255,0),(100,175),(100,125),2)
                       
    if 110<=mx<=160 and 125<my<=175:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="eraser"
            toolTitleA="Eraser"
            draw.line(screen,(255,0,0),(110,125),(160,125),2)
            draw.line(screen,(255,0,0),(110,125),(110,175),2)
        if rightClick:
            drawBlackBorder2() #Removing current highlight
            drawStampBorder2()
            tool2="eraser"
            toolTitleB="Eraser"
            draw.line(screen,(0,255,0),(160,125),(160,175),2) #setting highlight
            draw.line(screen,(0,255,0),(110,175),(160,175),2)
            
    if 50<=mx<=100 and 180<=my<=230:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="spray"
            toolTitleA="Spray"
            draw.line(screen,(255,0,0),(50,180),(50,230),2)
            draw.line(screen,(255,0,0),(50,180),(100,180),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="spray"
            draw.line(screen,(0,255,0),(50,230),(100,230),2)
            draw.line(screen,(0,255,0),(100,180),(100,230),2)
          
    if 110<=mx<=160 and 180<=my<=230:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="brush"
            toolTitleA="Brush"
            draw.line(screen,(255,0,0),(110,180),(110,230),2)
            draw.line(screen,(255,0,0),(110,180),(160,180),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="brush"
            toolTitleB="Brush"
            draw.line(screen,(0,255,0),(110,230),(160,230),2)
            draw.line(screen,(0,255,0),(160,180),(160,230),2)
    if 50<=mx<=100 and 235<=my<=285:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="rectangle"
            toolTitleA="EmptyRectangle"
            draw.line(screen,(255,0,0),(50,235),(50,285),2)
            draw.line(screen,(255,0,0),(50,235),(100,235),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="filledRectangle"
            toolTitleB="Filled Rectangle"
            draw.line(screen,(0,255,0),(50,285),(100,285),2)
            draw.line(screen,(0,255,0),(100,235),(100,285),2)
    if 110<=mx<=160 and 235<=my<=285:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="line"
            toolTitleA="Line"
            draw.line(screen,(255,0,0),(110,235),(110,285),2)
            draw.line(screen,(255,0,0),(110,235),(160,235),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="line"
            toolTitleB="Line"
            draw.line(screen,(0,255,0),(160,235),(160,285),2)
            draw.line(screen,(0,255,0),(110,285),(160,285),2)
    if 50<=mx<=100 and 290<=my<=340:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="emptyEllipse"
            toolTitleA="Empty Ellipse"
            draw.line(screen,(255,0,0),(50,290),(50,340),2)
            draw.line(screen,(255,0,0),(50,290),(100,290),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="filledEllipse"
            toolTitleB="Filled Ellipse"
            draw.line(screen,(0,255,0),(100,290),(100,340),2)
            draw.line(screen,(0,255,0),(50,340),(100,340),2)
    if 110<=mx<=160 and 290<=my<=340:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="fill"
            toolTitleA="Fill Bucket"
            draw.line(screen,(255,0,0),(110,290),(110,340),2)
            draw.line(screen,(255,0,0),(110,290),(160,290),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="fill"
            toolTitleB="Fill Bucket"
            draw.line(screen,(0,255,0),(160,290),(160,340),2)
            draw.line(screen,(0,255,0),(160,340),(110,340),2)
    if 175<=mx<=225 and 180<=my<=230:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="highlighter"
            toolTitleA="Highlighter"
            draw.line(screen,(255,0,0),(175,180),(225,180),2)
            draw.line(screen,(255,0,0),(175,180),(175,230),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="highlighter"
            toolTitleB="Highlighter"
            draw.line(screen,(0,255,0),(225,180),(225,230),2)
            draw.line(screen,(0,255,0),(175,230),(225,230),2)
    if 175<=mx<=225 and 235<=my<=285:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="pencilEraser"
            toolTitleA="Pencil Eraser"
            draw.line(screen,(255,0,0),(175,235),(175,285),2)
            draw.line(screen,(255,0,0),(175,235),(225,235),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="pencilEraser"
            toolTitleB="Pencil Eraser"
            draw.line(screen,(0,255,0),(175,285),(225,285),2)
            draw.line(screen,(0,255,0),(225,235),(225,285),2)
    #you need both right and left click selected on freeform to use it
    if 175<=mx<=225 and 290<=my<340:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool = "freeform"
            toolTitleA="Free Form Shape A"
            points = [] #empties points to draw fresh
            draw.line(screen,(255,0,0),(175,290),(175,340),2)
            draw.line(screen,(255,0,0),(175,290),(225,290),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="freeform"
            toolTitleB="Free Form Shape B"
            draw.line(screen,(0,255,0),(175,340),(225,340),2)
            draw.line(screen,(0,255,0),(225,290),(225,340),2)
    if 175<=mx<=225 and 60<=my<=110:
        if leftClick:
            drawBlackBorder()
            drawStampBorder()
            tool="eyeDropper"
            toolTitleA="Eye Dropper"
            draw.line(screen,(255,0,0),(175,60),(225,60),2)
            draw.line(screen,(255,0,0),(175,60),(175,110),2)
        if rightClick:
            drawBlackBorder2()
            drawStampBorder2()
            tool2="eyeDropper"
            toolTitleB="Eye Dropper"
            draw.line(screen,(0,255,0),(175,110),(225,110),2)
            draw.line(screen,(0,255,0),(225,60),(225,110),2)
                      
#---------------------------------STAMP SELECTION------------------
    """The first if statement detects if there is no stamp on the cursor and if
    the mouse is on the box. If the user clicks, the appropraite borders are
    drawn and the cursor is replaced with the stamp. The stamp then remains
    the cursor until the user drops it off on the canvas (See 861-873)
    We also change the titles based on which stamp is on it."""

    if dragon1Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=dragon1
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="dragon1"
            toolTitleA="Dragon 1"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(270,610),(345,610),2) #highlights
            draw.line(screen,(255,0,0),(270,610),(270,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=dragon1
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="dragon1"
            toolTitleB="Dragon 1"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(270,685),(345,685),2)
            draw.line(screen,(0,255,0),(345,610),(345,685),2)
            stampBack=screen.copy()
    if dragon2Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=dragon2
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="dragon2"
            toolTitleA="Dragon 2"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(350,610),(425,610),2)
            draw.line(screen,(255,0,0),(350,610),(350,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=dragon2
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="dragon2"
            toolTitleB="Dragon 2"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(350,685),(425,685),2)
            draw.line(screen,(0,255,0),(425,610),(425,685),2)
            stampBack=screen.copy()
    if dragon3Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=dragon3
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="dragon3"
            toolTitleA="Dragon 3"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(430,610),(505,610),2)
            draw.line(screen,(255,0,0),(430,610),(430,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=dragon3
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="dragon3"
            toolTitleB="Dragon 3"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(430,685),(505,685),2)
            draw.line(screen,(0,255,0),(505,610),(505,685),2)
            stampBack=screen.copy()
    if dragon4Rect.collidepoint(mx,my) and cursor==False:
        if leftClick:
            cursor=dragon4
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="dragon4"
            toolTitleA="Dragon 4"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(510,610),(585,610),2)
            draw.line(screen,(255,0,0),(510,610),(510,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=dragon4
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="dragon4"
            toolTitleB="Dragon 4"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(510,685),(585,685),2)
            draw.line(screen,(0,255,0),(585,610),(585,685),2)
            stampBack=screen.copy()
    if beast1Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=beast1
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="beast1"
            toolTitleA="Beast 1"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(590,610),(665,610),2)
            draw.line(screen,(255,0,0),(590,610),(590,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=beast1
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="beast1"
            toolTitleB="Beast 1"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(590,685),(665,685),2)
            draw.line(screen,(0,255,0),(665,610),(665,685),2)
            stampBack=screen.copy()
    if beast2Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=beast2
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="beast2"
            toolTitleA="Beast 2"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(670,610),(745,610),2)
            draw.line(screen,(255,0,0),(670,610),(670,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=beast2
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="beast2"
            toolTitleB="Beast 2"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(670,685),(745,685),2)
            draw.line(screen,(0,255,0),(745,610),(745,685),2)
            stampBack=screen.copy()
    if beast3Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=beast3
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="beast3"
            toolTitleA="Beast 3"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(750,610),(825,610),2)
            draw.line(screen,(255,0,0),(750,610),(750,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=beast3
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="beast3"
            toolTitleB="Beast 3"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(750,685),(825,685),2)
            draw.line(screen,(0,255,0),(825,610),(825,685),2)
            stampBack=screen.copy()
    if beast4Rect.collidepoint(mx,my) and cursorB==False:
        if leftClick:
            cursor=beast4
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool="beast4"
            toolTitleA="Mystery Stamp"
            cursorB=True
            drawStampBorder()
            drawBlackBorder()
            draw.line(screen,(255,0,0),(830,610),(905,610),2)
            draw.line(screen,(255,0,0),(830,610),(830,685),2)
            stampBack=screen.copy()
        if rightClick:
            cursor=beast4
            cw=cursor.get_width()
            ch=cursor.get_height()
            tool2="beast4"
            toolTitleB="Mystery Stamp"
            cursorB=True
            drawStampBorder2()
            drawBlackBorder2()
            draw.line(screen,(0,255,0),(830,685),(905,685),2)
            draw.line(screen,(0,255,0),(905,610),(905,685),2)
            stampBack=screen.copy()
    if cursor: #if the cursor is a stamp
        if (leftClick or rightClick) and canvas.collidepoint(mx,my):
            screen.set_clip(None) #the hardest part
            screen.blit(stampBack,(0,0)) #perma blitting the stampback
            screen.set_clip(canvas) #reset clip
            screen.blit(cursor,(mx-cw/2,my-ch/2)) #blitting the actual stamp
            cursor=False #resetting variables
            cursorB=False
            mouse.set_visible(True) #reshowing the mouse
        else:
            screen.blit(stampBack,(0,0)) #blitting the stampBack
            mouse.set_visible(False) #making sure mouse isnt visible
            screen.blit(cursor,(mx-cw/2,my-ch/2)) #temp blit with cursor
            
    
#-----------------------------Main Drawing Functions------------------
    """calling functions based on selected tool and which mouse event"""
    if 250<=mx<=950 and 125<=my<=600 and (mb[0]==1 or mb[2]==1): #Checking if on canvas
            screen.set_clip(canvas)
            if mb[0]==1: #Left Click
                if tool=="pencil":
                    pencil(colour)
                if tool=="spray":
                    spray(sizeRad,colour)
                if tool=="eraser":
                    eraser(sizeRad)
                if tool=="line":
                    drawLine(colour)
                if tool=="rectangle":
                    drawRect(colour)
                if tool=="filledRectangle":
                    drawFilledRect(colour)
                if tool=="emptyEllipse":
                    drawEmptyEllipse(colour)
                if tool=="brush":
                    brush(sizeRad,colour)
                if tool=="fill":
                    fill(colour)
                if tool=="highlighter":
                    highlighter()
                if tool=="pencilEraser":
                    pencilEraser()
                if tool=="eyeDropper":
                    colour=screen.get_at((mx,my)) #takes pixel colour 
            if mb[2]==1: #Right Click
                if tool2=="pencil":
                    pencil(colour2)
                if tool2=="spray":
                    spray(sizeRad,colour2)
                if tool2=="eraser":
                    eraser(sizeRad)
                if tool2=="line":
                    drawLine(colour2)
                if tool2=="rectangle":
                    drawRect(colour2)
                if tool2=="filledRectangle":
                    drawFilledRect(colour2)
                if tool2=="filledEllipse":
                    drawFilledEllipse(colour2)
                if tool2=="brush":
                    brush(sizeRad,colour2)
                if tool2=="fill":
                    fill(colour2)
                if tool2=="highlighter":
                    highlighter()
                if tool2=="pencilEraser":
                    pencilEraser()
                if tool2=="eyeDropper":
                    colour2=screen.get_at((mx,my)) #takes pixel colour

#----------------Setting the info box text--------
    """Hovering over the box changes the info box in the bottom right
    if the user isnt hovering over a box, it displays credits"""
    toolText="Skyrim Paint"
    description=" By Tailai Wang, ICS 3U"
    description2=" Based on Elder Scrolls V: Skyrim"
    description3=""
    if 50<=mx<=100 and 125<=my<=175: 
        toolText="Pencil"
        description=" Free draw using the standard"
        description2=" HB pencil"
        description3=""
    if 110<=mx<=160 and 125<=my<=175:
        toolText="Eraser"
        description=" Erase anything completely"
        description2=" with your selected radius"
        description3=""
    if 50<=mx<=100 and 180<=my<=230:
        toolText="Spray"
        description=" Spray/Airbrush a circular"
        description2=" region with your selected radius"
        description3=" and colour"
    if 110<=mx<=160 and 180<=my<=230:
        toolText="Brush"
        description=" Free draw using the classic"
        description2=" brush with your selected radius"
        description3=""
    if 50<=mx<=100 and 235<=my<=285:
        toolText="Rectangle"
        description=" Left-Click to draw unfilled rectangle"
        description2=" or Right-Click to draw filled ones"
        description3=""
    if 110<=mx<=160 and 235<=my<=285:
        toolText="Line"
        description=" Draw perfectly straight lines"
        description2=" "
        description3=""
    if 50<=mx<=100 and 290<=my<=340:
        toolText="Ellipse"
        description=" Left-Click to draw unfilled ellipses"
        description2=" or Right-Click to draw filled ones"
        description3=""
    if 110<=mx<=160 and 290<=my<=340:
        toolText="Fill Bucket"
        description=" Fill a selected region with"
        description2=" an individual colour"
        description3=""
    if 175<=mx<=225 and 180<=my<=230:
        toolText="Highlighter"
        description=" Free draw with the original"
        description2=" yellow highlighter"
        description3=""
    if 175<=mx<=225 and 235<=my<=285:
        toolText="Pencil Eraser"
        description=" Semi-erase objects with the back"
        description2=" of your HB pencil"
        description3=""
    if 175<=mx<=225 and 130<=my<=180:
        toolText="Clear Screen"
        description=" Reset the canvas"
        description2=""
        description3=""
    if 15<=mx<=241 and 535<=my<=691:
        toolText="Colour Selection"
        description=" Select individual colours for both"
        description2=" tools (left-click and right-click)"
        description3=""
    if 175<=mx<=225 and 290<=my<=340:
        toolText="Free Form"
        description=" Left click to select points then"
        description2=" Right click to watch them join!"
        description3=" (Both clicks must be on)"
    if 175<=mx<=225 and 50<=my<=100:
        toolText="Eye Dropper"
        description=" Click anywhere on the canvas to"
        description2=" select a colour to be yours!"
    if dragon1Rect.collidepoint(mx,my):
        toolText="Dragon 1"
        description=" Beige Dragon Stamp"
        description2=""
        description3=""
    if dragon2Rect.collidepoint(mx,my):
        toolText="Dragon 2" 
        description=" Blue Dragon Stamp"
        description2=""
        description3=""
    if dragon3Rect.collidepoint(mx,my):
        toolText="Dragon 3"
        description=" Large Dragon Stamp"
        description2=""
        description3=""
    if dragon4Rect.collidepoint(mx,my):
        toolText="Dragon 4"
        description=" Wyvern-Dragon Stamp"
        description2=""
        description3=""
    if beast1Rect.collidepoint(mx,my):
        toolText="Beast 1"
        description=" It's a man! No it's a wolf! No!"
        description2=" IT'S A WEREWOLF!"
        description3=""
    if beast2Rect.collidepoint(mx,my):
        toolText="Beast 2"
        description=" It's 'dat boi' Dovahkin!"
        description2=""
        description3=""
    if beast3Rect.collidepoint(mx,my):
        toolText="Beast 3"
        description=" Just your average Villager..."
        description2=""
        description3=""
    if beast4Rect.collidepoint(mx,my):
        toolText="Mystery Stamp"
        description=" Who could it be...?"
        description2=" #NotMyPresident"
        description3=""
    if undoRect.collidepoint(mx,my):
        toolText="Undo"
        description=" Undo the last action"
        description2=""
        description3=""
    if redoRect.collidepoint(mx,my):
        toolText="Redo"
        description=" Redo an action"
        description2=""
        description3=""
    if saveRect.collidepoint(mx,my):
        toolText="Save to File"
        description=" Save the canvas as a loadable image"
        description2=""
        description3=""
    if loadRect.collidepoint(mx,my):
        toolText="Load File"
        description=" Load a file or image you previously"
        description2=" saved"
        description3=""
    if backRect.collidepoint(mx,my):
        toolText="Last Track"
        description="Play the previous track"
        description2=""
        description3=""
    if skipRect.collidepoint(mx,my):
        toolText="Next Track"
        description="Play the next track"
        description2=""
        description3=""
    if pauseRect.collidepoint(mx,my):
        if paused:
            toolText="Unpause"
            description="Unpause the Dank Music"
            description2=""
            description3=""
        else:
            toolText="Pause"
            description="Pause the Dank Music"
            description2=""
            description3=""
    if 955<=mx<=1255 and 30<=my<=50:
        toolText="Now Playing"
        description=" Current Song, Left-Click to select"
        description2=" your own music (.mp3 or .mp4)"
        description3=""
    if 25<=mx<=230 and 350<=my<=490:
        toolText="Colour Info"
        description=" Displays your currently selected"
        description2=" colours and radius"
        description3=" (Adjust the radius by scrolling)"
    if 965<=mx<=1195 and 300<=my<=390:
        toolText="Tool Info"
        description=" Displays your currently selected"
        description2=" tools"
        description3=""
    if 965<=mx<=1195 and 420<=my<=600:
        toolText="Tool Description"
        description=" A description of the tool you are"
        description2=" hovering over will appear here"
        description3=""
    if 965<=mx<=1195 and 610<=my<=685:
        toolText="Mouse Info"
        description=" This shows you your mouse's current"
        description2=" position on the screen"
        description3=""
    
#--------------Resetting Variables/Squares-----------        
    if 250<=mx<=950 and 125<=my<=600:#Checking that mouse is on canvas
        omx,omy=mx,my #Reset, used in pencil
        
    draw.rect(screen,(255,255,255),(25,350,205,140),0) #white rect
    draw.rect(screen,(0,0,0),(25,350,205,140),2)
    draw.rect(screen,(colour),(170,355,40,40),0) #colour 1
    draw.rect(screen,(0,0,0),(170,355,40,40),2)
    draw.rect(screen,(colour2),(170,400,40,40),0) #colour 2
    draw.rect(screen,(0,0,0),(170,400,40,40),2)
    screen.blit(colText1,(35,360)) #colour Text 
    screen.blit(colText2,(35,405)) #colour Text 2
    radiusText=algerFont2.render("Radius:        "+str(sizeRad),True,(111,111,111))
    screen.blit(radiusText,(35,445)) #displaying radius size
    
    draw.rect(screen,(255,255,255),(965,420,230,180)) #info box
    draw.rect(screen,(0,0,0),(964,419,231,181),2) #info box border
    toolText1=algerFont2.render(toolText,True,(111,111,111)) #indicates tool 
    screen.blit(toolText1,(965,420))
    desText=algerFont3.render(description,True,(0,0,0)) #description
    desText2=algerFont3.render(description2,True,(0,0,0)) #description
    desText3=algerFont3.render(description3,True,(0,0,0)) #description
    screen.blit(desText,(965,480))
    screen.blit(desText2,(965,500))
    screen.blit(desText3,(965,520))

    draw.rect(screen,(255,255,255),(965,300,230,90)) #info on current tool
    draw.rect(screen,(0,0,0),(964,299,231,91),2)
    toolTitle1=algerFont4.render("Tool 1:"+str(toolTitleA),True,(0,0,0))
    toolTitle2=algerFont4.render("Tool 2:"+str(toolTitleB),True,(0,0,0))
    screen.blit(toolTitle1,(965,300))
    screen.blit(toolTitle2,(965,340))

    draw.rect(screen,(255,255,255),(955,30,300,20)) #music info box
    draw.rect(screen,(0,0,0),(955,30,300,20),2) #current song
    musicTitle1=algerFont3.render(cSong,True,(0,0,0))
    screen.blit(musicTitle1,(955,32))

    draw.rect(screen,(0,0,0),(canvas),2) #canvas border

    draw.rect(screen,(255,255,255),(965,610,230,75))
    draw.rect(screen,(0,0,0),(965,610,230,75),2)
    posTitle1=algerFont2.render(" Mouse Position",True,(111,111,111))
    posTitle2=algerFont2.render(" "+str(mx)+","+str(my),True,(0,0,0))
    screen.blit(posTitle1,(980,610))
    screen.blit(posTitle2,(1030,645))
    
    
            
#----------------------------Undo/Redo-----------------------
    if canvas.collidepoint(mx,my) and mouseUp: #more info in event loop
        undos.append(back1) #append back1 on mouseUp
    if canvas.collidepoint(mx,my) and (mb[0]==1 or mb[2]==1):
        del redos[:]#clearing redo list
    if undoRect.collidepoint(mx,my) and mb[0]==1 and  mouseDown: #redo
        #more than one element in undo list
        redos.append(screen.subsurface(canvas).copy()) #blank screen
        screen.blit(undos[-1],(250,125)) #blits last element
        undos.pop() #removing last element
        if len(undos)==0:
            undos.append(screen.subsurface(canvas).copy())
    if redoRect.collidepoint(mx,my) and leftClick:
        if len(redos)>0: #more than one in redo list
            undos.append(redos.pop())
            screen.blit(undos[-1],(250,125))
#----------------------Music pause/play/skip/mute-----------
    if pauseRect.collidepoint(mx,my):
        if leftClick:
            if paused: #if the music is already paused
                pygame.mixer.music.unpause()#unpauses music
                paused=False
                draw.rect(screen,(255,255,255),pauseRect) #draws new logo
                draw.rect(screen,(0,0,0),pauseRect,2)
                screen.blit(pause1Logo,(968,77))
            else: #if its playing
                pygame.mixer.music.pause()#pauses music
                paused=True
                draw.rect(screen,(255,255,255),pauseRect)#draws new logo
                draw.rect(screen,(0,0,0),pauseRect,2)
                screen.blit(pause2Logo,(968,77))
    if skipRect.collidepoint(mx,my):#skipping tracks
        if leftClick:
            cSongIndex+=1#cSongIndex indicates position in music list
            if cSongIndex==len(music):#if at the end, moves it back to start
                cSongIndex=0
            cSong=music[cSongIndex]#playing new music
            pygame.mixer.music.load(cSong)
            pygame.mixer.music.play()
    if backRect.collidepoint(mx,my):#Back track
        if leftClick:
            cSongIndex-=1 #cSongIndex indicates position in music list
            if cSongIndex==0-len(music): #if at beggining, move to end
                cSongIndex=0
            cSong=music[cSongIndex] #playing new music
            pygame.mixer.music.load(cSong)
            pygame.mixer.music.play()
#---------------------------Freeform/draw poly----------
    if tool=="freeform": #free form is always on the alert if selected
        freeFormShape(colour)
                    
    screen.set_clip(None) #setting clip
    display.flip() #resetting display
quit() #<---the worst thing ever
