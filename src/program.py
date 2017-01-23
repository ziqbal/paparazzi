
from __future__ import division

import os
from os.path import abspath, dirname, join
import sys
import time
import signal
from random import randint

from subprocess import Popen, PIPE, STDOUT

from PIL import Image, ImageDraw, ImageFont

import pygame
from pygame.locals import *

from picamera import PiCamera
import RPi.GPIO as GPIO


print( "BOOT" )

def signal_term_handler( signal , frame ):
    global flagRun
    print "SIGTERM"
    flagRun=False
 
signal.signal( signal.SIGTERM , signal_term_handler )



class paparazzi :
    screen = None 
    screenrect = None 
    
    def __init__( self ):
        disp_no = os.getenv( "DISPLAY" )

        if disp_no:
            print("I'm running under X display = {0}"+format( disp_no ))
        
        drivers = [ "fbcon" , "directfb" , "svgalib" ]

        found = False

        for driver in drivers:
            if not os.getenv( "SDL_VIDEODRIVER" ):
                os.putenv( "SDL_VIDEODRIVER" , driver )

            try:
                print( driver )
                pygame.display.init( )
            except pygame.error:
                print("Driver: {0} failed."+format( driver ))
                continue

            found = True
            break
    
        if not found:
            raise Exception( "No suitable video driver found!" )
        
        size = ( pygame.display.Info( ).current_w , pygame.display.Info( ).current_h )
        self.screenrect = ( 0 , 0 , size[0], size[1]) 
        print("Framebuffer size: %d x %d" % (size[ 0 ] , size[ 1 ] ))
        #self.screen = pygame.display.set_mode( size , pygame.FULLSCREEN )
        self.screen = pygame.display.set_mode( size )
        self.screen.fill( ( 0 , 0 , 0 ) )        
        # Initialise font support
        pygame.font.init( )
        pygame.mouse.set_visible( False )
        pygame.display.update( )

    def __del__( self ):
        print("QUIT")
        camera.close( )
        pygame.quit( )

    def test( self ):
        black = ( 0 , 0 , 0 )
        white = ( 255 , 255 , 255 )
        red = ( 255 , 0 , 0 )
        green = ( 0 , 255 , 0 )

        x1 = randint( 0 , self.screenrect[ 2 ] )
        y1 = randint( 0 , self.screenrect[ 3 ] )
        x2 = randint( 0 , self.screenrect[ 2 ] )
        y2 = randint( 0 , self.screenrect[ 3 ] )

        self.screen.fill( black )

        pygame.draw.rect( self.screen , white , self.screenrect , 1 )
        pygame.draw.line( self.screen , green , ( x1 , y1 ) , ( x2 , y2 ) , 3 )

        pygame.display.update( )



GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
button = 24
GPIO.setup( button, GPIO.IN , GPIO.PUD_UP )


camera = PiCamera( )
camera.rotation = 180
paparazzi = paparazzi( )



#img = Image.open('resources/paparazzi-overlay.png')
#pad = Image.new('RGB', (
#    ((img.size[0] + 31) // 32) * 32,
#    ((img.size[1] + 15) // 16) * 16,
#    ))
#pad.paste(img, (100, 200))

#o = camera.add_overlay(pad.tostring(), size=img.size)
#o.alpha = 0
#o.layer = 3


#raspidmx/pngview

#path = abspath(join(dirname(__file__), '../subdir1/some_executable'))

#p = Popen(['./raspidmx/pngview','-b 0x0000','-l 3','./resources/paparazzi-overlay.png'], stdout=None, stdin=PIPE, stderr=PIPE,shell=True)
p = Popen(['raspidmx/pngview/pngview','-b 0x0000','-l 3','./resources/paparazzi-overlay.png'], stdout=PIPE,stdin=PIPE)



flagRun = True


print( "LOOP" )
while flagRun:
    #print("TICK")
    paparazzi.test( )
    #print("TOCK")

    button_state = GPIO.input( button )
    if button_state == GPIO.LOW:
        #o.alpha = 128
        camera.start_preview( )
        time.sleep( 3 )
        camera.stop_preview( )
        p.stdin.write("q\n");    
        #p.kill() 
        #o.alpha = 0

    time.sleep( 0.1 )


p.stdin.close()


