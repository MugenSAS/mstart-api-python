#!/usr/bin/python
#Written by Amel Bouchemoua @Mugen - 2016

import RPi.GPIO as GPIO


""" This class helps to detect the events related to gpios and 
    to notify the dataManagement class
"""
class PiManager() :

    
    """ Class constructor 
        - dataManagement(DataManagement): the class which provides connection to 
          an M-START Server and deals with the different events
        - mode: the pin numbering mode (GPIO.BCM or GPIO.BOARD)
    """
    def __init__(self, dataManagement, mode = GPIO.BCM) :
        GPIO.setmode(mode)
        self.dataManagement = dataManagement
        
        
    """ Sets up gpios as an input
        - gpios(int/int list): the gpios to set as an input
        - pullUpDown : the default value of the input (GPIO.PUD_DOW for
        the value "low", GPIO.PUD_UP for "high"
    """
    def setInput(self, gpios, pullUpDown = GPIO.PUD_DOWN) :
        if isinstance(gpios, int) :
            gpios = [gpios]

            for pin in gpios :
                GPIO.setup(pin, GPIO.IN, pull_up_down = pullUpDown)
                
                
    """ Sets up gpios as an output
        - gpios(int/int list): the gpios to set as an output
        - initial(bool) : the initial value of the gpios (False 
        for "low" and True for "high")
    """
    def setOutput(self, gpios, initial = False) :
        if isinstance(gpios, int) :
            gpios = [gpios]

        for pin in gpios :
            if initial == None :
                GPIO.setup(pin, GPIO.OUT)
            elif initial :
                GPIO.setup(pin, GPIO.OUT, initial = GPIO.HIGH)
            else :
                GPIO.setup(pin, GPIO.OUT, initial = GPIO.LOW)
                    

    """ Sets the values of gpios
        - gpios(int list) : the gpios ids
        - values(list) : the values of the gpios (True/1/GPIO.HIGH for
        "high" and False/0/GPIO.LOW for "low")
    """ 
    def setValues(self, gpios, values) :

        for (pin, value) in zip(gpios, values) :
            GPIO.output(pin, value)

            

    """ Gets the list of bool values of gpios
        - gpios(int list) : the gpios ids
    """ 
    def getValues(self, gpios) :

        values = []
        for pin in gpios :
            values.append(input(pin) == GPIO.HIGH)
        return values

    

    """ Set event detection and callbacks to notify the data management class
        - gpios(int list) : the gpios ids
    """
    def setEventDetection(self, gpios) :
        if isinstance(gpios, int) :
            gpios = [gpios]
            
        def mycallback(channel) :
                self.dataManagement.gpioEvent(channel, GPIO.input(channel) == GPIO.HIGH)
                
        for pin in gpios :
            GPIO.add_event_detect(pin, GPIO.BOTH, callback = mycallback)

            

    """ Cleans up the a part or all the ressources
        - gpios(int/int list/tuple) the gpios to cleanup, everything will be cleanup 
         if its value is None
    """
    def cleanup(self, gpios = None) :
        if gpios == None :
            GPIO.cleanup()
        else :
            GPIO.cleanup(gpios)
        

        
        
            
            

    
