#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: AX25 BPSK TX
# GNU Radio version: 3.7.13.4
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
import limesdr
import satnogs
import sys
from gnuradio import qtgui


class ax25_bpsk_tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "AX25 BPSK TX")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("AX25 BPSK TX")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "ax25_bpsk_tx")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 48000
        self.rf_samp_rate = rf_samp_rate = 2.4e6

        self.bpsk = bpsk = digital.constellation_bpsk().base()

        self.baud_rate = baud_rate = 9600

        ##################################################
        # Blocks
        ##################################################
        self.satnogs_udp_msg_source_0 = satnogs.udp_msg_source("127.0.0.1", 16886, 1500, 0)
        self.satnogs_ax25_encoder_mb_0 = satnogs.ax25_encoder_mb('', 0, '', 0, 16, 16, True)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(rf_samp_rate),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.limesdr_sink_0 = limesdr.sink('0009072C00D6172C', 0, '', '')
        self.limesdr_sink_0.set_sample_rate(rf_samp_rate)
        self.limesdr_sink_0.set_center_freq(436.4e6, 0)
        self.limesdr_sink_0.set_bandwidth(5e6,0)
        self.limesdr_sink_0.set_gain(60,0)
        self.limesdr_sink_0.set_antenna(255,0)
        self.limesdr_sink_0.calibrate(5e6, 0)

        self.digital_constellation_modulator_0 = digital.generic_mod(
          constellation=bpsk,
          differential=False,
          samples_per_symbol=int(samp_rate/baud_rate),
          pre_diff_code=True,
          excess_bw=0.5,
          verbose=False,
          log=False,
          )
        self.blocks_unpacked_to_packed_xx_0 = blocks.unpacked_to_packed_bb(1, gr.GR_MSB_FIRST)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((0.5, ))
        self.analog_sig_source_x_0 = analog.sig_source_c(rf_samp_rate, analog.GR_COS_WAVE, 0, 1, 0)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.satnogs_udp_msg_source_0, 'msg'), (self.satnogs_ax25_encoder_mb_0, 'info'))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_unpacked_to_packed_xx_0, 0), (self.digital_constellation_modulator_0, 0))
        self.connect((self.digital_constellation_modulator_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.satnogs_ax25_encoder_mb_0, 0), (self.blocks_unpacked_to_packed_xx_0, 0))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "ax25_bpsk_tx")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate
        self.analog_sig_source_x_0.set_sampling_freq(self.rf_samp_rate)

    def get_bpsk(self):
        return self.bpsk

    def set_bpsk(self, bpsk):
        self.bpsk = bpsk

    def get_baud_rate(self):
        return self.baud_rate

    def set_baud_rate(self, baud_rate):
        self.baud_rate = baud_rate


def main(top_block_cls=ax25_bpsk_tx, options=None):

    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()


if __name__ == '__main__':
    main()
