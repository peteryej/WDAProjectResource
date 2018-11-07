//#include <assert.h>
#include <FreeRTOS_ARM.h>
#include <IPAddress.h>
#include <PowerDueWiFi.h>

// update these
#define WIFI_SSID "PowerDue"
#define WIFI_PASS "powerdue"


#define SERVER_PORT 9999

#define SERVER_IP "172.29.93.49" 

/*------------------------------------------------------------*/



void tcpClient(void * argument)
{  
  char buf[20];

  struct sockaddr_in serverAddr;  
  socklen_t socklen;
  memset(&serverAddr, 0, sizeof(serverAddr));

  serverAddr.sin_len = sizeof(serverAddr);
  serverAddr.sin_family = AF_INET;
  serverAddr.sin_port = htons(SERVER_PORT); 
  inet_pton(AF_INET, SERVER_IP, &(serverAddr.sin_addr)); //another powerdue running as server


  int s = lwip_socket(AF_INET, SOCK_STREAM, 0);

  while(lwip_connect(s, (struct sockaddr *)&serverAddr, sizeof(serverAddr))){
    lwip_close(s);
    SerialUSB.println("Failed to connect to server. Retrying...");
    s = lwip_socket(AF_INET, SOCK_STREAM, 0);
    delay(1000);
    
  }
  SerialUSB.println("Connected to server");
  

  int n = lwip_read(s, buf, 20);  //blocks when no signal is received
  SerialUSB.print("received: ");
  SerialUSB.println(buf);  

  // close socket after everything is done
  lwip_close(s);
  SerialUSB.println("socket closed");

  //<------ Start your function here -------->
//  turnOffLEDs();  // dummy code
//  delay(200);


  vTaskDelete( NULL );

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
  initLEDs();
  while(!SerialUSB);
  SerialUSB.begin(0);
  turnOnLEDs();
  

  PowerDueWiFi.init(WIFI_SSID, WIFI_PASS);
  PowerDueWiFi.setCallbacks(onReady, onError);
   
  vTaskStartScheduler();
  SerialUSB.println("Insufficient RAM");
  while(1);
}

void loop() {
  // not used in freertos
}
