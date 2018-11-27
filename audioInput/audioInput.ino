#include <Wire.h>
#include "WM8731_AudioMod.h"
#include "arduinoFFT.h"

arduinoFFT FFT = arduinoFFT(); /* Create FFT object */
/*
  These values can be changed in order to evaluate the functions
*/
const uint16_t SAMPLES = OUT_BUFF; //This value MUST NOT be modified, ALWAYS be a power of 2
const double SAMP_FREC = 88200.0; //This value MUST NOT be modified

/*
  These are the input and output vectors
  Input vectors receive computed results from FFT
*/
double vReal[SAMPLES]; //= out_buf;
double vImag[SAMPLES]; // = {0.0};

#define SCL_INDEX 0x00
#define SCL_TIME 0x01
#define SCL_FREQUENCY 0x02
#define SCL_PLOT 0x03

unsigned long prevTime, elapsedTime;


void setup(void) {
  pinMode(6, OUTPUT);
  pinMode(7, OUTPUT);
  pinMode(8, OUTPUT);
  digitalWrite(6, LOW);
  digitalWrite(7, LOW);
  digitalWrite(8, LOW);

  SerialUSB.begin(115200);
  while (!SerialUSB);
  SerialUSB.println("started");
  //while(!SerialUSB.available());
  digitalWrite(6, HIGH);
  digitalWrite(7, HIGH);
  digitalWrite(8, HIGH);



  Codec.begin();

  //  SerialUSB.print("out buffer at: ");
  //  SerialUSB.println((long)out_buf);

  SerialUSB.println("waiting");
  prevTime = millis();
  while (!out_buf_ready);
  elapsedTime = millis() - prevTime;
  SerialUSB.print("buffer delay time: ");
  SerialUSB.println(elapsedTime);
  SerialUSB.println("buf ready");

  //print out the audio signal values in the buffer
  //  for(uint16_t i=0; i<OUT_BUFF; ++i){
  //    SerialUSB.println(out_buf[i]);
  //  }

}

void loop()
{

  prevTime = millis();
  for (uint16_t i = 0; i < SAMPLES; i++)
  {
    vReal[i] = (double)out_buf[i];
    vImag[i] = 0.0; //Imaginary part must be zeroed in case of looping to avoid wrong calculations and overflows
  }

  /* Print the results of the simulated sampling according to time */
  //SerialUSB.println("Data:");
  //PrintVector(vReal, SAMPLES, SCL_TIME);
  FFT.Windowing(vReal, SAMPLES, FFT_WIN_TYP_BLACKMAN, FFT_FORWARD);  /* Weigh data */
  //SerialUSB.println("Weighed data:");
  //PrintVector(vReal, SAMPLES, SCL_TIME);
  FFT.Compute(vReal, vImag, SAMPLES, FFT_FORWARD); /* Compute FFT */
  //SerialUSB.println("Computed Real values:");
  //PrintVector(vReal, SAMPLES, SCL_INDEX);
  //SerialUSB.println("Computed Imaginary values:");
  //PrintVector(vImag, SAMPLES, SCL_INDEX);
  FFT.ComplexToMagnitude(vReal, vImag, SAMPLES); /* Compute magnitudes */

  double maxFreq = FFT.MajorPeak(vReal, SAMPLES, SAMP_FREC);

  elapsedTime = millis() - prevTime;

  //SerialUSB.println("Computed magnitudes:");
  //PrintVector(vReal, (SAMPLES >> 1), SCL_FREQUENCY);

  SerialUSB.print("max frequency: ");
  SerialUSB.println(maxFreq, 6);

  SerialUSB.print("elapsedTime: ");
  SerialUSB.println(elapsedTime);

  //while(1); /* Run Once */
  //delay(2000); /* Repeat after delay */

}


void PrintVector(double *vData, uint16_t bufferSize, uint8_t scaleType)
{
  for (uint16_t i = 0; i < bufferSize; i++)
  {
    double abscissa;
    /* Print abscissa value */
    switch (scaleType)
    {
      case SCL_INDEX:
        abscissa = (i * 1.0);
        break;
      case SCL_TIME:
        abscissa = ((i * 1.0) / SAMP_FREC);
        break;
      case SCL_FREQUENCY:
        abscissa = ((i * 1.0 * SAMP_FREC) / SAMPLES);
        break;
    }
    SerialUSB.print(abscissa, 6);
    if (scaleType == SCL_FREQUENCY)
      //SerialUSB.print("Hz");
      SerialUSB.print(",");
    SerialUSB.print(" ");
    SerialUSB.println(vData[i], 4);
  }
  SerialUSB.println();
}
