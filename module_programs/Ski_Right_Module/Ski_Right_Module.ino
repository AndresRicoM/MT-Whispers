 /*

███████╗██╗  ██╗██╗    ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ███████╗
██╔════╝██║ ██╔╝██║    ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝
███████╗█████╔╝ ██║    ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝███████╗
╚════██║██╔═██╗ ██║    ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
███████║██║  ██╗██║    ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                    
  Code for right ski data system. The system is based on a Teensy 3.2 Board and a terMITE
  This module coññllects data from:
  - 9 axis IMU
  - Pressure Sensor
  - Temperature Sensor
  - Analog SM Piezo Array

  Data is stored locally and activation of the device is triggered via RF communication received from the main UI module. 
  
  Andres Rico - MIT Media Lab City Science Group - 2019

*/

#include <SPI.h> //Include libraries for communication with an SD card.
#include <SD.h>

#include <nRF24L01.h> //Radio communication. 
#include <RF24.h>

#include <Adafruit_NeoPixel.h> //LED Indicator
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

RF24 radio(9, 10); // CE, CSN         
const byte addresses [][6] = {"10911", "10917"};
char file_name[6] = "";

String t1_data; //Data Handling Strings.

unsigned long millis_stamp;

const byte ter1_Chars = 40;

char ter1_receivedChar[ter1_Chars]; // an array to store the received data

String received;
String debug;

bool new_t1_data = true;
bool active_recording = false;
bool active_pin = false;

bool collecting = false; 

int buttonPin = 2;

File myFile; //Declare file object for using SD library fucntions.
Adafruit_NeoPixel strip = Adafruit_NeoPixel(1, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  
  Serial.begin(115200); //Begin Serial
  Serial1.begin(57600); 
  
  strip.begin();


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

  Serial.println("Initializing Radio Communication...");

  radio.begin();                  //Starting the Wireless communication
  radio.openWritingPipe(addresses[0]); //Setting the address where we will send the data
  radio.openReadingPipe(1, addresses[1]);  //Setting the address for receiving data
  radio.setPALevel(RF24_PA_MIN);  //You can set it as minimum or maximum depending on the distance between the transmitter and receiver.
  radio.stopListening();
  Serial.println("Radio Initialized!");

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
    
  Serial.println("Calibrating Gyro...");
  //delay(60000); //Wait for calibration of Gyro. 
  strip.setPixelColor(0,0,255,255);
  strip.show();
  Serial.println("Ready to Start!");
}

void loop() {
  //get_data();
  
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

    Serial.println("Received file name!");
    
    Serial.println("RECORDING DATA");
    strip.setPixelColor(0,255,0,0);
    strip.show();
    Serial.flush();

        
  }

  
  while (active_recording) {

    myFile.print(get_data());
    //get_data();
    check_radio_activation();
    check_pin();
    
  }

  strip.setPixelColor(0,0,255,255);
  strip.show();
  myFile.close();
  
} 

String get_data() {

  static byte index = 0;
  char end_signal = '\n';
  new_t1_data = false;
  String received_termite = "";
  bool starting = false;
  
     while (Serial1.available() > 0 && new_t1_data == false) {
      char t = Serial1.read();
      received_termite += t; 
      if (t == end_signal) {
        //Serial.print(received_termite);
        //A0 = Front -> A9 = Back
        String extra = String(millis()) + "," + String(analogRead(A0)) + "," + String(analogRead(A1)) + "," + String(analogRead(A2)) + "," + String(analogRead(A6)) + "," + String(analogRead(A9)) + "," ;
        received_termite += extra;
        new_t1_data = true;
        Serial.println(received_termite);
        return received_termite;
      }
      }
}



void write_data() {
   
 if (new_t1_data == true) { //&& new_t2_data == true) {

   myFile = SD.open(file_name, FILE_WRITE);
   
    if (myFile) {
      
      myFile.print(received);
      
      myFile.close();
      Serial.println("Done Writing.");
    } else {
      Serial.println("Error writing.");
    }
  }
}

void send_rf_cmd(String message) { //Function sends a command via radio. Takes string as argument and converts to char to send. 

  char mess[4] = "000";
  strcpy(mess, message.c_str());
  //Serial.println(mess);
  radio.stopListening();
  radio.write(&mess, sizeof(mess));
  Serial.println("Sent Radio Message");
  
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
  //Serial.println(radio.available());
  if (radio.available()) {
    
    char incoming[3] = ""; 

    radio.read(&incoming, sizeof(incoming));
    Serial.println(incoming);
    
    
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
