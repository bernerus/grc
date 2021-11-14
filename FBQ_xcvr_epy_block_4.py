"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""
import pprint
import numpy as np
from gnuradio import gr


class blk(gr.basic_block):  # other base classes are basic_block, decim_block, interp_block
    """Stream padder. This block allows disparate streams to form a set of synchronized streams to avoid blockage. Missing samples are padded with zeros"""

    def __init__(self, channels=3):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.basic_block.__init__(
            self,
            name='Stream padder',   # will show up in GRC
            in_sig=[np.float32 for i in range(channels)],
            out_sig=[np.float32 for i in range(channels)]
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.channels = channels
        print("Stream padder, channels=%d"%self.channels)

    def fixed_rate():
        return false;

    def no_forecast(self, noutput_items, ninput_items_required):
        # setup size of input_items[i] for work call
        print("noutput_items=", noutput_items, "ninput_items_required=",ninput_items_required)
        for i in range(noutput_items-1):
            ninput_items_required[i] = noutput_items
        ninput_items_required[self.channels-1] = 0

    def general_work(self, noutput_items, ninput_items, input_items, output_items):
        """Make all output items as long as its longest input"""
        print("Stream padder: To produce=%d"%noutput_items)
        for i in range(self.channels):
            to_copy = min(len(input_items[i]), noutput_items)
            to_pad = noutput_items - to_copy

            output_items[i][:] = input_items[i][:to_copy]
            consume(i, to_copy)
            for i in range(to_pad):
                output_items[i].append(0.0)
            produce(i, noutput_items)

        print("output_items=", output_items)

        return max_len
