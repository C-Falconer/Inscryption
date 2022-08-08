#include <ShiftIn.h>
#include <SPI.h>
#include <MFRC522.h>

#define SCK 13
#define MISO 12
#define MOSI 11
#define MUX 10
#define RST 9
//8
//7
#define CP 6
#define _Q7 5
//4
#define MFRC9 3
#define MFRC10 2
#define s0 A0
#define s1 A1
#define s2 A2
#define _PL A3
#define _CE A4
//A5

int selectionLines[3] = {s0, s1, s2};

MFRC522 mfrc522(MUX, RST);
MFRC522 mfrc522_9(MFRC9, RST);
MFRC522 mfrc522_10(MFRC10, RST);

MFRC522 mfrc522s[3] = {mfrc522, mfrc522_9, mfrc522_10};

ShiftIn<2> shift;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  while(!Serial);
  SPI.begin();
  mfrc522.PCD_Init();
  mfrc522_9.PCD_Init();
  mfrc522_10.PCD_Init();
  pinMode(CP, OUTPUT);
  pinMode(_Q7, INPUT);
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(_PL, OUTPUT);
  pinMode(_CE, OUTPUT);
  mfrc522.PCD_DumpVersionToSerial();
  mfrc522.PICC_DumpToSerial(&(mfrc522.uid));
  lineSelectMux(0);
  tester();
  shift.begin(_PL, _CE, _Q7, CP);
}

byte incoming;
byte incoming2;
byte preIncoming;
String input;
int current_MFRC = 0;
void loop() {
  // put your main code here, to run repeatedly:
//  pulsePL();
//  incoming = getData165();
//  //incoming2 = shiftIn(_Q7, CP, LSBFIRST);
//  if(incoming != preIncoming) {
//    Serial.println(incoming, BIN);
//    //Serial.println(incoming2, BIN);
//  }
//  preIncoming = incoming;
  if(shift.update()) {
    displayValues();
  }
  if(mfrc522s[current_MFRC].PICC_IsNewCardPresent() && mfrc522s[current_MFRC].PICC_ReadCardSerial()) {
    dump_byte_array(mfrc522s[current_MFRC].uid.uidByte, mfrc522s[current_MFRC].uid.size);
    Serial.println();
  }
  delay(200);
//  while (Serial.available() == 0) {if(mfrc522s[current_MFRC].PICC_IsNewCardPresent() && mfrc522s[current_MFRC].PICC_ReadCardSerial()) {
//    dump_byte_array(mfrc522s[current_MFRC].uid.uidByte, mfrc522s[current_MFRC].uid.size);
//    Serial.println();
//  }}
//  input = Serial.readString();
//  lineSelectMux(input.toInt());
}

//Shift Register
void pulsePL() {
  digitalWrite(_PL, LOW);
  delayMicroseconds(5);
  digitalWrite(_PL, HIGH);
  delayMicroseconds(5);
}

byte getData165() {
  digitalWrite(CP, HIGH);
  digitalWrite(_CE, LOW);
  byte incoming = shiftIn(_Q7, CP, LSBFIRST);
  digitalWrite(_CE, HIGH);
  return incoming;
}

void displayValues() {
  for(int i = 0; i < shift.getDataWidth(); i++)
    Serial.print( shift.state(i) ); // get state of button i
  Serial.println();
}

//Multiplexer
void lineSelectMux(int num) {
  if(num > 9 || num < 0) {
    return;
  }
  Serial.println(num);
  if(num == 8) {
    mfrc522_9.PCD_Init();
    current_MFRC = 1;
    //Serial.print("8");
    return;
  } else if(num == 9) {
    mfrc522_10.PCD_Init();
    current_MFRC = 2;
    //Serial.print("9");
    return;
  }
  for(int i = 0; i < 3; i++) {
    digitalWrite(selectionLines[i], num % 2);
    //Serial.print(num % 2);
    num /= 2;
  }
  current_MFRC = 0;
  mfrc522.PCD_Init();
}

//Extra Functions
void dump_byte_array(byte * buffer, byte bufferSize) {
  for (byte i = 0; i < bufferSize; i++) {
    Serial.print(buffer[i] < 0x10 ? " 0" : " ");
    Serial.print(buffer[i], HEX);
  }
}

void tester() {
  byte tmp;
  mfrc522.PCD_WriteRegister(mfrc522.TPrescalerReg, 0x3E);   // TPreScaler = TModeReg[3..0]:TPrescalerReg, ie 0x0A9 = 169 => f_timer=40kHz, ie a timer period of 25�s.
  tmp = mfrc522.PCD_ReadRegister(mfrc522.TPrescalerReg);
  Serial.print("TPrescalerReg ");
  Serial.println(tmp, HEX);
  
  mfrc522.PCD_WriteRegister(mfrc522.TReloadRegH, 0);    // Reload timer with 0x3E8 = 1000, ie 25ms before timeout.
  tmp = mfrc522.PCD_ReadRegister(mfrc522.TReloadRegH);
  Serial.print("TReloadRegH ");
  Serial.println(tmp, HEX);
  
  mfrc522.PCD_WriteRegister(mfrc522.TReloadRegL, 30);
  tmp = mfrc522.PCD_ReadRegister(mfrc522.TReloadRegL);
  Serial.print("TReloadRegL ");
  Serial.println(tmp, HEX);
  

  mfrc522.PCD_WriteRegister(mfrc522.ModeReg, 0x3D);   // Default 0x3F. Set the preset value for the CRC coprocessor for the CalcCRC command to 0x6363 (ISO 14443-3 part 6.2.4)
  tmp = mfrc522.PCD_ReadRegister(mfrc522.ModeReg);
  Serial.print("ModeReg ");
  Serial.println(tmp, HEX);
  
  tmp = mfrc522.PCD_ReadRegister(mfrc522.VersionReg);
  Serial.print("VersionReg ");
  Serial.println(tmp, HEX);

  
  
  mfrc522.PCD_Init();   // Init MFRC522
}
