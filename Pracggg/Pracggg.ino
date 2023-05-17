#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>

const char* ssid = "Phoenix";
const char* password = "rover@mist";

WebSocketsServer webSocket(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length);

void setup() {
  Serial.begin(115200);
  
  // Connect to access point
  Serial.println("Connecting");
  // Define Static IP Settings
  IPAddress local_IP(192,168,0,201);
  IPAddress gateway(192,168,0,1);
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
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);

    int x = doc["x"].as<int>();
    int y = doc["y"].as<int>();
    float degree = doc["degree"].as<float>();
    float force = doc["force"].as<float>();

    Serial.print("X: ");
    Serial.print(x);
    Serial.print(", Y: ");
    Serial.print(y);
    Serial.print(", Degree: ");
    Serial.print(degree);
    Serial.print(", Force: ");
    Serial.println(force);
  }
}