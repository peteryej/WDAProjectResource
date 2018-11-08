# Audio processing for WDA semester project

## Attention on Your Code Structure
1. Make sure you have the below code in the beginning of your setup on the transmission side.
```
  initLEDs();
  SerialUSB.begin(115200);
  while(!SerialUSB);
  turnOnLEDs();
  SerialUSB.println("started");
```
`initLEDs()` sets up the LED pins and turns them off. 

`while(!SerialUSB);` waits for openning the serail port which is used to start the energy measurement.

`SerialUSB.begin(115200);` sets up the SerialUSB. 

`turnOnLEDs();` gives a visual signal that the program starts. 

2. On the receiving side make sure you follow the code in the receivingTemplate folder. Your receiving side should be not depend on the server side to turn on. This eliminates the communication back and forth during the competition. Your receiving side should just turn on and then waits for correct LoRa message and then sends it to the tcp server, and it repeats the process. 

3. Board 10 has wifi issues, so don't use it on the receiving side, since it may not be able to connect to the wifi network. Board 11 LoRa has issues that `LoRa.begin(FREQUENCY)` doesn't work consistently, it may be due to the use of SPI chip.

## Test on the lab laptop
There are two laptops setup in the lab. The one in the inner corner is setup to upload code to the transmission side, and the outer laptop is setup to upload code to the receiving side. We keep it the same as how the competition will use. 

It's necessary to test your code on the lab laptop because it will be the setup of the competition. There are a few things that can affect depending on the test machine. 
- The audio is run by GNURadio and through the headphone wire, so your code need to make sure that you can get the correct frequencies with this setup. 
- The tcp server is running on the computer, so make sure your tcp client can connect to the server. 

1. On the lab laptop, make sure you are loggined as peter, which is the default if you didn't log out. Then upload you code to the powerdue board, then connect to the lab laptop.
2. Go to WDAProjectResource folder `cd ~/projects/WDAProjectResource` 
3. Go to GNURadioGenerate and use gnuradio to generate the audio, keep the volumn as the default and change the frequency values only.
`cd audioGenerate/GNURadioGenerate`

4. run
```
cd tcpServer
python2env
python newtcpServer.py
```
4. Go to singleTansmisster or doubleTransmitter folder depending on whether you are testing on transmitter or two at the same time. 

5. Run 
```
python2env
# if run single transmitter
python powerdueControl.py team1 try1
# if run two transmitter2. team1 will corresponds to the lower port number board.
python powerdueControl.py team1 team2 try1
```

6. Go to competition_result to check your result. `cd ~/Desktop/competition_result` 
You should find the csv files corresponds to what you have entered to start the transmitter. You can also open the competitionLogSingle.txt or competitionLogDoubble.txt to see the recorded time and energy results.


There are a few ways to transfer your code to the laptop, if you want to edit on the lab laptop.
1. You can upload the code to google drive then download it on the laptop. 
2. Download the [id_rsa_lablaptop](https://canvas.cmu.edu/courses/5895/files/3082952?module_item_id=902229) file from canvas which can be found under the semester project section to your computer, then `cd ` into to where the file is downloaded and run the command in a terminal `ssh-add id_rsa_lablaptop`. To transfer file to the lab laptop desktop from your computer, run `scp path/to/file peter@172.29.93.49:~/Desktop/` change the `path/to/file` to the actual file location on your computer.
3. Use a USB flash drive. 



## Setup
Go to your desired folder that you want to put the project directory, then run the below commands in a terminal.

`git clone https://github.com/peteryej/WDAProjectResource.git`

`git checkout twolabsetups`


## Get your energy consumption and time
The processor and LoRa transmission energy is measured during a 25-second interval. The time is measured from when the energy measurement starts to when the tcpServer receives the answer. The instruction on how to test and get the result is in the powerdueStreamData folder.




