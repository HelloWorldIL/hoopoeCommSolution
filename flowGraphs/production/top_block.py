#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: NBFM Transmit output (After 3Khz LPF)
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

import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from PyQt4 import Qt
from bpsk_demod import bpsk_demod  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from optparse import OptionParser
from rms_agc import rms_agc  # grc-generated hier_block
import bruninga
import epy_block_0
import epy_block_1
import limesdr
import sip
from gnuradio import qtgui


class top_block(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "NBFM Transmit output (After 3Khz LPF)")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("NBFM Transmit output (After 3Khz LPF)")
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

        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())


        ##################################################
        # Variables
        ##################################################
        self.tx_offset = tx_offset = 50e3
        self.tx_freq = tx_freq = 145.97e6
        self.samp_rate = samp_rate = 48000
        self.rx_offset = rx_offset = 50e3
        self.rx_freq = rx_freq = 436.4e6
        self.rf_samp_rate = rf_samp_rate = 2.4e6
        self.bfo = bfo = 12e3
        self.LO_correction = LO_correction = 0

        ##################################################
        # Blocks
        ##################################################
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(rf_samp_rate),
                decimation=int(samp_rate),
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_sink_x_0 = qtgui.sink_c(
        	1024, #fftsize
        	firdes.WIN_BLACKMAN_hARRIS, #wintype
        	0, #fc
        	samp_rate, #bw
        	"", #name
        	True, #plotfreq
        	True, #plotwaterfall
        	True, #plottime
        	True, #plotconst
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win)

        self.qtgui_sink_x_0.enable_rf_freq(False)



        self.limesdr_source_0 = limesdr.source('0009072C00D6172C', 0, '')
        self.limesdr_source_0.set_sample_rate(rf_samp_rate)
        self.limesdr_source_0.set_center_freq(rx_freq-rx_offset+LO_correction, 0)
        self.limesdr_source_0.set_bandwidth(5e6,0)
        self.limesdr_source_0.set_digital_filter(5e3,0)
        self.limesdr_source_0.set_gain(60,0)
        self.limesdr_source_0.set_antenna(3,0)
        self.limesdr_source_0.calibrate(10e6, 0)

        self.limesdr_sink_0 = limesdr.sink('0009072C00D6172C', 0, '', '')
        self.limesdr_sink_0.set_sample_rate(rf_samp_rate)
        self.limesdr_sink_0.set_center_freq(tx_freq-tx_offset+LO_correction, 0)
        self.limesdr_sink_0.set_bandwidth(5e6,0)
        self.limesdr_sink_0.set_gain(60,0)
        self.limesdr_sink_0.set_antenna(1,0)
        self.limesdr_sink_0.calibrate(2.5e6, 0)

        self.freq_xlating_fir_filter_xxx_0_0 = filter.freq_xlating_fir_filter_ccc(int(rf_samp_rate/samp_rate), (firdes.low_pass(1, rf_samp_rate, 12000, 500)), rx_offset, rf_samp_rate)
        self.epy_block_1 = epy_block_1.blk()
        self.epy_block_0 = epy_block_0.blk()
        self.bruninga_ax25_fsk_mod_0 = bruninga.ax25_fsk_mod(samp_rate, 300, 5, 2200, 1200, 1200)
        self.bpsk_demod_1 = bpsk_demod(
            bfo=12e3,
            boud_rate=9600,
        )
        self.blocks_socket_pdu_1_0 = blocks.socket_pdu("TCP_SERVER", '', '52003', 10000, False)
        self.blocks_socket_pdu_1 = blocks.socket_pdu("TCP_SERVER", '', '52002', 10000, False)
        self.blocks_socket_pdu_0 = blocks.socket_pdu("TCP_SERVER", '', '52001', 10000, False)
        self.blocks_multiply_xx_1 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((0.9, ))
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.analog_sig_source_x_1 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, bfo, 1, 0)
        self.analog_sig_source_x_0 = analog.sig_source_c(rf_samp_rate, analog.GR_COS_WAVE, tx_offset, 1, 0)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=75e-6,
        	max_dev=5e3,
        	fh=-1.0,
                )



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.blocks_socket_pdu_0, 'pdus'), (self.epy_block_1, 'in'))
        self.msg_connect((self.epy_block_1, 'out'), (self.bruninga_ax25_fsk_mod_0, 'in'))
        self.connect((self.analog_nbfm_tx_0, 0), (self.epy_block_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_1, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.bpsk_demod_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.epy_block_0, 1))
        self.connect((self.blocks_multiply_xx_0, 0), (self.limesdr_sink_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.bpsk_demod_1, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.bruninga_ax25_fsk_mod_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.epy_block_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.freq_xlating_fir_filter_xxx_0_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.limesdr_source_0, 0), (self.freq_xlating_fir_filter_xxx_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_multiply_xx_0, 1))

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "top_block")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_tx_offset(self):
        return self.tx_offset

    def set_tx_offset(self, tx_offset):
        self.tx_offset = tx_offset
        self.limesdr_sink_0.set_center_freq(self.tx_freq-self.tx_offset+self.LO_correction, 0)
        self.analog_sig_source_x_0.set_frequency(self.tx_offset)

    def get_tx_freq(self):
        return self.tx_freq

    def set_tx_freq(self, tx_freq):
        self.tx_freq = tx_freq
        self.limesdr_sink_0.set_center_freq(self.tx_freq-self.tx_offset+self.LO_correction, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_sink_x_0.set_frequency_range(0, self.samp_rate)
        self.analog_sig_source_x_1.set_sampling_freq(self.samp_rate)

    def get_rx_offset(self):
        return self.rx_offset

    def set_rx_offset(self, rx_offset):
        self.rx_offset = rx_offset
        self.limesdr_source_0.set_center_freq(self.rx_freq-self.rx_offset+self.LO_correction, 0)
        self.freq_xlating_fir_filter_xxx_0_0.set_center_freq(self.rx_offset)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.limesdr_source_0.set_center_freq(self.rx_freq-self.rx_offset+self.LO_correction, 0)

    def get_rf_samp_rate(self):
        return self.rf_samp_rate

    def set_rf_samp_rate(self, rf_samp_rate):
        self.rf_samp_rate = rf_samp_rate
        self.freq_xlating_fir_filter_xxx_0_0.set_taps((firdes.low_pass(1, self.rf_samp_rate, 12000, 500)))
        self.analog_sig_source_x_0.set_sampling_freq(self.rf_samp_rate)

    def get_bfo(self):
        return self.bfo

    def set_bfo(self, bfo):
        self.bfo = bfo
        self.analog_sig_source_x_1.set_frequency(self.bfo)

    def get_LO_correction(self):
        return self.LO_correction

    def set_LO_correction(self, LO_correction):
        self.LO_correction = LO_correction
        self.limesdr_source_0.set_center_freq(self.rx_freq-self.rx_offset+self.LO_correction, 0)
        self.limesdr_sink_0.set_center_freq(self.tx_freq-self.tx_offset+self.LO_correction, 0)


def main(top_block_cls=top_block, options=None):

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
