from flask import session, request
from flask_socketio import emit, send, join_room, leave_room
from .. import socketio
from .. import database
from .emotion_detection import getEmotionDetection

actions = { "JOINED": 0, "LEFT":1, "RENAME":2 }

current_user_list = {}

# @section.on('get_all_users')
# def getAllUsers():
#     emit('user_list', current_user_list, broadcast=True)

@socketio.on('user_action')
def actionHandler(message):
    action = message['action']
    # Save as loged in user in database
    if (action == 0):
        print('action token')
        user_action_obj = database.UserActionInterface()
        current_user_list[request.sid] = user_action_obj.saveNewLogin(message['from']['user_id'])
    # Logout user from database
    elif (action == 1):
        logOutUser(current_user_list[request.sid])
        del current_user_list[request.sid]
    emit('user_action',message, broadcast=True)

@socketio.on('connect')
def handle_my_custom_event():
    print ('connected', request.sid)

@socketio.on('disconnect')
def handle_my_custom_event():
    logOutUser(current_user_list[request.sid])
    del current_user_list[request.sid]
    print ('disconnected')

@socketio.on('message')
def handle_message(message):
    if 'action' in message:
        actionHandler(message)
    if 'content' in message:
        print(message)
        message['content'] = message['content'] + getEmotionDetection(message['content'])
    emit('message',message, broadcast=True)

def logOutUser(action_row_id):
    user_action_obj = database.UserActionInterface()
    user_action_obj.logOutUser(action_row_id)
