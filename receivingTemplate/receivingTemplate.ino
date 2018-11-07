#include <SPI.h>
#include <LoRa.h>
#include <assert.h>
#include <FreeRTOS_ARM.h>
#include <IPAddress.h>
#include <PowerDueWiFi.h>


#define WIFI_SSID "PowerDue"
#define WIFI_PASS "powerdue"


#define SERVER_PORT 9999
#define SERVER_IP "172.29.93.49" 

/*------------------------------------------------------------*/

// parameters
#define FREQUENCY         915E6   // 915MHz or 920MHz
#define BANDWIDTH         125000  // 125kHz bandwidth

// vary these parameters
#define TX_POWER          20   // valid values are from 6 to 20
#define SPREADING_FACTOR  7    // valid values are 7, 9 

#define DATALEN 30

/*------------------------------------------------------------*/
char buf[DATALEN]; //"teamName: 110, 220"



//<------ write your function here -------->
void getAnswer(){
  // TODO: put your answer in the buf 

}



void tcpClient(void * argument)
{  
  // the receiver runs continuously and doesn't need to restart 
  // after each round
  while(true){   

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
    
    //<------ Call your function here -------->
    getAnswer();  // function call

    // send data  
    if (lwip_write(s, buf, DATALEN)){
      SerialUSB.println("sent");
    }else{
      SerialUSB.println("failed to send");
    }  

    // close socket after everything is done
    lwip_close(s);
    SerialUSB.println("socket closed");

  }

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
  //while(!SerialUSB);
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
