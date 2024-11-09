import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):
    CLIENTS_REQUIRED = 10

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CONSUMERS_LIST = []
        self.username = None

    async def connect(self):
        self.username = self.scope["query_string"].decode("utf-8").split("=")[1]

        # Connect to the chat group
        await self.channel_layer.group_add("chat_room", self.channel_name)

        await self.accept()
        print("WebSocket connected!")  # Debug print
        self.CONSUMERS_LIST.append(self.channel_name)

    async def disconnect(self, close_code):
        # Leave chat group
        await self.channel_layer.group_discard("chat_room", self.channel_name)
        print(f"WebSocket disconnected with code: {close_code}")  # Debug print

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message = text_data_json["message"]
            print(f"Received message: {message}")  # Debug print

            await self.channel_layer.group_send(
                "chat_room", {"type": "chat_message", "message": message}
            )
        except Exception as e:
            print(f"Error in receive: {e}")  # Debug print

    async def chat_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
