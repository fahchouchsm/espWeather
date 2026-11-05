#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>
#include <DHT.h>
#include "secrets.h"

#define DHTPIN D1
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(115200);
  dht.begin();
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Connexion Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWi-Fi connecte");
  Serial.println(WiFi.localIP());
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Erreur lecture DHT11");
    delay(5000);
    return;
  }

  String json = "{\"temperature\":" + String(temperature, 1)
              + ",\"humidity\":" + String(humidity, 1) + "}";
  Serial.println("JSON envoye : " + json);

  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    HTTPClient http;
    http.begin(client, SERVER_URL);
    http.addHeader("Content-Type", "application/json");
    int httpCode = http.POST(json);
    Serial.print("Code HTTP : ");
    Serial.println(httpCode);
    if (httpCode > 0) {
      Serial.println("Reponse : " + http.getString());
    } else {
      Serial.println("Erreur connexion : " + http.errorToString(httpCode));
    }
    http.end();
  } else {
    Serial.println("Wi-Fi deconnecte");
  }
  delay(1200000UL); // Une mesure toutes les 20 minutes (20 * 60 * 1000 ms)
}
