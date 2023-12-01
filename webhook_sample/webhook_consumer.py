from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit
#import socketio
import json
import uuid

app = Flask(__name__)

socketio = SocketIO(app,logger=True,engineio_logger=True,cors_allowed_origins="*")

# CORS(app)
#Render the assigned template file
@app.route("/", methods=['GET'])
def index():
    return render_template('webhook_consumer.html')

app.config['uid'] = "room12"

# Sending Message through the websocket
def send_message(event, message):
    print("Message = ", message)
    socketio.emit(event, message)
    #emit(event, message, broadcast=True, include_self=False)

# Receive the webhooks and emit websocket events
@app.route('/consumeevent', methods=['POST'])
def consumeevent():
    if request.method == 'POST':
        data = request.json
        if data:
            var = json.loads(data)
            roomid = app.config['uid']
            print(f"Received Data = {data}, msg = {var}, room = {roomid}")
            send_message(event='msg', message=data)
    return 'OK'

#Execute on connecting
@socketio.on('connect')
def socket_connect():
    # Display message upon connecting to the namespace
    print('Client Connected - request.sid')

#Execute on disconnecting
@socketio.on('disconnect')
def socket_connect():
    # Display message upon disconnecting from the namespace
    print('Client disconnected - request.sid')

#Execute upon joining a specific room
@socketio.on('join_room')
def on_room():
    print("HERE IN ON ROOM")
    if app.config['uid']:
        room = str(app.config['uid'])
        # Display message upon joining a room specific to the session previously stored.
        print(f"Socket joining room {room}")
        join_room(room)

#Execute upon encountering any error related to the websocket
@socketio.on_error_default
def error_handler(e):
    # Display message on error.
    print(f"socket error: {e}, {str(request.event)}")

#Run using port 5001
if __name__ == "__main__":
    socketio.run(app, host='localhost', port=5001, debug=False)