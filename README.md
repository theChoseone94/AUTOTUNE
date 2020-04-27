# AUTOTUNE - Aarhus University Telescope Operations to Utilize New Equipment
Software package for remote operations with PlaneWave Instruments CDK700 telescopes

These files are for doing remote operations of a CDK700 telescope from PlaneWave Instruments via XMLrpc server sending
HTTP commands to the telescope computer where PWI2 (the PlaneWaver Interface) is running. 
It is written in python3.


The daemon is started in a python terminal and runs in the background to have continous access to the telescope. 
It calls the functions in PW_Class.py which sends the HTTP commands via "requests".

A client is started in a python terminal and interacts with the daemon to call the commands in the PW_Class script. 

In PW_Class, all functions have descriptions with general information on the function, what arguments it takes,
example of calling the function, and what the function returns. 

This work was done for my Master thesis regarding the new telescope node for the Stellar Observation Network Group (SONG) project. It has been tested locally with both the simulator for PWI2 and on the physical telescope. 
