/*
This example program makes use of the simple
sound library to generate a sine wave and write the
output to sound.wav.
For complete documentation on the library, see:
http://www.nd.edu/~dthain/courses/cse20211/fall2013/wavfile
Go ahead and modify this program for your own purposes.
*/


#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <errno.h>

#include "wavfile.h"

const int VOLUME = 32000;  //max is 32767 since it's short int array

void generateFrequency(short data[], int len, int start, double freq){
	int i;
	double t;
	printf("start: %d\n", start);
	for(i=start;i<len+start;i++) {
		t = (double) (i-start) / WAVFILE_SAMPLES_PER_SECOND;
		data[i] = VOLUME*sin(freq*t*2*M_PI);
	}
}

int main()
{

	int num_sample1 = (WAVFILE_SAMPLES_PER_SECOND);
	int num_sample2 = (WAVFILE_SAMPLES_PER_SECOND);
	int num_sample3 = (WAVFILE_SAMPLES_PER_SECOND);

 	int num_samples = num_sample1 + num_sample2; //+ num_sample3;
 	printf("total: %d\n", num_samples);

	short waveform[num_samples];
	// https://pages.mtu.edu/~suits/notefreqs.html has the pitch frequencies
	double frequency1 = 261.63; //pitch C4
	double frequency2 = 523.25; //pitch C3



	generateFrequency(waveform, num_sample1, 0, frequency1);
	generateFrequency(waveform, num_sample2, num_sample1, frequency2);


	FILE * f = wavfile_open("sound.wav");
	if(!f) {
		printf("couldn't open sound.wav for writing: %s",strerror(errno));
		return 1;
	}

	wavfile_write(f,waveform,num_samples);
	wavfile_close(f);

	return 0;
}