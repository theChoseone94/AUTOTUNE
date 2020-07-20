import socket
from io import StringIO
import time
import io
import ShutterConfig as conf

"""
This script is a script designed to operate the mirror covers on the CDK600 telescope from PlaneWave. 

Some of the script is based on code from PlaneWave Instruments, but I fixed it so it could run. 

The config file for this script is: ShutterConfig.py

@Hasse Hansen, hasse302@hotmail.com


"""

def __init__():
    """
    A function that initializes the connection to the PlaneWave shutter control software. 

    Args:
        None
    Returns:
        None
    """

    global sock
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((conf.IP_address,conf.PORT))
    return 

def readline(sock):    
    """
    A function that reads the output from the PlaneWave Shutter control
    software through the TCP port.
    Args:
        None
    Returns:
        The return message from the PlaneWave Shutter Control software.
    """
    buf = io.StringIO()
    while True:
        data = sock.recv(1)
        buf.write(data.decode('utf-8'))
        if data.decode('utf-8') == '\n':
            print('There was a new line')
            return buf.getvalue()
        return buf.getvalue()


def sendreceive(sock,command):
    """
    A function that sends a command, which is encoded as bytes to
    the TCP port that the PlaneWave Shutter Control software is 
    transmitting on. 
    It then reads the response from the Shutter Control software.

    Args:
        Command to send. The following commands are acceptable:
        open
        close
        beginopen
        beginclose
        isconnected
        connect
        shutterstate
    Returns: 
        The reponse code along with any error text.
    """
    sock.send((command.encode("utf-8")+"\n".encode("utf-8")))
    response = readline(sock)

    fields = response.split(" ")
    response_code = int(fields[0])
    error_text = ""
    if len(fields) > 1:
        error_text = fields[1]
    return (response_code,error_text)


def CheckConnection():
    """
    A function that checks the connection between PlaneWave 
    Shutter Control software and the mirrors covers. 

    Args:
        None
    Returns:
        None
    """
    __init__()
    print("Checking connection")
    (code,text) = sendreceive(sock,"isconnected")
    if code == 0:
        print("PWShutter is connected to the controller")
        return
    elif code == 1:
        print("PWShutter is NOT connected to the controller")
        return
    else:
        print("Error",code,text)
        return


def ConnectToShutter():
    """
    A function that connects the PlaneWave Shutter Control software
    to the mirror covers. 

    Args:
        None
    Returns:
        None
    """
    __init__()
    print("Trying to connect to controller")
    (code,text) = sendreceive(sock,"connect")
    if code == 0:
        print("Controller is connected to the shutter")
    else:
        print("Error", code, text)

def OpenShutters():
    """
    A function that opens the shutters. The command is sent and the
    terminal can be used again after the command is sent. 
    If the command is executed, the function will print a message
    stating that the shutters are starting to open. 

    Args:
        None
    Returns:
        None
    """
    __init__()
    print("Trying to open the shutters...")
    (code,text) = sendreceive(sock,"beginopen")
    if code == 0:
        print("Shutters are starting to open")
    else: 
        print("Error",code,text)


def CloseShutters():
    """
    A function that closes the shutters on the mirror cover. 
    After the command is sent, the user can use the terminal again,
    without waiting for the covers to open.

    A statement is printed based on the response from the mirrorcovers

    Args:
        None
    Returns:
        None
    """
    __init__()
    print("Trying to close the shutters..")
    (code,text) = sendreceive(sock,"beginclose")
    if code == 0:
        print("Shutters are starting to close")
    else:
        print("Error",code,text)


def getStatus():
    """
    A function that states the status of the mirrorcovers. 
    The following states are possible: Open, Closed, Opening,
    Partly open and Error. 

    The state is printed to the user.

    Args:
        None
    Returns:
        None

    """
    __init__()
    print("Monitoring shutter status while opening...")
    timeout_sec = 1
    timeout = time.time() + timeout_sec
    while time.time() < timeout:
        (code,text) = sendreceive(sock,"shutterstate")
        if code == 0:
            print("Open")
        elif code == 1:
            print("Closed")
        elif code == 2:
            print("Opening")
        elif code == 3:
            print("Closing")
        elif code == 4: 
            print("Error")
        elif code == 5:
            print("Partly open")
        else:
            print("Error",code,text)
        #if code != 2:
        #    break
        time.sleep(1)
    print("Done!")
