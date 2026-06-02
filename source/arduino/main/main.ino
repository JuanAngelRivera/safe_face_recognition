#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "Santos111@_2.4Gnormal"; // tiene que ser 2.4G
const char* password = "CARH780217HTLRDG02@";

WebServer server(80);

const int greenLed = 33;
const int redLed = 27;
const int buzzer = 25;

void handleOpen() {
  digitalWrite(greenLed, HIGH);
  tone(buzzer, 1000);
  delay(1000);

  digitalWrite(greenLed, LOW);
  noTone(buzzer);

  server.send(200, "text/plain", "ACCESS GRANTED");
}

void handleDeny() {
  digitalWrite(redLed, HIGH);
  tone(buzzer, 300);
  delay(1500);

  digitalWrite(redLed, LOW);
  noTone(buzzer);

  server.send(200, "text/plain", "ACCESS DENIED");
}

void setup() {
  Serial.begin(115200);

  pinMode(greenLed, OUTPUT);
  pinMode(redLed, OUTPUT);
  pinMode(buzzer, OUTPUT);

  WiFi.begin(ssid, password);

  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  Serial.println(WiFi.localIP());

  server.on("/open", handleOpen);
  server.on("/deny", handleDeny);

  server.begin();
}

void loop() {
  server.handleClient();
}