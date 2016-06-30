#!/usr/bin/python
#Written by Amel Bouchemoua @Mugen - 2016

import RPi.GPIO as GPIO
from DataManagement import DataManagement
from PiManager import PiManager
import time, sys


"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
  This exemple is showing the use of the DataManagement and PiManagement classes. 
  It computes the distance between a captor (HC-SR04) and a obstacle,
  sends it to an M-START Servor and switch on/off a led if the 
  distance is lower/higher than 30cm.
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""


""" This class is the implementation of the DataManagement class
    defined the treatments to apply when a message is received
    and when an event occurs on tge gpios, in the case of this exemple.
"""
class DataManagementTest(DataManagement) :

    
    """ Class constructor which provides connection to an M-START Server
            - anActivity(String): the Activity name as it is set in the M-START Server database
            - IP(String): the M-START Server IP address
            - port(int): the M-Start Server port
    """
    def __init__(self, anActivity, IP, port) :
        super(DataManagementTest, self).__init__(anActivity, IP, port)
        self.startingTime = 0


    """ This method is called when a message from the M-START Server is received.
        - aMessage(string) : the message received
        Note : It here prints the message received but other treatments can be 
        defined.
    """
    def messageReceived(self, aMessage) :
        print(aMessage)

        
    """ This method is called when the pulse is send
        time(float) : the time when the pulse was sent
    """
    def setStartingTime(self, time) :
        self.startingTime = time

        
    """ This method is called by PiManager to notify that a gpio has been rising 
         or falling.
         Here, it computes the distance between the receptor and the obstacle
         and sends it to the servor, in order to display it on the connected interfaces.
         - id(int) : the id of the gpio
         - rising(bool) : True if the gpio has been rising and False else
    """    
    def gpioEvent(self, id, rising) :

        # the gpio 20 is here the echo receptor
        if id == 20 and not rising :
            elapsed = time.time() - self.startingTime
            distance = (elapsed * 34000)/2 # in cm
            
            if distance < 30 :
                # Switches on the light
                GPIO.output(6, GPIO.HIGH)
            else :
                # Switches off the light
                GPIO.output(6, GPIO.LOW)

            # Sends the distance value to the M-START Servor which will send it to the interfaces
            # to display this value

            self.sendMessageTo("/testManagement/object/indicator/1/intprop/distance", distance)
        
try :

    # Initialisations
    dm = DataManagementTest("PiManagerTest","192.168.1.32", 59900)
    pm = PiManager(dm, mode = GPIO.BCM)
    led = 6 
    echo = 20
    trigger = 21
    pm.setOutput([led, trigger], initial = False)
    pm.setInput(echo, pullUpDown = GPIO.PUD_DOWN)

    # Setting detection for the echo gpio
    pm.setEventDetection(echo)

    # Loop to send 10 us pulse to trigger every 0.05s
    while True :
        pm.setValues([trigger], [True])
        time.sleep(0.00001)
        pm.setValues([trigger], [False])
        dm.setStartingTime(time.time()) # Notify the data manager of time when the pulse was send
        time.sleep(0.05)


except (KeyboardInterrupt) :
    dm.close()
    pm.cleanup() 
    sys.exit
