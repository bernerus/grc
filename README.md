# GNU Radio Projects

## The VHF/UHF transceiver

This project aims to develop a functioning VHF/UHF transceiver that use the HackRF hardware over a SoapyRemote connection.

As of the initial commit, the transceiver has been used to work exactly 1 QSO over FT8 on 144 MHz. A few months later, I have worked
over 50 QSOs over FT8 and MSK144 on 2m. 70cm has also been tested on CW. 

Of course, there is more hardware involved than the HackRF. The QSO:s on 144 MHz were done using the following stuff:

* An iMac for running the GRC script.

* A local (wired) Gigabit LAN

* A Raspberry PI 4 acting as a SoapySDR remote server and controlling the HackRF.

* A homebrew MMIC amplifier utilizing a PGA103+ for boosting the transmit power up to about 100mW or so

* The HackRF itself, modified to have a separate transmit port.

For 144 MHz, the additional equipment is

* A 3 stage helical filter to keep unwanted signals from being sent

* A linear transistor amplifier using an old 2N6082 to reach about a Watt or two.

* My very old kilowatt PA (Dual 4CX250B designed by W2GN and K2RIW in the 1980s) taking the power to some 250W.

* A home build 15 element yagi as described by DJ9BV in the mid 1990s

For 432 MHz, the additional equipment is

* A 3 stage helical filter to keep unwanted signals from being sent

* A 3 stage linear transistor amplifier as described by DJ6SC also in the mid 1990s, giving about 15 Watts output.

* A 21 element yagi by F9FT

There are a number of issues left with this code, so any suggestions fore improvements are welcome.

Also some fixes had to be done to SoapyHackRF to make this work. See my forked Repo for this.

###Prerequisites

To be able to run this, there are a bunch of things to fix first.

You need to have gnuradio installed.
You also need the SoapySDR framework installed. You do not need all components,
but install using the instructions at https://github.com/pothosware/SoapySDR

### Mac M1 specific info

As of today, gnuradio is not available in M1 native mode. Thus you will have to install Rosetta
if running on Apple Silicon. I installed using homebrew by making a copy of the 
terminal.app and specified in the info field that it should start with Rosetta.
Then specifically ran /usr/local/bin/brew install <whatever>

If lucky you can then start gnuradio-companion. Make sure it is not in /opt/homebrew, that's where homebrew put M1 native stuff.

#### Audio config for WSJT-X

In order to run some FT8 and MSK144 I installed the WSJT-X program and to get it to work with
this transceiver some audio plumbing was necessary.
The current plumbing uses blackhole-2ch for the receive audio, i.e. to WSJT-X, and
blackhole-16ch for transmit audio from WSJT-X.

Blackhole can be installed with homebrew and it is not necessary to involve Rosetta here.

The transceiver uses a multiple output unit named WSJT-3 which sends audio to the internal speaker and to blackhole-2ch.
WSJT-X similarly uses a multiple output unit named WSJT-out which sends output to the internal speaker and to blackhole-16ch
Of course other possibilities exist. WSJT-X audio is configured to take input from Blackhole-2ch and so send on WSJT-out, and the 
transceiver as is sends on WSJT-3 and listens on blackhole-15ch.

Note that installing WSJT-X requires configuration of shared memory. See the README file accompanying the WSJT-app for Mac.

