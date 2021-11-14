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
    """Message gate. This module either transfer messages reads a message from the input port and
        applies a python expression on it before sending it along on the output port

        Parameters:
            expr: String. The expression to apply. May use variables."""

    def __init__(self, variables=None):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Message formatter',  # will show up in GRC
            in_sig=None,
            out_sig=None
        )

        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('msg_out'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)

        self._variables=variables
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).


    @property
    def variables(self):
        """The gate control parameter tells whether messages are to be transferred or not"""
        return self._variables

    @variables.setter
    def variables(self, value):
        self._variables = value
        print("Variables set to", self._variables)

    @variables.deleter
    def variables(self):
        del self._variables



    def handle_msg(self, msg):
            new_value = pmt.to_python(pmt.cdr(msg)) % self._variables
            p = pmt.to_pmt(new_value)
            self.message_port_pub(pmt.intern("msg_out"), pmt.cons(pmt.intern("msg"), p))
