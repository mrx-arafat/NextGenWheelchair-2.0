#include <WiFi.h>
#include <WebSocketsServer.h>
#include <ArduinoJson.h>
#include <ESP32_Servo.h> 

Servo myservo1, myservo2;

/* Motor starts */
static int flag = 0, flag1 = 0;
static int xx = 0;
const int servo1 = 2;
const int servo2 = 4;
/* Motor starts */

/* Wifi Starts */
const char* ssid = "The King BOB";
const char* password = "TheKingBOB69";
WebSocketsServer webSocket(81);

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length);
/* Wifi ends */

/* Sonar Pins starts */
const int pingPin1 = 5; // Trigger Pin of Ultrasonic Sensor
const int echoPin1 = 18; // Echo Pin of Ultrasonic Sensor

long duration1, duration2, cm1, cm2;
/* Sonar Pins ends */

// /* Joystick Variables starts*/
// int x = 0; // To store value of the X axis
// int y = 0; // To store value of the Y axis
// /* Joystick Variables ends*/

void setup() {
    Serial.begin(115200); // Starts the serial communication

    /* Joystick starts */
    myservo1.attach(servo1);
    myservo2.attach(servo2);
    /* Joystick ends */

    /* Wifi Communication Starts */
    // Connect to access point
    Serial.println("Connecting");
    // Define Static IP Settings
    IPAddress local_IP(192,168,0,201); 
    IPAddress gateway(192,168,0,1);
    IPAddress subnet(255,255,0,0);
    IPAddress primaryDNS(8,8,8,8);
    IPAddress secondaryDNS(8,8,4,4);
    WiFi.begin(ssid, password);
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
    /* Wifi Communication Ends */
}

void loop() {
    /* Sonar Sensor starts*/
    pinMode(pingPin1, OUTPUT);
    digitalWrite(pingPin1, LOW);
    delayMicroseconds(2);
    digitalWrite(pingPin1, HIGH);
    delayMicroseconds(10);
    digitalWrite(pingPin1, LOW);
    pinMode(echoPin1, INPUT);
    duration1 = pulseIn(echoPin1, HIGH);
    cm1 = microsecondsToCentimeters(duration1);
    pinMode(echoPin1, OUTPUT);

    Serial.print(cm2);
    Serial.print("cm ");
    Serial.println();
    /* Sonar Sensor ends*/

    if(cm1 >= 50) {
        webSocket.loop();
        if(flag1 == 0) {
        xx++;
        Serial.println(xx);
        if(xx >= 1000) {
            myservo1.write(90);
            myservo2.write(90);
        }
        
        } else {
        xx = 0;
        flag1 = 0;
        }
    }
    sendDataToServer("Your data goes here");
}

void webSocketEvent(uint8_t num, WStype_t type, uint8_t* payload, size_t length) {
  flag1= 1;
  if (type == WStype_TEXT) {
    StaticJsonDocument<200> doc;
    deserializeJson(doc, payload);

    int x = doc["x"].as<int>();
    int y = doc["y"].as<int>();
    // float degree = doc["degree"].as<float>();
    // float force = doc["force"].as<float>();

    // Serial.print("X: ");
    // Serial.print(x);
    // Serial.print(", Y: ");
    // Serial.print(y);

    Serial.print(x);
    Serial.print(" ");
    Serial.println(y);
    // Serial.print(", Degree: ");
    // Serial.print(degree);
    // Serial.print(", Force: ");
    // Serial.println(force);
    if(x>=(2048 - 848) && x<=(2048 + 848) && y >= (4095 - 898)) {
      
      // Forward
      // flag = 1
      if(flag != 1) {
        myservo1.write(90);
        myservo2.write(90);
      }
      else flag = 1;
      Serial.println("Forward");
      myservo1.write(120);
      myservo2.write(120);
      delay(10);
      // myservo1.write(90);
      // myservo2.write(90);
    }
    else if(x>=(2048 - 848) && x<=(2048 + 848) && y <= (0 + 898)) {
      // BackWard
      // flag = 2
      if(flag != 2) {
        myservo1.write(90);
        myservo2.write(90);
      }
      else flag = 2;
      Serial.println("Backward");
      myservo1.write(60);
      myservo2.write(60);
      delay(10);
      // myservo1.write(90);
      // myservo2.write(90);
    }
    else if(x<=(0 + 848) && y>=(2048 - 848) && y<=(2048 + 848)) {
      // Left
      // flag = 3
      if(flag != 3) {
        myservo1.write(90);
        myservo2.write(90);
      }
      else flag = 3;
       Serial.println("Left");
      // myservo1.write(140);
      myservo2.write(130);
      delay(10);
      // myservo1.write(90);
      // myservo2.write(90);
    }
    else if(x>=(4095 - 848) && y>=(2048 - 848) && y<=(2048 + 848)) {
      // Right
      // flag = 4
      if(flag != 4) {
        myservo1.write(90);
        myservo2.write(90);
      }
      else flag = 4;
       Serial.println("Right");
      myservo1.write(130);
      // myservo2.write(140);
      delay(10);
      // myservo1.write(90);
      // myservo2.write(90);
    }
  }
}

long microsecondsToCentimeters(long microseconds) {
   return microseconds / 29 / 2;
}

void sendDataToServer(String message) {
    webSocket.broadcastTXT(message);
}

