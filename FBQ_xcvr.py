#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SM6FBQ VHF transceiver
# Author: Christer Bernérus, SM6FBQ
# Description: VHF-UHF transceiver with CW and SSB
# GNU Radio version: 3.9.2.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from PyQt5.QtCore import QObject, pyqtSlot
from gnuradio import eng_notation
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import soapy
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import FBQ_xcvr_epy_block_0_0 as epy_block_0_0  # embedded python block
import FBQ_xcvr_epy_block_1 as epy_block_1  # embedded python block
import FBQ_xcvr_epy_block_1_0 as epy_block_1_0  # embedded python block
import time
import threading



from gnuradio import qtgui

class FBQ_xcvr(gr.top_block, Qt.QWidget):

    def __init__(self, preset_fq=144.174e6):
        gr.top_block.__init__(self, "SM6FBQ VHF transceiver", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("SM6FBQ VHF transceiver")
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

        self.settings = Qt.QSettings("GNU Radio", "FBQ_xcvr")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Parameters
        ##################################################
        self.preset_fq = preset_fq

        ##################################################
        # Variables
        ##################################################
        self.band_chooser = band_chooser = 9
        self.band_center = band_center = (50.2e6, 50.45e6, 144.200e6,144.450e6, 432.2e6,432.45e6, 1296.4e6, 1296.850e6, preset_fq,144.174e6)
        self.tune = tune = 0
        self.rit = rit = 0
        self.fine_tune = fine_tune = 0
        self.f0 = f0 = band_center[band_chooser]
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.tx_center_fq = tx_center_fq = (f0 + tune + fine_tune)
        self.ssb_txing = ssb_txing = 0
        self.rx_center_freq = rx_center_freq = f0-100e3
        self.filter_freq = filter_freq = 100e3+rit + tune + fine_tune
        self.cw_txing = cw_txing = 0
        self.wf_gain = wf_gain = 1
        self.vox_gain = vox_gain = 50
        self.vga_gain = vga_gain = 53
        self.variable_static_text_1_0 = variable_static_text_1_0 = '{:.0f}'.format(rx_center_freq+filter_freq)
        self.variable_static_text_1 = variable_static_text_1 = '{:.0f}'.format(tx_center_fq)
        self.variable_static_text_0 = variable_static_text_0 = ('{:.1f}'.format(variable_function_probe_0))
        self.variable_qtgui_entry_0 = variable_qtgui_entry_0 = '{:.0f}'.format(filter_freq)
        self.var_bw = var_bw = 0
        self.usb_chain_gain = usb_chain_gain = 1,0,1,1
        self.txing = txing = cw_txing or ssb_txing
        self.tx_samp_rate = tx_samp_rate = 2000000
        self.tx_gain = tx_gain = 47
        self.symbol_rate = symbol_rate = 300
        self.ssb_txing_btn = ssb_txing_btn = 0
        self.ssb_tx_mode = ssb_tx_mode = 1,1,0,0
        self.ssb_tx_bandwidth = ssb_tx_bandwidth = 4000
        self.sq = sq = -110
        self.side_band = side_band = 0
        self.sb_t = sb_t = [1,-1,1,1]
        self.sb_r = sb_r = [-1,1,1,-1]
        self.rx_samp_rate = rx_samp_rate = 1000000
        self.rx_preamp = rx_preamp = 0
        self.rx_corr = rx_corr = 0,0,580,0
        self.pwr = pwr = 1
        self.morse_speed = morse_speed = 100
        self.monitor = monitor = 1
        self.mic_gain = mic_gain = 1.4
        self.lsb_chain_gain = lsb_chain_gain = 0,1,0,1
        self.lna_gain = lna_gain = 39
        self.fft_corr = fft_corr = 0,0,880,0
        self.cw_samp_rate = cw_samp_rate = 50e3
        self.cw_midear_beat = cw_midear_beat = 0,0,880,880
        self.cw_level = cw_level = 0.8
        self.bpf_low = bpf_low = 100,100,380,480
        self.bpf_high = bpf_high = 3900,2700,880,680
        self.band_width = band_width = (400e3, 100e3, 400e3,100e3, 400e3,100e3, 800e3, 200e3, 1000e3, 200e3)
        self.audio_samp_rate = audio_samp_rate = 48000
        self.af_right = af_right = 0.5
        self.af_gain = af_gain = 6
        self.RX_power_offset_dB = RX_power_offset_dB = -104

        ##################################################
        # Blocks
        ##################################################
        self._wf_gain_range = Range(0, 100, 1, 1, 200)
        self._wf_gain_win = RangeWidget(self._wf_gain_range, self.set_wf_gain, 'Waterfall gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._wf_gain_win)
        self._vox_gain_range = Range(0, 200, 1, 50, 200)
        self._vox_gain_win = RangeWidget(self._vox_gain_range, self.set_vox_gain, 'VOX GAIN', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._vox_gain_win)
        self._vga_gain_range = Range(0, 61, 1, 53, 200)
        self._vga_gain_win = RangeWidget(self._vga_gain_range, self.set_vga_gain, 'RX VGA Gain', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._vga_gain_win, 3, 0, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._var_bw_options = [0, 1, 2, 3]
        # Create the labels list
        self._var_bw_labels = ['3.9', '2.7', '0.5', '0.05']
        # Create the combo box
        self._var_bw_tool_bar = Qt.QToolBar(self)
        self._var_bw_tool_bar.addWidget(Qt.QLabel('RECEIVER BANDWIDTH - kHz' + ": "))
        self._var_bw_combo_box = Qt.QComboBox()
        self._var_bw_tool_bar.addWidget(self._var_bw_combo_box)
        for _label in self._var_bw_labels: self._var_bw_combo_box.addItem(_label)
        self._var_bw_callback = lambda i: Qt.QMetaObject.invokeMethod(self._var_bw_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._var_bw_options.index(i)))
        self._var_bw_callback(self.var_bw)
        self._var_bw_combo_box.currentIndexChanged.connect(
            lambda i: self.set_var_bw(self._var_bw_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._var_bw_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._tx_gain_range = Range(0, 47, 1, 47, 200)
        self._tx_gain_win = RangeWidget(self._tx_gain_range, self.set_tx_gain, 'TX GAIN', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tx_gain_win, 5, 3, 1, 1)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        _ssb_txing_btn_push_button = Qt.QPushButton('')
        _ssb_txing_btn_push_button = Qt.QPushButton('ssb_txing_btn')
        self._ssb_txing_btn_choices = {'Pressed': 1, 'Released': 0}
        _ssb_txing_btn_push_button.pressed.connect(lambda: self.set_ssb_txing_btn(self._ssb_txing_btn_choices['Pressed']))
        _ssb_txing_btn_push_button.released.connect(lambda: self.set_ssb_txing_btn(self._ssb_txing_btn_choices['Released']))
        self.top_layout.addWidget(_ssb_txing_btn_push_button)
        self._sq_range = Range(-110, 0, 1, -110, 200)
        self._sq_win = RangeWidget(self._sq_range, self.set_sq, 'SQUELCH', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._sq_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._side_band_options = [0, 1, 2, 3]
        # Create the labels list
        self._side_band_labels = ['USB', 'LSB', 'CW', 'CW Stereo']
        # Create the combo box
        self._side_band_tool_bar = Qt.QToolBar(self)
        self._side_band_tool_bar.addWidget(Qt.QLabel('MODE' + ": "))
        self._side_band_combo_box = Qt.QComboBox()
        self._side_band_tool_bar.addWidget(self._side_band_combo_box)
        for _label in self._side_band_labels: self._side_band_combo_box.addItem(_label)
        self._side_band_callback = lambda i: Qt.QMetaObject.invokeMethod(self._side_band_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._side_band_options.index(i)))
        self._side_band_callback(self.side_band)
        self._side_band_combo_box.currentIndexChanged.connect(
            lambda i: self.set_side_band(self._side_band_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._side_band_tool_bar, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._rx_preamp_options = [0, 1]
        # Create the labels list
        self._rx_preamp_labels = ['OFF', 'ON']
        # Create the combo box
        # Create the radio buttons
        self._rx_preamp_group_box = Qt.QGroupBox('RX Preamp' + ": ")
        self._rx_preamp_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._rx_preamp_button_group = variable_chooser_button_group()
        self._rx_preamp_group_box.setLayout(self._rx_preamp_box)
        for i, _label in enumerate(self._rx_preamp_labels):
            radio_button = Qt.QRadioButton(_label)
            self._rx_preamp_box.addWidget(radio_button)
            self._rx_preamp_button_group.addButton(radio_button, i)
        self._rx_preamp_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_preamp_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._rx_preamp_options.index(i)))
        self._rx_preamp_callback(self.rx_preamp)
        self._rx_preamp_button_group.buttonClicked[int].connect(
            lambda i: self.set_rx_preamp(self._rx_preamp_options[i]))
        self.top_grid_layout.addWidget(self._rx_preamp_group_box, 4, 0, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._morse_speed_range = Range(40, 200, 1, 100, 200)
        self._morse_speed_win = RangeWidget(self._morse_speed_range, self.set_morse_speed, 'morse_speed', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._morse_speed_win, 9, 3, 1, 1)
        for r in range(9, 10):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._monitor_options = [0, 1]
        # Create the labels list
        self._monitor_labels = ['Monitor', 'RX/TX']
        # Create the combo box
        # Create the radio buttons
        self._monitor_group_box = Qt.QGroupBox('TRANSMIT SOUND' + ": ")
        self._monitor_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._monitor_button_group = variable_chooser_button_group()
        self._monitor_group_box.setLayout(self._monitor_box)
        for i, _label in enumerate(self._monitor_labels):
            radio_button = Qt.QRadioButton(_label)
            self._monitor_box.addWidget(radio_button)
            self._monitor_button_group.addButton(radio_button, i)
        self._monitor_callback = lambda i: Qt.QMetaObject.invokeMethod(self._monitor_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._monitor_options.index(i)))
        self._monitor_callback(self.monitor)
        self._monitor_button_group.buttonClicked[int].connect(
            lambda i: self.set_monitor(self._monitor_options[i]))
        self.top_grid_layout.addWidget(self._monitor_group_box, 3, 3, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._mic_gain_range = Range(0, 1.5, 0.1, 1.4, 200)
        self._mic_gain_win = RangeWidget(self._mic_gain_range, self.set_mic_gain, 'MIC GAIN', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._mic_gain_win, 7, 3, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._lna_gain_range = Range(0, 39, 1, 39, 200)
        self._lna_gain_win = RangeWidget(self._lna_gain_range, self.set_lna_gain, 'LNA GAIN', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._lna_gain_win, 4, 1, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._cw_level_range = Range(0, 0.95, 0.01, 0.8, 200)
        self._cw_level_win = RangeWidget(self._cw_level_range, self.set_cw_level, 'CW level', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._cw_level_win, 11, 3, 1, 1)
        for r in range(11, 12):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        # Create the options list
        self._band_chooser_options = [0, 1, 2, 3, 9, 4, 5, 6, 7, 8]
        # Create the labels list
        self._band_chooser_labels = ['50', '50 Fyr', '144', '144 Fyr', '144 FT8', '432', '432 Fyr', '1296', '1296 fyr', 'preset']
        # Create the combo box
        # Create the radio buttons
        self._band_chooser_group_box = Qt.QGroupBox('FREQUENCY BAND' + ": ")
        self._band_chooser_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._band_chooser_button_group = variable_chooser_button_group()
        self._band_chooser_group_box.setLayout(self._band_chooser_box)
        for i, _label in enumerate(self._band_chooser_labels):
            radio_button = Qt.QRadioButton(_label)
            self._band_chooser_box.addWidget(radio_button)
            self._band_chooser_button_group.addButton(radio_button, i)
        self._band_chooser_callback = lambda i: Qt.QMetaObject.invokeMethod(self._band_chooser_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._band_chooser_options.index(i)))
        self._band_chooser_callback(self.band_chooser)
        self._band_chooser_button_group.buttonClicked[int].connect(
            lambda i: self.set_band_chooser(self._band_chooser_options[i]))
        self.top_grid_layout.addWidget(self._band_chooser_group_box, 0, 2, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._af_right_range = Range(0, 1, 0.01, 0.5, 200)
        self._af_right_win = RangeWidget(self._af_right_range, self.set_af_right, 'AF BAL', "slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._af_right_win, 7, 1, 1, 1)
        for r in range(7, 8):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._af_gain_range = Range(0, 2000, 1, 6, 200)
        self._af_gain_win = RangeWidget(self._af_gain_range, self.set_af_gain, '  AF VOL', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._af_gain_win, 3, 1, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_static_text_1_0_tool_bar = Qt.QToolBar(self)
        self._variable_static_text_1_0_tool_bar.addWidget(Qt.QLabel('                                          RECEIVE FQ' + ": "))
        self._variable_static_text_1_0_line_edit = Qt.QLineEdit(str(self.variable_static_text_1_0))
        self._variable_static_text_1_0_tool_bar.addWidget(self._variable_static_text_1_0_line_edit)
        self._variable_static_text_1_0_line_edit.returnPressed.connect(
            lambda: self.set_variable_static_text_1_0(str(str(self._variable_static_text_1_0_line_edit.text()))))
        self.top_grid_layout.addWidget(self._variable_static_text_1_0_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_static_text_1_tool_bar = Qt.QToolBar(self)
        self._variable_static_text_1_tool_bar.addWidget(Qt.QLabel('                                          TRANSMIT FQ' + ": "))
        self._variable_static_text_1_line_edit = Qt.QLineEdit(str(self.variable_static_text_1))
        self._variable_static_text_1_tool_bar.addWidget(self._variable_static_text_1_line_edit)
        self._variable_static_text_1_line_edit.returnPressed.connect(
            lambda: self.set_variable_static_text_1(str(str(self._variable_static_text_1_line_edit.text()))))
        self.top_grid_layout.addWidget(self._variable_static_text_1_tool_bar, 0, 3, 1, 1)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_static_text_0_tool_bar = Qt.QToolBar(self)
        self._variable_static_text_0_tool_bar.addWidget(Qt.QLabel("                                         S-METER (dBm)" + ": "))
        self._variable_static_text_0_line_edit = Qt.QLineEdit(str(self.variable_static_text_0))
        self._variable_static_text_0_tool_bar.addWidget(self._variable_static_text_0_line_edit)
        self._variable_static_text_0_line_edit.returnPressed.connect(
            lambda: self.set_variable_static_text_0(str(str(self._variable_static_text_0_line_edit.text()))))
        self.top_grid_layout.addWidget(self._variable_static_text_0_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._variable_qtgui_entry_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_entry_0_tool_bar.addWidget(Qt.QLabel('RX filter offset' + ": "))
        self._variable_qtgui_entry_0_line_edit = Qt.QLineEdit(str(self.variable_qtgui_entry_0))
        self._variable_qtgui_entry_0_tool_bar.addWidget(self._variable_qtgui_entry_0_line_edit)
        self._variable_qtgui_entry_0_line_edit.returnPressed.connect(
            lambda: self.set_variable_qtgui_entry_0(str(str(self._variable_qtgui_entry_0_line_edit.text()))))
        self.top_grid_layout.addWidget(self._variable_qtgui_entry_0_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        def _variable_function_probe_0_probe():
          while True:

            val = self.blocks_probe_signal_x_0.level()
            try:
              try:
                self.doc.add_next_tick_callback(functools.partial(self.set_variable_function_probe_0,val))
              except AttributeError:
                self.set_variable_function_probe_0(val)
            except AttributeError:
              pass
            time.sleep(1.0 / (35))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()
        self._tune_range = Range(-band_width[band_chooser]/2, band_width[band_chooser]/2, band_width[band_chooser]/200, 0, 200)
        self._tune_win = RangeWidget(self._tune_range, self.set_tune, '  TUNE', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._tune_win, 1, 2, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, 'driver=remote,remote=tcp://192.168.1.125:1234,remote:type=hackrf',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, rx_samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, rx_center_freq+45)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', rx_preamp)
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(lna_gain, 0.0), 40.0))
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(vga_gain, 0.0), 62.0))
        self.soapy_hackrf_sink_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_sink_0 = soapy.sink(dev, "fc32", 1, 'driver=remote,remote=tcp://192.168.1.125:1234,remote:type=hackrf',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_sink_0.set_sample_rate(0, tx_samp_rate)
        self.soapy_hackrf_sink_0.set_bandwidth(0, 0)
        self.soapy_hackrf_sink_0.set_frequency(0, tx_center_fq+45+4000)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', True)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(tx_gain, 0.0), 47.0))
        self.root_raised_cosine_filter_0_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                cw_level,
                cw_samp_rate,
                symbol_rate,
                0.35,
                200))
        self.root_raised_cosine_filter_0 = filter.fir_filter_fff(
            1,
            firdes.root_raised_cosine(
                1,
                cw_samp_rate,
                symbol_rate,
                0.35,
                200))
        self._rit_range = Range(-1000, 1000, 1, 0, 200)
        self._rit_win = RangeWidget(self._rit_range, self.set_rit, 'RIT', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._rit_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rational_resampler_xxx_4_0 = filter.rational_resampler_ccc(
                interpolation=int(2*tx_samp_rate/audio_samp_rate),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccc(
                interpolation=48,
                decimation=50,
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=48,
                decimation=50,
                taps=[],
                fractional_bw=0.4)
        self.qtgui_waterfall_sink_x_0 = qtgui.waterfall_sink_c(
            1024, #size
            window.WIN_HANN, #wintype
            fft_corr[side_band], #fc
            band_width[band_chooser], #bw
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_waterfall_sink_x_0.set_update_time(0.10)
        self.qtgui_waterfall_sink_x_0.enable_grid(True)
        self.qtgui_waterfall_sink_x_0.enable_axis_labels(True)



        labels = ['Line 1 label', '', '', '', '',
                  '', '', '', '', '']
        colors = [0, 0, 0, 0, 0,
                  0, 0, 0, 0, 0]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_waterfall_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_waterfall_sink_x_0.set_color_map(i, colors[i])
            self.qtgui_waterfall_sink_x_0.set_line_alpha(i, alphas[i])

        self.qtgui_waterfall_sink_x_0.set_intensity_range(-100, 10)

        self._qtgui_waterfall_sink_x_0_win = sip.wrapinstance(self.qtgui_waterfall_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_waterfall_sink_x_0_win, 5, 1, 1, 2)
        for r in range(5, 6):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0_0 = self._qtgui_ledindicator_0_0_win = qtgui.GrLEDIndicator('ON AIR SSB', "red", "black", ssb_txing, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0_0 = self._qtgui_ledindicator_0_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_0_win, 8, 1, 1, 1)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win = qtgui.GrLEDIndicator('ON AIR CW', "red", "black", cw_txing, 40, 1, 1, 1, self)
        self.qtgui_ledindicator_0 = self._qtgui_ledindicator_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_win, 8, 0, 1, 1)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', '', False, True, '', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.pyqwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_edit_box_msg_0_win, 8, 2, 1, 2)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._pwr_options = [0, 1, 2]
        # Create the labels list
        self._pwr_labels = ['0', '1', '2']
        # Create the combo box
        self._pwr_tool_bar = Qt.QToolBar(self)
        self._pwr_tool_bar.addWidget(Qt.QLabel('Transmit Power' + ": "))
        self._pwr_combo_box = Qt.QComboBox()
        self._pwr_tool_bar.addWidget(self._pwr_combo_box)
        for _label in self._pwr_labels: self._pwr_combo_box.addItem(_label)
        self._pwr_callback = lambda i: Qt.QMetaObject.invokeMethod(self._pwr_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._pwr_options.index(i)))
        self._pwr_callback(self.pwr)
        self._pwr_combo_box.currentIndexChanged.connect(
            lambda i: self.set_pwr(self._pwr_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._pwr_tool_bar, 4, 3, 1, 1)
        for r in range(4, 5):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.pfb_decimator_ccf_0_1 = pfb.decimator_ccf(
             3*int(rx_samp_rate/1000000),
            firdes.low_pass(.028,rx_samp_rate/32,5000,100),
            0,
            100,
            True,
            True)
        self.pfb_decimator_ccf_0_1.declare_sample_delay(0)
        self.pfb_decimator_ccf_0_0_0 = pfb.decimator_ccf(
            int(rx_samp_rate/100000),
            firdes.low_pass(1,rx_samp_rate/2, 3900,100),
            0,
            60,
            True,
            True)
        self.pfb_decimator_ccf_0_0_0.declare_sample_delay(0)
        self.pfb_decimator_ccf_0_0 = pfb.decimator_ccf(
            int(rx_samp_rate/100000),
            firdes.low_pass(1,rx_samp_rate/2, 3900,100),
            0,
            60,
            True,
            True)
        self.pfb_decimator_ccf_0_0.declare_sample_delay(0)
        self.mulc_usb_0 = blocks.multiply_const_ff(-1)
        self.mulc_usb1 = blocks.multiply_const_ff(-1)
        self.mulc_lsb_0 = blocks.multiply_const_ff(1)
        self.mulc_lsb1 = blocks.multiply_const_ff(1)
        self.mmse_resampler_xx_0 = filter.mmse_resampler_ff(0, audio_samp_rate/cw_samp_rate)
        self.low_pass_filter_0_0 = filter.fir_filter_fff(
            2,
            firdes.low_pass(
                1,
                audio_samp_rate,
                ssb_tx_bandwidth,
                50,
                window.WIN_HAMMING,
                6.76))
        self.low_pass_filter_0 = filter.fir_filter_fff(
            2,
            firdes.low_pass(
                1,
                audio_samp_rate,
                ssb_tx_bandwidth,
                50,
                window.WIN_HAMMING,
                6.76))
        self.freq_xlating_fft_filter_ccc_1_0 = filter.freq_xlating_fft_filter_ccc(1, firdes.low_pass(1,rx_samp_rate,rx_samp_rate/(2*1),4000), filter_freq-cw_midear_beat[side_band], rx_samp_rate)
        self.freq_xlating_fft_filter_ccc_1_0.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_1_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_1 = filter.freq_xlating_fft_filter_ccc(1, firdes.low_pass(1,rx_samp_rate,rx_samp_rate/(2*1),4000), filter_freq+cw_midear_beat[side_band], rx_samp_rate)
        self.freq_xlating_fft_filter_ccc_1.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_1.declare_sample_delay(0)
        self._fine_tune_range = Range(-3000, 3000, 1, 0, 200)
        self._fine_tune_win = RangeWidget(self._fine_tune_range, self.set_fine_tune, '  FINE TUNE', "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._fine_tune_win, 2, 2, 1, 2)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.epy_block_1_0 = epy_block_1_0.blk(threshold=2, attack=10, delay=0.5)
        self.epy_block_1 = epy_block_1.blk(threshold=0.8, attack=10, delay=6/morse_speed * 25)
        self.epy_block_0_0 = epy_block_0_0.mc_sync_block()
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_selector_3 = blocks.selector(gr.sizeof_float*1,int(cw_txing),0)
        self.blocks_selector_3.set_enabled(True)
        self.blocks_selector_2 = blocks.selector(gr.sizeof_float*1,int(cw_txing),0)
        self.blocks_selector_2.set_enabled(True)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_gr_complex*1,side_band,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0_y = blocks.selector(gr.sizeof_float*1,side_band,0)
        self.blocks_selector_0_y.set_enabled(True)
        self.blocks_selector_0_y.set_max_output_buffer(2)
        self.blocks_selector_0_x = blocks.selector(gr.sizeof_float*1,side_band,0)
        self.blocks_selector_0_x.set_enabled(True)
        self.blocks_selector_0_x.set_max_output_buffer(2)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,(ssb_txing or ssb_txing_btn))
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_gr_complex*1, int(tx_samp_rate/cw_samp_rate))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, 3000)
        self.blocks_null_sink_3 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10.6, 1, RX_power_offset_dB)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_const_vxx_4_0_0_0 = blocks.multiply_const_cc(wf_gain)
        self.blocks_multiply_const_vxx_4_0_0 = blocks.multiply_const_cc(usb_chain_gain[side_band])
        self.blocks_multiply_const_vxx_4_0 = blocks.multiply_const_cc(lsb_chain_gain[side_band])
        self.blocks_multiply_const_vxx_3_0 = blocks.multiply_const_ff(af_gain *af_right)
        self.blocks_multiply_const_vxx_3 = blocks.multiply_const_ff(af_gain*(1-af_right))
        self.blocks_multiply_const_vxx_1_0_1 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_1_0_0_1 = blocks.multiply_const_ff(vox_gain)
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_ff(mic_gain)
        self.blocks_multiply_const_vxx_1 = blocks.multiply_const_ff(1)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(monitor)
        self.blocks_msgpair_to_var_0_0 = blocks.msg_pair_to_var(self.set_ssb_txing)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_cw_txing)
        self.blocks_moving_average_xx_0 = blocks.moving_average_ff(1000, 1/10, 480, 1)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_integrate_xx_1 = blocks.integrate_ff(50, 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(50000*5, 1)
        self.blocks_float_to_complex_0_3 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_float*1, 20)
        self.blocks_complex_to_real_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_float_0_2_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_2_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_2 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_1_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.band_pass_filter_0_1 = filter.fir_filter_ccc(
            2,
            firdes.complex_band_pass(
                1,
                100000,
                (bpf_low[var_bw]),
                (bpf_high[var_bw]),
                100,
                window.WIN_BLACKMAN,
                6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(
            2,
            firdes.complex_band_pass(
                1,
                100000,
                (bpf_low[var_bw]),
                (bpf_high[var_bw]),
                100,
                window.WIN_BLACKMAN,
                6.76))
        self.band_pass_filter_0 = filter.fir_filter_fff(
            1,
            firdes.band_pass(
                1,
                audio_samp_rate,
                200,
                2700,
                100,
                window.WIN_HAMMING,
                6.76))
        self.audio_source_0 = audio.source(audio_samp_rate, "BlackHole 16ch", True)
        self.audio_sink_0 = audio.sink(audio_samp_rate, "WSJT-3", True)
        self.analog_simple_squelch_cc_0_0 = analog.simple_squelch_cc(sq, .001)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sq, .001)
        self.analog_sig_source_x_1_0 = analog.sig_source_f(audio_samp_rate, analog.GR_COS_WAVE, ssb_tx_bandwidth, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(audio_samp_rate, analog.GR_SIN_WAVE, ssb_tx_bandwidth, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(48e3, analog.GR_COS_WAVE, cw_midear_beat[side_band], 1, 0, 0)
        self.analog_agc3_xx_0_0 = analog.agc3_cc((1e-1), 1e-7, (.001)*0+.002, .1, 1)
        self.analog_agc3_xx_0_0.set_max_gain(.1)
        self.analog_agc3_xx_0 = analog.agc3_cc((1e-1), 1e-7, (.001)*0+.002, .1, 1)
        self.analog_agc3_xx_0.set_max_gain(.1)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'clear_input'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.epy_block_1, 'onair'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_1, 'onair'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_1_0, 'onair'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_1_0, 'onair'), (self.blocks_msgpair_to_var_0_0, 'inpair'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.epy_block_0_0, 'msg_in'))
        self.connect((self.analog_agc3_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_agc3_xx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0_0, 0), (self.analog_agc3_xx_0_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_1_0_0_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_1_0_0_1, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_xx_0_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_xx_0_0_0, 1))
        self.connect((self.band_pass_filter_0_0, 0), (self.blocks_complex_to_float_0_1_0, 0))
        self.connect((self.band_pass_filter_0_1, 0), (self.blocks_complex_to_float_0_2_0_0, 0))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.blocks_complex_to_float_0_1_0, 0), (self.blocks_float_to_complex_0_0_0, 1))
        self.connect((self.blocks_complex_to_float_0_1_0, 1), (self.mulc_lsb1, 0))
        self.connect((self.blocks_complex_to_float_0_2, 0), (self.blocks_float_to_complex_0_1, 1))
        self.connect((self.blocks_complex_to_float_0_2, 1), (self.mulc_lsb_0, 0))
        self.connect((self.blocks_complex_to_float_0_2_0, 0), (self.blocks_float_to_complex_0_1_0, 1))
        self.connect((self.blocks_complex_to_float_0_2_0, 1), (self.mulc_usb_0, 0))
        self.connect((self.blocks_complex_to_float_0_2_0_0, 0), (self.blocks_float_to_complex_0_1_0_0, 1))
        self.connect((self.blocks_complex_to_float_0_2_0_0, 1), (self.mulc_usb1, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.blocks_integrate_xx_0, 0))
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_1, 0))
        self.connect((self.blocks_complex_to_real_0_0_0, 0), (self.blocks_multiply_const_vxx_1_0_1, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_float_to_complex_0_3, 0))
        self.connect((self.blocks_delay_0, 0), (self.mmse_resampler_xx_0, 0))
        self.connect((self.blocks_float_to_char_0, 0), (self.epy_block_1, 0))
        self.connect((self.blocks_float_to_complex_0_0_0, 0), (self.analog_simple_squelch_cc_0, 0))
        self.connect((self.blocks_float_to_complex_0_0_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_float_to_complex_0_0_1, 0), (self.blocks_selector_0, 0))
        self.connect((self.blocks_float_to_complex_0_1, 0), (self.band_pass_filter_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_1_0, 0), (self.band_pass_filter_0_1, 0))
        self.connect((self.blocks_float_to_complex_0_1_0_0, 0), (self.analog_simple_squelch_cc_0_0, 0))
        self.connect((self.blocks_float_to_complex_0_1_0_0, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_float_to_complex_0_3, 0), (self.blocks_repeat_0_0, 0))
        self.connect((self.blocks_integrate_xx_0, 0), (self.blocks_nlog10_ff_0, 0))
        self.connect((self.blocks_integrate_xx_1, 0), (self.blocks_float_to_char_0, 0))
        self.connect((self.blocks_moving_average_xx_0, 0), (self.epy_block_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_selector_2, 1))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_selector_3, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_selector_0_x, 1))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_selector_0_x, 3))
        self.connect((self.blocks_multiply_const_vxx_1, 0), (self.blocks_selector_0_y, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_1, 0), (self.blocks_moving_average_xx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_selector_0_x, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_selector_0_x, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_selector_0_y, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_selector_0_y, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_1, 0), (self.blocks_selector_0_y, 3))
        self.connect((self.blocks_multiply_const_vxx_3, 0), (self.audio_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_3_0, 0), (self.audio_sink_0, 1))
        self.connect((self.blocks_multiply_const_vxx_4_0, 0), (self.blocks_complex_to_float_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_4_0_0, 0), (self.blocks_complex_to_float_0_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_4_0_0_0, 0), (self.pfb_decimator_ccf_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_4_0_0_0, 0), (self.qtgui_waterfall_sink_x_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.low_pass_filter_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.low_pass_filter_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_selector_1, 2))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_selector_1, 3))
        self.connect((self.blocks_selector_0, 0), (self.blocks_null_sink_2, 0))
        self.connect((self.blocks_selector_0, 1), (self.rational_resampler_xxx_4_0, 0))
        self.connect((self.blocks_selector_0_x, 0), (self.blocks_selector_2, 0))
        self.connect((self.blocks_selector_0_y, 0), (self.blocks_selector_3, 0))
        self.connect((self.blocks_selector_1, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.blocks_selector_2, 0), (self.blocks_multiply_const_vxx_3_0, 0))
        self.connect((self.blocks_selector_3, 0), (self.blocks_multiply_const_vxx_3, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_1, 0), (self.pfb_decimator_ccf_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_1_0, 0), (self.blocks_multiply_const_vxx_4_0_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_1_0, 0), (self.pfb_decimator_ccf_0_0_0, 0))
        self.connect((self.low_pass_filter_0, 0), (self.blocks_float_to_complex_0_0_1, 1))
        self.connect((self.low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0_0_1, 0))
        self.connect((self.mmse_resampler_xx_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.mulc_lsb1, 0), (self.blocks_float_to_complex_0_0_0, 0))
        self.connect((self.mulc_lsb_0, 0), (self.blocks_float_to_complex_0_1, 0))
        self.connect((self.mulc_usb1, 0), (self.blocks_float_to_complex_0_1_0_0, 0))
        self.connect((self.mulc_usb_0, 0), (self.blocks_float_to_complex_0_1_0, 0))
        self.connect((self.pfb_decimator_ccf_0_0, 0), (self.blocks_multiply_const_vxx_4_0, 0))
        self.connect((self.pfb_decimator_ccf_0_0_0, 0), (self.blocks_multiply_const_vxx_4_0_0, 0))
        self.connect((self.pfb_decimator_ccf_0_1, 0), (self.blocks_null_sink_3, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_complex_to_real_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_4_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.rational_resampler_xxx_4_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_integrate_xx_1, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.freq_xlating_fft_filter_ccc_1, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.freq_xlating_fft_filter_ccc_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FBQ_xcvr")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_preset_fq(self):
        return self.preset_fq

    def set_preset_fq(self, preset_fq):
        self.preset_fq = preset_fq
        self.set_band_center((50.2e6, 50.45e6, 144.200e6,144.450e6, 432.2e6,432.45e6, 1296.4e6, 1296.850e6, self.preset_fq,144.174e6))

    def get_band_chooser(self):
        return self.band_chooser

    def set_band_chooser(self, band_chooser):
        self.band_chooser = band_chooser
        self._band_chooser_callback(self.band_chooser)
        self.set_f0(self.band_center[self.band_chooser])
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.fft_corr[self.side_band], self.band_width[self.band_chooser])

    def get_band_center(self):
        return self.band_center

    def set_band_center(self, band_center):
        self.band_center = band_center
        self.set_f0(self.band_center[self.band_chooser])

    def get_tune(self):
        return self.tune

    def set_tune(self, tune):
        self.tune = tune
        self.set_filter_freq(100e3+self.rit + self.tune + self.fine_tune)
        self.set_tx_center_fq((self.f0 + self.tune + self.fine_tune))

    def get_rit(self):
        return self.rit

    def set_rit(self, rit):
        self.rit = rit
        self.set_filter_freq(100e3+self.rit + self.tune + self.fine_tune)

    def get_fine_tune(self):
        return self.fine_tune

    def set_fine_tune(self, fine_tune):
        self.fine_tune = fine_tune
        self.set_filter_freq(100e3+self.rit + self.tune + self.fine_tune)
        self.set_tx_center_fq((self.f0 + self.tune + self.fine_tune))

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.set_rx_center_freq(self.f0-100e3)
        self.set_tx_center_fq((self.f0 + self.tune + self.fine_tune))

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0
        self.set_variable_static_text_0(('{:.1f}'.format(self.variable_function_probe_0)))

    def get_tx_center_fq(self):
        return self.tx_center_fq

    def set_tx_center_fq(self, tx_center_fq):
        self.tx_center_fq = tx_center_fq
        self.set_variable_static_text_1('{:.0f}'.format(self.tx_center_fq))
        self.soapy_hackrf_sink_0.set_frequency(0, self.tx_center_fq+45+4000)

    def get_ssb_txing(self):
        return self.ssb_txing

    def set_ssb_txing(self, ssb_txing):
        self.ssb_txing = ssb_txing
        self.set_txing(self.cw_txing or self.ssb_txing)
        self.blocks_selector_0.set_output_index((self.ssb_txing or self.ssb_txing_btn))
        self.qtgui_ledindicator_0_0.setState(self.ssb_txing)

    def get_rx_center_freq(self):
        return self.rx_center_freq

    def set_rx_center_freq(self, rx_center_freq):
        self.rx_center_freq = rx_center_freq
        self.set_variable_static_text_1_0('{:.0f}'.format(self.rx_center_freq+self.filter_freq))
        self.soapy_hackrf_source_0.set_frequency(0, self.rx_center_freq+45)

    def get_filter_freq(self):
        return self.filter_freq

    def set_filter_freq(self, filter_freq):
        self.filter_freq = filter_freq
        self.set_variable_qtgui_entry_0('{:.0f}'.format(self.filter_freq))
        self.set_variable_static_text_1_0('{:.0f}'.format(self.rx_center_freq+self.filter_freq))
        self.freq_xlating_fft_filter_ccc_1.set_center_freq(self.filter_freq+self.cw_midear_beat[self.side_band])
        self.freq_xlating_fft_filter_ccc_1_0.set_center_freq(self.filter_freq-self.cw_midear_beat[self.side_band])

    def get_cw_txing(self):
        return self.cw_txing

    def set_cw_txing(self, cw_txing):
        self.cw_txing = cw_txing
        self.set_txing(self.cw_txing or self.ssb_txing)
        self.blocks_selector_2.set_input_index(int(self.cw_txing))
        self.blocks_selector_3.set_input_index(int(self.cw_txing))
        self.qtgui_ledindicator_0.setState(self.cw_txing)

    def get_wf_gain(self):
        return self.wf_gain

    def set_wf_gain(self, wf_gain):
        self.wf_gain = wf_gain
        self.blocks_multiply_const_vxx_4_0_0_0.set_k(self.wf_gain)

    def get_vox_gain(self):
        return self.vox_gain

    def set_vox_gain(self, vox_gain):
        self.vox_gain = vox_gain
        self.blocks_multiply_const_vxx_1_0_0_1.set_k(self.vox_gain)

    def get_vga_gain(self):
        return self.vga_gain

    def set_vga_gain(self, vga_gain):
        self.vga_gain = vga_gain
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(self.vga_gain, 0.0), 62.0))

    def get_variable_static_text_1_0(self):
        return self.variable_static_text_1_0

    def set_variable_static_text_1_0(self, variable_static_text_1_0):
        self.variable_static_text_1_0 = variable_static_text_1_0
        Qt.QMetaObject.invokeMethod(self._variable_static_text_1_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.variable_static_text_1_0)))

    def get_variable_static_text_1(self):
        return self.variable_static_text_1

    def set_variable_static_text_1(self, variable_static_text_1):
        self.variable_static_text_1 = variable_static_text_1
        Qt.QMetaObject.invokeMethod(self._variable_static_text_1_line_edit, "setText", Qt.Q_ARG("QString", str(self.variable_static_text_1)))

    def get_variable_static_text_0(self):
        return self.variable_static_text_0

    def set_variable_static_text_0(self, variable_static_text_0):
        self.variable_static_text_0 = variable_static_text_0
        Qt.QMetaObject.invokeMethod(self._variable_static_text_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.variable_static_text_0)))

    def get_variable_qtgui_entry_0(self):
        return self.variable_qtgui_entry_0

    def set_variable_qtgui_entry_0(self, variable_qtgui_entry_0):
        self.variable_qtgui_entry_0 = variable_qtgui_entry_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_entry_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_entry_0)))

    def get_var_bw(self):
        return self.var_bw

    def set_var_bw(self, var_bw):
        self.var_bw = var_bw
        self._var_bw_callback(self.var_bw)
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, 100000, (self.bpf_low[self.var_bw]), (self.bpf_high[self.var_bw]), 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, 100000, (self.bpf_low[self.var_bw]), (self.bpf_high[self.var_bw]), 100, window.WIN_BLACKMAN, 6.76))

    def get_usb_chain_gain(self):
        return self.usb_chain_gain

    def set_usb_chain_gain(self, usb_chain_gain):
        self.usb_chain_gain = usb_chain_gain
        self.blocks_multiply_const_vxx_4_0_0.set_k(self.usb_chain_gain[self.side_band])

    def get_txing(self):
        return self.txing

    def set_txing(self, txing):
        self.txing = txing

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.blocks_repeat_0_0.set_interpolation(int(self.tx_samp_rate/self.cw_samp_rate))
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.tx_samp_rate)

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(self.tx_gain, 0.0), 47.0))

    def get_symbol_rate(self):
        return self.symbol_rate

    def set_symbol_rate(self, symbol_rate):
        self.symbol_rate = symbol_rate
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.cw_samp_rate, self.symbol_rate, 0.35, 200))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(self.cw_level, self.cw_samp_rate, self.symbol_rate, 0.35, 200))

    def get_ssb_txing_btn(self):
        return self.ssb_txing_btn

    def set_ssb_txing_btn(self, ssb_txing_btn):
        self.ssb_txing_btn = ssb_txing_btn
        self.blocks_selector_0.set_output_index((self.ssb_txing or self.ssb_txing_btn))

    def get_ssb_tx_mode(self):
        return self.ssb_tx_mode

    def set_ssb_tx_mode(self, ssb_tx_mode):
        self.ssb_tx_mode = ssb_tx_mode

    def get_ssb_tx_bandwidth(self):
        return self.ssb_tx_bandwidth

    def set_ssb_tx_bandwidth(self, ssb_tx_bandwidth):
        self.ssb_tx_bandwidth = ssb_tx_bandwidth
        self.analog_sig_source_x_0_0.set_frequency(self.ssb_tx_bandwidth)
        self.analog_sig_source_x_1_0.set_frequency(self.ssb_tx_bandwidth)
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth, 50, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth, 50, window.WIN_HAMMING, 6.76))

    def get_sq(self):
        return self.sq

    def set_sq(self, sq):
        self.sq = sq
        self.analog_simple_squelch_cc_0.set_threshold(self.sq)
        self.analog_simple_squelch_cc_0_0.set_threshold(self.sq)

    def get_side_band(self):
        return self.side_band

    def set_side_band(self, side_band):
        self.side_band = side_band
        self._side_band_callback(self.side_band)
        self.analog_sig_source_x_0.set_frequency(self.cw_midear_beat[self.side_band])
        self.blocks_multiply_const_vxx_4_0.set_k(self.lsb_chain_gain[self.side_band])
        self.blocks_multiply_const_vxx_4_0_0.set_k(self.usb_chain_gain[self.side_band])
        self.blocks_selector_0_x.set_input_index(self.side_band)
        self.blocks_selector_0_y.set_input_index(self.side_band)
        self.blocks_selector_1.set_input_index(self.side_band)
        self.freq_xlating_fft_filter_ccc_1.set_center_freq(self.filter_freq+self.cw_midear_beat[self.side_band])
        self.freq_xlating_fft_filter_ccc_1_0.set_center_freq(self.filter_freq-self.cw_midear_beat[self.side_band])
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.fft_corr[self.side_band], self.band_width[self.band_chooser])

    def get_sb_t(self):
        return self.sb_t

    def set_sb_t(self, sb_t):
        self.sb_t = sb_t

    def get_sb_r(self):
        return self.sb_r

    def set_sb_r(self, sb_r):
        self.sb_r = sb_r

    def get_rx_samp_rate(self):
        return self.rx_samp_rate

    def set_rx_samp_rate(self, rx_samp_rate):
        self.rx_samp_rate = rx_samp_rate
        self.freq_xlating_fft_filter_ccc_1.set_taps(firdes.low_pass(1,self.rx_samp_rate,self.rx_samp_rate/(2*1),4000))
        self.freq_xlating_fft_filter_ccc_1_0.set_taps(firdes.low_pass(1,self.rx_samp_rate,self.rx_samp_rate/(2*1),4000))
        self.pfb_decimator_ccf_0_0.set_taps(firdes.low_pass(1,self.rx_samp_rate/2, 3900,100))
        self.pfb_decimator_ccf_0_0_0.set_taps(firdes.low_pass(1,self.rx_samp_rate/2, 3900,100))
        self.pfb_decimator_ccf_0_1.set_taps(firdes.low_pass(.028,self.rx_samp_rate/32,5000,100))
        self.soapy_hackrf_source_0.set_sample_rate(0, self.rx_samp_rate)

    def get_rx_preamp(self):
        return self.rx_preamp

    def set_rx_preamp(self, rx_preamp):
        self.rx_preamp = rx_preamp
        self._rx_preamp_callback(self.rx_preamp)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', self.rx_preamp)

    def get_rx_corr(self):
        return self.rx_corr

    def set_rx_corr(self, rx_corr):
        self.rx_corr = rx_corr

    def get_pwr(self):
        return self.pwr

    def set_pwr(self, pwr):
        self.pwr = pwr
        self._pwr_callback(self.pwr)

    def get_morse_speed(self):
        return self.morse_speed

    def set_morse_speed(self, morse_speed):
        self.morse_speed = morse_speed
        self.epy_block_1.delay = 6/self.morse_speed * 25

    def get_monitor(self):
        return self.monitor

    def set_monitor(self, monitor):
        self.monitor = monitor
        self._monitor_callback(self.monitor)
        self.blocks_multiply_const_vxx_0.set_k(self.monitor)

    def get_mic_gain(self):
        return self.mic_gain

    def set_mic_gain(self, mic_gain):
        self.mic_gain = mic_gain
        self.blocks_multiply_const_vxx_1_0_0_0.set_k(self.mic_gain)

    def get_lsb_chain_gain(self):
        return self.lsb_chain_gain

    def set_lsb_chain_gain(self, lsb_chain_gain):
        self.lsb_chain_gain = lsb_chain_gain
        self.blocks_multiply_const_vxx_4_0.set_k(self.lsb_chain_gain[self.side_band])

    def get_lna_gain(self):
        return self.lna_gain

    def set_lna_gain(self, lna_gain):
        self.lna_gain = lna_gain
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(self.lna_gain, 0.0), 40.0))

    def get_fft_corr(self):
        return self.fft_corr

    def set_fft_corr(self, fft_corr):
        self.fft_corr = fft_corr
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.fft_corr[self.side_band], self.band_width[self.band_chooser])

    def get_cw_samp_rate(self):
        return self.cw_samp_rate

    def set_cw_samp_rate(self, cw_samp_rate):
        self.cw_samp_rate = cw_samp_rate
        self.blocks_repeat_0_0.set_interpolation(int(self.tx_samp_rate/self.cw_samp_rate))
        self.mmse_resampler_xx_0.set_resamp_ratio(self.audio_samp_rate/self.cw_samp_rate)
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.cw_samp_rate, self.symbol_rate, 0.35, 200))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(self.cw_level, self.cw_samp_rate, self.symbol_rate, 0.35, 200))

    def get_cw_midear_beat(self):
        return self.cw_midear_beat

    def set_cw_midear_beat(self, cw_midear_beat):
        self.cw_midear_beat = cw_midear_beat
        self.analog_sig_source_x_0.set_frequency(self.cw_midear_beat[self.side_band])
        self.freq_xlating_fft_filter_ccc_1.set_center_freq(self.filter_freq+self.cw_midear_beat[self.side_band])
        self.freq_xlating_fft_filter_ccc_1_0.set_center_freq(self.filter_freq-self.cw_midear_beat[self.side_band])

    def get_cw_level(self):
        return self.cw_level

    def set_cw_level(self, cw_level):
        self.cw_level = cw_level
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(self.cw_level, self.cw_samp_rate, self.symbol_rate, 0.35, 200))

    def get_bpf_low(self):
        return self.bpf_low

    def set_bpf_low(self, bpf_low):
        self.bpf_low = bpf_low
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, 100000, (self.bpf_low[self.var_bw]), (self.bpf_high[self.var_bw]), 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, 100000, (self.bpf_low[self.var_bw]), (self.bpf_high[self.var_bw]), 100, window.WIN_BLACKMAN, 6.76))

    def get_bpf_high(self):
        return self.bpf_high

    def set_bpf_high(self, bpf_high):
        self.bpf_high = bpf_high
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, 100000, (self.bpf_low[self.var_bw]), (self.bpf_high[self.var_bw]), 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, 100000, (self.bpf_low[self.var_bw]), (self.bpf_high[self.var_bw]), 100, window.WIN_BLACKMAN, 6.76))

    def get_band_width(self):
        return self.band_width

    def set_band_width(self, band_width):
        self.band_width = band_width
        self.qtgui_waterfall_sink_x_0.set_frequency_range(self.fft_corr[self.side_band], self.band_width[self.band_chooser])

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_1_0.set_sampling_freq(self.audio_samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.audio_samp_rate, 200, 2700, 100, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth, 50, window.WIN_HAMMING, 6.76))
        self.low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth, 50, window.WIN_HAMMING, 6.76))
        self.mmse_resampler_xx_0.set_resamp_ratio(self.audio_samp_rate/self.cw_samp_rate)

    def get_af_right(self):
        return self.af_right

    def set_af_right(self, af_right):
        self.af_right = af_right
        self.blocks_multiply_const_vxx_3.set_k(self.af_gain*(1-self.af_right))
        self.blocks_multiply_const_vxx_3_0.set_k(self.af_gain *self.af_right)

    def get_af_gain(self):
        return self.af_gain

    def set_af_gain(self, af_gain):
        self.af_gain = af_gain
        self.blocks_multiply_const_vxx_3.set_k(self.af_gain*(1-self.af_right))
        self.blocks_multiply_const_vxx_3_0.set_k(self.af_gain *self.af_right)

    def get_RX_power_offset_dB(self):
        return self.RX_power_offset_dB

    def set_RX_power_offset_dB(self, RX_power_offset_dB):
        self.RX_power_offset_dB = RX_power_offset_dB



def argument_parser():
    description = 'VHF-UHF transceiver with CW and SSB'
    parser = ArgumentParser(description=description)
    return parser


def main(top_block_cls=FBQ_xcvr, options=None):
    if options is None:
        options = argument_parser().parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
