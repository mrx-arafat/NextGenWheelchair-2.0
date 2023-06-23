#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

const char* ssid = "Goribs";
const char* password = "agetakadewalagbe";

WebSocketsServer webSocket(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length);

void setup() {
  Serial.begin(115200);
  
  // Connect to access point
  Serial.println("Connecting");
  // Define Static IP Settings
  IPAddress local_IP(192,168,1,204);
  IPAddress gateway(192,168,1,1);
  IPAddress subnet(255,255,0,0);
  IPAddress primaryDNS(8,8,8,8);
  IPAddress secondaryDNS(8,8,4,4);
  // WiFi.begin(ssid, password);
    if(!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("STA Failed to configure");
  }
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  // Print our IP address
  Serial.println("Connected!");
  Serial.print("My IP address: ");
  Serial.println(WiFi.localIP());

  webSocket.begin();
  webSocket.onEvent(webSocketEvent);
}

void loop() {
  webSocket.loop();
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  if (type == WStype_TEXT) {
    // Handle the received message
    StaticJsonDocument<200>doc;
    deserializeJson(doc,payload);

    if(doc.containsKey("status"))
    {
      String message = doc["status"].as<String>();
      Serial.print("Recieved Message: ");
      Serial.println(message);
    }



    //String message = String((char*)payload);
    //Serial.println("Received message: " + message);
  }
}