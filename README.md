# Audio processing for WDA semester project

## Attention on Your Code Structure
1. Make sure you have the below code in the beginning of your setup on the transmission side.
```
  initLEDs();
  SerialUSB.begin(0);
  while(!SerialUSB);
  turnOnLEDs();
```
`initLEDs()` sets up the LED pins and turn them off. 

`SerialUSB.begin(0);` sets up the SerailUSB. 

`while(!SerialUSB);` waits for openning the serail port which is used to start the energy measurement.

`turnOnLEDs();` gives a visual signal that the program starts. 

2. Your receiving side should be not depend on the server side to turn on. This eliminates the communication back and forth during the competition. Your receiving side should just turn on and then waits for correct LoRa message and then sends it to the tcp server, and it repeats the process. The details can be found in the tcpClient folder instruction.

3. Board 10 has wifi issues, so don't use it on the receiving side, since it may not be able to connect to the wifi network. 


## Setup
Go to your desired folder that you want to put the project directory, then run the below commands in a terminal.

`git clone https://github.com/peteryej/WDAProjectResource.git`


There is a lab station with speaker and microphone connected to PowerDues. We will have more of the station setup next week. 

Check back often for update of code and more resources. You can run `git pull` in your directory to receive the updates.

## Get your energy consumption and time
The processor and LoRa transmission energy is measured during a 25-second interval. The time is measured from when the energy measurement starts to when the tcpServer receives the answer. The instruction on how to test and get the result is in the powerdueStreamData folder.

## Three ways to generate audio
### 1. Use PowerDue to generate audio
Under audioGenerate/audioOutPowerDue folder, it uses WM8731_Audio library to generate a single frequency output. 

### 2. Generate sound on computer with wav file
Under audioGenerate/wavGen folder, it uses its own wavfile library to generate a wav file.

### 3. Use GNU Radio to generate sound on computer
Under audioGenerate/GNURadioGenerate folder, it uses GNU Radio to generate sound on computer. You can test it out on your computer with the virutal machine setup mentioned in the pre-lab section of lab 2. 



## Use FFT to get the frequency information from the microphone
In the audioInput folder, in oder to run the the Arduino file, you need to download the FFT library first. Go to the Arduino library manager, which is under Sketch-\>Include Library, you can search "fft" and install the "arduinoFFT by kosme" library as shown in the piture below.![picture](https://github.com/peteryej/WDASemesterProj/blob/master/arduinoLibrary.jpg) 

