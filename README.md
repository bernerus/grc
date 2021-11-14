# GNU Radio Projects

## The VHF transceiver

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

* My very old kilowatt PA (Dual 4CX250B designed by W2GN and K2RIW) taking the power to some 200W. (Running very cool :)

* A home build 15 element yagi as described by DJ9BV in the mid 1990s

For 432 MHz, the additinal equipment is

* A 3 stage helical filter to keep unwanted signals from being sent

* A 3 stage linear transistor amplifier as described by DJ6SC also in the mid 1990s.

* A 21 element yagi by F9FT

There are a number of issues left with this code, so any suggestions fore improvements are welcome.

Also some fixes had to be done to SoapyHackRF to make this work. See my forked Repo for this.


