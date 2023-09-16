# GNU Radio Projects

## The VHF/UHF transceiver

This project aims to develop a functioning VHF/UHF transceiver that use the HackRF hardware over a SoapyRemote connection.

There are many files in this repository. The interesting file is the Gnuradio flowchart _fbq_xcvr_exp.grc_
It is a very large flowchart, you need to be able to scroll sideways to see everything.

As of the initial commit, the transceiver has been used to work exactly 1 QSO over FT8 on 144 MHz. A year later, I have worked
over 100:s QSOs over FT8 on both 2m and 70cm. Also many meteor scatter QSOs have been worked on 2m.

Of course, there is more hardware involved than the HackRF. The QSO:s on 144 MHz were done using the following stuff:

* An iMac for running the GRC script.

* A local (wired) Gigabit LAN

* A Raspberry PI 4 acting as a SoapySDR remote server and controlling the HackRF.

* A homebrew MMIC amplifier utilizing a PGA103+ and PHA202+ for filtering and boosting the transmit power up to about 1 W or so

* The HackRF itself, modified to have a separate transmit port.

For 144 MHz, the additional equipment is

* A linear transistor amplifier using an old 2N6082 to reach about a Watt or two.

* My very old kilowatt PA (Dual 4CX250B designed by W2GN and K2RIW in the 1980s) taking the output RF power to about 400W.

* A home build 15 element yagi as described by DJ9BV in the mid 1990s

For 432 MHz, the additional equipment is

* A homebrew MMIC amplifier utilizing a PGA103+ and PHA202+ for filtering and boosting the transmit power up to about 1 W or so

* A 3 stage linear transistor amplifier as described by DJ6SC also in the mid 1990s, giving about 15 Watts output.

* A 21 element yagi by F9FT

There are a number of issues left with this code, so any suggestions fore improvements are welcome.

Also some fixes had to be done to SoapyHackRF to make this work. See my forked Repo for this.

###Prerequisites

To be able to run this, there are a bunch of things to fix first.

You need to have GnuRadio 3.10.7 or later installed.
You may also need the SoapySDR framework installed. You do not need all components,
but install using the instructions at https://github.com/pothosware/SoapySDR

### Mac M1 specific info

Today, GnuRadio is available in M1 native mode. However, there seems to be issues regarding
the CPU core allocation within MacOS. This causes the received Audio to stutter.
Running in Rosetta mode seems to alleviate this problem.
Thus you will have to install Rosetta mif running on Apple Silicon. 
I used arch `x86_64 brew install gnuradio` in order to get an intel version.
The ARM version can be used for running GRC, though, but for runtime, the x86_64 version
seems more stable.

#### Audio configuration

The transceiver has separate audio source and sinks for WSJT-X. See below.
The audio volume of these channels is controlled by the knobs in the MGM tab. Audio level to the speaker is controlled by
the AF VOL knob which does noy affect the MGM level.

The TX MODE selects the audio input, so that in MGM mode the transmitter audio is taken from the MGM channel, otherwise
input is from the Mac microphone. When input is from the Mic, it is likely that the Speaker audio trigger the VOX. 
You may want to use a separate microphone or earphones when in SSB mode.

Please note that the audio sample rate expected is 48 kHz, make sure that any audio devices used, including the microphone, is set at 48 kHz.
Be aware that the Mac in certain situations reset the audio sampling rate to 44.1 kHz, when this happens everything seems to go haywire.

#### Audio config for WSJT-X

In order to run some FT8 and MSK144 I installed the WSJT-X program and to get it to work with
this transceiver some audio plumbing was necessary.
The current plumbing uses blackhole-2ch for the receive audio, i.e. to WSJT-X, and
blackhole-16ch for transmit audio from WSJT-X.

Blackhole can be installed with homebrew and it is not necessary to involve Rosetta here.

The transceiver sends audio to the blackhole_16ch and to std_spkr, and listens on blackhole_2ch and on "MacBook Pro-mikrofon"
WSJT-X sends output to the internal to blackhole-2ch and listens on blackhole_16ch
You may want to change these channels in the GnuRadio flowchart.

Note that installing WSJT-X requires configuration of shared memory. See the README file accompanying the WSJT-app for Mac.

### FM
The transceiver can demodulate both Wide band Stereo FM and NBFM. 
There is also a NBFM modulator for transmit.
For WBFM, there is no modulator and transmission is blocked.

### AM
The transceiver now also demodulated AM. There is no AM transmit mode implemented (yet)

### SSB & CW Rx
The transceiver can demodulate both LSB and USB. For CW the USB demodulator is used, but the frequency is silently downshifted 880 Hz, to make it possible
to fine-tune the station with a tuning fork. There is also a CW stereo mode which utilizes both USB and LSB demodulators simultaneously. In this mode the LSB frequency 
is instead upshifted 880 Hz, which means that when you listen to both tones in stereo, you can fine tune the receiver so that when you hear the same tone in both ears,
and there is almost no fluttering, you are exactly at the frequency of the received signal. With this you can use a beacon with a well defined frequency to check 
your SDR receiver calibration down to 1 Hz.

### SSB Tx
The Transceiver can modulate both USB and LSB. The modulator is of the Weaver type.

### CW Tx
For CW, the transceiver uses pure DC, 0 or 1, to modulate the carrier. There are some input help in the CW tab. Unfortunately I do not know any standard way of connecting a
CW key, or a keyer paddle to the computer, so working CW is a bit awkward.

### MGM
MGM uses the separate audio channel for WSJT-X as described above. In this mode the microphone is turned off. 

## Warnings
Although band limits are specified in the band list, there is nothing to stop you from tuning the transmitter outside the specified bands.
This is due to a bug in the dial widget.

When switching between modes, especially to and from the CW stereo mode, very loud sound bangs might be generated. 
Take care of your ears and don't have earphones on when shifting.


