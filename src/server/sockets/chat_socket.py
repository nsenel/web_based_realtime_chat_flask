


from flask import session
from flask_socketio import emit, join_room, leave_room
from .. import socketio

# def messageReceived(methods=['GET', 'POST']):
#     print('message was received!!!')

# @socketio.on('connect')
# def handle_my_custom_event(json, methods=['GET', 'POST']):
#     print('received my event: ' + str(json))
#     socketio.emit('my response', json, callback=messageReceived)

@socketio.on('connect')
def handle_my_custom_event():
    print('burda')

@socketio.on('message')
def handle_message(message):
    if 'content' in message:
        print('received message: ')
        print(message)
        #message = {'message':message['content'], 'id':1}
    emit('message',message, broadcast=True)

@socketio.on('joined', namespace='/chat')
def joined(message):
    print('joined')
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    print('message')
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('disconnect', namespace='/chat')
def left(message):
    print('left')
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)