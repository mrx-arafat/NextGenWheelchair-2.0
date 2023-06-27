import speech_recognition as sr
import websocket
import time
import json

# ESP32 WebSocket server URL
websocket_url = "ws://192.168.1.201:81/"

def connect_to_websocket():
    print("Connecting to ESP32 WebSocket server...")
    ws = websocket.WebSocket()
    ws.connect(websocket_url)
    print("Connected to ESP32 WebSocket server.")
    return ws

def send_command(ws, status):
    data = {"status": status}
    print("Sending command:", data)
    ws.send(json.dumps(data))

def recognize_and_send(ws):
    previous_command = None
    while True:
        with sr.Microphone(device_index=0) as source:
            recognizer = sr.Recognizer()
            recognizer.adjust_for_ambient_noise(source)
            recognizer.dynamic_energy_threshold = 1000

            try:
                print("Listening....")
                audio = recognizer.listen(source, timeout=1.5)
                response = recognizer.recognize_google(audio)
                print("Recognized:", response)

                # Check if recognized word is a valid command
                command = None
                if response.lower() in ["stop", "halt", "terminate"]:
                    command = "stop"
                elif response.lower() in ["forward", "ahead", "advance"]:
                    command = "forward"
                elif response.lower() in ["back", "backward", "reverse"]:
                    command = "back"
                elif response.lower() in ["right", "rightward"]:
                    command = "right"
                elif response.lower() in ["left", "leftward"]:
                    command = "left"

                # Send command if it's different from the previous one
                if command and command != previous_command:
                    send_command(ws, command)
                    previous_command = command

            except sr.UnknownValueError:
                print("Didn't recognize that.")

def main():
    connected = False
    while not connected:
        try:
            ws = connect_to_websocket()
            connected = True
        except ConnectionRefusedError:
            print("Connection failed. Retrying in 3 seconds...")
            time.sleep(3)

    recognize_and_send(ws)

if __name__ == "__main__":
    main()
