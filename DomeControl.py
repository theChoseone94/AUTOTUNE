"""

This code is made by the MINERVA project, located at: https://github.com/MinervaCollaboration/minerva-control
I have tweaked the code to suit our dome and for testing. 
- Hasse Hansen, hasse302@hotmail.com

This python code is for controlling the telescope dome. 
It opens a serial port to the dome-control and sends commands to move the shutter of the dome.

"""

import telnetlib
import socket
import sys
import os
import datetime
import logging
import json
import threading 
import time
from configobj import ConfigObj
sys.dont_write_bytecode = True
from filelock import FileLock
import serial
import time

class astrohaven:

	#initialize class by specify configuration file and software base directory
    def __init__(self,config,base):
        """
        A function that initialiazes the configuration of the dome.

        """

        self.base_directory = base
        self.config_file = config
        self.load_config()
        self.create_objects()   
        self.status = {'Shutter1':'UNKNOWN','Shutter2':'UNKNOWN'}
			
        self.initialized = False
        self.lock = threading.Lock()
        self.status_lock = threading.RLock()
        
        self.rainChangeDate = datetime.datetime.utcnow()
        self.lastRain = 0.0

        #This is a status dictionary for the serial response from the dome. 
        self.StatusDic={"0":{'Shutter1':'CLOSED','Shutter2':'CLOSED'},
                        "1":{'Shutter1': 'CLOSED','Shutter2': 'NOT CLOSED'},
                        "2":{'Shutter1': 'NOT CLOSED','Shutter2':'CLOSED'},
                        "3":{'Shutter1': 'NOT CLOSED','Shutter2': 'NOT CLOSED'},
                        "a":{'Shutter1':'opening','Shutter2':self.status['Shutter2']},
                        "A":{'Shutter1':'closing','Shutter2':self.status['Shutter2']},
                        "b":{'Shutter1':self.status['Shutter1'],'Shutter2':'opening'},
                        "B":{'Shutter1':self.status['Shutter1'],'Shutter2':'closing'},
                        "x":{'Shutter1':'open','Shutter2':self.status['Shutter2']},
                        "X":{'Shutter1':'closed','Shutter2':self.status['Shutter2']},
                        "y":{'Shutter1':self.status['Shutter1'],'Shutter2':'open'},
                        "Y":{'Shutter1':self.status['Shutter1'],'Shutter2':'closed'}
            }
        
    def load_config(self):
		#create configuration file object
        try:
            config = ConfigObj(self.base_directory+self.config_file)
            self.port = config['Setup']['PORT']
            self.baudrate = config['Setup']['BAUDRATE']
            self.logger_name = config['Setup']['LOGNAME']
            self.num = config['Setup']['NUM']
            self.id = config['Setup']['ID']
        except:
            print('ERROR accessing configuration file: ' + self.config_file)
            sys.exit()
            today = datetime.datetime.utcnow()
            if datetime.datetime.now().hour >= 10 and datetime.datetime.now().hour <= 16:
                        today = today + datetime.timedelta(days=1)
                        self.night = 'n' + today.strftime('%Y%m%d')

    def create_objects(self):
        self.ser = serial.Serial(self.port,baudrate=self.baudrate)            
        self.ser.close()
    
    def nudgeshutter(self, direction, shutter, desiredcounts=1):      
        """
        A function that moves the shutter/side of the dome. 
        Direction can be either 'open' or 'close' where 'open'.
            'open' refers to moving the shutter further down and thereby opening the dome some more.
            'close' refers to moving the shutter further up and thereby closing the dome some more
        Shutter can be either 1 or 2 for each side of the dome.
        Desiredcounts is the number of times the serial command is sent to the dome.
            It is per default set to 1, but can be set manually. 1 step is a small step on the order of a few centimeters of movement for the dome shutter/side.
            A desiredcounts between 20 and 25 seems to open/close the dome shutter/side fully.
        
        Example of command:
        nudgeshutter('open',1,5)
            This command would slightly open side #1 of the dome.
        
        Returns:
            Nothing
        """   
        if direction == 'open':
            if shutter == 1: cmd = 'a'
            elif shutter == 2: cmd = 'b'
            else: print("shutter" + str(shutter) + "not allowed")
        elif direction == 'close':
            if shutter == 1: cmd = 'A'
            elif shutter == 2: cmd = 'B'
            else: print("shutter" + str(shutter) + "not allowed")
        else: 
            print("direction" +str(direction) + "not defined")
        self.ser.open()
        currentcount = 0
        while (currentcount < desiredcounts):
            self.ser.write(str.encode(cmd))
            currentcount = currentcount + 1 
            time.sleep(0.6)
            response = ''

            while self.ser.inWaiting() > 0: 
                response = self.ser.read(1).decode()
            if direction == 'open':
                if shutter == 1 and response == 'x': break
                elif shutter == 2 and response == 'y': break
            if direction == 'close':
                if shutter == 1 and response == 'X': break
                elif shutter == 2 and response == 'Y': break
        
        
        if response in self.StatusDic:
            print(response) #For testing
            print(self.status) #For testing
            self.status = self.StatusDic[response]
            print(self.status) #For testing 
        else:
            print('Error - response from dome is not in dictionary')
            print(response)
        
            
        self.ser.close()
         
    def open_shutter(self,shutter,desiredcounts = 20):
        """
        A function that opens a shutter based on user input.
        shutter can be either: 1 or 2

        Example of command:
        open_shutter(1)
            This command would open shutter #1.
        
        Returns:
            Nothing
        """
        self.nudgeshutter('open',shutter,desiredcounts=desiredcounts)
             
    def close_shutter(self,shutter,desiredcounts = 25):
        """
        A function that closes a shutter, set by the user.
        shutter can be either: 1 or 2

        Example of command:
        close_shutter(2)
            This command would close shutter #2.
        
        Returns: 
            Nothing
        """
        self.nudgeshutter('close',shutter,desiredcounts=desiredcounts)
                      
    def open_both(self):
        """
        A function that opens both shutters of the dome. 
        It relies on the function "open_shutter(x)" to open shutter/side #x of the dome. 

        Example of command:
        open_both()

        Returns:
            Nothing
        """
        self.open_shutter(1)
        self.open_shutter(2)
                             
    def close_both(self):
        """
        A function that closes both shutters of the dome.
        This function relies on the function "close_shutter(x)" where x refers to which side of the dome to open. 
        
        This function is set to first close shutter 2 and then shutter 1. This seems best given the way the two shutters overlap when they close.

        Example of command:
        close_both()
        
        Returns:
            Nothing.
        """
        self.close_shutter(2) 
        self.close_shutter(1)
             
    def get_status(self):
        """
        A function that fetches the current status on whether the dome shutter are closed/open etc. 

        Example of command
        get_status()

        Returns:
            self.status which contains the status for both shutters.

        """

        self.ser.open()
        while self.ser.inWaiting() == 0: 
            time.sleep(0.6)
        while self.ser.inWaiting() > 0: 
            response = self.ser.read(1).decode()
        self.ser.close()



        if response in self.StatusDic:
            print(response) #For testing
            print(self.status) #For testing
            self.status = self.StatusDic[response]
            print(self.status) #For testing
        else:
            print('Error - response from dome is not in dictionary')
            print(response)
        
        return self.status            
            
    def isOpen(self):
        filename = self.base_directory + '/minerva_library/astrohaven' + str(self.num) + '.stat'
		#with FileLock(filename):
        if True:	
            with open(filename,'r') as fh: line = fh.readline().split()
            try:
                lastUpdate = datetime.datetime.strptime(' '.join(line[0:2]),'%Y-%m-%d %H:%M:%S.%f')
                if (datetime.datetime.utcnow() - lastUpdate).total_seconds() > 300:
                    self.logger.error("Dome status hasn't updated in 5 minutes; assuming closed")
                    return False
                return line[2] == 'True'
            except:
                #self.logger.exception("Failed to read aqawan status file")
                return False
        return False

    def heartbeat(self):
            pass
							
if __name__ == '__main__':
        #We need to change this around once we move this code to the server.
        if socket.gethostname() == 'thechosenone': base_directory = '/home/hasse/Dropbox/Speciale/'
        else: base_directory = '/home/hasse/Dropbox/Speciale/'
        dome = astrohaven('DomeConfig.ini',base_directory)
	# while True:
		# print dome.logger_name + ' test program'
		# print ' a. open shutter 1'
		# print ' b. close shutter 1'
		# print ' c. open shutter 2'
		# print ' d. close shutter 2'
		# print ' e. open both shutters'
		# print ' f. close both shutters'
		# print '----------------------------'
		# choice = raw_input('choice:')

		# if choice == 'a':
			# dome.open_shutter(1)
		# elif choice == 'b':
			# dome.close_shutter(1)
		# elif choice == 'c':
			# dome.open_shutter(2)
		# elif choice == 'd':
			# dome.close_shutter(2)
		# elif choice == 'e':
			# dome.open_both()
		# elif choice == 'f':
			# dome.close_both()
		# else:
			# print 'invalid choice'
	
	

