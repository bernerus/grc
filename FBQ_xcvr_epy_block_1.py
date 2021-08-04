"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import threading
import typing as T

import numpy as np
import pmt
from gnuradio import gr
import time


class one_shot:

    def __init__(self, delay: float, callback: T.Callable):
        self.delay = delay
        self.timer = None
        self.callback = callback
        self.last_start = None
        self.to_sleep = None
        self.thread = None

    def countdown(self):
        now = time.time_ns()
        if self.to_sleep is None:
            self.last_start = None
            print("Timer timed out, at %d last_start is now %s" % (now, self.last_start))
            self.timer.cancel()
            self.callback()
            return
        self.timer = threading.Timer(self.to_sleep, self.countdown)
        self.timer.start()
        self.last_start = now
        print("Timer restarted at %d for %f seconds" % (self.last_start, self.to_sleep))
        self.to_sleep = None

    def trigger(self):
        now = time.time_ns()
        if self.last_start is None:
            self.to_sleep = self.delay
            self.timer = threading.Timer(self.to_sleep, self.countdown)
            self.timer.start()
            self.last_start = now
            print("Timer started at %d for %f seconds" % (self.last_start, self.to_sleep))
            self.to_sleep = None
            return
        else:
            print("Trig, last_start=%f" % self.last_start)
            self.to_sleep = (now - self.last_start) / 1000000000
            print("Timer retrig at %d, To_sleep = %f" % (now, self.to_sleep))


# noinspection PyPep8Naming
class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """VOX detector - sends a message when detecting a signal and another some time after the signal has been absent
       threshold is the signal level needed to trigger an on-air message
       attack is the number of consecutive samples needed before the message is sent
       delay is the number of seconds after the last sample over the threshold level that the off-air
       message is sent.

       The on-air message is represented by the message pair ("onair", 1) and the off-air message is represented by the
       message pair ("onair", 0)

       The output stream contains 100 zeros if the last message sent is am off-air message and 100 ones
       if the last message sent is a on-air message. Whenever a message is sent a ramp string of samples
       are sent, going from 0 to 1 on any on-air signal and from 1 to 0 on any off-air signal.

       Note that the incoming stream needs to represent the volume level of the audio, not the audio samples themselves.

       """

    def __init__(self, threshold=5, attack=10, delay=0.5):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='VOX detector',  # will show up in GRC
            in_sig=[np.ubyte],
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.threshold = threshold
        self.attack = attack
        self.delay = delay

        self.attack_counter = attack  # Counts down to 0
        self.one_shot = None
        self.message_port_register_out(pmt.intern("onair"))
        self.onair = False
        # self.to_output = []

    def send_onair_message(self):
        if not self.onair:
            self.message_port_pub(pmt.intern("onair"), pmt.cons(pmt.string_to_symbol("onair"), pmt.to_pmt(1)))
            self.onair = True
            # self.ramp_up()

    def send_offair_message(self):
        if self.onair:
            self.message_port_pub(pmt.intern("onair"), pmt.cons(pmt.string_to_symbol("onair"), pmt.to_pmt(0)))
            self.onair = False
            # self.ramp_down()

    def ramp_up(self):
        self.to_output = []
        for i in range(0, 128):
            self.to_output.append(i/128)

    def ramp_down(self):
        self.to_output = []
        for i in range(0, 100):
            self.to_output.append(1 - i/128)


    def work(self, input_items, output_items):
        print("Input0(%d)=" % len(input_items[0]), input_items[0])
        # print("Output0(%d)=" % len(output_items[0]), output_items[0])
        for item in input_items[0]:
            if item is not None:
                item = -item if item < 0 else item
                if item > self.threshold:
                    self.attack_counter -= 1
                    if self.attack_counter <= 0:
                        self.send_onair_message()
                        self.trigger_one_shot()
                        self.attack_counter = self.attack
                else:
                    self.attack_counter = self.attack
        else:
            self.attack_counter = self.attack

        self.consume(0, len(input_items[0]))
        # self.produce(0, 128)
        # output_items[0] = self.to_output
        # self.to_output = [1 if self.onair else 0 for i in range(0, 128)]

        # return len(output_items[0])
        return 0

    def trigger_one_shot(self):
        if self.one_shot is None:
            self.one_shot = one_shot(self.delay, self.send_offair_message)
            print("Oneshot created")
        self.one_shot.trigger()
        print("Oneshot triggered")
