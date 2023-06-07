import websocket
import json

# Connect to WebSocket server
ws = websocket.WebSocket()
ws.connect("ws://192.168.0.201:81")
print("Connected to WebSocket server")

try:
    while True:
        # Wait for the server to send JSON data
        result = ws.recv()
        print("Received: " + result)

        # Parse the received JSON data
        data = json.loads(result)

        # Check if speechResult is present in the received data
        if "speechResult" in data:
            speech_result = data["speechResult"]
            print("Speech Result:", speech_result)
            # Perform your desired actions with the speech result here
            

except KeyboardInterrupt:
    print("Closing WebSocket connection")
    ws.close()
