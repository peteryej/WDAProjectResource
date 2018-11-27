#include <PowerDue.h>
#include <LoRa.h>

// fixed parameters
#define FREQUENCY         920E6   // 915MHz
#define BANDWIDTH         125000  // 125kHz bandwidth
#define SLEEPTIME         4000    // 4 seconds

// vary these parameters
#define TX_POWER          20   // valid values are from 6 to 20
#define SPREADING_FACTOR  7    // valid values are 7, 8, 9 or 10
#define ANSWER            "testTeam 6000 7500"

int counter = 0;

void setup() {
  pd_rgb_led_init();
  while (!SerialUSB);
  SerialUSB.begin(0);
  pd_rgb_led(PD_WHITE);
  
  SerialUSB.println("LoRa Sender");

  LoRa.setPins(22, 59, 51);
  while (!LoRa.begin(FREQUENCY)) {
    SerialUSB.println("Starting LoRa failed!");
    delay(200);
  }

  LoRa.setTxPower(TX_POWER);
  LoRa.setSpreadingFactor(SPREADING_FACTOR);
  LoRa.setSignalBandwidth(BANDWIDTH);
  
}

void loop() {
  SerialUSB.print("Sending packet: ");
  SerialUSB.print(ANSWER);
  SerialUSB.print("  ");
  SerialUSB.println(counter);

  // send packet
  LoRa.beginPacket();
  LoRa.print(ANSWER);
  //LoRa.print(counter);
  LoRa.endPacket();

  counter++;

  if(counter > 20) {
    delay(500);
    counter = 0;
  }

  
}
