# Audio processing for WDA semester project

## generate wav sound file
In the wavGen folder, it has two examples of generating wav files at user specified frequency. You can play the sound.wav and sound1.wav to hear the sound. You can modify the example.c code to generate other frequency sounds and combinations as you want. 

To generate new sound file on Linux/Mac machines (given you have gcc installed on Mac)

Go to your desired folder that you want to put the project directory, then run the below commands in a terminal.

`git clone git@github.com:peteryej/WDASemesterProj.git`

Modify the example.c file if you want to generate other frequency sounds.
```shell
gcc example.c wavfile.c -o example -lm
./example 
```
You should find the wav file generated with specified name in the example.c.

