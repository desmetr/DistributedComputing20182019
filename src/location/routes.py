from flask import Flask, render_template, jsonify, redirect, request
from location.key import key
from location import locationApp
from location.forms import LocationForm
import requests
import imghdr
import urlsConfig

search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
details_url = "https://maps.googleapis.com/maps/api/place/details/json"
photos_url = "https://maps.googleapis.com/maps/api/place/photo"
template_embed_url = "https://www.google.com/maps/embed/v1/place?key=" + key + "&q="
# geo_location_url = "https://maps.googleapis.com/maps/api/js?key=" + key + "&callback=initMap"         

IN_RADIUS = False
ICON = False
current_user = None

@locationApp.route("/location", methods=["GET", "POST"])
def showOthersOnMap():
	global current_user

	# Structure of an address:
	#	[id, username, lat, lng]
	# can be extended to
	#	[id, username, lat, lng, icon]
	
	current_user_id = request.cookies.get("currentSessionCookie")
	if current_user_id:
		# Get current user information
		current_user = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id)).json()['data']

		addresses = getAllAddressesFromUsers()

		locationScriptStart = open("static/locationScriptStart.js", "r")
		locationScript = locationScriptStart.read()
		locationScriptStart.close()

		for _, address in enumerate(addresses):
			# Don't wanna see yourself, so excluded.
			print(current_user['id'] != address[0])
			if current_user['id'] != address[0]:
				lat = address[2]
				lng = address[3]

				currentVegetables = requests.get(urlsConfig.URLS['garden_url'] + "/" + str(address[0]) + "/getVegetables")
				currentFruits = requests.get(urlsConfig.URLS['garden_url'] + "/" + str(address[0]) + "/getFruits")
				currentHerbs = requests.get(urlsConfig.URLS['garden_url'] + "/" + str(address[0]) + "/getHerbs")

				if ICON:
					locationScript += """
						icon: '""" + address[4] + """',
						"""

				contentString = getContentString(address, currentVegetables.json(), currentFruits.json(), currentHerbs.json())
						
				locationScript += """
					var contentString = """ + contentString + """;
					var infoWindow""" + str(address[0]) + """ = new google.maps.InfoWindow({
						position: {lat: """ + str(lat) + """, lng: """ + str(lng) + """},
						content: contentString,"""

				if not IN_RADIUS:
					locationScript += """
						map: map,
						"""

				locationScript += """
					})

					"""

				contentString = ""
			
				if IN_RADIUS:
					locationScript += """
						if (checkRadius(currentPso.lat, currentPos.lng, """ + str(lat) + """, """ + str(lng) + """, zoomLevel))
							marker""" + str(address[0]) + """.setMap(null);
						else
							marker""" + str(address[0]) + """.setMap(map);
					"""

		locationScriptEnd = open("static/locationScriptEnd.js", "r")
		locationScript += locationScriptEnd.read()
		locationScriptEnd.close()

		f = open("static/locationScript.js", "w+")
		f.write(locationScript)
		f.close()

		return render_template("location.html")
	else:
		return redirect(urlsConfig.URLS['login_url'])

@locationApp.route("/callback/<id>", methods=["GET", "POST", "OPTIONS"])
def callback(id):
	print("You clicked on user with id ", id)
	response = requests.get(urlsConfig.URLS['single_user_url'], params={'user_id': str(id)})

	responseData = response.json()["data"]
	return redirect(urlsConfig.URLS['garden_url'])

def getAllAddressesFromUsers():
	addresses = []

	response = requests.get(urlsConfig.URLS['users_url'])

	for user in response.json():
		addresses.append([user["id"], user["username"], user["lat"], user["lng"]])

	return addresses

def getContentString(address, currentVegetables, currentFruits, currentHerbs):
	global current_user

	contentString = """
		'<div id="content">' +
		'User: <b>""" + address[1] + """</b>' +
		'<br>Vegetables:' +
		'<ul>' +
		"""

	for vegetable in currentVegetables:
		contentString += """'<li><b>""" + str(vegetable[0]) + """</b> (""" + str(vegetable[2]) + """)</li>'+"""

	contentString += """
		'</ul>'+
		'Fruits:'+
		'<ul>'+
	"""

	for fruit in currentFruits:			
		contentString += """'<li><b>""" + str(fruit[0]) + """</b> (""" + str(fruit[2]) + """)</li>'+"""

	contentString += """
		'</ul>'+
		'Herbs:'+
		'<ul>'+
	"""

	for herb in currentHerbs:
		contentString += """'<li><b>""" + str(herb[0]) + """</b> (""" + str(herb[2]) + """)</li>'+"""

	contentString += """'</ul>'+"""

	# TODO correct url
	contentString += """
		'<a href=\"""" + urlsConfig.URLS['garden_url'] + """">Go To Garden</a><br>'+
	"""
	# contentString += """'\t<a href=\"""" + urlsConfig.URLS['garden_url'] + str(address[0]) + """">Go To User's Garden</a><br>'+"""
	
	# TODO correct url
	contentString += """
		'<a href=\"""" + urlsConfig.URLS['chat_url'] + """">Chat With User</a><br>'+
	"""
	# contentString += '<a href="' + urlsConfig.URLS['chat_url'] + '/' + str(address[0]) + '">Chat With User</a><br>'
	
	friendshipExist = requests.get(urlsConfig.URLS['friendship_exists_url'] + str(current_user['id']) + "&user2=" + str(address[0]))
	if friendshipExist:
		contentString += """
			'<a href=\"""" + urlsConfig.URLS['unfriend_url'] + str(address[0]) + """">Unfriend</a>' +
		"""
	else:
		contentString += """
			'<a href=\"""" + urlsConfig.URLS['friendship_url'] + str(address[0]) + """">Become Friends</a>'+
		"""
	
	contentString += "'</div>'"

	return contentString

# @locationApp.errorhandler(Exception)
# def exceptionHandler(error):
# 	errorString = "Something went wrong! It seems there was a " + error.__class__.__name__ + " while making a request"
# 	if "garden" in repr(error).lower():
# 		errorString += " to the Garden service."
# 	elif "user" in repr(error).lower():
# 		errorString += " to the Login service."
# 	else:
# 		errorString += "."
# 	return errorString
