# # chat/consumers.py
# import json
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import sync_to_async


# from .models import Message

# class ChatConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = f"chat_{self.room_name}"

#         # Join room group
#         await self.channel_layer.group_add(
#             self.room_group_name, 
#             self.channel_name)

#         await self.accept()

#     async def disconnect(self, close_code):
#         # Leave room group
#         await self.channel_layer.group_discard(
#             self.room_group_name, 
#             self.channel_name)

#     async def receive(self, text_data):
#         text_data_json = json.loads(text_data)
#         message = text_data_json["message"]
#         username = text_data_json['username']
#         room = text_data_json['room']
#         author = text_data_json['author']

#         # Save message with author information
#         await self.save_message(username, room, message, author)


#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.room_group_name, {
#                 "type": "chat.message", 
#                 "message": message,
#                 "username": username,
#                 "author": author}
#         )


#     async def chat_message(self, event):
#         message = event["message"]
#         username = event["username"]
#         author = event["author"]


#        # Send message to WebSocket with author information
#         await self.send(text_data=json.dumps({
#             "message": message,
#             "username": username,
#             "author": author,
#             }))

#     # Adjust the function signature to accept the additional parameter
#     @sync_to_async
#     def save_message(self, username, room, message, author):
#         Message.objects.create(username=username, room=room, content=message, author=author)
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name, 
            self.channel_name)


        await self.accept()


    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json['username']
        room = text_data_json['room']

        # Save message with author information
        await self.save_message(username, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message", 
                "message": message,
                "username": username,
                #"author": username  # Assuming author is the same as the username
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        username = event["username"]
        
        # Send message to WebSocket with author information
        await self.send(text_data=json.dumps({
            "message": message,
            "username": username,
        }))

    @sync_to_async
    def save_message(self, username, room, message):
        Message.objects.create(username=username, room=room, content=message)