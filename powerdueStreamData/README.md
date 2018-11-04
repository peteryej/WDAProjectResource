
## run test

`python powerdueControl.py` 


Then follow the prompt to enter the port number of the instrument port. The instrument port can be found using the Arduino IDE to identify which is the instrument and which is the target.

Then enter the csv file name if you don't want to default name, and it will be saved in the testOutput on Desktop.

You can choose to start one powerdue or two powerdues. For starting only one powerdue, just leave the port empty for the second port prompt. Then it will start collection the energy for 25 seconds. 

At the end of the 25 seconds, the energy consumption is printed out. One note on the processor energy consumption calculation is that it ignores voltage level values below 100 mV to account for the difference in boards shutdown voltage level, so it only calculates energy when the processor is awake.

One example output is shown here 

![example](https://github.com/peteryej/WDAProjectResource/blob/labtest/powerdueStreamData/exampleOutput.png).

If youa are also testing the transmission, make sure you also run the tcpServer so you can get the end time of your transmission.

## visualize energy consumption

You can visulize your csv energy file using the "visualize energy consumption.ipynb" file. 
To run it, open a new terminal window and navigate to this folder. Run `jupyter notebook` and a browser window will open. Change the `fileName` variable to the file that you want to test and make sure the file is in the testOutput folder on the Desktop. 

You can change the input argument of `plotTimeRange(0,25)` to produce plots at differnt time range in seconds. 

Under `Knernel-> Restart & Run All` to execute the whole notebook, or you can execute individual cell by click on the cell and click the `run` button on the top.


## get the total time 

The start time is printed out when you run the `powerdueControl.py` file. The end time is obtained on the tcpServer output when it receives the answer, it prints out the end time. To make it easier for you to find the elapsed time. There is the `getTimeDiff.ipynb` file. You just change the timeStr1 and timeStr1 variable and run the script under Kernel->Restart & Run  All. You will the time in seconds.
