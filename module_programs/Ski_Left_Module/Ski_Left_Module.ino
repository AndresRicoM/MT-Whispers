/*

███████╗██╗  ██╗██╗    ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ███████╗
██╔════╝██║ ██╔╝██║    ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝
███████╗█████╔╝ ██║    ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝███████╗
╚════██║██╔═██╗ ██║    ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
███████║██║  ██╗██║    ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                    
  Code for right ski data system. The system is based on a adafrut Feather M0 logger Board.
  The system collects data from:
  
  - GPS Module
  - Embedded Capacitive Sensor. 

  Data is stored locally and activation of the device is triggered via RF communication received from the main UI module. 
  
  Andres Rico - MIT Media Lab City Science Group - 2019

*/

#include <SPI.h>
#include <SD.h>

#include <nRF24L01.h>
#include <RF24.h>

#include <Adafruit_GPS.h>

#include <CapacitiveSensor.h>

#include <Adafruit_NeoPixel.h> //LED Indicator
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6 //Pin for LED indicator. 

#define GPSSerial Serial1

#define GPSECHO  false

Adafruit_GPS GPS(&GPSSerial);

RF24 radio(9, 10); // CE, CSN   
const byte addresses [][6] = {"10911", "10917"};
char file_name[6] = "";

uint32_t timer = millis(); //Used for GPS Control. 

bool active_recording = false;
bool active_pin = false;

int buttonPin = 5;

//bool collecting = false; 

File myFile; //Declare file object for using SD library fucntions.
Adafruit_NeoPixel strip = Adafruit_NeoPixel(1, PIN, NEO_GRB + NEO_KHZ800);

float latitude = 0;
float longitude = 0;
String lat, lon;

String filename;

CapacitiveSensor   cs_4_2 = CapacitiveSensor(11,12);

void setup() {

  Serial.begin(115200);

  strip.begin(); //Start LED indicator.

  pinMode(buttonPin, INPUT_PULLUP);

  randomSeed(analogRead(A0));

  Serial.println("Initializing SD Card...");

  if (!SD.begin(4)) {
    Serial.println("SD initialization has failed");
    for (int i = 0; i < 5; i++) {
      strip.setPixelColor(0,255,0,0);
      strip.show();
      delay(200);
      strip.setPixelColor(0,0,0,0);
      strip.show();
      delay(200);
    }
    return;
  }
  Serial.println("SD Initialized!");

  Serial.println("Initializing GPS Communication...");
  GPS.begin(9600); //Start communication with GPS. 
  GPS.sendCommand(PMTK_SET_NMEA_OUTPUT_RMCGGA);
  GPS.sendCommand(PMTK_SET_NMEA_UPDATE_1HZ);
  GPS.sendCommand(PGCMD_ANTENNA);
  Serial.println("GPS Initialized!");

  Serial.println("Initializing Radio Communication...");
  radio.begin();                  //Starting the Wireless communication Radio. 
  radio.openWritingPipe(addresses[1]); //Setting the address where we will send the data
  radio.openReadingPipe(1, addresses[0]);  //Setting the address for receiving data
  radio.setPALevel(RF24_PA_MAX);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.stopListening();
  Serial.println("Radio Initilized!");


  delay(1000);
  send_rf_cmd("RR");
  delay(200);
  send_rf_cmd("LR");
  delay(500);

   for (int i = 0; i < 5; i++) { //Blink in white to show success. 
    
      strip.setPixelColor(0,255,255,255);
      strip.show();
      delay(200);
      strip.setPixelColor(0,0,0,0);
      strip.show();
      delay(200);
      
    }

  strip.setPixelColor(0,0,255,255);
  strip.show();
  Serial.println("Ready to Start!");
  
}

void loop() {

  if (!active_recording) {
    check_radio_activation();
    check_pin();
  }

  if (active_pin) {
    
    String prand = String(random(100,999));
    file_name[0] = prand [0];
    file_name[1] = prand [1];
    file_name[2] = prand [2];
    file_name[3] = '.';
    file_name[4] = 't';
    file_name[5] = 'x';
    file_name[6] = 't';
    myFile = SD.open(file_name, FILE_WRITE);    
    Serial.println("RECORDING DATA");
    strip.setPixelColor(0,255,0,0);
    strip.show();
    Serial.flush();
    
  }
  
  if (active_recording && !active_pin) {
    radio.startListening();
    char incoming[4] = ""; 

    Serial.println("Waiting for file name...");
    
    while (!radio.available());
      
    radio.read(&incoming, sizeof(incoming)); //Read file name. 
    Serial.println(incoming);
    
    file_name[0] = incoming [0];
    file_name[1] = incoming [1];
    file_name[2] = incoming [2];
    file_name[3] = '.';
    file_name[4] = 't';
    file_name[5] = 'x';
    file_name[6] = 't';
    
    Serial.println(file_name);

    myFile = SD.open(file_name, FILE_WRITE);
  
    /*delay(200);
    send_rf_cmd("RR");
    delay(100);// Send confirmation Message.
    send_rf_cmd("LR");*/
    
    //radio.stopListening();
    Serial.println("Received file name!");
  
    Serial.println("RECORDING DATA");
    strip.setPixelColor(0,255,0,0);
    strip.show();
    Serial.flush();
      
  }

  while (active_recording) {

    strip.setPixelColor(0,255,0,0);
    strip.show();
    
    //Serial.println("I am here");
    char c = GPS.read();
    
    if (GPS.newNMEAreceived()) {
  
      if (!GPS.parse(GPS.lastNMEA()));
        //Serial.println("I WILL RETURN!");   
        //return; 
    }
  
    if (timer > millis())  timer = millis(); //Reset timer if it wraps. 
  
    if (millis() - timer > 25) { //Prints out current information every 25 milliseconds. 
      
      timer = millis(); // reset the timer

  
      if (GPS.fix) {

        strip.setPixelColor(0,0,255,0);
        strip.show();
 
        long start = millis();
        long total1 =  cs_4_2.capacitiveSensor(30);
        
        latitude = (GPS.latitude);
        longitude = (GPS.longitude);
        lat = GPS.lat;
        lon = GPS.lon;

        Serial.print(millis()); Serial.print(",");
        Serial.print(latitude, 4); Serial.print(",");
        Serial.print(lat); Serial.print(",");
        Serial.print(longitude, 4); Serial.print(",");
        Serial.print(lon); Serial.print(",");
        Serial.println (total1);

        myFile = SD.open(file_name, FILE_WRITE);

        myFile.print(millis()); myFile.print(",");
        myFile.print(latitude, 4); myFile.print(",");
        myFile.print(lat); myFile.print(",");
        myFile.print(longitude, 4); myFile.print(",");
        myFile.print(lon); myFile.print(",");
        myFile.println (total1);

        myFile.close();

        strip.setPixelColor(0,0,0,0);
        strip.show();
                
      } 
      
    }
    
    check_radio_activation();
    check_pin();
    
  }

  strip.setPixelColor(0,0,255,255);
  strip.show();
  myFile.close();
  
}

void print_radio() {
  
  radio.startListening();

  if (radio.available()) {                      //Looking for the data.{
      
      char incoming[4] = "";                      //Saving the incoming data
      radio.read(&incoming, sizeof(incoming));    //Reading the data
      Serial.println(incoming);
  
      delay(200);
      send_rf_cmd("RR");
      delay(100);
      send_rf_cmd("LR");

    }
}

void send_rf_cmd(String message) { //Function sends a command via radio. Takes string as argument and converts to char to send. 

  char mess[4] = "000";
  strcpy(mess, message.c_str());
  Serial.println(mess);
  radio.stopListening();
  radio.write(&mess, sizeof(mess));
  
}

void check_pin() {
  //Serial.println(digitalRead(buttonPin));
  if (!digitalRead(buttonPin)) {
    if (!active_recording) {
      active_recording = true;
      active_pin = true;
      Serial.println("Acivation By Buuton");
      delay(350);
    } else if (active_recording) {
      active_recording = false;
      active_pin = false;
      Serial.println("Stoped With Button");
      delay(350);
    }
  }
}

void check_radio_activation() {
  radio.startListening();
  
  if (radio.available()) {
    
    char incoming[3] = ""; 

    radio.read(&incoming, sizeof(incoming));
    Serial.println(incoming);
    delay(200);
    
    /*send_rf_cmd("RR");
    delay(100);
    send_rf_cmd("LR");*/
    
    if (incoming[0] == 'B' && incoming[1] == 'R') {
      
      active_recording = true; 
      Serial.println("Recording Has Been Activated");
    } 

    if (incoming[0] == 'E' && incoming[1] == 'R') {
      
      active_recording = false; 
      Serial.println("Recording Has Been Deactivated");
    }

  } 
}
