
from __future__ import division

import sys
import time
import signal
import pygame
from pygame.locals import *


def signal_term_handler(signal, frame):
    global flagRun
    print "SIGTERM"
    flagRun=False
 
signal.signal(signal.SIGTERM, signal_term_handler)



print( "BOOT" )

pygame.init( )

infoObject = pygame.display.Info( )

size = width , height = ( infoObject.current_w , infoObject.current_h )

screenrect = ( 0 , 0 , infoObject.current_w , infoObject.current_h ) 

black = 0 , 0 , 0
white = 255 , 255 , 255

screen = pygame.display.set_mode( ( infoObject.current_w , infoObject.current_h ) , pygame.FULLSCREEN )
pygame.mouse.set_visible(False)

resource = pygame.image.load( "resources/Vincent_Willem_van_Gogh_128.jpg" )



resourceorigrect = resource.get_rect( )

wr = resourceorigrect.size[ 0 ]
hr = resourceorigrect.size[ 1 ]
ws = infoObject.current_w
hs = infoObject.current_h

ar = wr/hr

print(ar)

h=hs
w=h*ar
x=(w-ws)/2
y=0
if w<ws:
    print("w>ws")
    w=ws
    h=w/ar
    x=0
    y=(h-hs)/2

w=int(round(w))
h=int(round(h))
x=int(round(x))
y=int(round(y))

print((x,y))    


#print(resourceorigrect.size[1])

resource = pygame.transform.scale(resource, (w,h))
#resource = pygame.transform.scale( resource, size )

resourcerect = resource.get_rect( )

flagRun = True

print( "LOOP" )
while flagRun:
    #print( "TICK" )
    for event in pygame.event.get( ):
        if event.type == pygame.QUIT:
            flagRun=False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                flagRun=False

    screen.fill( black )
    #screen.blit( resource , (100,200), (10,10,30,20) )
    screen.blit( resource , (0,0), ( x,y , infoObject.current_w , infoObject.current_h ) )
    pygame.draw.rect( screen , white , screenrect , 1 )
    pygame.display.flip( )
    #print( "TOCK" )
    time.sleep(1)
    #flagRun=False

pygame.quit( )
sys.exit( )