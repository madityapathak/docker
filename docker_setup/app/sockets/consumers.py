from django.http import HttpResponse
from channels.exceptions import StopConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
import json
from datetime import datetime
import pytz


class EchoConsumer(AsyncConsumer):
   async def websocket_connect(self, event):
      room=self.scope['url_route']['kwargs']['room_id']
      try:
         test_room_id=int(room)
      except:
         raise StopConsumer()
         
      self.chatroom=f"{room}"
      await self.channel_layer.group_add(
            self.chatroom,
            self.channel_name)
      if self.scope['user'].is_authenticated:
         await self.send({
            "type": "websocket.accept",   })
      else:
         await self.send({
            "type": "websocket.disconnect",  })

   async def websocket_receive(self, event):   
      rtext=event.get('text',None)
      if rtext is not None:
         email = "Invalid User"
         msg = "Authenticate first"
         if self.scope['user'].is_authenticated:
            user=self.scope['user']
            email=user.email
            msg = rtext
            
         response={
            'message': msg,
            'user':email,
         }
         
         await self.channel_layer.group_send(
            self.chatroom,
            {
               "type": "chat_message",
               "text" : json.dumps(response)
            })

   async def chat_message(self,event): 
      await self.send({                  
         "type": "websocket.send",
         "text": event['text']})
   
   async def websocket_disconnect(self,event):
      await self.channel_layer.group_discard(
         self.chatroom,
         self.channel_name )
      raise StopConsumer()

