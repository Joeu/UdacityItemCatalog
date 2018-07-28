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
CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

#Connect to Database and create database session
engine = create_engine('sqlite:///gamecategory.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Category Routes
@app.route("/")
@app.route("/categories/")
def categories():
    categories = session.query(Category).all()
    return render_template('categories.html', categories=categories)

@app.route("/categories/<int:category_id>")
def categoryGames(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    games = session.query(Game).filter_by(category_id = category.id)
    return render_template("categoryGames.html", category = category, games = games)

@app.route('/category/new', methods=['GET','POST'])
def newCategory():
    if request.method == 'POST':
        newCategory = Category(name = request.form['name'])
        session.add(newCategory)
        session.commit()
        flash("New game category created!")
        return redirect(url_for('categories'))
    else:
        return render_template('newCategory.html')

@app.route('/category/<int:category_id>/edit/', methods=['GET','POST'])
def editCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        if request.form['name']:
            category.name = request.form['name']
        session.add(category)
        session.commit()
        flash(category.name + " edited!")
        return redirect(url_for('categories'))
    else:
        return render_template('editCategory.html', category = category)

@app.route('/category/<int:category_id>/delete/', methods=['GET','POST'])
def deleteCategory(category_id):
    category = session.query(Category).filter_by(id = category_id).one()
    if request.method == 'POST':
        session.delete(category)
        session.commit()
        flash(category.name + " deleted!")
        return redirect(url_for('categories'))
    else:
        return render_template('deleteCategory.html', category = category)


# Game Routes
@app.route("/category/<int:category_id>/<int:game_id>/", methods=["GET"])
def gameDescription(category_id, game_id):
    category = session.query(Category).filter_by(id = category_id).one()
    game = session.query(Game).filter_by(id = game_id).one()
    return render_template('gameDescription.html', category_id = category_id, game_id = game_id, game = game, category = category)

@app.route('/category/<int:category_id>/new', methods=['GET','POST'])
def newGame(category_id):
    if request.method == 'POST':
        newGame = Game(name = request.form['name'], category_id = category_id)
        session.add(newGame)
        session.commit()
        flash("New game created!")
        return redirect(url_for('categories', category_id = category_id))
    else:
        return render_template('newGame.html', category_id = category_id)

# Task 2: Create route for editGame function here
@app.route('/category/<int:category_id>/<int:game_id>/edit/', methods=['GET','POST'])
def editGame(category_id, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    if request.method == 'POST':
        if request.form['name']:
            game.name = request.form['name']
        if request.form['description']:
            game.description = request.form['description']
        session.add(game)
        session.commit()
        flash(game.name + " edited!")
        return redirect(url_for('categories', category_id = category_id))
    else:
        return render_template('editGame.html', category_id = category_id, game_id = game_id, game = game)

# Task 3: Create a route for deleteGame function here
@app.route('/category/<int:category_id>/<int:game_id>/delete/', methods=['GET','POST'])
def deleteGame(category_id, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    if request.method == 'POST':
        session.delete(game)
        session.commit()
        flash(game.name + " deleted!")
        return redirect(url_for('categories', category_id = category_id))
    else:
        # return render_template('deleteGame.html', category_id = category_id, game_id = game_id, game = game)
        return render_template('deleteGame.html', category_id = category_id, game_id = game_id, game = game)

# Login Routes





#API endpoint (GET)
@app.route('/categories/<int:category_id>/games/JSON')
def CategoryGamesJSON(category_id):
    # restaurant = session.query(Restaurant).filter_by(id = category_id).one()
    items = session.query(Game).filter_by(category_id = category_id).all()
    return jsonify(Games = [i.serialize for i in items])

@app.route('/categories/<int:category_id>/games/<int:game_id>/JSON')
def GamesJSON(category_id, game_id):
    game = session.query(Game).filter_by(id = game_id).one()
    return jsonify(Game = game.serialize)


# Running app
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)