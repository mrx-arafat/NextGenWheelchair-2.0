import websocket
import json

# Connect to WebSocket server
ws = websocket.WebSocket()
ws.connect("ws://192.168.1.201:81")
print("Connected to WebSocket server")

try:
    while True:
        # Wait for server to send JSON data
        result = ws.recv()
        print("Received: " + result)
        data = json.loads(result)
        if "degree" in data: 
            x = data["x"]
            y = data["y"]
            degree = data["degree"]
            force = data["force"]

            # Print the parsed values
            print(f"X: {x}, Y: {y}, Degree: {degree}, Force: {force}")
        elif "speechResult" in data:
            speech_result = data["speechResult"]
            print("Speech Result:", speech_result)
        elif "direction" in data: 
            direction = data["direction"]
            angle = data["angle"]
            print(f"direction: {direction}, angle: {angle}")
        
except KeyboardInterrupt:
    print("Closing WebSocket connection")
    ws.close()