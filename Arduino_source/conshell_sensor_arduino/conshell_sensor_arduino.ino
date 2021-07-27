// install "HX711 Arduino Library" by Bogdan Necula
#include "HX711.h"
// install "Adafruit Unified Sensor" by Adafruit 
#include <Adafruit_Sensor.h>
// install "DHT sensor library" by Adafruit
#include <DHT.h>
#include <DHT_U.h>

#define calibration_factor_2    600       // Roadcell 2 calibration value
//#define calibration_factor_3    900     // Roadcell 3 calibration value 
//#define calibration_factor_4    -400    // Roadcell 4 calibration value 
#define DHTPIN                  11        // Digital pin connected to the DHT sensor 
#define DHTTYPE                 DHT22     // DHT 22 (AM2302)
#define toggle_sw               13        // toggle switch 
#define led                     7         // LED 

const int LOADCELL_2_DOUT_PIN = 3;        // HX711 circuit wiring
const int LOADCELL_2_SCK_PIN = 2;
//const int LOADCELL_3_DOUT_PIN = 5;      // HX711 circuit wiring
//const int LOADCELL_3_SCK_PIN = 4;
//const int LOADCELL_4_DOUT_PIN = 9;      // HX711 circuit wiring
//const int LOADCELL_4_SCK_PIN = 6;

// Sensor data struct
struct cage_data{
  float temperature;                      // DHT22 temperature value
  float humidity;                         // DHT22 humidity value 
  float weight;                           // HX711 roadcell weight value
};

// Roadcell instance
HX711 scale_2;
//HX711 scale_3;
//HX711 scale_4;
                       
DHT_Unified dht(DHTPIN, DHTTYPE);         // Temperature and humidity instance 
cage_data cage = { 0.0, 0.0, 0.0};        // cage data struct instance 

long scale_2_var;
//long scale_3_var;
//long scale_4_var;

void setup() { 
  Serial.begin(115200);
  Serial.println("Conshell Start");
  pinMode(toggle_sw, INPUT);
  pinMode(led, OUTPUT);

  // DTH sensor
  dht.begin();
  sensor_t sensor;
  dht.temperature().getSensor(&sensor);
  dht.humidity().getSensor(&sensor);
  
  // roadcell 
  scale_2.begin(LOADCELL_2_DOUT_PIN, LOADCELL_2_SCK_PIN);
  scale_2.set_scale(calibration_factor_2);
  scale_2.tare();
  //scale_3.begin(LOADCELL_3_DOUT_PIN, LOADCELL_3_SCK_PIN);
  //scale_3.set_scale(calibration_factor_3);
  //scale_3.tare();
  //scale_4.begin(LOADCELL_4_DOUT_PIN, LOADCELL_4_SCK_PIN);
  //scale_4.set_scale(calibration_factor_4);
  //scale_4.tare();
}



void loop() {

  int sw_in = 0;
  char inCommand;
  char onoff;
  String inString = "";
  if(Serial.available()>0){
    if(Serial.available()){
      inString = Serial.readStringUntil('\n');
    } 
    inCommand = inString[0];
    onoff = inString[1];
    if(inCommand == 'a'){
      if(onoff == '1'){
        digitalWrite(led, HIGH);
      }else if(onoff == '0'){
        digitalWrite(led, LOW);
      }
    }
  }
  // Roadcell operation 
  if (scale_2.is_ready()) {
    scale_2_var = (long)scale_2.get_units();
  }
  //if (scale_3.is_ready()) {
  //  scale_3_var = (long)scale_3.get_units();
  //}
  //if (scale_4.is_ready()) {
  //  scale_4_var = (long)scale_4.get_units();
  //}
  //cage.weight = (float)((scale_2_var+scale_3_var+scale_4_var)/3);
  cage.weight = (float)scale_2_var;
  
  // DTH sensor operation 
  sensors_event_t event;
  dht.temperature().getEvent(&event);
  if (isnan(event.temperature)) {
    Serial.println("temperature error");
  }else {
    cage.temperature = event.temperature;
  }

  // Get humidity event and get its value.
  dht.humidity().getEvent(&event);
  if (isnan(event.relative_humidity)) {
    Serial.println("humidity error");
  }else {
    cage.humidity = event.relative_humidity;
  }

  // check toggle switch on/off
  sw_in = digitalRead(toggle_sw);
  // Send data to Raspberry pi 
  // protocol: a+"roadcell value"+b+"temperature value"+c+"humidity value"+d+"switch on/off"+e
  Serial.print("a");
  Serial.print(cage.weight);
  Serial.print("b");
  Serial.print(cage.temperature);
  Serial.print("c");
  Serial.print(cage.humidity);
  Serial.print("d");
  if(sw_in == HIGH){
    Serial.print("1");
  }else{
    Serial.print("0");
  }
  Serial.println("e");
  // To send packet to RPI properly, keep 500ms interval for loop().
  delay(500);
}
