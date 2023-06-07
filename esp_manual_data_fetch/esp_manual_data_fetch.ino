void setup() {
  Serial.begin(9600); // Set baud rate to match Python code
}

void loop() {
  char buffer[32];
  int index = 0;
  
  // Read data from serial connection until comma separator is received
  while (Serial.available()) {
    char c = Serial.read();
    if (c == ',') {
      buffer[index] = '\0'; // Null terminate the buffer
      break;
    }
    buffer[index++] = c;
    if (index >= sizeof(buffer)) {
      break; // Prevent buffer overflow
    }
  }
  
  if (index > 0) {
    // Parse and print the received data
    String data = String(buffer);
    Serial.println(data);
  }
}
