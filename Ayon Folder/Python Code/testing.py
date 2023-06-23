import asyncio
import websockets

# Define the WebSocket server address
server_address = 'ws://192.168.1.204:81'

async def send_message():
    async with websockets.connect(server_address) as websocket:
        message = 'Hello'
        await websocket.send(message)
        print(f"Sent message: {message}")

# Run the send_message function
asyncio.get_event_loop().run_until_complete(send_message())
