# GNU Radio Projects

## The VHF/UHF transceiver

This project aims to develop a functioning VHF/UHF transceiver that use the HackRF hardware over a SoapyRemote connection.

As of the initial commit, the transceiver has been used to work exactly 1 QSO over FT8 on 144 MHz. A year later, I have worked
over 100:s QSOs over FT8 on both 2m and 70cm. Also many meteor scatter QSOs have been worked on 2m.

Of course, there is more hardware involved than the HackRF. The QSO:s on 144 MHz were done using the following stuff:

* An iMac for running the GRC script.

* A local (wired) Gigabit LAN

* A Raspberry PI 4 acting as a SoapySDR remote server and controlling the HackRF.

* A homebrew MMIC amplifier utilizing a PGA103+ for boosting the transmit power up to about 100mW or so

* The HackRF itself, modified to have a separate transmit port.

For 144 MHz, the additional equipment is

* A 3 stage helical filter to keep unwanted signals from being sent

* A linear transistor amplifier using an old 2N6082 to reach about a Watt or two.

* My very old kilowatt PA (Dual 4CX250B designed by W2GN and K2RIW in the 1980s) taking the output RF power to about 400W.

* A home build 15 element yagi as described by DJ9BV in the mid 1990s

For 432 MHz, the additional equipment is

* A 3 stage helical filter to keep unwanted signals from being sent

* A 3 stage linear transistor amplifier as described by DJ6SC also in the mid 1990s, giving about 15 Watts output.

* A 21 element yagi by F9FT

There are a number of issues left with this code, so any suggestions fore improvements are welcome.

Also some fixes had to be done to SoapyHackRF to make this work. See my forked Repo for this.

###Prerequisites

To be able to run this, there are a bunch of things to fix first.

You need to have GnuRadio 3.10.2 or later installed.
You also need the SoapySDR framework installed. You do not need all components,
but install using the instructions at https://github.com/pothosware/SoapySDR

### Mac M1 specific info

As of today, GnuRadio is not available in M1 native mode. Thus you will have to install Rosetta
if running on Apple Silicon. I installed using homebrew by making a copy of the 
terminal.app and specified in the info field that it should start with Rosetta.
Then specifically ran /usr/local/bin/brew install <whatever>

If lucky you can then start gnuradio-companion. Make sure it is not in /opt/homebrew, which is where homebrew put M1 native stuff.

#### Audio configuration

The transceiver has separate audio source and sinks for WSJT-X. See below.
The audio volume of these channels is controlled by the knobs in the MGM tab. Audio level to the speaker is controlled by
the AF VOL knob which does noy affect the MGM level.

The TX MODE selects the audio input, so that in MGM mode the transmitter audio is taken from the MGM channel, otherwise
input is from the Mac microphone. When input is from the Mic, it is likely that the Speaker audio trigger the VOX. 
You may want to use a separate microphone or earphones when in SSB mode.

Please note that the audio sample rate expected is 48 kHz, make sure that any audio devices used, including the microphone, is set at 48 kHz.

#### Audio config for WSJT-X

In order to run some FT8 and MSK144 I installed the WSJT-X program and to get it to work with
this transceiver some audio plumbing was necessary.
The current plumbing uses blackhole-2ch for the receive audio, i.e. to WSJT-X, and
blackhole-16ch for transmit audio from WSJT-X.

Blackhole can be installed with homebrew and it is not necessary to involve Rosetta here.

The transceiver uses a multiple output unit named WSJT-3 which sends audio to the internal speaker and to blackhole-2ch.
WSJT-X similarly uses a multiple output unit named WSJT-out which sends output to the internal speaker and to blackhole-16ch
Of course other possibilities exist. WSJT-X audio is configured to take input from Blackhole-2ch and to send on WSJT-out, and the 
transceiver as is sends on WSJT-3 and listens on blackhole-15ch.

Note that installing WSJT-X requires configuration of shared memory. See the README file accompanying the WSJT-app for Mac.

### FM
The transceiver can demodulate both Wide band Stereo FM and NBFM. 
There is also a NBFM modulator for transmit which has not been tested live.
In WBFM, transmission is blocked.

### SSB & CW Rx
The transceiver can demodulate both LSB and USB. For CW the USR demodulator is used, but the frequency is silently downshifted 880 Hz, to make it possible
to fine-tune the station with a tuning fork. There is also a CW stereo mode which utilizes both USB and LSB demodulators. In this mode the LSB frequency 
is upshifted 880 Hz, which means that when you listen to both tones in stereo, you can fine tine the receiver so that when you hear the same tone in both ears,
snd there is almost no fluttering, you are exactly at the frequency of the received signal. With this you can use a beacon with a well defined frequency to check 
your SDR receiver calibration down to 1 Hz.

### SSB Tx
The Transceiver can modulate both USB and LSB. The modulator is of the Weaver Type.

### CW Tx
For CW, the transceiver uses pure DC, 0 or 1, to modulate the carrier. There are some input help in the CW tab. Unfortunately I do not know any standard way of connecting a
CW key, or a keyer paddle to the computer, so working CW is a bit awkward.

### MGM
MGM uses the separate audio channel for WSJT-X as described above. In this mode the microphone is turned off. 



