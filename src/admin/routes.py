from admin import app
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from admin.forms import DeleteForm
from admin import urlsConfig
import requests
import json
import urllib.request

current_user_id=0

@app.route("/admin", methods=['GET'])
def admin():
    global current_user_id
    current_user_id = request.cookies.get("currentSessionCookie")
    if current_user_id:
        # Get current user information
        print(current_user_id)
        current_user_response = requests.get(urlsConfig.URLS['single_user_url'] + str(current_user_id))

        if current_user_response.status_code == 200:
            users = requests.get(urlsConfig.URLS['users_url']).json()
            comments = requests.get(urlsConfig.URLS['all_comments_all_posts_url']).json()
            posts = requests.get(urlsConfig.URLS['all_posts_url']).json()
            advertisements = json.loads(urllib.request.urlopen(urlsConfig.URLS['all_advertisements_url']).read())
            # advertisements = requests.get(urlsConfig.URLS['advertisements_url']).json()

            form = DeleteForm()

            return render_template("admin.html", users=users, comments=comments, posts=posts, advertisements=advertisements, deleteForm=form)

        else:
            return redirect(urlsConfig.URLS['login_url'])
    else:
        return redirect(urlsConfig.URLS['login_url'])

@app.route("/deleteUser", methods=['GET', 'POST'])
def deleteUser():
    if 'userID' in request.form:
        userID = request.form['userID']
        response = requests.get(urlsConfig.URLS['delete_user_url'] + str(userID))
    return redirect('admin')

@app.route("/deleteComment", methods=['GET', 'POST'])
def deleteComment():
    if 'commentID' in request.form:
        commentID = request.form['commentID']
        response= requests.get(urlsConfig.URLS['delete_comment_url'] + str(commentID))
    return redirect('admin')

@app.route("/deletePost", methods=['GET', 'POST'])
def deletePost():
    if 'postID' in request.form:
        postID = request.form['postID']
        response= requests.get(urlsConfig.URLS['delete_post_url'] + str(postID))
    return redirect('admin')

@app.route("/deleteAdvertisement", methods=['GET', 'POST'])
def deleteAdvertisement():
    if 'advertisingID' in request.form:
        advertisingID = request.form['advertisingID']
        response= requests.get(urlsConfig.URLS['delete_advertisement_url'] + str(advertisingID))
    return redirect('admin')

# Needed to redirect to urls of another service
@app.route("/redirectToGarden", methods=["GET"])
def redirectToGarden():
    global current_user_id

    response = redirect(urlsConfig.URLS['garden_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToNewsfeed", methods=["GET"])
def redirectToNewsfeed():
    global current_user_id

    response = redirect(urlsConfig.URLS['newsfeed_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToChat",methods=["GET"])
def redirectToChat():
    global current_user_id

    response = redirect(urlsConfig.URLS['chat_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToPost", methods=["GET"])
def redirectToPost():
    global current_user_id

    response = redirect(urlsConfig.URLS['post_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.route("/redirectToLocation", methods=["GET"])
def redirectToLocation():
    global current_user_id

    response = redirect(urlsConfig.URLS['location_url'])
    response.set_cookie("currentSessionCookie", str(current_user_id))
    return response 

@app.errorhandler(Exception)
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
    elif "location" in repr(error).lower():
        errorString += " to the Location service."
    else:
        errorString += "."
    return errorString
