# chatroom_with_dndslm
Chatroom server with the connection to the Dungeons and Dragons Assistant SLM, written on python, chatroom client


# How does it work
chatroom_server.py - Launches the server, accepts up to 100 clients. 
chatroom_client.py - Launches the client, connects with the server. After successful connection clients can send messages to the room. Everybody in the room would see the messages.
!ai [prompt] - Command to call for the Dungeons and Dragons Assistant Model
!ai [prompt] is typed by a client -> server recognises command -> server sends a HTTP POST to the backend server (link to the code: https://github.com/andrey-qrqm/AI_dungeon_master_tool/blob/main/backend/main.py) -> Backend Server asks a local microservice with launched pretrained model -> Response from the model is transferred to the chatroom server -> Chatroom server publishes the response to the chatroom.

This is just an example of possible application to showcase its workability. This application could be used as a backend for a full Chatroom application with the UI. Model could be easily changed to the one more suitable for exact case. 

Have fun!

