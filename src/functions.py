


#    frm = inspect.stack()[1]
#    mod = inspect.getmodule(frm[0])

def log( msg ):

	with open("_cache_/default.log", "a") as myfile:
	    myfile.write(msg+"\n")