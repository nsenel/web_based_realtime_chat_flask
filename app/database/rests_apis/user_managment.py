from validate_email import validate_email
from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPTokenAuth

from app import app, db
from app.database.models.user import User
from app.database.models.user_actions import UserAction
from app.database.models.user_actions import UserActionInterface
from app.database.models_schema.user_schema import UserSchema
from .user_login_rest import token_auth

url_prefix = app.config.get('REST_URL_PREFIX')


@app.route(url_prefix + '/auth/register', methods=['POST'])
def register_api():
    # get the auth token
    auth_token = request.headers.get('Authorization')
    # get the post data
    post_data = request.get_json()
    # Check if mail address is valid
    if not(validate_email(post_data.get('user_mail'))):
        responseObject = {
            'status': 'Fail',
            'message': "Please enter valid mail adress"
        }
        return make_response(jsonify(responseObject)), 200
    # Database process
    try:
        user_name = User.query.filter_by(user_name=post_data.get('user_name')).first()
        user_email = User.query.filter_by(email=post_data.get('user_mail')).first()
        # If user name already exits return Fail
        if (user_name or user_email):
            responseObject = {
            'status': 'Fail',
            'message': '{} allready exist'.format('User name' if user_name else 'Email')
            }
            return make_response(jsonify(responseObject)), 200
        else:
            # create user
            user_name = post_data.get('user_name')
            email = post_data.get('user_mail')
            user_pwd = post_data.get('user_password')
            age = post_data.get('user_age')
            city = post_data.get('user_city')
            user = User(user_name, email, user_pwd, age, city)
            # add user to database
            db.session.add(user)
            db.session.commit()
            responseObject = {
            'status': 'Success',
            'message': "New user created"
            }
            return make_response(jsonify(responseObject)), 200
    except Exception as e:
        print(e)
        responseObject = {
            'status': 'Fail',
            'message': 'Database error'
        }
        return make_response(jsonify(responseObject)), 503

# Get all loged in users
@app.route(url_prefix + '/auth/user_list', methods=['GET'])
#@token_auth.login_required
def get_user_list():
    # Select all users which is currently logedin
    logged_in_users = UserAction.query.filter_by(login=True).all()
    # list comprehension for geting related users(forein key)
    users = [logged_in_user.user_relation for logged_in_user in logged_in_users]
    result, error = UserSchema().dump(users, many=True)
    return make_response(jsonify(result)), 200