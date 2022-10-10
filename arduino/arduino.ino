#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

#include <Wire.h>
#include "mbedtls/md.h"

#include <BH1750.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

BH1750 lightMeter;
Adafruit_BME280 bme;

const char* ssid = "UPC3739675";
const char* password = "Zz3dvtzkhxw7";

String serverName = "http://192.168.0.164:8000/api/post";

unsigned long lastTime = 0;
unsigned long timerDelay = 1000;
int val = 0;
int soilPin = A0; 
int soilPower = 0;

void setup(){
  Serial.begin(9600);

  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");  
  }

  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());

  Wire.begin();
  bool status_bh = lightMeter.begin();
  if (!status_bh) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
  }

  bool status_bme = bme.begin(0x76);  
  if (!status_bme) {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
  }

  pinMode(soilPower, OUTPUT);
  digitalWrite(soilPower, LOW);
  
}

void loop() {
  
  hashdata();

  Serial.println();
  Serial.print("Soil Moisture = "); 
  Serial.println(readSoil());
  
  Serial.println();
  printValues();
  delay(1000);

  if ((millis() - lastTime) > timerDelay) {
    if(WiFi.status()== WL_CONNECTED){
      HTTPClient http;
    
      http.begin(serverName);

      http.addHeader("Content-Type", "application/x-www-form-urlencoded");
      String httpRequestData = construct_post_request();
      Serial.println(httpRequestData);
      int httpResponseCode = http.POST(httpRequestData);
     
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
        
      http.end();
    }
    else {
      Serial.println("WiFi Disconnected");
    }
    lastTime = millis();
  }
}

void printValues() {
  Serial.print("Light: ");
  Serial.print(lightMeter.readLightLevel());
  Serial.println(" lx");
  
  Serial.print("Temperature = ");
  Serial.print(bme.readTemperature());
  Serial.println(" *C");
  
  Serial.print("Pressure = ");
  Serial.print(bme.readPressure() / 100.0F);
  Serial.println(" hPa");
  
  Serial.print("Humidity = ");
  Serial.print(bme.readHumidity());
  Serial.println(" %");
  
  Serial.println();
}

void hashdata() {

  char *key = "secretKeys";
  char *payload = "Tomako";
  byte hmacResult[32];
 
  mbedtls_md_context_t ctx;
  mbedtls_md_type_t md_type = MBEDTLS_MD_SHA256;
 
  const size_t payloadLength = strlen(payload);
  const size_t keyLength = strlen(key);            
 
  mbedtls_md_init(&ctx);
  mbedtls_md_setup(&ctx, mbedtls_md_info_from_type(md_type), 1);
  mbedtls_md_hmac_starts(&ctx, (const unsigned char *) key, keyLength);
  mbedtls_md_hmac_update(&ctx, (const unsigned char *) payload, payloadLength);
  mbedtls_md_hmac_finish(&ctx, hmacResult);
  mbedtls_md_free(&ctx);
 
  Serial.print("Hash: ");
 
  for(int i= 0; i< sizeof(hmacResult); i++){
      char str[3];
 
      sprintf(str, "%02x", (int)hmacResult[i]);
      Serial.print(str);
  }
}

int readSoil(){

    digitalWrite(soilPower, HIGH);
    delay(10);
    val = analogRead(soilPin); 
    digitalWrite(soilPower, LOW);
    return val;
}

void connect_wifi() {
    WiFi.begin(ssid, password);
    Serial.println("Connecting");
    while(WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");  
    }

    Serial.println("");
    Serial.print("Connected to WiFi network with IP Address: ");
    Serial.println(WiFi.localIP());

    return;
}

String construct_post_request() {
  StaticJsonDocument<200> data;

  data["temp"] = bme.readTemperature();
  data["humid"] = bme.readHumidity();
  data["pressure"] = bme.readPressure() / 100.0F;
  data["lumen"] = lightMeter.readLightLevel();
  data["moisture"] = readSoil();

  String requestBody;
  serializeJson(data, requestBody);

  return requestBody;
}
