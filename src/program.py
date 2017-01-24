
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
    flagRun = False
 
signal.signal( signal.SIGTERM , signal_term_handler )


runsFile = "runs.dat" 
runs = 1
if os.path.isfile( runsFile ):
    with open( runsFile , "r" ) as f:
        runs = int( f.read( ).replace( "\n" , "" ) ) + 1
        f.close( )

with open( runsFile , "w" ) as f:
    f.write( str( runs ) )
    f.close( )

print("RUNS = "+str(runs))





class paparazzi :
    screen = None 
    screenrect = None 
    img = None    
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

        
        self.img = pygame.image.load('resources/paparazzi-cover.png')

        pygame.display.update( )

    def __del__( self ):
        print( "QUIT" )
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
        self.screen.blit( self.img , ( 0 , 0 ) )

        #pygame.draw.rect( self.screen , white , self.screenrect , 1 )
        #pygame.draw.line( self.screen , green , ( x1 , y1 ) , ( x2 , y2 ) , 3 )

        pygame.display.update( )


buttonInput = 24
buttonOutput = 23

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
GPIO.setup( buttonInput , GPIO.IN , GPIO.PUD_UP )
GPIO.setup( buttonOutput , GPIO.OUT )
GPIO.output( buttonOutput , GPIO.HIGH )


camera = PiCamera( )
#camera.rotation = 180
#camera.resolution = (800,600)
camera.hflip = True

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
#p = Popen(['raspidmx/pngview/pngview','-b 0x0000','-l 3','./resources/paparazzi-overlay.png'], stdout=PIPE,stdin=PIPE)



flagRun = True

frame=1

print( "LOOP" )
while flagRun:

    paparazzi.test( )

    buttonInputState = GPIO.input( buttonInput )
    if buttonInputState == GPIO.LOW:
        timeStart = time.time( )
        camera.start_preview( )
        #time.sleep( 3 )
        GPIO.output( buttonOutput , GPIO.LOW )
        #fn = "/media/usb/f-" + str( int( time.time( ) * 1000 ) ) + "-" + str( frame ) + ".jpg"
        #fn = "_cache_/f-" + str( int( time.time( ) * 1000 ) ) + "-" + str( frame ) + ".jpg"
        #fn = "/ram/f-" + str(runs).zfill(9)+"-"+str( int( time.time( ) * 1000 ) ) + "-" + str( frame ) + ".jpg"
        fn = "/ram/f-" + str( runs ).zfill( 9 ) + "-" + str( frame ) + "-" + str( int( time.time( ) * 1000 ) ) + ".jpg"
        #fn = "/ram/f-" + str( int( time.time( ) * 1000 ) ) + "-" + str( frame ) + ".data"
        #camera.capture('image.data', 'yuv')
        #camera.capture( fn ,'yuv')
        time.sleep( 1 )
        camera.stop_preview( )
        camera.capture( fn )
        GPIO.output( buttonOutput , GPIO.HIGH )
        frame = frame + 1
        print(time.time( )-timeStart)
        #p.stdin.write("q\n");    
        #p.kill() 
        #o.alpha = 0

    time.sleep( 0.05 )

#p.stdin.write( "q\n" ) ;
#p.stdin.close( )


