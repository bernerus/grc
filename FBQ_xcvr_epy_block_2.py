"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Message gate. This module either transfer messages reads a message from the input port and
        applies a python expression on it before sending it along on the output port

        Parameters:
            expr: String. The expression to apply. May use variables."""

    def __init__(self, offset=0, factor=10):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Message mangler',  # will show up in GRC
            in_sig=None,
            out_sig=None
        )

        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('msg_out'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.offset=offset
        self.factor=factor
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).


    def handle_msg(self, msg):
            adj = self.factor*pmt.to_python(pmt.cdr(msg))
            new_value = self.offset + adj
            print(adj, new_value)
            p = pmt.to_pmt(new_value)
            self.message_port_pub(pmt.intern("msg_out"), pmt.cons(pmt.intern("fq"), p))
            time.sleep(0.1)
            self.message_port_pub(pmt.intern("msg_out"), pmt.cons(pmt.intern("fq"), p))