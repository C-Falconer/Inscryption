# Interactive RFID Card Game
### Based on the game Inscryption by Daniel Mullins
---
#### So, here's the project...

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220924_013645.jpg" alt = "Wire Monster Final Phase" title = "Wire Monster Final Phase" width = "25%"> <a href="http://www.youtube.com/watch?feature=player_embedded&v=RWWOy5Cf8dE
" target="_blank"><img src="http://img.youtube.com/vi/RWWOy5Cf8dE/0.jpg" 
alt="Python Game" width="480" height="337" border="10" /></a>

#### ... but we might want to back up first.

From May-August (except for some future presentation), 2022 I decided to start a project. This project uses 10 MFRC522 RFID tags and an Arduino to simulate the game Inscryption through interacting with a Python program using Pygame. 
The Python program itself uses threading to be able to talk to the Serial port while simultaneously run event checking. The Arduino code helps to handle the incoming Serial information of the RFID readers along with the IR Sensors. The Arduino code is also responsible for handling the shift registers and multiplexer. But before we get to the project journey, let's get some technical details out of the way.

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
* ShiftIn - Arduino
* SPI - Arduino
* MFRC522 - Arduino

#### Other parts include that of a table to act as a placemat (next step) and a custom 3D printed card sleeve. 
---
# Project Journey
**5/20** - The project first started with purchasing the MFRC522 RFID Readers, Bidirectional Logic Level Converters, and Soldering Tools. While waiting, I decided to design a 3D model of the cards. 

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220520_161408.jpg" alt = "Card Top 3D" title = "Card Top 3D" width = "33%"> <img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220520_201146.jpg" alt = "Card Bottom 3D" title = "Card Bottom 3D" width = "33%">

**5/21** - With the items arriving (Logic Level Converters shown later), I needed to decide what to do next. 

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220521_221237.jpg" alt = "RFID Reader" title = "RFID Reader" width = "33%"> <img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220521_221244.jpg" alt = "Soldering Tools" title = "Soldering Tools" width = "33%">

**5/26** - I decided to still focus a little more on the 3D model and make an assembly.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220526_223827(2).jpg" alt = "Card Extended Assembly" title = "Card Extended Assembly" width = "33%"> <img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220526_224056(2).jpg" alt = "Card Compressed Assembly" title = "Card Compressed Assembly" width = "22.73%">

**5/28** - Next up was to print out my first prototype. Sadly though, my floor wasn't level so it wasn't able to print on my 3D printer.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220528_010427.jpg" alt = "3D Print" title = "3D Print" width = "33%"> <img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220528_012137.jpg" alt = "3D Print Fail" title = "3D Print Fail" width = "33%">

**6/2** - Deciding to move on for the time being, I decided to move to the soldering. I had never soldered before, so I set up a station in my backyard, and with plenty of video tutorials watched, went ahead and soldered one of the Bidirectional Logic Level Converters. I decided to solder these before the RFID Readers in order not to mess up the more expensive Readers.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220602_181527.jpg" alt = "First Solder" title = "First Solder" width = "33%">

...Soon after I went to testing the connections I had just soldered. It was a bit difficult at first to figure out how to work the Level Converter, but it would take a bit more time before I became knowledgeable enough to properly use them.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220602_190946.jpg" alt = "LLC Test" title = "LLC Test" width = "33%">

**6/4** - With my first round of equipment arriving, my full set up was looking more and more chaotic by the second (the Lead solder at the top right was handled with considerably more care in the future). 

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220604_230249.jpg" alt = "Equipment Round 1" title = "Equipment Round 1" width = "33%">

**6/8** - I eventually decided to redo the 3D printing on the cards, as I had found better resources for reference online. I had also developed better techniques for modeling accurately.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220608_203107.jpg" alt = "New Card Bottom 3D" title = "New Card Bottom 3D" width = "33%">

**6/16** - Around this time I got a full time job unrelated to the project, so the consistency of work intervals was low. However, it became a mental escape for me as I enjoyed the problem solving and multistep processes. I went and modeled more of the card and went to print it at my University, where I had access to better printers.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220616_181405.jpg" alt = "Card Bottom Back" title = "Card Bottom Back" width = "33%"> <img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220616_230227.jpg" alt = "Better 3D Print" title = "Better 3D Print" width = "33%">

...Sadly during the process, I bent the smaller from plate while removing it from supports. I was significantly more careful in the future with this, however the low thickness caused them to often bend.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220616_225925.jpg" alt = "Bent 3D Piece" title = "Bent 3D Piece" width = "33%">

**6/22** - Soon enough I tried connecting the RFID Reader to my Arduino through 2 Logic Level Converters. There was a lot of difficulty getting the specifics to work, but getting it to work with the Logic Level Converters helped the integrity of the RFID Readers stay quality.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220622_171150.jpg" alt = "LLC with RFID" title = "LLC with RFID" width = "33%">

...My soldering station had also had improvements from me wanting to stay as safe as I could while working with it. In the future, I will probably avoid LED solder all together, as the potential of micro accumulations are worrying.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220622_171303.jpg" alt = "Soldering Setup" title = "Soldering Setup" width = "33%">

**6/23** - Using the setup from before, I was able to connect Python, through the serial port, to the Arduino and respond to the cards read.

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220623_171956.jpg" alt = "Python Read" title = "Python Read" width = "33%">

**6/25** - One of the biggest issues for me, throughout the beginning of the project, was figuring out how to make multiple RFID Readers activate how I wanted to. One way I attempted to do this was by pouring through the functions of the MFRC522 Arduino library. While unsuccessful, it was helpful to have to learn how the inner parts were working. 

<img src="https://github.com/C-Falconer/Inscryption/blob/main/Project_Journey_Files/20220625_231957.jpg" alt = "MFRC522 Library Functions" title = "MFRC522 Library Functions" width = "33%">

...
