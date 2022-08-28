# Interactive RFID Card Game
### Based on the game Inscryption by Daniel Mullins
This project uses 10 MFRC522 RFID tags and an Arduino to simulate the game Inscryption through interacting with a Python program using Pygame. 
The Python program itself uses threading to be able to talk to the Serial port while simultaneously run event checking. The Arduino code helps to handle the incoming Serial information of the RFID readers along with the IR Sensors. The Arduino code is also responsible for handling the shift registers and multiplexer. 

## Parts Used:
* 10  MFRC522 RFID Readers
* 20  RFID Tags
* 10  IR Sensors
* 2   Daisy Chained CD74HC165 Shift Registers
* 1   CD74HCT4051e 8:1 Multiplexer
* 4   4 Channel Bidirectional Logic Level Converters
* 10  10k Resistors
* 3   2k Resistors
* 1   100uF 50V Electrolytic Capacitor
* 1   Arduino Uno R3 (Connected to a device running Python)
* 1   Breadboard
* Plenty of Wires

## Libraries Used:
* pygame
* pyautogui (size)
* os (listdir)
* sys (exit)
* serial (Serial)
* threading (Thread)
* PIL (Image)
* random (uniform)
* math (floor)

Other parts include that of a table to act as a placemat (next step) and a custom 3D printed card sleeve. 
