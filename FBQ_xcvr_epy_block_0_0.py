"""
Morse code vector source
"""

#  epy_block_0.py
#  revised 09/10/2019 - finish code table
#  revised 09/11/2019 - test for bad character
#  revised 09/27/2019 - get input from a Message Edit block (code from Volker Schroer dl1ksv)

import numpy as np
from gnuradio import gr

import pmt

textboxValue = ""

Morse = {
    # codes from https://www.itu.int/rec/R-REC-M.1677-1-200910-I/en
    "A": "10111",
    "B": "111010101",
    "C": "11101011101",
    "D": "1110101",
    "E": "1",
    "F": "101011101",
    "G": "111011101",
    "H": "1010101",
    "I": "101",
    "J": "1011101110111",
    "K": "111010111",
    "L": "101110101",
    "M": "1110111",
    "N": "11101",
    "O": "11101110111",
    "P": "10111011101",
    "Q": "1110111010111",
    "R": "1011101",
    "S": "10101",
    "T": "111",
    "U": "1010111",
    "V": "101010111",
    "W": "101110111",
    "X": "11101010111",
    "Y": "1110101110111",
    "Z": "11101110101",
    "Å": "101110111010111",
    "Ä": "10111010111",
    "Ö": "1110111011101",
    " ": "0",
    "1": "10111011101110111",
    "2": "101011101110111",
    "3": "1010101110111",
    "4": "10101010111",
    "5": "101010101",
    "6": "11101010101",
    "7": "1110111010101",
    "8": "111011101110101",
    "9": "11101110111011101",
    "0": "1110111011101110111",
    ".": "10111010111010111",  # period
    ",": "1110111010101110111",  # comma
    ":": "11101110111010101",  # colon
    "?": "101011101110101",  # question
    "'": "1011101110111011101",  # apostrophe
    "-": "111010101010111",  # dash or minus
    "/": "1110101011101",  # slash
    "(": "111010111011101",  # left parenthesis
    ")": "1110101110111010111",  # right parenthesis
    "\"": "101110101011101",  # quote
    "=": "1110101010111",  # equals
    "+": "1011101011101",  # plus
    "@": "10111011101011101",  # at sign (@)
    # these punctuation marks are not included in the ITU recommendation
    # but are found in https://en.wikipedia.org/wiki/Morse_code
    "!": "1110101110101110111",  # exclamation point
    "&": "10111010101",  # ampersand (also prosign for 'WAIT')
    ";": "11101011101011101",  # semicolon
    "_": "10101110111010111",  # underscore
    "$": "10101011101010111"  # dollar sign
}


class mc_sync_block(gr.sync_block):
    """
    reads input from a message port
    generates a vector of Morse code bits
    """

    def __init__(self, enable=True):
        gr.sync_block.__init__(self,
                               name="Morse code vector source",
                               in_sig=None,
                               out_sig=[np.byte])
        self.message_port_register_in(pmt.intern('msg_in'))
        self.message_port_register_out(pmt.intern('clear_input'))
        self.set_msg_handler(pmt.intern('msg_in'), self.handle_msg)
        self.enable=enable
        self.textboxValue = None

    def handle_msg(self, msg):
        global textboxValue
        print(msg)
        if pmt.is_symbol(msg):
            self.textboxValue = pmt.symbol_to_string(msg)
        else:
            self.textboxValue = pmt.to_python(pmt.cdr(msg))
        print(textboxValue)

    def work(self, input_items, output_items):

        nbit_stream = ""

        if not self.enable:
            self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
            return 0

        if not self.textboxValue:
            return 0

        for ch in self.textboxValue:
            nbit_stream += (Morse.get(ch.upper()) if ch.upper() in Morse else Morse.get('?')) + "000"
        nbit_stream += "0000"

        for x in range(len(nbit_stream)):
            output_items[0][x] = int(nbit_stream[x])

        # clear input line
        self.textboxValue = ""
        self.message_port_pub(pmt.intern('clear_input'), pmt.intern(''))
        return len(nbit_stream)
