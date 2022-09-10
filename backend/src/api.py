import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, rollback_db, close_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

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
def get_drinks():
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
def get_drinks_detail():
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
def create_drink():
    try:
        new_drink_data = request.get_json()
        print(new_drink_data)
        # new_drink = Drink(title="", recipe="")
        # new_drink.insert()
        # drink = Drink.query.get(new_drink.id)
        # drink_long = drink.long()
        return {
            "success": True,
            "drinks": "drink_long"
        }
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()


# PATCH /drinks/<id>

@app.route("/drinks/<int:id>", methods=["PATCH"])
@requires_auth("patch:drinks")
def update_drink(id):
    drink = Drink.query.get(id)
    if drink == None:
        abort(404)
    try:
        update_data = request.get_json()
        print(update_data)
        # drink.title = update_data.
        return {
            "success": True,
            "drinks": "drink_long"
        }
    except:
        rollback_db()
        abort(500)
    finally:
        close_db()

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        it should update the corresponding row for <id>
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

# DELETE /drinks/<id>

@app.route("/drinks/<int:id>", methods=["DELETE"])
@requires_auth("delete:drinks")
def delete_drink(id):
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