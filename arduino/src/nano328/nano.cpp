#include <Arduino.h>
#include "constants.h"
#include "DHTlib.h"

// Definitions
void blink();
int getHumidityYL38();

#define DHT22_PIN 6

// Initialization
dht DHT;
// dht11 dht11;
long _last_toggle = millis();
bool _last_state_led = true;

void setup()
{
  // IO
  Serial.begin(115200);
  pinMode(DHT22_PIN, INPUT);

  // Start messages
  // Serial.println("Start");
  // Serial.println("blinking");
}

void loop()
{
  // Blink LED
  // blink();

  // Humidity from YL-38
  // Serial.println("------ YL-38 ------");
  // Serial.print("Humidity: ");
  // // Serial.print((float)getHumidityYL38()/10.24);
  // // Serial.println("\%");
  // Serial.println(getHumidityYL38());

  // Temperature and humidity from DHT11
  // dht11.read(4);

  // Read DHT22 data
  // Serial.print("DHT22, \t");
  // int chk = DHT.read22(DHT22_PIN);
  // switch (chk)
  // {
  //   case DHTLIB_OK:  
  //   Serial.print("OK,\t");
  //   break;
  //   case DHTLIB_ERROR_CHECKSUM: 
  //   Serial.print("Checksum error,\t"); 
  //   break;
  //   case DHTLIB_ERROR_TIMEOUT: 
  //   Serial.print("Time out error,\t"); 
  //   break;
  //   default: 
  //   Serial.print("Unknown error,\t"); 
  //   break;
  // }
  // Display data: human readable
  // Serial.println();
  // Serial.println("------ DHT22 ------");
  // Serial.print("Temperature: ");
  // Serial.println(DHT.temperature, 1);
  // Serial.print("Humidity:    ");
  // Serial.print(DHT.humidity, 1);
  // Serial.print("\%     ");

  int chk = DHT.read22(DHT22_PIN);
  switch (chk)
  {
    case DHTLIB_OK:
      Serial.println();
      Serial.print("temp: ");
      Serial.println(DHT.temperature, 1);
      Serial.print("humi: ");
      Serial.println(DHT.humidity, 1);
    break;
    case DHTLIB_ERROR_CHECKSUM: 
    break;
    case DHTLIB_ERROR_TIMEOUT: 
    break;
    default: 
    break;
  }

  delay(500);
}

void blink() {
  if(millis() - _last_toggle > LED_PRD/2) {
    if(_last_state_led == true) {
      digitalWrite(LED, LOW);
      _last_state_led = false;
    }
    else {
      digitalWrite(LED, HIGH);
      _last_state_led = true;
    }
    _last_toggle = millis();
  }
}


int getHumidityYL38() {
  return analogRead(A5);
}

