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
    """Rx distancer. This module aims at making sure that the hardware receive frequency is kept within a defined range of hz below the desired frequency,
    and that the remaining difference is set into a variable. Only when the desired frequency would result in the hardware receive frequency
    would go outside the limits, the frequencies will be changed.
    The desired frequency is received through the message port.
    New hardware and filter frequencies are sent through the hw_fq_out, and the filter:fq_out ports.
    For proper operation, these ports should be connected to Messsage_pair_to_var blocks that
    transfer the new values back to the hw_var and filter_var variables respectively. If not, the operation of this block is undefined.

         """

    def __init__(self, desired_fq=0.0, min_distance=100e3, max_distance=1e6, hw_var=None, filter_var=None):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Rx distancer',  # will show up in GRC
            in_sig=None,
            out_sig=None
        )

        self.message_port_register_in(pmt.intern('freq_in'))
        self.set_msg_handler(pmt.intern('freq_in'), self.handle_msg)
        self.message_port_register_out(pmt.intern("hw_fq_out"))
        self.message_port_register_out(pmt.intern("filter_fq_out"))

        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).

        self.min_distance=min_distance
        self.max_distance=max_distance
        self._desired_fq=desired_fq
        self.hw_var=hw_var
        self.filter_var=filter_var
        # gr.log.error("Desired fq %f initially" % desired_fq)
        if desired_fq:
            self.compute_and_send(desired_fq)  # Initialize desired fq

    def compute_and_send(self, new_val):
        hw_var = self.hw_var
        # gr.log.error("New value %f" % new_val)

        hw_chunk = (self.max_distance - self.min_distance) / 2.0
        # gr.log.error("Chunk size= %f" % hw_chunk)

        distance = new_val - hw_var
        # gr.log.error("Distance = %f" % distance)

        while distance > self.max_distance:
            # gr.log.error("Distance = %f" % distance)
            hw_var += hw_chunk
            # gr.log.error("HW var = %f" % hw_var)
            distance = new_val - hw_var

        while distance < self.min_distance:
            # gr.log.error("Distance = %f" % distance)
            hw_var -= hw_chunk
            # gr.log.error("HW var = %f" % hw_var)
            distance = new_val - hw_var

        # gr.log.error("New HW var = %f" % hw_var)


        if hw_var != self.hw_var:
            gr.log.info("New HW fq = %f" % hw_var)
            self.message_port_pub(pmt.intern("hw_fq_out"), pmt.cons(pmt.intern("hw_fq"), pmt.to_pmt(hw_var)))
        new_filter = new_val - hw_var

        # gr.log.error("New filter var = %f" % new_filter)

        if new_filter != self.filter_var:
            gr.log.info("New filter var = %f" % new_filter)
            self.message_port_pub(pmt.intern("filter_fq_out"), pmt.cons(pmt.intern("filter_fq"), pmt.to_pmt(new_filter)))
        pass

    @property
    def desired_fq(self):
        """The gate control parameter tells whether messages are to be transferred or not"""
        return self._desired_fq

    @desired_fq.setter
    def desired_fq(self, value):
        self._desired_fq = value
        self.compute_and_send(value)

    @desired_fq.deleter
    def desired_fq(self):
        del self._desired_fq


    def handle_msg(self, msg):
        if not pmt.is_pair(msg) or pmt.is_dict(msg) or pmt.is_pdu(msg):
            gr.log.warn("Input message %s is not a simple pair, dropping" % repr(msg))
            return
        # gr.log.error("Input message %s received" % repr(msg))
        # gr.log.error("Max distance %d" % self.max_distance)
        # gr.log.error("Min distance %d" % self.min_distance)

        new_val = pmt.to_python(pmt.cdr(msg))

        self.compute_and_send(new_val)



    def stop(self):
        return True