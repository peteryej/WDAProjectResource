
Your receiving side code should not depend on the transmission side to turn on. By commenting out the last line in `tcpClient(void* argument)` function, `vTaskDelete( NULL );`, the function will run continuously instead of once. You need to make your program check whether you received the correct answer and then send the data. `prepareBuffer(answer);` is where you want to put the check logic, so that everytime when you receives a correct LoRa message and then send it to tcp server. In this way, you can just leave the receiving side on. 


To test in the lab, you can connect to the powerdue wifi as in the default. 

Change the ip address to where you are running the tcpServer. On Mac/Linux, you can find the ip address using `ifconfig` or on Windows `ipconfig`. See one example ![below](https://github.com/peteryej/WDAProjectResource/blob/master/tcpClient/ipaddress.jpg).
