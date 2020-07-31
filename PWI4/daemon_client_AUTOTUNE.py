#!/usr/bin/python
""" 
   @author: Mads Fredslund Andersen and Hasse Hansen
"""

import xmlrpc.client
import sys
from optparse import OptionParser
import time
import PWI4_config as conf


"""
This program is for handling the client side of the daemon. 

First the two servers, "server" and "server2", is setup on their respective port. 
Then all the functions registered in the daemon_server_AUTOTUNE is defined. 
The naming scheme of the functions is the same as in PW_Class.py.

The idea is that the daemon is running on a server, 
while the client script here is then called from a terminal. The client is then 
imported as i.e. "telescope" and the functions can then be called with: "telescope.command". 
An example could be: telescope.ConnectMNT()
The client then calls the server, running on the daemon, which then calls PWI and thereby the
telescope in Australia and the command is executed. 

"""


parser = OptionParser()
parser.add_option("-c", "--command", dest="command", default="restart", help="")                                                                           
(options, args) = parser.parse_args()



#attempt connection to server
conn = xmlrpc.client.ServerProxy('http://%s:%i/'%(conf.NOVO_daemon_host,conf.NOVO_daemon_port1))

conn2 = xmlrpc.client.ServerProxy('http://%s:%i/'%(conf.NOVO_daemon_host,conf.NOVO_daemon_port2))

#Functions for the client side to call the server, which again calls PW_Class

###### Functions that run on conn2 (server2) that's only designed for the stop commands. 
def MountSTOP():
    try:
        reply = conn2.MountSTOP()
    except Exception as e:
        print(e)
    else:
        print(reply)

def FocSTOP():
    try:
        reply = conn2.FocSTOP()
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def RotSTOP():
    try:
        reply = conn2.RotSTOP()
    except Exception as e:
        print(e)
    else:
        print(reply)
#####

##### All other commands for operating the telescope.
def StopServerConnection():
	try:
		reply = conn.stop_server()
	except Exception as e:
		print('Could not connect to the server!')
		print(e)
	else:
		print(reply)


def ConnectMNT():
    try: 
        reply = conn.ConnectMNT()
    except Exception as e:
        print('Could not connect mount')
        print(e)
    else:
        print(reply)

def ConnectFOC():
    try: 
        reply = conn.ConnectFOC()
    except Exception as e:
        print('Could not connect mount')
        print(e)
    else:
        print(reply)
        
        
def parkMount():
    try: 
        reply = conn.parkMount()
    except Exception as e:
        print(e)
    else: 
        print(reply)
    
def getStatus():
    try: 
        reply = conn.getStatus()
    except Exception as e:
        print(e)
    else: 
        print(reply)
        
def DisconnectMNT():
    try:
        reply = conn.DisconnectMNT()
    except Exception as e:
        print(e)
    else: 
        print(reply)
        
def DisconnectFOC():
    try:
        reply = conn.DisconnectFOC()
    except Exception as e:
        print(e)
    else: 
        print(reply)
        
        
def Initialize():
    try:
        reply = conn.Initialize()
    except Exception as e:
        print(e)
    else: 
        print(reply)
        
def getRA2000():
    try:
        reply = conn.getRA2000()
    except Exception as e:
        print(e)
    else: 
        print(reply)    

def getDEC2000():
    try:
        reply = conn.getDEC2000()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def getMNT_CONNECT():
    try:
        reply = conn.getMNT_CONNECT()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def getFOC_CONNECT():
    try:
        reply = conn.getFOC_CONNECT()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def getROT_CONNECT():
    try:
        reply = conn.getROT_CONNECT()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def update():
    try:
        reply = conn.update()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def getIsTrackingOn():
    try:
        reply = conn.getIsTrackingOn()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def startTracking():
    try:
        reply = conn.startTracking()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def setTargetRaDecJ2000(RA,DEC):
    try:
        reply = conn.setTargetRaDecJ2000(RA,DEC)
    except Exception as e:
        print(e)
    else:
        print(reply)

def setTargetAltAzm(Alt,Azm):
    try:
        reply = conn.setTargetAltAzm(Alt,Azm)
    except Exception as e:
        print(e)
    else:
        print(reply)

def setTargetRaDec(Ra,Dec):
    try:
        reply = conn.setTargetRaDec(Ra,Dec)
    except Exception as e:
        print(e)
    else:
        print(reply)

def FansON():
    try:
        reply = conn.FansON()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def FansOFF():
    try:
        reply = conn.FansOFF()
    except Exception as e:
        print(e)
    else: 
        print(reply)
        
        
def MntMotorReset():
    try:
        reply = conn.MntMotorReset()
    except Exception as e:
        print(e)
    else: 
        print(reply)
        
def MntMotorEnable():
    try:
        reply = conn.MntMotorEnable()
    except Exception as e:
        print(e)
    else: 
        print(reply)        
        
def MntMotorDisable():
    try:
        reply = conn.MntMotorDisable()
    except Exception as e:
        print(e)
    else: 
        print(reply)

def startMntHoming():
    try:
        reply = conn.startMntHoming()
    except Exception as e:
        print(e)
    else:
        print(reply)

def MoveFocuserPos(position):
    try:
        reply = conn.MoveFocuserPos(position)
    except Exception as e:
        print(e)
    else: 
        print(reply)
    return

def MntMoveRaDecJ2000():
    try:
        reply = conn.MntMoveRaDecJ2000()
    except Exception as e:
        print(e)
    else:
        print(reply)

def stopTracking():
    try:
        reply = conn.stopTracking()
    except Exception as e:
        print(e)
    else:
        print(reply)   
        
def getALL():
    try: 
        reply = conn.getALL()
    except Exception as e:
        print(e)
    else:
        print(reply)

def getTrackingRMSError():
    try:
        reply = conn.getTrackingRMSError()
    except Exception as e:
        print(e)
    else:
        print(reply)

def getTemps():
    try:
        reply = conn.getTemps()
    except Exception as e:
        print(e)
    else:
        print(reply)

def getFocuserPos():
    try:
        reply = conn.getFocuserPos()
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def checkFormatRaDec(Ra,Dec):
    try:
        reply = conn.checkFormatRaDec(Ra,Dec)
    except Exception as e:
        print(e)
    else:
        print(reply)

def checkFormatAltAzm(Alt,Azm):
    try:
        reply = conn.checkFormatAltAzm(Alt,Azm)
    except Exception as e:
        print(e)
    else:
        print(reply)

def checkFormatArcsec(Arcsec):
    try:
        reply = conn.checkFormatArcsec(Arcsec)
    except Exception as e:
        print(e)
    else:
        print(reply)      

def MntMoveRaDec():
    try:
        reply = conn.MntMoveRaDec()
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def MntMoveAltAzm():
    try:
        reply = conn.MntMoveAltAzm()
    except Exception as e:
        print(e)
    else:
        print(reply)


def LoadPointingModel(filename):
    try:
        reply = conn.LoadPointingModel(filename)
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def AddPointToModel(Ra,Dec):
    try:
        reply = conn.AddPointToModel(Ra,Dec)
    except Exception as e:
        print(e)
    else:
        print(reply)

def SavePointingModel(filename):
    try:
        reply = conn.SavePointingModel(filename)
    except Exception as e:
        print(e)
    else:
        print(reply)

def ClearPointingModel():
    try:
        reply = conn.ClearPointingModel()
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def getRotatorPos():
    try:
        reply = conn.getRotatorPos()
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def getRotatorDerotate():
    try:
        reply = conn.getRotatorDerotate()
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def Rot_Move(position):
    try:
        reply = conn.Rot_Move(position)
    except Exception as e:
        print(e)
    else:
        print(reply)
        
def Rot_derotateStart():
    try:
        reply = conn.Rot_derotateStart()
    except Exception as e:
        print(e)
    else:
        print(reply)

def Rot_derotateStop():
    try:
        reply = conn.Rot_derotateStop()
    except Exception as e:
        print(e)
    else:
        print(reply)        