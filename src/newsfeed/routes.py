from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from newsfeed import newsfeedApp
from werkzeug.urls import url_parse
from newsfeed.forms import CommentForm
import requests
from newsfeed import urlsConfig
import json
import urllib.request

current_user_id=""

@newsfeedApp.route("/newsfeed", methods=["GET"])
def newsfeed():
	global current_user_id
	current_user_id = request.cookies.get("currentSessionCookie")
	if current_user_id:
		# Get current user information
		current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))

		if current_user_response.status_code == 200:
			# Success!
			isAdmin = current_user_response.json()['data']['admin']
			isAdmin = "true" if isAdmin else "false" # Python uses True and False, javascript uses true and false, need to translate it

			# Get all posts
			allPosts = requests.get(urlsConfig.URLS['all_posts_url']).json()
			# allPosts = []

			# Get all comments
			allComments = requests.get(urlsConfig.URLS['all_comments_all_posts_url']).json()
			# allComments = []

			# Get all advertisements
			allAdvertisements = json.loads(urllib.request.urlopen(urlsConfig.URLS['advertisements_url']+"/"+str(current_user_id)).read())
			# allAdvertisements = []

			commentForm = CommentForm()

			# Show list
			return render_template("newsfeed.html", commentForm=commentForm, posts=allPosts, comments=allComments, advertisements=allAdvertisements, userID=current_user_id, isAdmin=isAdmin)
		else:
			return redirect(urlsConfig.URLS['login_url'])
	else:
		return redirect(urlsConfig.URLS['login_url'])

# Needed to redirect to urls of another service
@newsfeedApp.route("/redirectToGarden", methods=["GET"])
def redirectToGarden():
    global current_user_id

    response = redirect(urlsConfig.URLS['garden_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@newsfeedApp.route("/delete/<id>", methods=['GET', 'POST'])
def deletePost():
    if 'postID' in request.form:
        postID = request.form['postID']
        response= requests.get(urlsConfig.URLS['delete_post'] +  str(postID))
    return "Delete post"

@newsfeedApp.route("/redirectToChat",methods=["GET"])
def redirectToChat():
    global current_user_id

    response = redirect(urlsConfig.URLS['chat_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@newsfeedApp.route("/redirectToPost", methods=["GET"])
def redirectToPost():
    global current_user_id

    response = redirect(urlsConfig.URLS['post_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@newsfeedApp.route("/redirectToLocation", methods=["GET"])
def redirectToLocation():
    global current_user_id

    response = redirect(urlsConfig.URLS['location_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@newsfeedApp.errorhandler(Exception)
def exceptionHandler(error):
	print(error)
	errorString = "Something went wrong! It seems there was a " + error.__class__.__name__ + " while making a request"
	if "post" in repr(error).lower():
		errorString += " to the Post service."
	elif "comment" in repr(error).lower():
		errorString += " to the Comment service."
	elif "photo" in repr(error).lower():
		errorString += " to the Photo service."
	elif "advertisements" in repr(error).lower():
		errorString += " to the Advertisement service."
	elif "user" in repr(error).lower():
		errorString += " to the Login service."
	else:
		errorString += "."
	return errorString
