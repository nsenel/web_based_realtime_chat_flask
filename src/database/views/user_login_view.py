# src/database//user_login_veiew.py

import os, sys, re, datetime
from flask import Flask, request, make_response, jsonify
from flask_httpauth import HTTPTokenAuth
from validate_email import validate_email

from src.server import app, db
from src.database.models.user import User, BlacklistToken
from src.database.models_schema.user_schema import UserSchema

token_auth = HTTPTokenAuth('Token')

url_prefix = app.config.get('REST_URL_PREFIX')
test_token = app.config.get('TEST_TOKEN')

@token_auth.verify_token
def verify_token(token):
    resp = User.decode_auth_token(token)
    if not isinstance(resp, str):
        user = User.query.filter_by(user_id=resp).first()
        if user:
            return True
    return False

# # User login // To do numan remove
# @app.route(url_prefix + '/auth/test', methods=['GET'])
# def test_api():
#                 responseObject = {
#                     'status': 'success',
#                     'message': 'Successfully logged in.'
#                 }
#                 return make_response(jsonify(responseObject)), 200

# User login
@app.route(url_prefix + '/auth/login', methods=['POST'])
def login_api():
    # get the post data
    post_data = request.get_json()
    # fetch the user data
    user = User.query.filter_by(email=post_data.get('email')).first()
    if (user):
        pwd_valid = user.validate_password(post_data.get('password'))
        if pwd_valid:
            # Create auth token if user name and password are correct
            auth_token = user.encode_auth_token(user.user_id)
            if auth_token:
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 200
    responseObject = {
        'status': 'fail',
        'message': 'Email address or password is not correct!'
    }
    return make_response(jsonify(responseObject)), 404

@app.route(url_prefix + '/auth/register', methods=['POST'])
def register_api():
    # get the auth token
    auth_token = request.headers.get('Authorization')
    # get the post data
    post_data = request.get_json()
    # Check if mail address is valid
    if not(validate_email(post_data.get('email'))):
        responseObject = {
            'status': 'Fail',
            'message': "Please enter valid mail adress"
        }
        return make_response(jsonify(responseObject)), 200
    # Database process
    try:
        user_name = User.query.filter_by(user_name=post_data.get('user_name')).first()
        user_email = User.query.filter_by(email=post_data.get('email')).first()
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
            email = post_data.get('email')
            user_pwd = post_data.get('password')
            user = User(user_name, email, user_pwd)
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

# User status and check if logged in
@app.route(url_prefix + '/auth/status', methods=['GET'])
def user_api():
    # get the auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            user = User.query.filter_by(user_id=resp).first()
            responseObject = { # To do numan bune schema la yolla
                'status': 'success',
                'data': {
                    'user_id': user.user_id,
                    'user_name': user.user_name,
                    'admin': user.admin
                }
            }
            return make_response(jsonify(responseObject)), 200
        responseObject = {
            'status': 'fail',
            'message': resp
        }
        return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403

# User logout
@app.route(url_prefix + '/auth/logout', methods=['POST'])
def logout_api():
    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            responseObject = {
                'status': 'fail',
                'message': 'Bearer token malformed.'
            }
            return make_response(jsonify(responseObject)), 401
    if auth_token:
        resp = User.decode_auth_token(auth_token)
        if not isinstance(resp, str):
            # mark the token as blacklisted
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                # insert the token
                db.session.add(blacklist_token)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return make_response(jsonify(responseObject)), 200
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': resp
            }
            return make_response(jsonify(responseObject)), 401
    else:
        responseObject = {
            'status': 'fail',
            'message': 'Provide a valid auth token.'
        }
        return make_response(jsonify(responseObject)), 403
