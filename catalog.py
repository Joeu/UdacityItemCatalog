from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, Game, User

#ANTI FORGERY
from flask import session as login_session
import random, string

#CALLBACK
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

#CLIENT ID
CLIENT_ID = json.loads(open("client_secrets.json", "r").read())["web"]["client_id"]

#Connect to Database and create database session
engine = create_engine("sqlite:///gamecategory.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Login Routes
@app.route("/login")
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for x in xrange(32))
    login_session["state"] = state
    # Rendering template login
    return render_template("login.html", STATE = state)

@app.route('/gconnect', methods = ['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data

    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope = '')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    gulps_id = credentials.id_token['sub']
    if result['user_id'] != gulps_id:
        response = make_response(json.dumps("Token's user ID doesn't match diven user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    if result['issued_to'] != CLIENT_ID:
        response.make_response(json.dumps("Token's client ID doesn't match  app's"), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gulps_id == stored_gplus_id:
        response = make_response(json.dumps("Current user is already connected."), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    login_session['credentials'] = credentials
    login_session['gplus_id'] = gulps_id

    #user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params = params)
    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # check if user exists
    user_id = getUserId(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" %login_session['username'])
    print "done!"
    return output

def getUserId(email):
    try:
        user = session.query(User).filter_by(email = email).one()
        return user.id
    except:
        return None

def getUserInfo(user_id):
    user = session.query(User).filter_by(id = user_id).one()
    return user

def createUser(login_session):
    newUser = User(
        name = login_session['username'],
        email = login_session['email'],
        picture = login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email = login_session['email']).one()
    return user.id


# Category Routes
@app.route("/")
@app.route("/categories/")
def categories():
    categories = session.query(Category).all()
    return render_template("categories.html", categories=categories)

@app.route("/categories/<int:category_id>")
def categoryGames(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    games = session.query(Game).filter_by(category_id = category.id)
    return render_template("categoryGames.html", category = category, games = games)

@app.route("/category/new", methods=["GET","POST"])
def newCategory():
    if request.method == "POST":
        newCategory = Category(name = request.form["name"])
        session.add(newCategory)
        session.commit()
        flash("New game category created!")
        return redirect(url_for("categories"))
    else:
        return render_template("newCategory.html")

@app.route("/category/<int:category_id>/edit/", methods=["GET","POST"])
def editCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == "POST":
        if request.form["name"]:
            category.name = request.form["name"]
        session.add(category)
        session.commit()
        flash(category.name + " edited!")
        return redirect(url_for("categories"))
    else:
        return render_template("editCategory.html", category = category)

@app.route("/category/<int:category_id>/delete/", methods=["GET","POST"])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == "POST":
        session.delete(category)
        session.commit()
        flash(category.name + " deleted!")
        return redirect(url_for("categories"))
    else:
        return render_template("deleteCategory.html", category = category)


# Game Routes
@app.route("/category/<int:category_id>/<int:game_id>/", methods=["GET"])
def gameDescription(category_id, game_id):
    category = session.query(Category).filter_by(id = category_id).one()
    game = session.query(Game).filter_by(id = game_id).one()
    return render_template("gameDescription.html", category_id = category_id, game_id = game_id, game = game, category = category)

@app.route("/category/<int:category_id>/new", methods=["GET","POST"])
def newGame(category_id):
    if request.method == "POST":
        newGame = Game(name = request.form["name"], category_id = category_id)
        session.add(newGame)
        session.commit()
        flash("New game created!")
        return redirect(url_for("categories", category_id = category_id))
    else:
        return render_template("newGame.html", category_id = category_id)

# Task 2: Create route for editGame function here
@app.route("/category/<int:category_id>/<int:game_id>/edit/", methods=["GET","POST"])
def editGame(category_id, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    if request.method == "POST":
        if request.form["name"]:
            game.name = request.form["name"]
        if request.form["description"]:
            game.description = request.form["description"]
        session.add(game)
        session.commit()
        flash(game.name + " edited!")
        return redirect(url_for("categories", category_id = category_id))
    else:
        return render_template("editGame.html", category_id = category_id, game_id = game_id, game = game)

# Task 3: Create a route for deleteGame function here
@app.route("/category/<int:category_id>/<int:game_id>/delete/", methods=["GET","POST"])
def deleteGame(category_id, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    if request.method == "POST":
        session.delete(game)
        session.commit()
        flash(game.name + " deleted!")
        return redirect(url_for("categories", category_id = category_id))
    else:
        # return render_template("deleteGame.html", category_id = category_id, game_id = game_id, game = game)
        return render_template("deleteGame.html", category_id = category_id, game_id = game_id, game = game)

# Login Routes





#API endpoint (GET)
@app.route("/categories/<int:category_id>/games/JSON")
def CategoryGamesJSON(category_id):
    # restaurant = session.query(Restaurant).filter_by(id = category_id).one()
    items = session.query(Game).filter_by(category_id = category_id).all()
    return jsonify(Games = [i.serialize for i in items])

@app.route("/categories/<int:category_id>/games/<int:game_id>/JSON")
def GamesJSON(category_id, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    return jsonify(Game = game.serialize)


# Running app
if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = "0.0.0.0", port = 5000)