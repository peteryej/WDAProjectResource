# Audio Sound Generation

## Use PowerDue to play audio
In the audioOutPowerDue.ino code, you can modify the frequency of the audo by change the curFreq variable, and you can change the volume by the input value of the Codec.setOutputVolumen() function.

## Generate wav sound file
In the wavGen folder, it has two examples of generating wav files at user specified frequency. You can play the sound.wav and sound1.wav to hear the sound. You can modify the example.c code to generate other frequency sounds and combinations as you want. 

To generate new sound wav file, you can modify the example.c file if you want to generate other frequency sounds. Run the below commands on a terminal or in a IDE that can compile c code.
```shell
gcc example.c wavfile.c -o example -lm
./example 
```
You should find the new wav file generated with specified name as the input argument of `FILE * f = wavfile_open("sound.wav");` in the example.c file.

## Use GNU Radio to generate sound
This is the most flexible way to generate sound because it can easily combine different frequencies and noise. You can also adjust the frequency and noise level dynamically using a GUI interface. You are also able to see the FFT and waterfall diagram of the generated sound.

