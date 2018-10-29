#include <assert.h>
#include <FreeRTOS_ARM.h>
#include <IPAddress.h>
#include <PowerDueWiFi.h>

// update these
//#define WIFI_SSID "PowerDue"
//#define WIFI_PASS "powerdue"

#define WIFI_SSID "lopy-wlan-8b72"
#define WIFI_PASS "www.pycom.io"

#define SERVER_PORT 9999
//#define SERVER_IP "10.230.12.76"
#define SERVER_IP "192.168.4.3"

/*------------------------------------------------------------*/

#define DATALEN 100
char buf[DATALEN];

char answer[DATALEN] = "team: teamName; answer: 110, 220";  //change to be your answers to send

void prepareBuffer(char answer[]){
  strcpy(buf, answer);
}

void tcpClient(void * argument)
{  
  struct sockaddr_in serverAddr;  
  socklen_t socklen;
  memset(&serverAddr, 0, sizeof(serverAddr));

  serverAddr.sin_len = sizeof(serverAddr);
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(SERVER_PORT); 
  inet_pton(AF_INET, SERVER_IP, &(serverAddr.sin_addr)); //another powerdue running as server


  int s = lwip_socket(AF_INET, SOCK_STREAM, 0);

  while(lwip_connect(s, (struct sockaddr *)&serverAddr, sizeof(serverAddr))){
    SerialUSB.println("Failed to connect to server. Retrying...");
    //assert(false);
    delay(1000);
  }
  SerialUSB.println("Connected to server");
  prepareBuffer(answer);

  // send data  
  if (lwip_write(s, buf, DATALEN)){
    turnOnLEDs();
    delay(500);
    SerialUSB.println("sent");
    turnOffLEDs();
  }else{
    SerialUSB.println("failed to send");
  }
  
  // close socket after everything is done
  lwip_close(s);
  SerialUSB.println("socket closed");
  vTaskSuspend( NULL );
}

/*------------------------------------------------------------*/

void initLEDs(){
  // turn off LEDs
  pinMode(6,OUTPUT);
  pinMode(7,OUTPUT);
  pinMode(8,OUTPUT);
  turnOffLEDs();
}

void turnOffLEDs(){
  digitalWrite(6,LOW);
  digitalWrite(7,LOW);
  digitalWrite(8,LOW);
}

void turnOnLEDs(){
  digitalWrite(6,HIGH);
  digitalWrite(7,HIGH);
  digitalWrite(8,HIGH);
}

void onError(int errorCode){
  SerialUSB.print("Error received: ");
  SerialUSB.println(errorCode);
}

void onReady(){
  SerialUSB.println("Device ready");  
  SerialUSB.print("Device IP: ");
  SerialUSB.println(IPAddress(PowerDueWiFi.getDeviceIP()));  
  
  xTaskCreate(tcpClient, "tcpClient", configMINIMAL_STACK_SIZE, NULL, 1, NULL);
}

void setup() {
  SerialUSB.begin(0);
  while(!SerialUSB);

  initLEDs();

  PowerDueWiFi.init(WIFI_SSID, WIFI_PASS);
  PowerDueWiFi.setCallbacks(onReady, onError);
   
  vTaskStartScheduler();
  SerialUSB.println("Insufficient RAM");
  while(1);
}

void loop() {
  // not used in freertos
}
