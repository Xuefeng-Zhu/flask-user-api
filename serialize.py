def serialize(object):
    result = {}
    for key in object:
    	if key == "id" or key == "user" or key == "game_info":
    		pass
    	else:
       	    result[key] = object[key]
    return result