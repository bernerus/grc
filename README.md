# GNU Radio Projects

## The VHF transceiver

This project aims to develop a functioning VHF/UHF transceiver that use the HackRF hardware over a SoapyRemote connection.

As of the initial commit, the transceiver has been used to work exactly 1 QSO over FT8 on 144 MHz.

Of course, there is more hardware involver that the HackRF. The QSO was done using the following stuff:

* An iMac for running the GRC script.

* A local (wired) LAN

* A Raspberry PI 4 acting as a SoapySDR remote server and controlling the HackRF.

* A homebrew MMIC amplifier utilizing a PGA103+ for boosting the transmit power up to about 100mW or so

* A 3 stage helical filter to keep unwanted signals from being sent

* A linear transistor amplifier using an old 2N6082 to reach about a Watt or two.

* My very old kilowatt PA (Dual 4CX250B designed by W2GN and K2RIW) taking the power to some 200W. (Running very cool :)

* The HackRF was modified to have a separate transmit port.

There are a number of issues left with this code so please don't try this at home yet.

Also some fixes had to be done to SoapyHackRF to make this work. See my forked Repo.


