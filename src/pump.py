
import json
import os
import functions
import requests

functions.log( "PUMP" )

import time

config = None

confPath = "/opt/paparazzi.json" 

if os.path.isfile( confPath ):
    with open( confPath ) as json_data:
        config = json.load( json_data )
        #print( config )

else:
    functions.log( "No Config!!" )
    exit


firstfilepath = None

filespath = config["filespath"] 
for index, filename in enumerate(sorted(os.listdir(filespath))):
    if filename.endswith('.jpg'):
        firstfilepath = config["filespath"] + filename
        break


functions.log("found "+firstfilepath)


files = {'file': open(firstfilepath, 'rb')}

r = requests.post(config["serverpushurl"]+"?key="+config["key"], files=files)
functions.log(r.text)