# CWA400_LIN
LIN Example for CWA400

## Purpose
This python file describes requesting and sending data with a Pierburg CWA400 water pump over LIN. It's been confirmed to work with a OE BMW unit on a bench. 

## Method
Several functions are used to generate LIN-specific functions like the break pulse, PID parity bits, and enhanced checksum (LIN2.0). These are combined into an example program that sweeps through the RPM range and turns the pump off. Status data is logged to a local file for analysis. A USB-LIN adapter from embeddedProjects on Tindie is used to interface with a PC. A voltage-compliant RS485 converter may work as well.

## ToDo
Only some of the returned data bytes have been mapped to values. High confidence on Voltage, RPM, and temperature. Current (I) seems to track but at unconfirmed units. The final byte changes with the second byte of TX data but with no apparent functional changes.
