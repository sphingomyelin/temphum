#ifndef _DHT11_
#define _DHT11_

#include <Arduino.h>

#define DHTLIB_OK 			   0
#define DHTLIB_ERROR_CHECKSUM -1
#define DHTLIB_ERROR_TIMEOUT -2

class dht11 {
public:
	int read(int pin);
	int humidity;
	int temperature;
};

#endif