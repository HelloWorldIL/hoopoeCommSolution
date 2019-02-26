"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import pickle
from bruninga import packet


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Convert a message of a binary AX.25 packet to a serialized AX25Packet object"""

    def __init__(self):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        gr.sync_block.__init__(
            self,
            name='Binary Packet to Serialized object',   # will show up in GRC
            in_sig=None,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg_pmt):
        print "Got message!"
        msg = pmt.to_python(msg_pmt)
        p = packet.from_bytes(bytearray(msg[1]))
        print "Dest: " +  str(p.dest)
        print "Src: " + str(p.src)
        print "Data: " + str(p.info.__repr__())
        out = (None, pickle.dumps(p))
        self.message_port_pub(pmt.intern('out'), pmt.to_pmt(out))

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        output_items[0][:] = input_items[0] * self.example_param
        return len(output_items[0])
