# Audio processing for WDA semester project

## Attention on Your Code Structure
1. Make sure you have the below code in the beginning of your setup on the transmission side.
```
  initLEDs();
  while(!SerialUSB);
  SerialUSB.begin(9600);
  turnOnLEDs();
```
`initLEDs()` sets up the LED pins and turns them off. 

`while(!SerialUSB);` waits for openning the serail port which is used to start the energy measurement.

`SerialUSB.begin(9600);` sets up the SerialUSB. 

`turnOnLEDs();` gives a visual signal that the program starts. 

2. On the receiving side make sure you follow the code in the receivingTemplate folder. Your receiving side should be not depend on the server side to turn on. This eliminates the communication back and forth during the competition. Your receiving side should just turn on and then waits for correct LoRa message and then sends it to the tcp server, and it repeats the process. 

3. Board 10 has wifi issues, so don't use it on the receiving side, since it may not be able to connect to the wifi network. Board 11 LoRa has issues that `LoRa.begin(FREQUENCY)` doesn't work consistently, it may be due to the use of SPI chip.

## Test on the lab laptop
There are two laptops setup in the lab. The one in the inner corner is setup to upload code to the transmission side, and the outer laptop is setup to upload code to the receiving side. We keep it the same as how the competition will use. 

To test your code on the laptop, there are a few ways to transfer your code to the laptop. 
1. You can upload the code to google drive then download it on the laptop. 
2. Download the [id_rsa_lablaptop](https://canvas.cmu.edu/courses/5895/files/3082952?module_item_id=902229) file from canvas which can be found under the semester project section to your computer, then `cd ` into to where the file is downloaded and run the command in a terminal `ssh-add id_rsa_lablaptop`. To transfer file to the lab laptop desktop from your computer, run `scp path/to/file peter@172.29.93.49:~/Desktop/` change the `path/to/file` to the actual file location on your computer.
3. Use a USB flash drive. 



## Setup
Go to your desired folder that you want to put the project directory, then run the below commands in a terminal.

`git clone https://github.com/peteryej/WDAProjectResource.git`

`git checkout twolabsetups`


## Get your energy consumption and time
The processor and LoRa transmission energy is measured during a 25-second interval. The time is measured from when the energy measurement starts to when the tcpServer receives the answer. The instruction on how to test and get the result is in the powerdueStreamData folder.




