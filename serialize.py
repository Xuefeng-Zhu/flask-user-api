def serialize(object):
    result = {}
    for key in object:
    	if key != "id":
       	    result[key] = object[key]
    return result