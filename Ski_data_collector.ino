 /*

███████╗██╗  ██╗██╗    ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ███████╗
██╔════╝██║ ██╔╝██║    ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝
███████╗█████╔╝ ██║    ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝███████╗
╚════██║██╔═██╗ ██║    ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
███████║██║  ██╗██║    ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                    
  Main code for ski sensor data storage. 
  Andres Rico - MIT Media Lab City Science Group - 2019

*/

#include <SPI.h> //Include libraries for communication with an SD card.
#include <SD.h>

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6

//String piezo_0, piezo_1, piezo_2, piezo_3, piezo_4, complete_piezo, t1_data, t2_data, complete_data, GPS_Data; //Data Handling Strings.
String t1_data; //Data Handling Strings.
String file_name = "";

/*const int piezo_pin0 = A0; //Decalare pins to use by each piezo electric strip. 
const int piezo_pin1 = A1;
const int piezo_pin2 = A2; 
const int piezo_pin3 = A3; 
const int piezo_pin4 = A4;*/

const int buttonPin = A9;
int buttonState = 0;
bool collecting = false; 

int reset_count = 0;

const byte ter1_Chars = 100;
//const byte ter2_Chars = 35;

char ter1_receivedChar[ter1_Chars]; // an array to store the received data
//char ter2_receivedChar[ter2_Chars]; // an array to store the received data

boolean new_t1_data = false;
boolean new_t2_data = false;

File myFile; //Declare file object for using SD library fucntions.
Adafruit_NeoPixel strip = Adafruit_NeoPixel(1, PIN, NEO_GRB + NEO_KHZ800);

void setup() {
  
  Serial.begin(115200); //Begin Serial
  Serial1.begin(57600); 
  Serial2.begin(57600);
  strip.begin();

  pinMode(buttonPin, INPUT);

  randomSeed(analogRead(A0));
  
  Serial.println("Initializing SD card...");

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
  Serial.println("SD initialization done!");
  for (int i = 0; i < 5; i++) {
      strip.setPixelColor(0,255,255,255);
      strip.show();
      delay(200);
      strip.setPixelColor(0,0,0,0);
      strip.show();
      delay(200);
    }
  delay(10000);
  strip.setPixelColor(0,0,255,255);
  strip.show();
  Serial.println("Ready to Start!");
}

void loop() {
  buttonState = digitalRead(buttonPin);
  //Serial.println(buttonState);
  /*get_termite1();
  write_data();*/

  if (buttonState == HIGH && collecting == false) {
    Serial.println("Data Collection Enabeled");
    file_name = String(random(0,1000));
    file_name = file_name + "_ski.txt";
    myFile = SD.open(file_name, FILE_WRITE); //Open file for writing sensor data.
    strip.setPixelColor(0,255,0,0);
    strip.show();
    collecting = true;
    delay(400);
    buttonState = digitalRead(buttonPin);
  }
  
  while (collecting) {
    //Serial.println("Collecting =) ! ");
    get_termite1();
    write_data();

    if (reset_count > 50) {
      myFile.close();
      myFile = SD.open(file_name, FILE_WRITE);
      reset_count = 0;
    }

    reset_count += 1;
    buttonState = digitalRead(buttonPin);
    
    if (buttonState == HIGH && collecting == true)  {
    Serial.println("Data Collection Disabeled");
    strip.setPixelColor(0,0,255,255);
    strip.show();
    collecting = false;
    myFile.close();
    delay(400);
    buttonState = digitalRead(buttonPin);
    }
  }
} 

void get_termite1() {
   static byte index = 0;
   char end_signal = '\n';
   char t;
   
     while (Serial1.available() > 0 && new_t1_data == false) {
      t = Serial1.read();
      Serial.print(t);
      if (t != end_signal) {
        ter1_receivedChar[index] = t;
        index++;
      if (index >= ter1_Chars) {
        index = ter1_Chars - 1;
        }
      }
      else {
        ter1_receivedChar[index] = '\0';
        index = 0;
        new_t1_data = true;
        //Serial.println(ter1_receivedChar);
      }
      }
}



void write_data() {
  
 new_t2_data = true;
 
 if (new_t1_data == true && new_t2_data == true) {

  if (strlen(ter1_receivedChar) < 99) {
    if (myFile) {
      myFile.print(ter1_receivedChar);
      //myFile.close();
      Serial.println("Done Writing.");
    } else {
      Serial.println("Error writing.");
    }  
    }
    new_t1_data = false;
    new_t2_data = false;
  }
}

//Function for assigning piezo electric strip data values.
/*void get_piezos () {
  
  piezo_0 = String(analogRead(piezo_pin0)); //Obtain analog values for each piezo strip. 
  piezo_1 = String(analogRead(piezo_pin1));
  piezo_2 = String(analogRead(piezo_pin2));
  piezo_3 = String(analogRead(piezo_pin3));
  piezo_4 = String(analogRead(piezo_pin4));

  complete_piezo = piezo_0 + "," + piezo_1 + "," + piezo_2 + "," + piezo_3 + "," + piezo_4;
  
}*/

//Use this fucntion to have access to two terMITes. 

/*void get_termite2() {
   static byte index = 0;
   char end_signal = '\n';
   char t;
   
   //if (Serial1.available() > 0) {
     while (Serial2.available() > 0 && new_t2_data == false) {
      t = Serial2.read();
      if (t != end_signal) {
        ter2_receivedChar[index] = t;
        index++;
      if (index >= ter2_Chars) {
        index = ter1_Chars - 1;
        }
      }
      else {
        ter2_receivedChar[index] = '\0';
        index = 0;
        new_t2_data = true;
      }
      }
   //}
}*/
