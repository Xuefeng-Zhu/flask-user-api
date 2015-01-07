def serialize(object):
    result = {}
    for key in object:
    	if key == "id" or key == "user" or key == "game_info":
    		pass
    	else:
       	    result[key] = object[key]
    return result

def profile_search_serialize(profiles):
	result = []
	for profile in profiles:
		result.append({
			'profile_id': str(profile.id),
			'username': profile.username,
			'profile_icon': profile.profile_icon,
			'school': profile.school
			})
	return result