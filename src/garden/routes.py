from garden.models import Garden
from flask import render_template, jsonify
from sqlalchemy import func
from garden import db
from sqlalchemy.sql import label
from garden import app

@app.route("/")
@app.route("/garden", methods=['GET' , 'POST'])
def garden():
    gardenItems = Garden.query.all();

    return (render_template('garden.html', title="Garden",  gardenItems=gardenItems))

@app.route("/garden/<User_id>/vegetable", methods=['GET','POST'])
def vegetable(User_id):
    vegetableItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        vegetableItems.append(row.vegetable)
    return (render_template('vegetables.html', title="vegetables",  vegItems=vegetableItems))

@app.route("/garden/<User_id>/fruits", methods=['GET','POST'])
def fruits(User_id):
    fruitItems = []
    for row in db.session.query(Garden).filter_by(User_id=User_id):
        fruitItems.append(row.fruits)
    return (render_template('fruits.html', title="fruits", fruitItems=fruitItems))

