"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Message gate. This module either transfer messages from the input port to the output port, or not.
        Parameters:
            gate_control(R): Boolean, true transfers messages, false swallows them
            resync(R): If true, the last swallowed message will be sent when the message gate opens"""

    def __init__(self, gate_control=True, resync=True):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Message Gate',  # will show up in GRC
            in_sig=None,
            out_sig=None
        )

        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('msg_out'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.last_msg = None
        self.resync = resync


        self._gate_control = gate_control

    @property
    def gate_control(self):
        """The gate control parameter tells whether messages are to be transferred or not"""
        return self._gate_control

    @gate_control.setter
    def gate_control(self, value):
        if self.resync and value and value != self._gate_control and self.last_msg is not None:
            self.message_port_pub(pmt.intern('msg_out'), self.last_msg)
            self.last_msg = None
        self._gate_control = value

    @gate_control.deleter
    def gate_control(self):
        del self._gate_control

    def handle_msg(self, msg):
        if self.gate_control:
            self.message_port_pub(pmt.intern('msg_out'), msg)
        else:
            self.last_msg = msg
