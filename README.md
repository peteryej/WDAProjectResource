# Audio processing for WDA semester project

## Three ways to generate audio
### Use PowerDue to generate audio
Under audioGenerate/audioOutPowerDue folder, it uses WM8731_Audio library to generate a single frequency output. 

### Generate sound on computer with wav file
Under audioGenerate/wavGen folder, it uses its own wavfile library to generate a wav file.

### Use GNU Radio to generate sound on computer
Under audioGenerate/GNURadioGenerate folder, it uses GNU Radio to generate sound on computer. You can test it out on your computer with the virutal machine setup mentioned in the pre-lab section of lab 2. 



## Use FFT to get the frequency information from the microphone
In the audioInput folder, in oder to run the the Arduino file, you need to download the FFT library first. Go to the Arduino library manager, which is under Sketch-\>Include Library, you can search "fft" and install the "arduinoFFT by kosme" library as shown in the piture below.![picture](https://github.com/peteryej/WDASemesterProj/blob/master/arduinoLibrary.jpg) 

