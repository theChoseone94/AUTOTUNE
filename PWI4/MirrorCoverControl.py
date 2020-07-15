import socket
from io import StringIO
import time
import io


def __init__():
    global sock
    print("Connecting to PWShutter TCP server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(("10.22.88.145",9897))
    return

def readline(sock):    
    buf = io.StringIO()
    while True:
        data = sock.recv(1)
        buf.write(data.decode('utf-8'))
        if data == '\n':
            return buf.getvalue()
        if data == '\r':
            return buf.getvalue()
        return buf.getvalue()


def sendreceive(sock,command):
    """
    """
    #command = command + "\n"
    sock.send((command.encode("utf-8")+"\n".encode("utf-8")))
    response = readline(sock)

    fields = response.split(" ")
    response_code = int(fields[0])
    error_text = ""
    if len(fields) > 1:
        error_text = fields[1]
    return (response_code,error_text)


def CheckConnection():
    __init__()
    print("Checking connection")
    (code,text) = sendreceive(sock,"isconnected")
    print(code)
    if code == 0:
        print("PWShutter is connected to the controler")
        return
    elif code == 1:
        print("PWShutter is NOT connected to the controller")
        return
    else:
        print("Error",code,text)
        return


def ConnectToShutter():
    print("Trying to connect to controller")
    (code,text) = sendreceive(sock,"connect")
    if code == 0:
        print("Controller is connected to the shutter")
    else:
        print("Error", code, text)

def OpenShutters():
    __init__()
    print("Trying to begin opening the shutter...")
    (code,text) = sendreceive(sock,"beginopen")
    if code == 0:
        print("Shutters are starting to open")
    else: 
        print("Error",code,text)


def CloseShutters():
    __init__()
    print("Trying to close the shutters..")
    (code,text) = sendreceive(sock,"beginclose")
    if code == 0:
        print("Shutters are starting to close")
    else:
        print("Error",code,text)


def getStatus():
    print("Monitoring shutter status while opening...")
    while True:
        (code,text) = sendreceive(sock,"shutterstate")
        print(code)
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
        if code != 2:
            break
        time.sleep(1)
    print("Done!")
