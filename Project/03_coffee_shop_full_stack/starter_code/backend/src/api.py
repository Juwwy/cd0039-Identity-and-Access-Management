
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this funciton will add one
'''
db_drop_and_create_all()

# ROUTES

#============ Drink Get all with short info session =================
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/api/v1/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_all_drinks(b):
    
    try:
        drinks = Drink.query.all()
        print(drinks)
        drink_response = [ drink.short() for drink in drinks ]
       
        return jsonify({
            "success": True,
            "drinks": drink_response
        })
    except Exception as error:
        abort(422)


#============ Drink Get By Detail session =================
'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

@app.route('/api/v1/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(b):
    
    try:
        drinks = Drink.query.all()
        drink_detail = [drink.long() for drink in drinks]
        return jsonify({
            "success": True,
            "drinks": drink_detail
        })
    except Exception as error:
        abort(422)



#============ Drink Create session =================
'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


try:
    @app.route('/api/v1/drinks', methods=['POST'])
    @requires_auth('post:drinks')
    def create_drink(b):
    

        try:
            recipe_data = []
            request_data = request.get_json()
            title = request_data['title']
            recipes = request_data['recipe']
            recipe ={}
            for r in recipes:
                recipe = {
                    'name': r['name'],
                    'color': r['color'],
                    'parts': r['parts']
                }
                recipe_data.append(recipe)

            result = json.dumps(recipe_data)
            drink = Drink(title=title, recipe=result)
            #print(drink)
            Drink.insert(drink)
            return jsonify({
                "code": 201,
                "success": True,
                "drinks": drink,
                "message": "Drink created successfully"
            })

        except:
            db.session.rollback()
            raise AuthError({
                        "code": "unauthorize",
                        'description': 'permission not inclusive for authentication token.'
                    },401)
            
        finally:
            db.session.close()
except:
    abort(403)

#============ Drink Update session =================
'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/api/v1/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(b, drink_id):
    
    try:
        drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
        request_data = request.get_json()
        
        drink.title = request_data['title']
        rec = request_data['recipe']
        drink.recipe = json.dumps(rec)
        
        Drink.update(drink)
        return jsonify({
            "code": 200,
            "success": True,
            "drinks": drink,
            "message": "Drink updated successfully"
        })
    except:
        db.session.rollback()
        abort(401)
    finally:
        db.session.close()

#============ Drink Delete session =================
'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''

@app.route('/api/v1/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(b, drink_id):

    try:
        drink = Drink.query.filter(Drink.id == drink_id).first()
        Drink.delete(drink)
        return jsonify({
            "code": 200,
            "success": True,
            "delete": drink_id,
            "message": "Drink was deleted successfully!"
        })
    except:
        db.session.rollback()
        abort(404)
    finally: 
        db.session.close()






#============ Drink Error Handling session =================

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
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above
'''

@app.errorhandler(401)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Not Authorize"
    }), 401

@app.errorhandler(403)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Forbidden request. You don't have access to perform this action"
    }), 403

@app.errorhandler(401)
def auth_error(error):
    raise AuthError({
        "code": 401,
        "description": "Authentication error"
    }, status_code=401)
