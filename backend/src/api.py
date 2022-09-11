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
@requires_auth("get:drinks")
def get_drinks(payload):
    try:
        drinks = Drink.query.all()
        drinks_short = [drink.short() for drink in drinks]
        return {
            "success": True,
            "drinks": drinks_short
        }
    except:
        abort(500)
    
# GET /drinks-detail

@app.route("/drinks-detail", methods=["GET"])
@requires_auth("get:drinks-detail")
def get_drinks_detail(payload):
    try:
        drinks = Drink.query.all()
        drinks_long = [drink.long() for drink in drinks]
        return {
            "success": True,
            "drinks": drinks_long
        }
    except:
        abort(500)


'''
@TODO implement endpoint
    POST /drinks
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

# POST /drinks

@app.route("/drinks", methods=["POST"])
@requires_auth("post:drinks")
def create_drink(payload):
    try:
        new_drink_data = request.get_json()
        title = new_drink_data.get("title", None)
        recipe = json.dumps(new_drink_data.get("recipe", None))
        new_drink = Drink(title=title, recipe=recipe)
        new_drink.insert()
        drink = Drink.query.get(new_drink.id)
        drink_long = drink.long()
        return {
            "success": True,
            "drinks": drink_long
        }
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()


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
    try:
        if title:
            drink.title = title
        if recipe:
            drink.recipe = json.dumps(recipe)
        drink.update()
        updated_drink = Drink.query.get(id)
        drink_long = updated_drink.long()
        return {
            "success": True,
            "drinks": drink_long
        }
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()


# DELETE /drinks/<id>

@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(payload,id):
    drink = Drink.query.get(id)
    if drink == None:
        abort(404)
    try:
        drink.delete()
        return {
            "success": True,
            "delete": id
        }
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()

# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''

'''
@TODO implement error handler for 404
    error handler should conform to general task above
'''


'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

if __name__ == "__main__":
    app.debug = True
    app.run("0.0.0.0", 5000)