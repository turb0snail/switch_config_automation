# Switch Config Automation

Switch Configuration Automation assists in automating the configuration process of network switches.

## Description

This repository contains scripts and tools for automating the tedious task of configuring network switches. With just a few commands, you can setup, modify, or delete configurations across one or multiple switches.

## Getting Started

### Prerequisites

- Python 3.x
- Serial connection to the switches ( for now ;))

P.S: When configuring switches via a serial connection, you first need to set an initial password for login. After that, you can proceed with switch configuration automation using the serial port. Importantly, after configuring the switches, you should connect to the switch via the serial connection to check if the configuration has been written. It's essential to manually save the configuration afterward. If you are running the script, ensure all serial connections to the switch are closed, as the serial port does not allow multiple connections.

I hope these scripts make your life easier. ⚛️
