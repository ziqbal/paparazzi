
import os
import pygame
import time
import random

class paparazzi :
    screen = None ;
    
    def __init__( self ):
        disp_no = os.getenv( "DISPLAY" )

        if disp_no:
            print "I'm running under X display = {0}".format( disp_no )
        
        drivers = [ "fbcon" , "directfb" , "svgalib" ]

        found = False

        for driver in drivers:
            if not os.getenv( "SDL_VIDEODRIVER" ):
                os.putenv( "SDL_VIDEODRIVER" , driver )

            try:
                print( driver )
                pygame.display.init( )
            except pygame.error:
                print "Driver: {0} failed.".format( driver )
                continue

            found = True
            break
    
        if not found:
            raise Exception( "No suitable video driver found!" )
        
        size = ( pygame.display.Info( ).current_w , pygame.display.Info( ).current_h )
        print "Framebuffer size: %d x %d" % (size[ 0 ] , size[ 1 ] )
        self.screen = pygame.display.set_mode( size , pygame.FULLSCREEN )
        self.screen.fill( ( 0 , 0 , 0 ) )        
        # Initialise font support
        pygame.font.init( )
        pygame.mouse.set_visible( False )
        pygame.display.update( )

    def __del__( self ):
        pygame.quit( )

    def test( self ):
        black = ( 0 , 0 , 0 )
        self.screen.fill( black )
        pygame.display.update( )

paparazzi = paparazzi( )
paparazzi.test( )
time.sleep( 3 )

