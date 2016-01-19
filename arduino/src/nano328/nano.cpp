#include <Arduino.h>
#include "constants.h"
#include "dht11.h"

// Definitions
void blink();
int getHumidityYL38();

// Initialization
dht11 dht11;
long _last_toggle = millis();
bool _last_state_led = true;

void setup()
{
  // IO
  Serial.begin(115200);
  pinMode(A5, INPUT);


  // Start messages
  Serial.println("Start");
  // Serial.println("blinking");
}

void loop()
{
    // Blink LED
    blink();

    // Humidity from YL-38
    // Serial.println("------ YL-38 ------");
    // Serial.print("Humidity: ");
    // // Serial.print((float)getHumidityYL38()/10.24);
    // // Serial.println("\%");
    // Serial.println(getHumidityYL38());

    // Temperature and humidity from DHT11
    dht11.read(4);
    Serial.println();
    Serial.println("------ DHT11 ------");
    Serial.print("Temperature: ");
    Serial.println(dht11.temperature);
    Serial.print("Humidity:    ");
    Serial.print(dht11.humidity);
    Serial.print("\%     ");

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

