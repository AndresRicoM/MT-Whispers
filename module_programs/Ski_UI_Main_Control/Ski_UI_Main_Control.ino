/*

███████╗██╗  ██╗██╗    ██╗    ██╗██╗  ██╗██╗███████╗██████╗ ███████╗██████╗ ███████╗
██╔════╝██║ ██╔╝██║    ██║    ██║██║  ██║██║██╔════╝██╔══██╗██╔════╝██╔══██╗██╔════╝
███████╗█████╔╝ ██║    ██║ █╗ ██║███████║██║███████╗██████╔╝█████╗  ██████╔╝███████╗
╚════██║██╔═██╗ ██║    ██║███╗██║██╔══██║██║╚════██║██╔═══╝ ██╔══╝  ██╔══██╗╚════██║
███████║██║  ██╗██║    ╚███╔███╔╝██║  ██║██║███████║██║     ███████╗██║  ██║███████║
╚══════╝╚═╝  ╚═╝╚═╝     ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝
                                                                                    
  Main code for Ski UI. The UI is responsible for controlling both ski modules. 
  It receives voice commands through voice shield, activates the visual fiber optic display
  and send commands to modules via RF.

  File name and flags are set by the main UI. 
    
  Andres Rico - MIT Media Lab City Science Group - 2019

*/

#include <SPI.h>
#include <SD.h>
//#include <nRF24L01.h>
#include <RF24.h>
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
  #include <avr/power.h>
#endif

#define PIN 6 //8 Teensy

int pixel_num = 1;

RF24 radio(9, 10); // CE, CSN (9,5) Teensy

Adafruit_NeoPixel strip = Adafruit_NeoPixel(pixel_num, PIN, NEO_GRB + NEO_KHZ800);

const byte addresses [][6] = {"10911", "10917"}; // MSN, MSG 

int button_pin = 2; //2 - 5
boolean button_state = 0;
bool stuck = false;
unsigned long start_time, block_time;
bool collecting = false;

byte audio = 0;
int voice_state = 0;


void setup() {
  
  Serial.begin(115200);
  Serial1.begin(9600); //Serial for voice interface. 

  Serial.println("Setting up voice interface");
  delay(2000);
  Serial1.write(0xAA);
  Serial1.write(0x37);
  delay(1000);
  Serial1.write(0xAA);
  Serial1.write(0x21);
  Serial.println("Finished setting up interface!");

  pinMode(button_pin, INPUT_PULLUP);

  randomSeed(analogRead(A0));

  radio.begin();
  radio.openWritingPipe(addresses[1]);
  radio.openReadingPipe(1, addresses[0]);      
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();  

  strip.begin();
  strip.show();

  Serial.println("Connecting to external modules...");
  //start_radio();
  /*all_lights_on(255,0,0);
  delay(1000);
  all_lights_on(0,255,0);
  delay(1000);
  all_lights_on(0,0,255);
  delay(1000);
  rainbow(15);
  delay(1000);*/
  all_lights_on(0,255,255);
  delay(100);
  Serial.println("Ready to begin!");
  
}

void loop() {

  
  if (Serial1.available()) {
    rainbow(10);
    audio = Serial1.read();
    Serial.println(audio);
  }

  voice_select();
  button_state = digitalRead(button_pin); //This will be changed to voice commands.
  
  if (voice_state == 4) {
    send_rf_cmd("FM");
    delay(300);

    for (int i = 0; i < 5 ; i++) {
      all_lights_on(0,255,0);
      delay(200);
      all_lights_off();
      delay(100);
    }
    all_lights_on(255,0,0);
    voice_state = 0;
    
  }
  
  if ((!button_state || voice_state == 2)  && !collecting) {

    collecting = true;
    
    send_rf_cmd("BR");
        
    String new_code = new_file_name();
    delay(400);
    //unfailable_send(new_code);
    for (int i = 0; i < 5; i++) {
      send_rf_cmd(new_code);
    }
    //send_rf_cmd(new_code);
    //delay(500);
    for (int i = 0; i < 5 ; i++) {
      all_lights_on(0,255,0);
      delay(200);
      all_lights_off();
      delay(100);
    }
    all_lights_on(255,0,0);
  }

  button_state = digitalRead(button_pin);
  //Serial.println(button_state);

  if ((!button_state || voice_state == 3)  && collecting) {
    collecting = false;

    //all_lights_on(0,255,255);

    //unfailable_send("ER");//End Recording
    for (int i = 0; i < 5; i++) {
      send_rf_cmd("ER");
      delay(10);
    }
    //String new_code = new_file_name();
    delay(300);
    //unfailable_send(new_code);
    //delay(500);
    for (int i = 0; i < 5 ; i++) {
      all_lights_on(0,255,0);
      delay(200);
      all_lights_off();
      delay(100);
    }
    all_lights_on(0,255,255);
  }
  
}

void start_radio() { //Function listens to find left and right modules. 
  
  bool right_connected = false;
  bool left_connected = false;
  char incoming[3] = ""; 

  radio.startListening();
  Serial.println(radio.available());

  while(!radio.available()); //Waits until new message is received. 
  
  radio.read(&incoming, sizeof(incoming));
  Serial.println(incoming);
  
  if (incoming[0] == 'R' && incoming[1] == 'R') {
    
    right_connected = true; 
    Serial.println("Right Radio Is Connected");
  
  } 

  if (incoming[0] == 'L' && incoming[1] == 'R') {
    
    left_connected = true; 
    Serial.println("Left Radio Is Connected");
    
  }

  while(!radio.available()); //Waits until new message is received. 

  radio.read(&incoming, sizeof(incoming)); 
  Serial.println(incoming);

  if (incoming[0] == 'R' && incoming[1] == 'R') {
    
    right_connected = true; 
    Serial.println("Right Radio Is Connected");
  
  } 

  if (incoming[0] == 'L' && incoming[1] == 'R') {
    
    left_connected = true; 
    Serial.println("Left Radio Is Connected");
  
  }

  if (right_connected && left_connected) {
    Serial.println("RF connection has been made!");
    //Add LED signal. 
  } else {
    Serial.println("Not Connected.");
    
  }
  
}

String new_file_name() { //Function creates a new random name to write on module files. 
  
  long random_number = random(100,999);
  String file_code = String(random_number);
  return  file_code;
  
}

void send_rf_cmd(String message) { //Function sends a command via radio. Takes string as argument and converts to char to send. 

  char mess[4] = "000";
  strcpy(mess, message.c_str());
  Serial.println(mess);
  radio.stopListening();
  radio.write(&mess, sizeof(mess));
  
}


bool confirm_rf(String conf_mess) { //Boolean function to confrim if RF was received by slave module. Takes a wanted string as argument. 
  
  char confirmation[4] = "000";
  
  strcpy(confirmation, conf_mess.c_str());
  
  radio.startListening();

  if (radio.available()) {

    char in[4] = "";
    radio.read(&in, sizeof(in));
    //Serial.println(in);
  
    if (in[0] == confirmation[0] && in[1] == confirmation[1]) {
      
      //Serial.println("Message has been correctly delivered by Radio");
      return true;
    }
    
  }
}

bool timed_check(String confirm_string) { //Checks that sent command has been received and adds timeout break. 

  start_time = millis();
    
    while (!confirm_rf(confirm_string) && !stuck) { //Confirms that both modules have received the file name.
      
      block_time = millis() - start_time;
      
      if (block_time >= 500) {
        Serial.println("Response Time Exceeded");
        stuck = true;
      }
    }

    if (stuck) {
      Serial.print("Did not receive confirmation from: ");
      Serial.println(confirm_string);
      //////////WILL NEED TO ADD IF STATEMENT FOR INDICATING WHICH MODULE FAILED.
    }  
}

void unfailable_send(String cmd) { //Resends message until confirmation from receivers is true. 
  
  do { //Make sure file name is received. 

      stuck = false;
      send_rf_cmd(cmd);
      Serial.println("Message has been sent.");
      delay(50);
  
      timed_check("RR");
      timed_check("LR");
      
      Serial.println("Message sending process ended.");
      
      if (stuck) {
        delay(2500);
      }
      
    } while (stuck);

    stuck = false;
    Serial.println("Never Fails");
  
}

void all_lights_on(unsigned int r1, unsigned int g1, unsigned int b1) { //Turns lights on with specified rgb values. 
  for (int i = 0; i <= pixel_num; i++) {
    strip.setPixelColor(i, r1, g1, b1);
    delay(10);
  }
  strip.show();
}

void all_lights_off() {
  for (int i = 0; i <= pixel_num; i++) {
    strip.setPixelColor(i, 0, 0, 0);
    delay(10);
  }
  strip.show();
}

void voice_select() {
  switch (audio) {
    case 0x11:
      Serial.println("Activating Ski...");
      voice_state = 1;
      all_lights_on(0,0,255);
      Serial.println("Ski has been activated!");
    break;

    case 0x12:
      Serial.println("Beginning Log...");
      voice_state = 2;
      //delay(2000);
      Serial.println("Log has begun!");
    break;

    case 0x13:
      Serial.println("Ending Data Collection...");
      voice_state = 3;
      //delay(2000);
      Serial.println("Data collection has ended!");
    break;

    case 0x14:
      Serial.println("Flagging Moment...");
      voice_state = 4;
      //delay(2000);
      Serial.println("Moment has been flagged!");
    
    break;

    case 0x15:
      Serial.println("Switching to group 2...");
      voice_state = 5;
      //delay(2000);
      Serial.println("Group 2 is Active!");
    break;
    
   }
   audio = 0;
}

void rainbow(uint8_t wait) {
  uint16_t i, j;

  for(j=0; j<256; j++) {
    for(i=0; i<strip.numPixels(); i++) {
      strip.setPixelColor(i, Wheel((i+j) & 255));
    }
    strip.show();
    delay(wait);
  }
}

uint32_t Wheel(byte WheelPos) {
  WheelPos = 255 - WheelPos;
  if(WheelPos < 85) {
    return strip.Color(255 - WheelPos * 3, 0, WheelPos * 3);
  }
  if(WheelPos < 170) {
    WheelPos -= 85;
    return strip.Color(0, WheelPos * 3, 255 - WheelPos * 3);
  }
  WheelPos -= 170;
  return strip.Color(WheelPos * 3, 255 - WheelPos * 3, 0);
}

///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////
//DEBUGGING FUNCTIONS /////////////////////////////////////////////////////////////////////
///////////////////////////////////////////////////////////////////////////////////////////

void print_radio() { //Fuction used for debugging. 
  
  radio.startListening();

  if (radio.available()) {                      //Looking for the data.{
      
      char incoming[4] = "";                      //Saving the incoming data
      radio.read(&incoming, sizeof(incoming));    //Reading the data
      Serial.println(incoming);

    }
}
