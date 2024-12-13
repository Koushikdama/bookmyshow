# movies/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Seat, Theater
from asgiref.sync import sync_to_async

class SeatAvailabilityConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the theater_id from the URL
        self.theater_id = self.scope['url_route']['kwargs']['theater_id']
        self.room_name = f"theater_{self.theater_id}"
        self.room_group_name = f"seat_availability_{self.room_name}"

        # Join the WebSocket room
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the room
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        action = text_data_json.get('action')

        # Handle seat booking or cancellation updates
        if action == 'update':
            await self.send_seat_availability()

    # Send seat availability update to WebSocket group
    @sync_to_async
    def get_seat_availability(self):
        theater = Theater.objects.get(id=self.theater_id)
        seats = Seat.objects.filter(theater=theater)

        seat_data = []
        for seat in seats:
            seat_data.append({
                'seat_number': seat.seat_number,
                'is_booked': seat.is_booked
            })

        return seat_data

    async def send_seat_availability(self):
        seat_data = await self.get_seat_availability()

        # Send seat data to WebSocket
        await self.send(text_data=json.dumps({
            'seats': seat_data
        }))
