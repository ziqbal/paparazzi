
from __future__ import division

import os
from os.path import abspath, dirname, join
import shutil
import sys
import time
import signal
from random import randint

from subprocess import call,Popen, PIPE, STDOUT

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



if not os.path.isfile( "/tmp/latest.jpg" ):
    shutil.copyfile( "resources/latest.jpg" , "/tmp/latest.jpg" )


runsFile = "runs.dat" 
runs = 1
if os.path.isfile( runsFile ):
    with open( runsFile , "r" ) as f:
        runs = int( f.read( ).replace( "\n" , "" ) ) + 1
        f.close( )

with open( runsFile , "w" ) as f:
    f.write( str( runs ) )
    f.close( )

print( "RUN " + str( runs ) )

class paparazzi :

    screen = None 
    screenrect = None 
    img = None    
    imgLatest = None    

    def __init__( self ):

        disp_no = os.getenv( "DISPLAY" )

        if disp_no:
            print( "X display = {0}" + format( disp_no ) )
        
        drivers = [ "fbcon" , "directfb" , "svgalib" ]

        found = False

        for driver in drivers:
            if not os.getenv( "SDL_VIDEODRIVER" ):
                os.putenv( "SDL_VIDEODRIVER" , driver )

            try:
                #print( driver )
                pygame.display.init( )
                pygame.font.init()

            except pygame.error:
                print( "Driver: {0} failed." + format( driver ) )
                continue

            found = True
            break
    
        if not found:
            raise Exception( "No video driver found!" )
        
        size = ( pygame.display.Info( ).current_w , pygame.display.Info( ).current_h )

        self.screenrect = ( 0 , 0 , size[ 0 ] , size[ 1 ] ) 

        #print( "resolution : %d x %d" % (size[ 0 ] , size[ 1 ] ) )

        self.screen = pygame.display.set_mode( size ,  pygame.HWSURFACE)

        pygame.mouse.set_visible( False )

        self.img = pygame.image.load( "resources/paparazzi-cover.png" ).convert()
        self.imgLatest = pygame.image.load( "/tmp/latest.jpg" ).convert()

        self.imgLatest = pygame.transform.scale(self.imgLatest, (60*2,80*2))

        pygame.display.update( )

    def __del__( self ):

        print( "QUIT" )
        camera.close( )
        pygame.quit( )

    def updateLatest( self ):
        self.imgLatest = pygame.image.load( "/tmp/latest.jpg" )
        self.imgLatest = pygame.transform.scale(self.imgLatest, (60*2,80*2)).convert()       

    def show3( self ):

        white = ( 255 , 255 , 255 )
        black = ( 0 , 0 , 0 )

        self.screen.fill( black )

        #pygame.draw.rect( self.screen , white , ( 100,100,100,200)  )


        myfont = pygame.font.SysFont("monospace", 600)
        label = myfont.render("3", 1, (255,255,0))
        self.screen.blit(label, (100, 100))        

        pygame.display.update( )

    def show2( self ):
        white = ( 255 , 255 , 255 )
        black = ( 0 , 0 , 0 )

        self.screen.fill( black )

        myfont = pygame.font.SysFont("monospace", 600)
        label = myfont.render("2", 1, (255,255,0))
        self.screen.blit(label, (100, 100))       

        pygame.display.update( )

    def show1( self ):
        white = ( 255 , 255 , 255 )
        black = ( 0 , 0 , 0 )
        self.screen.fill( black )

        myfont = pygame.font.SysFont("monospace", 600)
        label = myfont.render("1", 1, (255,255,0))
        self.screen.blit(label, (100, 100))       

        pygame.display.update( )


    def clear( self ):
        black = ( 0 , 0 , 0 )
        self.screen.fill( black )
        pygame.display.update( )        


             

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

        self.screen.blit( self.imgLatest , ( 100,200 ) )

        pygame.draw.line( self.screen , green , ( x1 , y1 ) , ( x2 , y2 ) , 3 )

        pygame.display.update( )


buttonInput = 24
buttonOutput = 23

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )
GPIO.setup( buttonInput , GPIO.IN , GPIO.PUD_UP )
GPIO.setup( buttonOutput , GPIO.OUT )
GPIO.output( buttonOutput , GPIO.HIGH )


camera = PiCamera( )
camera.resolution = (600,800)
camera.hflip = True
camera.framerate = 30
camera.start_preview( alpha=0 )
#camera.preview.alpha = 0

paparazzi = paparazzi( )


buttonInputStateLast = False
frame = 1

flagRun = True

print( "LOOP" )

while flagRun:

    paparazzi.test( )

    buttonInputState = GPIO.input( buttonInput )

    if buttonInputState == GPIO.LOW:

        if buttonInputStateLast == True:
            time.sleep( 0.05 )
            continue

        timeStart = time.time( )

        camera.preview.alpha = 192

        paparazzi.show3( )

        time.sleep( 1 )

        paparazzi.show2( )

        time.sleep( 1 )

        paparazzi.show1( )

        time.sleep( 1 )

        GPIO.output( buttonOutput , GPIO.LOW )

        camera.preview.alpha = 255 

        time.sleep( 1 )

        call( [ "scripts/sfx-shutter.sh" ] )

        fn = "/tmp/f-" + str( runs ).zfill( 3 ) + "-" + str( frame ).zfill( 6 ) + "-" + str( int( time.time( ) * 1000 ) ) + ".jpg"
        camera.capture_sequence( [ "/tmp/latest.jpg" ] , use_video_port = True )
        shutil.copyfile( "/tmp/latest.jpg" , fn )

        GPIO.output( buttonOutput , GPIO.HIGH )

        paparazzi.clear( )
        camera.preview.alpha = 0

        frame = frame + 1

        buttonInputStateLast = True

        paparazzi.updateLatest( )

        print( time.time( ) - timeStart )

    else:

        buttonInputStateLast = False



    time.sleep( 0.05 )



