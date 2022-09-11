import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, rollback_db, close_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app, origins=["*"])

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization, true")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, PUT, DELETE, OPTIONS")
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


'''
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
# db_drop_and_create_all()

# ROUTES

# GET /drinks

@app.route("/drinks", methods=["GET"])
# @requires_auth("get:drinks")
def get_drinks():
    try:
        drinks = Drink.query.all()
        drinks_short = [drink.short() for drink in drinks]
        
    except:
        abort(500)
    return {
            "success": True,
            "drinks": drinks_short
        }
    
# GET /drinks-detail

@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]
        
    except:
        abort(500)
    return {
            "success": True,
            "drinks": drinks_long
        }


# POST /drinks

@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(payload):
    new_drink_data = request.get_json()
    title = new_drink_data.get("title", None)
    recipe = new_drink_data.get("recipe", None)
    if not title or not recipe:
        abort(400)
    for ingrdt in recipe:
        name = ingrdt.get("name", None)
        color = ingrdt.get("color", None)
        parts = ingrdt.get("parts", None)
        if not name or not color or not parts:
            abort(400)
    drink_exists = Drink.query.filter_by(title=title).one_or_none()
    if drink_exists:
        abort(409)
    try:
        new_drink = Drink(title=title, recipe=json.dumps(recipe))
        new_drink.insert()
        drink = Drink.query.get(new_drink.id)
        drink_long = drink.long()
        
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()
    return {
            "success": True,
            "drinks": [drink_long]
        }


# PATCH /drinks/<id>

@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(payload,id):
    drink = Drink.query.get(id)
    if drink == None:
        abort(404)
    update_data = request.get_json()
    title = update_data.get("title", None)
    recipe = update_data.get("recipe", None)
    if not (title or recipe):
        abort(422)
    if recipe:
        for ingrdt in recipe:
            name = ingrdt.get("name", None)
            color = ingrdt.get("color", None)
            parts = ingrdt.get("parts", None)
            if not name or not color or not parts:
                abort(400)
    try:
        if title:
            drink.title = title
        if recipe:
            drink.recipe = json.dumps(recipe)
        drink.update()
        updated_drink = Drink.query.get(id)
        drink_long = updated_drink.long()
        
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()
    return {
            "success": True,
            "drinks": [drink_long]
        }


# DELETE /drinks/<id>

@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload,id):
    drink = Drink.query.get(id)
    if drink == None:
        abort(404)
    try:
        drink.delete()
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()
    return {
            "success": True,
            "delete": id
        }

# Error Handling
'''
Error handling for bad request
'''

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

'''
Error handling for resource not found
'''

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
Error handling for conflicts
'''

@app.errorhandler(409)
def conflicts_found(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "conflict in request"
    }), 409

'''
Error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

'''
Error handling for server error
'''


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "internal server error"
    }), 500




'''
Error handling for AuthError error
'''
@app.errorhandler(AuthError)
def authentication_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error.get("description", None)
    }), error.status_code


if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0", 5000)