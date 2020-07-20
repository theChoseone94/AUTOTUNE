# AUTOTUNE - Aarhus University Telescope Operations to Utilize New Equipment
Software package for remote operations with PlaneWave Instruments telescopes

## In the folder "PWI2":
These files are for doing remote operations of a CDK700 telescope from PlaneWave Instruments via XMLrpc server sending
HTTP commands to the telescope computer where PWI2 (the PlaneWaver Interface) is running. 
It is written in python3.

The daemon is started in a python terminal and runs in the background to have continous access to the telescope. 
It calls the functions in PW_Class.py which sends the HTTP commands via "requests".

A client is started in a python terminal and interacts with the daemon to call the commands in the PW_Class script. 

In PW_Class, all functions have descriptions with general information on the function, what arguments it takes,
example of calling the function, and what the function returns. 

This work was done for my Master thesis regarding the new telescope node for the Stellar Observation Network Group (SONG) project. It has been tested locally with both the simulator for PWI2 and on the physical telescope. 


## In the folder "PWI4":
Files for remote operations of the CDK600 telescope using the same setup as with the CDK700 and AUTOTUNE. This section is currently under development (7th July 2020).

## In the folder "MirrorCoverControl":
This folder contains the scripts for remotely operating the mirrorcovers on the CDK600 telescope. The script has a config file for setting the IP-address of the computer connected to the telescope with PlaneWave Instruments' "PlaneWave Shutter Control" software running. The TCP port used for communication is seeming hardwired. 

