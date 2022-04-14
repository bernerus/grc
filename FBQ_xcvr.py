#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: SM6FBQ VHF transceiver
# Author: Christer Bernérus, SM6FBQ
# Copyright: This design is free to use under GPL2
# Description: VHF-UHF transceiver with CW and SSB
# GNU Radio version: 3.9.3.0

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
from gnuradio import zeromq
from gnuradio.filter import pfb
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import FBQ_xcvr_epy_block_0_0 as epy_block_0_0  # embedded python block
import FBQ_xcvr_epy_block_1 as epy_block_1  # embedded python block
import FBQ_xcvr_epy_block_1_0 as epy_block_1_0  # embedded python block
import FBQ_xcvr_epy_block_2 as epy_block_2  # embedded python block
import FBQ_xcvr_msg_formatter as msg_formatter  # embedded python block
import FBQ_xcvr_msg_formatter_0 as msg_formatter_0  # embedded python block
import FBQ_xcvr_msg_formatter_0_0 as msg_formatter_0_0  # embedded python block
import FBQ_xcvr_msg_formatter_0_0_0 as msg_formatter_0_0_0  # embedded python block
import FBQ_xcvr_msg_formatter_1 as msg_formatter_1  # embedded python block
import FBQ_xcvr_rx_distancer as rx_distancer  # embedded python block
import FBQ_xcvr_tx_fq_sync as tx_fq_sync  # embedded python block
import FBQ_xcvr_tx_fq_sync_0 as tx_fq_sync_0  # embedded python block
import os
import time
import threading


def snipfcn_after_start(self):
    self._band_selector_combo_box.removeItem(0)
    for _label in self._band_selector_labels: self._band_selector_combo_box.addItem(_label)
    self._band_selector_callback = lambda i: Qt.QMetaObject.invokeMethod(self._band_selector_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._band_selector_options.index(i)))
    self._band_selector_combo_box.currentIndexChanged.connect(
        lambda i: self.set_band_selector(self._band_selector_options[i])
    )


    self._band_selector_combo_box.setCurrentIndex(20)
    self.rx_distancer.desired_fq=self.ham_bands['432-FT8'][2]

def snipfcn_band_plan(self):
    self.ham_bands = {
        '50-CW':    (50000000,   50100000,   50090000,    500, ['CW']),
        '50-SSB':   (50100000,   50300000,   50150000,   2700, ['CW', 'USB','LSB']),
        '50-FT8':   (50300000,   50400000,   50313000,   2700, ['FT8','USB']),
        '50-PSK':   (50300000,   50400000,   50305000,   2700, ['PSK','USB']),
        '50-MSK':   (50300000,   50400000,   50350000,   2700, ['MSK','USB']),
        '50-B':     (50400000,   50500000,   50450000,   1000, ['None']),  # Beacons only
        '50-FM':    (50500000,   52000000,   51510000,  12000, ['FM', 'CW', 'SSB']),
        '87-FM':    (87500000,  108000000,   89300000, 200000, ['None']),  # FM broadcast
        '144-SAT':  (144000000, 144025000,  144010000,   2700, ['None']),  # Sat downlink,
        '144-CW':   (144025000, 144100000,  144050000,    500, ['CW']),
        '144-MGM':  (144100000, 144150000,  144116000,    500, ['CW', 'Q65', 'JT65'],'USB'),
        '144-Q65':  (144100000, 144150000,  144125000,    500, ['Q65','USB']),
        '144-JT65': (144100000, 144150000,  144120000,    500, ['JT65','USB']),
        '144-FT8':  (144150000, 144400000,  144174000,   2700, ['FT8','USB']),
        '144-SSB':  (144150000, 144400000,  144300000,   2700, ['USB', 'CW', 'FT8', 'JT65', 'Q65','LSB']),
        '144-MSK':  (144150000, 144400000,  144360000,   2700, ['MSK','USB']),
        '144-B':    (144400000, 144490000,  144406000,    500, ['None']),  # Beacons
        '144-PB':   (144491000, 144493000,  144492000,    500, ['CW', 'FT8']),  # Personal beacons
        '432-EME':  (432000000, 432025000,  432010000,    500, ['CW']),
        '432-CW':   (432025000, 432100000,  432050000,    500, ['CW','PSK']),
        '432-FT8':  (432150000, 432400000,  432174000,   2700, ['FT8','USB']),
        '432-SSB':  (432100000, 432400000,  432200000,   2700, ['CW', 'USB']),
        '432-FSK':  (432100000, 432400000,  432370000,   2700, ['CW', 'USB', 'FSK441','LSB']),
        '432-B':    (432400000, 432490000,  432412170,    500, ['None']), # Beacons 70cm / SK6UHF
        '1296-B':  (1296800000, 1296994000,1296811000,    500, ['None']), # Beacons 23cm



    }
    self.ham_bands_keys = list(self.ham_bands)
    self._band_selector_options = self.ham_bands_keys
    self._band_selector_labels = self.ham_bands_keys

    self._band_selector_combo_box.setMinimumContentsLength(10)

    def find_valid_mode(self, valid_modes):
    	available_modes = self.mode.labels
    	print(available_modes)
    	print(valid_modes)

    	for mode in valid_modes:
    		if mode in available_modes:
    			return available_modes.index(mode)
    	return 0


def snippets_main_after_init(tb):
    snipfcn_band_plan(tb)

def snippets_main_after_start(tb):
    snipfcn_after_start(tb)

from gnuradio import qtgui

class FBQ_xcvr(gr.top_block, Qt.QWidget):

    def __init__(self):
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
        # Variables
        ##################################################
        self.ham_bands = ham_bands = {'                  ':(30e6,6e9,0,0,['CW'])}
        self.band_selector = band_selector = '                  '
        self.mode_labels = mode_labels = {'None':0 , 'USB':1, 'LSB':2, 'CW': 3, 'CW Stereo':4, 'FT8':5, 'MSK144':6}
        self.current_allowed_modes = current_allowed_modes = ham_bands[band_selector][4]
        self.mode_default_option = mode_default_option = mode_labels[(list(set(mode_labels) & set(current_allowed_modes))[0])]
        self.mode_to_sb_rx = mode_to_sb_rx = [3,1,2,3,4,1,1]
        self.mode = mode = mode_default_option
        self.current_min_fq = current_min_fq = ham_bands[band_selector][0]
        self.current_max_fq = current_max_fq = ham_bands[band_selector][1]
        self.current_default_fq = current_default_fq = ham_bands[band_selector][2]
        self.tx_gain = tx_gain = 47
        self.tx_fq = tx_fq = 0
        self.tx_center_fq = tx_center_fq = current_default_fq
        self.tx_bw_opts = tx_bw_opts = 1
        self.tx_bw = tx_bw = [5000.0,3500.0,2500.0,1750.0,500.0]
        self.ssb_txing = ssb_txing = 0
        self.side_band_rx = side_band_rx = mode_to_sb_rx[mode]
        self.rx_samp_rate = rx_samp_rate = 4000000
        self.rx_hw_fq = rx_hw_fq = 0
        self.mode_to_sb_tx = mode_to_sb_tx = [0,1,2,3,4,1,1]
        self.mic_gain = mic_gain = 0.2
        self.mgm_input_gain = mgm_input_gain = 1.4
        self.freq = freq = 0
        self.filter_fq = filter_fq = 0
        self.f0 = f0 = current_min_fq + (current_max_fq - current_min_fq)/2.0
        self.cw_txing = cw_txing = 0
        self.wf_gain = wf_gain = 1
        self.wf_fq = wf_fq = freq+rx_hw_fq
        self.vox_threshold = vox_threshold = [10000,0.6,0.6,0.4,0.4,0.4,0.4]
        self.vox_sensitivity = vox_sensitivity = 20
        self.vox_delay = vox_delay = [0,1.5,1.5,0.7,0.7,0.5,0.5]
        self.vox_attack = vox_attack = [10000,10,10,1,1,1,1]
        self.vga_gain = vga_gain = 53
        self.variable_qtgui_entry_0 = variable_qtgui_entry_0 = side_band_rx
        self.variable_function_probe_0 = variable_function_probe_0 = 0
        self.usb_chain_gain = usb_chain_gain = 1,1,0,1,1,1,1
        self.txing = txing = cw_txing or ssb_txing
        self.tx_samp_rate = tx_samp_rate = 3000000
        self.tx_rprt = tx_rprt = ''
        self.tx_mode_offset = tx_mode_offset = [0, tx_bw[tx_bw_opts]/2, -tx_bw[tx_bw_opts]/2, 0, 0, tx_bw[tx_bw_opts]/2,tx_bw[tx_bw_opts]/2]
        self.tx_fq_win = tx_fq_win = tx_center_fq
        self.tx_fq_q = tx_fq_q = int(tx_fq)
        self.tc_vga = tc_vga = tx_gain
        self.symbol_rate = symbol_rate = 20
        self.ssb_txing_btn = ssb_txing_btn = 0
        self.ssb_tx_bandwidth = ssb_tx_bandwidth = tx_bw[tx_bw_opts]
        self.sq = sq = -110
        self.split_fq = split_fq = True
        self.spkr_gain = spkr_gain = 75
        self.side_band_tx = side_band_tx = mode_to_sb_tx[mode]
        self.side_band_dislay = side_band_dislay = side_band_rx
        self.sb_t = sb_t = [1,-1,1,1]
        self.sb_r = sb_r = [-1,1,1,-1]
        self.rx_preamp = rx_preamp = 0
        self.rx_fq_win = rx_fq_win = current_default_fq
        self.rx_fq = rx_fq = 0
        self.rx_ctr_fq_0 = rx_ctr_fq_0 = int(filter_fq)
        self.rx_ctr_fq = rx_ctr_fq = int(rx_hw_fq)
        self.rx_center_fq = rx_center_fq = f0-100e3
        self.rx_bw = rx_bw = 2

        self.morse_speed = morse_speed = 120
        self.monitor = monitor = 25
        self.mode_to_audio_input = mode_to_audio_input = [0,2,2,0,0,1,1]
        self.mode_options = mode_options = [0, 1, 2, 3, 4, 5]
        self.mode_labels_values = mode_labels_values = list(mode_labels.values())
        self.mode_labels_keys = mode_labels_keys = list(mode_labels.keys())
        self.mode_display = mode_display = mode
        self.mic_inpt_gain_0 = mic_inpt_gain_0 = mic_gain
        self.mgm_output_gain = mgm_output_gain = 75
        self.mgm_inpt_gain = mgm_inpt_gain = mgm_input_gain
        self.lsb_chain_gain = lsb_chain_gain = 0,0,1,0,1,0,0
        self.lna_gain = lna_gain = 39
        self.if_samp_rate = if_samp_rate = 1000e3
        self.if2_samp_rate = if2_samp_rate = 50000
        self.if0_samp_rate = if0_samp_rate = rx_samp_rate
        self.ham_bands_keys = ham_bands_keys = ['                  ']
        self.fq_calibration = fq_calibration = 64
        self.fft_corr = fft_corr = 0,0,0,880,0
        self.f0_min = f0_min = ham_bands[band_selector][0]
        self.dx_call = dx_call = ''
        self.cw_samp_rate = cw_samp_rate = 50e3
        self.cw_midear_beat = cw_midear_beat = 0,0,0,880,880,0,0
        self.cw_level = cw_level = 0.8
        self.current_allowed_tx_bandwidth = current_allowed_tx_bandwidth = ham_bands[band_selector][3]
        self.cq_flavor = cq_flavor = ''
        self.channel_separation = channel_separation = [100,100,10,10,1000,1000]
        self.bpf_low = bpf_low = 100,100,100,230,630,780, 855
        self.bpf_high = bpf_high = 4000,3300,2800,1530,1130,1080, 905
        self.audio_samp_rate = audio_samp_rate = 48000
        self.af_right = af_right = 0.5
        self.af_mix_matrices = af_mix_matrices = [((1,0),(1,0)),  ((1,0), (1,0)),   ((0,1),(0,1)),   ((1,0),(1,0)),  ((1,0),(0,1))]
        self.RX_power_offset_dB = RX_power_offset_dB = -104

        ##################################################
        # Blocks
        ##################################################
        self.settings_tab = Qt.QTabWidget()
        self.settings_tab_widget_0 = Qt.QWidget()
        self.settings_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.settings_tab_widget_0)
        self.settings_tab_grid_layout_0 = Qt.QGridLayout()
        self.settings_tab_layout_0.addLayout(self.settings_tab_grid_layout_0)
        self.settings_tab.addTab(self.settings_tab_widget_0, 'RX_settings')
        self.settings_tab_widget_1 = Qt.QWidget()
        self.settings_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.settings_tab_widget_1)
        self.settings_tab_grid_layout_1 = Qt.QGridLayout()
        self.settings_tab_layout_1.addLayout(self.settings_tab_grid_layout_1)
        self.settings_tab.addTab(self.settings_tab_widget_1, 'TX_settings')
        self.settings_tab_widget_2 = Qt.QWidget()
        self.settings_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.settings_tab_widget_2)
        self.settings_tab_grid_layout_2 = Qt.QGridLayout()
        self.settings_tab_layout_2.addLayout(self.settings_tab_grid_layout_2)
        self.settings_tab.addTab(self.settings_tab_widget_2, 'Debug')
        self.top_layout.addWidget(self.settings_tab)
        self.op_tab = Qt.QTabWidget()
        self.op_tab_widget_0 = Qt.QWidget()
        self.op_tab_layout_0 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.op_tab_widget_0)
        self.op_tab_grid_layout_0 = Qt.QGridLayout()
        self.op_tab_layout_0.addLayout(self.op_tab_grid_layout_0)
        self.op_tab.addTab(self.op_tab_widget_0, 'SSB')
        self.op_tab_widget_1 = Qt.QWidget()
        self.op_tab_layout_1 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.op_tab_widget_1)
        self.op_tab_grid_layout_1 = Qt.QGridLayout()
        self.op_tab_layout_1.addLayout(self.op_tab_grid_layout_1)
        self.op_tab.addTab(self.op_tab_widget_1, 'MGM')
        self.op_tab_widget_2 = Qt.QWidget()
        self.op_tab_layout_2 = Qt.QBoxLayout(Qt.QBoxLayout.TopToBottom, self.op_tab_widget_2)
        self.op_tab_grid_layout_2 = Qt.QGridLayout()
        self.op_tab_layout_2.addLayout(self.op_tab_grid_layout_2)
        self.op_tab.addTab(self.op_tab_widget_2, 'CW')
        self.top_grid_layout.addWidget(self.op_tab, 4, 4, 3, 2)
        for r in range(4, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.blocks_probe_signal_x_0 = blocks.probe_signal_f()
        self._wf_gain_range = Range(0, 100, 1, 1, 100)
        self._wf_gain_win = RangeWidget(self._wf_gain_range, self.set_wf_gain, 'Waterfall gain', "dial", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._wf_gain_win, 8, 2, 1, 1)
        for r in range(8, 9):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        if "int" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _vox_sensitivity_dial_control = qtgui.GrDialControl('VOX SENS', self, 0,200,20,"teal",self.set_vox_sensitivity,isFloat, scaleFactor, 50, True, "'value'")
        self.vox_sensitivity = _vox_sensitivity_dial_control

        self.op_tab_grid_layout_0.addWidget(_vox_sensitivity_dial_control, 4, 6, 1, 1)
        for r in range(4, 5):
            self.op_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 7):
            self.op_tab_grid_layout_0.setColumnStretch(c, 1)
        if "int" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _vga_gain_dial_control = qtgui.GrDialControl('RX VGA Gain', self, 0,61,53,"teal",self.set_vga_gain,isFloat, scaleFactor, 50, True, "'value'")
        self.vga_gain = _vga_gain_dial_control

        self.settings_tab_grid_layout_0.addWidget(_vga_gain_dial_control, 5, 2, 1, 1)
        for r in range(5, 6):
            self.settings_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(2, 3):
            self.settings_tab_grid_layout_0.setColumnStretch(c, 1)
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
            time.sleep(1.0 / (20))
        _variable_function_probe_0_thread = threading.Thread(target=_variable_function_probe_0_probe)
        _variable_function_probe_0_thread.daemon = True
        _variable_function_probe_0_thread.start()
        self._tx_rprt_tool_bar = Qt.QToolBar(self)
        self._tx_rprt_tool_bar.addWidget(Qt.QLabel('TX report' + ": "))
        self._tx_rprt_line_edit = Qt.QLineEdit(str(self.tx_rprt))
        self._tx_rprt_tool_bar.addWidget(self._tx_rprt_line_edit)
        self._tx_rprt_line_edit.returnPressed.connect(
            lambda: self.set_tx_rprt(str(str(self._tx_rprt_line_edit.text()))))
        self.op_tab_grid_layout_2.addWidget(self._tx_rprt_tool_bar, 3, 1, 1, 1)
        for r in range(3, 4):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        if "int" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _tx_gain_dial_control = qtgui.GrDialControl('TX GAIN', self, 1,47,47,"orange",self.set_tx_gain,isFloat, scaleFactor, 50, True, "'value'")
        self.tx_gain = _tx_gain_dial_control

        self.settings_tab_grid_layout_1.addWidget(_tx_gain_dial_control, 3, 5, 1, 1)
        for r in range(3, 4):
            self.settings_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(5, 6):
            self.settings_tab_grid_layout_1.setColumnStretch(c, 1)
        # Create the options list
        self._tx_bw_opts_options = [0, 1, 2, 3, 4]
        # Create the labels list
        self._tx_bw_opts_labels = ['5', '3.5', '2.5', '1.75', '0.5']
        # Create the combo box
        # Create the radio buttons
        self._tx_bw_opts_group_box = Qt.QGroupBox('TX BW - kHz' + ": ")
        self._tx_bw_opts_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._tx_bw_opts_button_group = variable_chooser_button_group()
        self._tx_bw_opts_group_box.setLayout(self._tx_bw_opts_box)
        for i, _label in enumerate(self._tx_bw_opts_labels):
            radio_button = Qt.QRadioButton(_label)
            self._tx_bw_opts_box.addWidget(radio_button)
            self._tx_bw_opts_button_group.addButton(radio_button, i)
        self._tx_bw_opts_callback = lambda i: Qt.QMetaObject.invokeMethod(self._tx_bw_opts_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._tx_bw_opts_options.index(i)))
        self._tx_bw_opts_callback(self.tx_bw_opts)
        self._tx_bw_opts_button_group.buttonClicked[int].connect(
            lambda i: self.set_tx_bw_opts(self._tx_bw_opts_options[i]))
        self.top_grid_layout.addWidget(self._tx_bw_opts_group_box, 3, 4, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        _ssb_txing_btn_push_button = Qt.QPushButton('PTT')
        _ssb_txing_btn_push_button = Qt.QPushButton('PTT')
        self._ssb_txing_btn_choices = {'Pressed': 1, 'Released': 0}
        _ssb_txing_btn_push_button.pressed.connect(lambda: self.set_ssb_txing_btn(self._ssb_txing_btn_choices['Pressed']))
        _ssb_txing_btn_push_button.released.connect(lambda: self.set_ssb_txing_btn(self._ssb_txing_btn_choices['Released']))
        self.top_grid_layout.addWidget(_ssb_txing_btn_push_button, 2, 5, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._sq_range = Range(-110, 0, 1, -110, 50)
        self._sq_win = RangeWidget(self._sq_range, self.set_sq, 'SQUELCH', "dial", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._sq_win, 2, 0, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        _split_fq_check_box = Qt.QCheckBox('Split freq')
        self._split_fq_choices = {True: False, False: True}
        self._split_fq_choices_inv = dict((v,k) for k,v in self._split_fq_choices.items())
        self._split_fq_callback = lambda i: Qt.QMetaObject.invokeMethod(_split_fq_check_box, "setChecked", Qt.Q_ARG("bool", self._split_fq_choices_inv[i]))
        self._split_fq_callback(self.split_fq)
        _split_fq_check_box.stateChanged.connect(lambda i: self.set_split_fq(self._split_fq_choices[bool(i)]))
        self.top_grid_layout.addWidget(_split_fq_check_box, 2, 3, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        self._spkr_gain_range = Range(0, 200, 1, 75, 50)
        self._spkr_gain_win = RangeWidget(self._spkr_gain_range, self.set_spkr_gain, '  AF VOL', "dial", float, QtCore.Qt.Horizontal)
        self.top_grid_layout.addWidget(self._spkr_gain_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        # Create the options list
        self._rx_samp_rate_options = [1000000, 2000000, 3000000, 4000000, 5000000, 6000000, 7000000, 8000000]
        # Create the labels list
        self._rx_samp_rate_labels = ['1 MHz', '2 MHz', '3 MHz', '4 MHz', '5 MHz', '6 MHz', '7 MHz', '8 MHz']
        # Create the combo box
        # Create the radio buttons
        self._rx_samp_rate_group_box = Qt.QGroupBox('rx_samp_rate' + ": ")
        self._rx_samp_rate_box = Qt.QHBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._rx_samp_rate_button_group = variable_chooser_button_group()
        self._rx_samp_rate_group_box.setLayout(self._rx_samp_rate_box)
        for i, _label in enumerate(self._rx_samp_rate_labels):
            radio_button = Qt.QRadioButton(_label)
            self._rx_samp_rate_box.addWidget(radio_button)
            self._rx_samp_rate_button_group.addButton(radio_button, i)
        self._rx_samp_rate_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_samp_rate_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._rx_samp_rate_options.index(i)))
        self._rx_samp_rate_callback(self.rx_samp_rate)
        self._rx_samp_rate_button_group.buttonClicked[int].connect(
            lambda i: self.set_rx_samp_rate(self._rx_samp_rate_options[i]))
        self.top_layout.addWidget(self._rx_samp_rate_group_box)
        # Create the options list
        self._rx_preamp_options = [0, 1]
        # Create the labels list
        self._rx_preamp_labels = ['OFF', 'ON']
        # Create the combo box
        # Create the radio buttons
        self._rx_preamp_group_box = Qt.QGroupBox('RX Preamp' + ": ")
        self._rx_preamp_box = Qt.QVBoxLayout()
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
        self.settings_tab_grid_layout_0.addWidget(self._rx_preamp_group_box, 4, 1, 1, 1)
        for r in range(4, 5):
            self.settings_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.settings_tab_grid_layout_0.setColumnStretch(c, 1)
        # Create the options list
        self._rx_bw_options = [0, 1, 2, 3, 4, 5, 6]
        # Create the labels list
        self._rx_bw_labels = ['3.9', '3.2', '2.7', '1.3', '0.5', '0.2', '0.05']
        # Create the combo box
        # Create the radio buttons
        self._rx_bw_group_box = Qt.QGroupBox('RX BW - kHz' + ": ")
        self._rx_bw_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._rx_bw_button_group = variable_chooser_button_group()
        self._rx_bw_group_box.setLayout(self._rx_bw_box)
        for i, _label in enumerate(self._rx_bw_labels):
            radio_button = Qt.QRadioButton(_label)
            self._rx_bw_box.addWidget(radio_button)
            self._rx_bw_button_group.addButton(radio_button, i)
        self._rx_bw_callback = lambda i: Qt.QMetaObject.invokeMethod(self._rx_bw_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._rx_bw_options.index(i)))
        self._rx_bw_callback(self.rx_bw)
        self._rx_bw_button_group.buttonClicked[int].connect(
            lambda i: self.set_rx_bw(self._rx_bw_options[i]))
        self.top_grid_layout.addWidget(self._rx_bw_group_box, 3, 2, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _morse_speed_dial_control = qtgui.GrDialControl('MORSE SPEED [CPM]', self, 40,200,120,"navy",self.set_morse_speed,isFloat, scaleFactor, 50, True, "'value'")
        self.morse_speed = _morse_speed_dial_control

        self.op_tab_grid_layout_2.addWidget(_morse_speed_dial_control, 0, 1, 1, 1)
        for r in range(0, 1):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _monitor_dial_control = qtgui.GrDialControl('CW feedback', self, 0,100,25,"teal",self.set_monitor,isFloat, scaleFactor, 100, True, "'value'")
        self.monitor = _monitor_dial_control

        self.op_tab_grid_layout_2.addWidget(_monitor_dial_control, 0, 2, 1, 1)
        for r in range(0, 1):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        # Create the options list
        self._mode_options = [0, 1, 2, 3, 4, 5, 6]
        # Create the labels list
        self._mode_labels = ['None', 'USB', 'LSB', 'CW', 'CW Stereo', 'FT8', 'MSK144']
        # Create the combo box
        # Create the radio buttons
        self._mode_group_box = Qt.QGroupBox('TX MODE' + ": ")
        self._mode_box = Qt.QVBoxLayout()
        class variable_chooser_button_group(Qt.QButtonGroup):
            def __init__(self, parent=None):
                Qt.QButtonGroup.__init__(self, parent)
            @pyqtSlot(int)
            def updateButtonChecked(self, button_id):
                self.button(button_id).setChecked(True)
        self._mode_button_group = variable_chooser_button_group()
        self._mode_group_box.setLayout(self._mode_box)
        for i, _label in enumerate(self._mode_labels):
            radio_button = Qt.QRadioButton(_label)
            self._mode_box.addWidget(radio_button)
            self._mode_button_group.addButton(radio_button, i)
        self._mode_callback = lambda i: Qt.QMetaObject.invokeMethod(self._mode_button_group, "updateButtonChecked", Qt.Q_ARG("int", self._mode_options.index(i)))
        self._mode_callback(self.mode)
        self._mode_button_group.buttonClicked[int].connect(
            lambda i: self.set_mode(self._mode_options[i]))
        self.top_grid_layout.addWidget(self._mode_group_box, 3, 3, 1, 1)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 0.001

        _mic_gain_dial_control = qtgui.GrDialControl('MIC GAIN', self, 0,995,0.2,"silver",self.set_mic_gain,isFloat, scaleFactor, 50, True, "'value'")
        self.mic_gain = _mic_gain_dial_control

        self.op_tab_grid_layout_0.addWidget(_mic_gain_dial_control, 3, 6, 1, 1)
        for r in range(3, 4):
            self.op_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(6, 7):
            self.op_tab_grid_layout_0.setColumnStretch(c, 1)
        self._mgm_output_gain_range = Range(0, 200, 1, 75, 50)
        self._mgm_output_gain_win = RangeWidget(self._mgm_output_gain_range, self.set_mgm_output_gain, ' MGM VOL', "dial", float, QtCore.Qt.Horizontal)
        self.op_tab_grid_layout_1.addWidget(self._mgm_output_gain_win, 0, 1, 1, 1)
        for r in range(0, 1):
            self.op_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(1, 2):
            self.op_tab_grid_layout_1.setColumnStretch(c, 1)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 0.001

        _mgm_input_gain_dial_control = qtgui.GrDialControl('MGM INPUT GAIN', self, 0,1995,1.4,"silver",self.set_mgm_input_gain,isFloat, scaleFactor, 50, True, "'value'")
        self.mgm_input_gain = _mgm_input_gain_dial_control

        self.op_tab_grid_layout_1.addWidget(_mgm_input_gain_dial_control, 0, 0, 1, 1)
        for r in range(0, 1):
            self.op_tab_grid_layout_1.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_1.setColumnStretch(c, 1)
        self._lna_gain_range = Range(0, 39, 1, 39, 100)
        self._lna_gain_win = RangeWidget(self._lna_gain_range, self.set_lna_gain, 'RX LNA GAIN', "dial", float, QtCore.Qt.Horizontal)
        self.settings_tab_grid_layout_0.addWidget(self._lna_gain_win, 5, 1, 1, 1)
        for r in range(5, 6):
            self.settings_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 2):
            self.settings_tab_grid_layout_0.setColumnStretch(c, 1)
        self._dx_call_tool_bar = Qt.QToolBar(self)
        self._dx_call_tool_bar.addWidget(Qt.QLabel('DX call' + ": "))
        self._dx_call_line_edit = Qt.QLineEdit(str(self.dx_call))
        self._dx_call_tool_bar.addWidget(self._dx_call_line_edit)
        self._dx_call_line_edit.returnPressed.connect(
            lambda: self.set_dx_call(str(str(self._dx_call_line_edit.text()))))
        self.op_tab_grid_layout_2.addWidget(self._dx_call_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 0.01

        _cw_level_dial_control = qtgui.GrDialControl('CW TX LEVEL', self, 0,95,0.8,"lime",self.set_cw_level,isFloat, scaleFactor, 50, True, "'value'")
        self.cw_level = _cw_level_dial_control

        self.op_tab_grid_layout_2.addWidget(_cw_level_dial_control, 0, 0, 1, 1)
        for r in range(0, 1):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self._current_min_fq_tool_bar = Qt.QToolBar(self)
        self._current_min_fq_tool_bar.addWidget(Qt.QLabel('Min-fq' + ": "))
        self._current_min_fq_line_edit = Qt.QLineEdit(str(self.current_min_fq))
        self._current_min_fq_tool_bar.addWidget(self._current_min_fq_line_edit)
        self._current_min_fq_line_edit.returnPressed.connect(
            lambda: self.set_current_min_fq(eng_notation.str_to_num(str(self._current_min_fq_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._current_min_fq_tool_bar, 0, 0, 1, 1)
        for r in range(0, 1):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._current_max_fq_tool_bar = Qt.QToolBar(self)
        self._current_max_fq_tool_bar.addWidget(Qt.QLabel('Max-fq' + ": "))
        self._current_max_fq_line_edit = Qt.QLineEdit(str(self.current_max_fq))
        self._current_max_fq_tool_bar.addWidget(self._current_max_fq_line_edit)
        self._current_max_fq_line_edit.returnPressed.connect(
            lambda: self.set_current_max_fq(eng_notation.str_to_num(str(self._current_max_fq_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._current_max_fq_tool_bar, 0, 1, 1, 1)
        for r in range(0, 1):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._current_default_fq_tool_bar = Qt.QToolBar(self)
        self._current_default_fq_tool_bar.addWidget(Qt.QLabel('Def-fq' + ": "))
        self._current_default_fq_line_edit = Qt.QLineEdit(str(self.current_default_fq))
        self._current_default_fq_tool_bar.addWidget(self._current_default_fq_line_edit)
        self._current_default_fq_line_edit.returnPressed.connect(
            lambda: self.set_current_default_fq(eng_notation.str_to_num(str(self._current_default_fq_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._current_default_fq_tool_bar, 0, 2, 1, 1)
        for r in range(0, 1):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._current_allowed_tx_bandwidth_tool_bar = Qt.QToolBar(self)
        self._current_allowed_tx_bandwidth_tool_bar.addWidget(Qt.QLabel('Bw' + ": "))
        self._current_allowed_tx_bandwidth_line_edit = Qt.QLineEdit(str(self.current_allowed_tx_bandwidth))
        self._current_allowed_tx_bandwidth_tool_bar.addWidget(self._current_allowed_tx_bandwidth_line_edit)
        self._current_allowed_tx_bandwidth_line_edit.returnPressed.connect(
            lambda: self.set_current_allowed_tx_bandwidth(eng_notation.str_to_num(str(self._current_allowed_tx_bandwidth_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._current_allowed_tx_bandwidth_tool_bar, 0, 4, 1, 1)
        for r in range(0, 1):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(4, 5):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._cq_flavor_tool_bar = Qt.QToolBar(self)
        self._cq_flavor_tool_bar.addWidget(Qt.QLabel('CQ Flavor' + ": "))
        self._cq_flavor_line_edit = Qt.QLineEdit(str(self.cq_flavor))
        self._cq_flavor_tool_bar.addWidget(self._cq_flavor_line_edit)
        self._cq_flavor_line_edit.returnPressed.connect(
            lambda: self.set_cq_flavor(str(str(self._cq_flavor_line_edit.text()))))
        self.op_tab_grid_layout_2.addWidget(self._cq_flavor_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self._af_right_range = Range(0, 1, 0.01, 0.5, 100)
        self._af_right_win = RangeWidget(self._af_right_range, self.set_af_right, 'AF BAL', "slider", float, QtCore.Qt.Horizontal)
        self.settings_tab_grid_layout_0.addWidget(self._af_right_win, 10, 1, 1, 2)
        for r in range(10, 11):
            self.settings_tab_grid_layout_0.setRowStretch(r, 1)
        for c in range(1, 3):
            self.settings_tab_grid_layout_0.setColumnStretch(c, 1)
        self.zeromq_pull_msg_source_0 = zeromq.pull_msg_source('tcp://127.0.0.1:8755', 100, False)
        self.variable_qtgui_msg_push_button_0_0_0_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_0_0_0_toggle_button = qtgui.MsgPushButton('Send  RR 73', '','%s de SM6FBQ RR FB  73 Hej e e',"white","black")
        self.variable_qtgui_msg_push_button_0_0_0_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_0_0_0_toggle_button

        self.op_tab_grid_layout_2.addWidget(_variable_qtgui_msg_push_button_0_0_0_0_0_0_toggle_button, 7, 0, 1, 1)
        for r in range(7, 8):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0_0_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_0_0_toggle_button = qtgui.MsgPushButton('Send  R & report', '','%s de SM6FBQ R FB  %s %s %s/ JO67BQ JO67BQ HW? bk',"white","black")
        self.variable_qtgui_msg_push_button_0_0_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_0_0_toggle_button

        self.op_tab_grid_layout_2.addWidget(_variable_qtgui_msg_push_button_0_0_0_0_0_toggle_button, 6, 0, 1, 1)
        for r in range(6, 7):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_0_toggle_button = qtgui.MsgPushButton('Send report', '','%s de SM6FBQ UR %s %s %s/ JO67BQ JO67BQ HW? %s de SM6FBQ k',"white","black")
        self.variable_qtgui_msg_push_button_0_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_0_toggle_button

        self.op_tab_grid_layout_2.addWidget(_variable_qtgui_msg_push_button_0_0_0_0_toggle_button, 5, 0, 1, 1)
        for r in range(5, 6):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_toggle_button = qtgui.MsgPushButton('Call DX', '','%s de SM6FBQ',"white","black")
        self.variable_qtgui_msg_push_button_0_0_0 = _variable_qtgui_msg_push_button_0_0_0_toggle_button

        self.op_tab_grid_layout_2.addWidget(_variable_qtgui_msg_push_button_0_0_0_toggle_button, 4, 0, 1, 1)
        for r in range(4, 5):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self.variable_qtgui_msg_push_button_0_0 = _variable_qtgui_msg_push_button_0_0_toggle_button = qtgui.MsgPushButton('CALL CQ', '','CQ%s CQ%s CQ%s DE SM6FBQ SM6FBQ SM6FBQ %sk',"white","black")
        self.variable_qtgui_msg_push_button_0_0 = _variable_qtgui_msg_push_button_0_0_toggle_button

        self.op_tab_grid_layout_2.addWidget(_variable_qtgui_msg_push_button_0_0_toggle_button, 1, 1, 1, 1)
        for r in range(1, 2):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self._variable_qtgui_entry_0_tool_bar = Qt.QToolBar(self)
        self._variable_qtgui_entry_0_tool_bar.addWidget(Qt.QLabel('Selector' + ": "))
        self._variable_qtgui_entry_0_line_edit = Qt.QLineEdit(str(self.variable_qtgui_entry_0))
        self._variable_qtgui_entry_0_tool_bar.addWidget(self._variable_qtgui_entry_0_line_edit)
        self._variable_qtgui_entry_0_line_edit.returnPressed.connect(
            lambda: self.set_variable_qtgui_entry_0(int(str(self._variable_qtgui_entry_0_line_edit.text()))))
        self.top_layout.addWidget(self._variable_qtgui_entry_0_tool_bar)
        self._tx_fq_win_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl = 'TX FQ', min_freq_hz = current_min_fq + current_allowed_tx_bandwidth - 29e6, max_freq_hz=current_max_fq - current_allowed_tx_bandwidth, parent=self,  thousands_separator=".",background_color="black",fontColor="red", var_callback=self.set_tx_fq_win,outputmsgname="'freq'".replace("'",""))
        self._tx_fq_win_msgdigctl_win.setValue(tx_center_fq)
        self._tx_fq_win_msgdigctl_win.setReadOnly((not split_fq))
        self.tx_fq_win = self._tx_fq_win_msgdigctl_win

        self.top_grid_layout.addWidget(self._tx_fq_win_msgdigctl_win, 2, 4, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(4, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.tx_fq_sync_0 = tx_fq_sync_0.blk(gate_control=True, resync=True, repeat=2)
        self.tx_fq_sync = tx_fq_sync.blk(gate_control=split_fq, resync=True, repeat=2)
        self._tx_fq_q_tool_bar = Qt.QToolBar(self)
        self._tx_fq_q_tool_bar.addWidget(Qt.QLabel('TX fq' + ": "))
        self._tx_fq_q_line_edit = Qt.QLineEdit(str(self.tx_fq_q))
        self._tx_fq_q_tool_bar.addWidget(self._tx_fq_q_line_edit)
        self._tx_fq_q_line_edit.returnPressed.connect(
            lambda: self.set_tx_fq_q(int(str(self._tx_fq_q_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._tx_fq_q_tool_bar, 2, 0, 1, 1)
        for r in range(2, 3):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._tc_vga_tool_bar = Qt.QToolBar(self)
        self._tc_vga_tool_bar.addWidget(Qt.QLabel('TX VGA' + ": "))
        self._tc_vga_line_edit = Qt.QLineEdit(str(self.tc_vga))
        self._tc_vga_tool_bar.addWidget(self._tc_vga_line_edit)
        self._tc_vga_line_edit.returnPressed.connect(
            lambda: self.set_tc_vga(eng_notation.str_to_num(str(self._tc_vga_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._tc_vga_tool_bar, 2, 3, 1, 1)
        for r in range(2, 3):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(3, 4):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self.soapy_hackrf_source_0 = None
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.soapy_hackrf_source_0 = soapy.source(dev, "fc32", 1, 'driver=remote,remote=tcp://192.168.1.125:1234,remote:type=hackrf',
                                  stream_args, tune_args, settings)
        self.soapy_hackrf_source_0.set_sample_rate(0, rx_samp_rate)
        self.soapy_hackrf_source_0.set_bandwidth(0, 0)
        self.soapy_hackrf_source_0.set_frequency(0, rx_hw_fq + fq_calibration)
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
        self.soapy_hackrf_sink_0.set_bandwidth(0, tx_bw[tx_bw_opts])
        self.soapy_hackrf_sink_0.set_frequency(0, tx_fq+tx_mode_offset[side_band_tx] + fq_calibration)
        self.soapy_hackrf_sink_0.set_gain(0, 'AMP', True)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(tx_gain, 0.0), 47.0))
        self._side_band_dislay_tool_bar = Qt.QToolBar(self)
        self._side_band_dislay_tool_bar.addWidget(Qt.QLabel('Side-band' + ": "))
        self._side_band_dislay_line_edit = Qt.QLineEdit(str(self.side_band_dislay))
        self._side_band_dislay_tool_bar.addWidget(self._side_band_dislay_line_edit)
        self._side_band_dislay_line_edit.returnPressed.connect(
            lambda: self.set_side_band_dislay(int(str(self._side_band_dislay_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._side_band_dislay_tool_bar, 2, 2, 1, 1)
        for r in range(2, 3):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(2, 3):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._rx_fq_win_msgdigctl_win = qtgui.MsgDigitalNumberControl(lbl = 'RX FQ', min_freq_hz = current_min_fq - 29e6, max_freq_hz=current_max_fq, parent=self,  thousands_separator=".",background_color="black",fontColor="green", var_callback=self.set_rx_fq_win,outputmsgname="'freq'".replace("'",""))
        self._rx_fq_win_msgdigctl_win.setValue(current_default_fq)
        self._rx_fq_win_msgdigctl_win.setReadOnly(False)
        self.rx_fq_win = self._rx_fq_win_msgdigctl_win

        self.top_grid_layout.addWidget(self._rx_fq_win_msgdigctl_win, 2, 2, 1, 1)
        for r in range(2, 3):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.rx_distancer = rx_distancer.blk(desired_fq=current_default_fq, min_distance=100e3, max_distance=rx_samp_rate/2.0, hw_var=rx_hw_fq, filter_var=filter_fq)
        self._rx_ctr_fq_0_tool_bar = Qt.QToolBar(self)
        self._rx_ctr_fq_0_tool_bar.addWidget(Qt.QLabel('Rx filter fq' + ": "))
        self._rx_ctr_fq_0_line_edit = Qt.QLineEdit(str(self.rx_ctr_fq_0))
        self._rx_ctr_fq_0_tool_bar.addWidget(self._rx_ctr_fq_0_line_edit)
        self._rx_ctr_fq_0_line_edit.returnPressed.connect(
            lambda: self.set_rx_ctr_fq_0(int(str(self._rx_ctr_fq_0_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._rx_ctr_fq_0_tool_bar, 1, 1, 1, 1)
        for r in range(1, 2):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._rx_ctr_fq_tool_bar = Qt.QToolBar(self)
        self._rx_ctr_fq_tool_bar.addWidget(Qt.QLabel('Rx center fq' + ": "))
        self._rx_ctr_fq_line_edit = Qt.QLineEdit(str(self.rx_ctr_fq))
        self._rx_ctr_fq_tool_bar.addWidget(self._rx_ctr_fq_line_edit)
        self._rx_ctr_fq_line_edit.returnPressed.connect(
            lambda: self.set_rx_ctr_fq(int(str(self._rx_ctr_fq_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._rx_ctr_fq_tool_bar, 1, 0, 1, 1)
        for r in range(1, 2):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
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
        self.rational_resampler_xxx_4_0 = filter.rational_resampler_ccc(
                interpolation=int(2*tx_samp_rate/audio_samp_rate),
                decimation=1,
                taps=[],
                fractional_bw=0)
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=int(audio_samp_rate/1000),
                decimation=int(cw_samp_rate/1000),
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0_0_0 = filter.rational_resampler_ccc(
                interpolation=int(audio_samp_rate/1000),
                decimation=int(if2_samp_rate/1000),
                taps=[],
                fractional_bw=0.4)
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=int(audio_samp_rate/1000),
                decimation=int(if2_samp_rate/1000),
                taps=[],
                fractional_bw=0.4)
        self.qtgui_sink_x_0_0_0 = qtgui.sink_c(
            4096, #fftsize
            window.WIN_HAMMING, #wintype
            0, #fc
            ssb_tx_bandwidth*4, #bw
            "SOAPY RF", #name
            True, #plotfreq
            True, #plotwaterfall
            True, #plottime
            True, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0_0_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_sink_x_0_0_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0_0_0.enable_rf_freq(False)

        self.top_layout.addWidget(self._qtgui_sink_x_0_0_0_win)
        self.qtgui_sink_x_0 = qtgui.sink_c(
            4096, #fftsize
            window.WIN_HANN, #wintype
            fft_corr[side_band_rx], #fc
            rx_samp_rate, #bw
            "", #name
            False, #plotfreq
            True, #plotwaterfall
            False, #plottime
            False, #plotconst
            None # parent
        )
        self.qtgui_sink_x_0.set_update_time(1.0/10)
        self._qtgui_sink_x_0_win = sip.wrapinstance(self.qtgui_sink_x_0.qwidget(), Qt.QWidget)

        self.qtgui_sink_x_0.enable_rf_freq(False)

        self.top_grid_layout.addWidget(self._qtgui_sink_x_0_win, 4, 0, 3, 4)
        for r in range(4, 7):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 4):
            self.top_grid_layout.setColumnStretch(c, 1)
        if "real" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _qtgui_levelgauge_0_lg_win = qtgui.GrLevelGauge('S-meter [dBm]',"teal","silver","teal",-140,30, 50, False,1,isFloat,scaleFactor,True,self)
        _qtgui_levelgauge_0_lg_win.setValue(variable_function_probe_0)
        self.qtgui_levelgauge_0 = _qtgui_levelgauge_0_lg_win

        self.top_grid_layout.addWidget(_qtgui_levelgauge_0_lg_win, 3, 0, 1, 2)
        for r in range(3, 4):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_ledindicator_0_0 = self._qtgui_ledindicator_0_0_win = qtgui.GrLEDIndicator('ON AIR', "red", "black", (ssb_txing or ssb_txing_btn or cw_txing), 20, 1, 1, 1, self)
        self.qtgui_ledindicator_0_0 = self._qtgui_ledindicator_0_0_win
        self.top_grid_layout.addWidget(self._qtgui_ledindicator_0_0_win, 1, 5, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(5, 6):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_edit_box_msg_0 = qtgui.edit_box_msg(qtgui.STRING, '', 'CW message to send:', False, True, '', None)
        self._qtgui_edit_box_msg_0_win = sip.wrapinstance(self.qtgui_edit_box_msg_0.qwidget(), Qt.QWidget)
        self.op_tab_grid_layout_2.addWidget(self._qtgui_edit_box_msg_0_win, 2, 0, 1, 3)
        for r in range(2, 3):
            self.op_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 3):
            self.op_tab_grid_layout_2.setColumnStretch(c, 1)
        self.pfb_decimator_ccf_0_0_0 = pfb.decimator_ccf(
            int(if0_samp_rate/if_samp_rate),
            firdes.low_pass(1,rx_samp_rate/2, 3900,100),
            0,
            60,
            True,
            True)
        self.pfb_decimator_ccf_0_0_0.declare_sample_delay(0)
        self.pfb_decimator_ccf_0_0 = pfb.decimator_ccf(
            int(if0_samp_rate/if_samp_rate),
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
        self.msg_formatter_1 = msg_formatter_1.blk(variables=(cq_flavor, cq_flavor, cq_flavor, cq_flavor))
        self.msg_formatter_0_0_0 = msg_formatter_0_0_0.blk(variables=(dx_call, tx_rprt, tx_rprt, tx_rprt, dx_call))
        self.msg_formatter_0_0 = msg_formatter_0_0.blk(variables=(dx_call, tx_rprt, tx_rprt, tx_rprt, dx_call))
        self.msg_formatter_0 = msg_formatter_0.blk(variables=(dx_call, tx_rprt, tx_rprt, tx_rprt, dx_call))
        self.msg_formatter = msg_formatter.blk(variables=(dx_call))
        self._mode_display_tool_bar = Qt.QToolBar(self)
        self._mode_display_tool_bar.addWidget(Qt.QLabel('Mode' + ": "))
        self._mode_display_line_edit = Qt.QLineEdit(str(self.mode_display))
        self._mode_display_tool_bar.addWidget(self._mode_display_line_edit)
        self._mode_display_line_edit.returnPressed.connect(
            lambda: self.set_mode_display(int(str(self._mode_display_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._mode_display_tool_bar, 2, 1, 1, 1)
        for r in range(2, 3):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._mic_inpt_gain_0_tool_bar = Qt.QToolBar(self)
        self._mic_inpt_gain_0_tool_bar.addWidget(Qt.QLabel('MIC gain' + ": "))
        self._mic_inpt_gain_0_line_edit = Qt.QLineEdit(str(self.mic_inpt_gain_0))
        self._mic_inpt_gain_0_tool_bar.addWidget(self._mic_inpt_gain_0_line_edit)
        self._mic_inpt_gain_0_line_edit.returnPressed.connect(
            lambda: self.set_mic_inpt_gain_0(eng_notation.str_to_num(str(self._mic_inpt_gain_0_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._mic_inpt_gain_0_tool_bar, 3, 1, 1, 1)
        for r in range(3, 4):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(1, 2):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self._mgm_inpt_gain_tool_bar = Qt.QToolBar(self)
        self._mgm_inpt_gain_tool_bar.addWidget(Qt.QLabel('MGM input gain' + ": "))
        self._mgm_inpt_gain_line_edit = Qt.QLineEdit(str(self.mgm_inpt_gain))
        self._mgm_inpt_gain_tool_bar.addWidget(self._mgm_inpt_gain_line_edit)
        self._mgm_inpt_gain_line_edit.returnPressed.connect(
            lambda: self.set_mgm_inpt_gain(eng_notation.str_to_num(str(self._mgm_inpt_gain_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._mgm_inpt_gain_tool_bar, 3, 0, 1, 1)
        for r in range(3, 4):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(0, 1):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self.freq_xlating_fft_filter_ccc_1_0 = filter.freq_xlating_fft_filter_ccc(int(rx_samp_rate/if0_samp_rate), firdes.low_pass(1,rx_samp_rate,rx_samp_rate/(2*1),4000), filter_fq-cw_midear_beat[side_band_rx], rx_samp_rate)
        self.freq_xlating_fft_filter_ccc_1_0.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_1_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_1 = filter.freq_xlating_fft_filter_ccc(int(rx_samp_rate/if0_samp_rate), firdes.low_pass(1,rx_samp_rate,rx_samp_rate/(2*1),4000), filter_fq+cw_midear_beat[side_band_rx], rx_samp_rate)
        self.freq_xlating_fft_filter_ccc_1.set_nthreads(2)
        self.freq_xlating_fft_filter_ccc_1.declare_sample_delay(0)
        self.filter_fft_low_pass_filter_0_0_0 = filter.fft_filter_fff(2, firdes.low_pass(1, audio_samp_rate, ssb_tx_bandwidth/2-200, 50, window.WIN_HAMMING, 6.76), 1)
        self.filter_fft_low_pass_filter_0_0 = filter.fft_filter_fff(2, firdes.low_pass(1, audio_samp_rate, ssb_tx_bandwidth/2-200, 50, window.WIN_HAMMING, 6.76), 1)
        self.filter_fft_low_pass_filter_0 = filter.fft_filter_ccc(1, firdes.low_pass(1, tx_samp_rate, ssb_tx_bandwidth, 50, window.WIN_RECTANGULAR, 6.76), 1)
        self.epy_block_2 = epy_block_2.blk(offset=rx_hw_fq + filter_fq, factor=1)
        self.epy_block_1_0 = epy_block_1_0.blk(threshold=vox_threshold[mode], attack=vox_attack[mode], delay=vox_delay[mode])
        self.epy_block_1 = epy_block_1.blk(threshold=0.4, attack=1, delay=6/morse_speed * 25 + 2)
        self.epy_block_0_0 = epy_block_0_0.mc_sync_block(enable=True)
        self._current_allowed_modes_tool_bar = Qt.QToolBar(self)
        self._current_allowed_modes_tool_bar.addWidget(Qt.QLabel('Modes' + ": "))
        self._current_allowed_modes_line_edit = Qt.QLineEdit(str(self.current_allowed_modes))
        self._current_allowed_modes_tool_bar.addWidget(self._current_allowed_modes_line_edit)
        self._current_allowed_modes_line_edit.returnPressed.connect(
            lambda: self.set_current_allowed_modes(eval(str(self._current_allowed_modes_line_edit.text()))))
        self.settings_tab_grid_layout_2.addWidget(self._current_allowed_modes_tool_bar, 0, 5, 1, 1)
        for r in range(0, 1):
            self.settings_tab_grid_layout_2.setRowStretch(r, 1)
        for c in range(5, 6):
            self.settings_tab_grid_layout_2.setColumnStretch(c, 1)
        self.blocks_uchar_to_float_0 = blocks.uchar_to_float()
        self.blocks_selector_2 = blocks.selector(gr.sizeof_float*1,mode_to_audio_input[mode],0)
        self.blocks_selector_2.set_enabled(True)
        self.blocks_selector_1 = blocks.selector(gr.sizeof_gr_complex*1,side_band_tx,0)
        self.blocks_selector_1.set_enabled(True)
        self.blocks_selector_0 = blocks.selector(gr.sizeof_gr_complex*1,0,(ssb_txing or ssb_txing_btn) and mode > 0)
        self.blocks_selector_0.set_enabled(True)
        self.blocks_repeat_0_0 = blocks.repeat(gr.sizeof_gr_complex*1, int(tx_samp_rate/cw_samp_rate))
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, int(6* cw_samp_rate / morse_speed))
        self.blocks_null_source_1 = blocks.null_source(gr.sizeof_float*1)
        self.blocks_null_source_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_sink_2 = blocks.null_sink(gr.sizeof_gr_complex*1)
        self.blocks_nlog10_ff_0 = blocks.nlog10_ff(10.6, 1, RX_power_offset_dB)
        self.blocks_multiply_xx_0_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0_0 = blocks.multiply_vff(1)
        self.blocks_multiply_xx_0 = blocks.multiply_vff(1)
        self.blocks_multiply_matrix_xx_0 = blocks.multiply_matrix_ff(af_mix_matrices[side_band_rx], gr.TPP_DONT)
        self.blocks_multiply_const_vxx_4_0_0_0 = blocks.multiply_const_cc(wf_gain)
        self.blocks_multiply_const_vxx_4_0_0 = blocks.multiply_const_cc(usb_chain_gain[side_band_rx])
        self.blocks_multiply_const_vxx_4_0 = blocks.multiply_const_cc(lsb_chain_gain[side_band_rx])
        self.blocks_multiply_const_vxx_1_0_1_0_0 = blocks.multiply_const_ff(mgm_output_gain*(1-af_right))
        self.blocks_multiply_const_vxx_1_0_1_0 = blocks.multiply_const_ff(spkr_gain*(1-af_right))
        self.blocks_multiply_const_vxx_1_0_0_1 = blocks.multiply_const_ff(vox_sensitivity)
        self.blocks_multiply_const_vxx_1_0_0_0_0 = blocks.multiply_const_ff(mic_gain)
        self.blocks_multiply_const_vxx_1_0_0_0 = blocks.multiply_const_ff(mgm_input_gain)
        self.blocks_multiply_const_vxx_1_0_0 = blocks.multiply_const_ff(mgm_output_gain *af_right)
        self.blocks_multiply_const_vxx_1_0 = blocks.multiply_const_ff(spkr_gain *af_right)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_ff(cw_level)
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_ff(monitor*0.0001*1000)
        self.blocks_msgpair_to_var_1_1 = blocks.msg_pair_to_var(self.set_tx_fq)
        self.blocks_msgpair_to_var_1_0_0 = blocks.msg_pair_to_var(self.set_filter_fq)
        self.blocks_msgpair_to_var_1_0 = blocks.msg_pair_to_var(self.set_rx_hw_fq)
        self.blocks_msgpair_to_var_1 = blocks.msg_pair_to_var(self.set_rx_fq)
        self.blocks_msgpair_to_var_0_0 = blocks.msg_pair_to_var(self.set_ssb_txing)
        self.blocks_msgpair_to_var_0 = blocks.msg_pair_to_var(self.set_cw_txing)
        self.blocks_message_debug_0 = blocks.message_debug(True)
        self.blocks_integrate_xx_1 = blocks.integrate_ff(1, 1)
        self.blocks_integrate_xx_0 = blocks.integrate_ff(if2_samp_rate*2, 1)
        self.blocks_float_to_complex_0_3 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_char_0 = blocks.float_to_char(1, 1 if mode > 0 else 0)
        self.blocks_complex_to_real_0_0_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_complex_to_float_0_2_0_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_2_0 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_2 = blocks.complex_to_float(1)
        self.blocks_complex_to_float_0_1_0 = blocks.complex_to_float(1)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        # Create the options list
        self._band_selector_options = ['                  ']
        # Create the labels list
        self._band_selector_labels = ['                  ']
        # Create the combo box
        self._band_selector_tool_bar = Qt.QToolBar(self)
        self._band_selector_tool_bar.addWidget(Qt.QLabel('BAND' + ": "))
        self._band_selector_combo_box = Qt.QComboBox()
        self._band_selector_tool_bar.addWidget(self._band_selector_combo_box)
        for _label in self._band_selector_labels: self._band_selector_combo_box.addItem(_label)
        self._band_selector_callback = lambda i: Qt.QMetaObject.invokeMethod(self._band_selector_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._band_selector_options.index(i)))
        self._band_selector_callback(self.band_selector)
        self._band_selector_combo_box.currentIndexChanged.connect(
            lambda i: self.set_band_selector(self._band_selector_options[i]))
        # Create the radio buttons
        self.top_grid_layout.addWidget(self._band_selector_tool_bar, 1, 3, 1, 2)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(3, 5):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.band_pass_filter_0_1 = filter.fir_filter_ccc(
            int(if_samp_rate/if2_samp_rate),
            firdes.complex_band_pass(
                1,
                if_samp_rate,
                bpf_low[rx_bw],
                bpf_high[rx_bw],
                100,
                window.WIN_BLACKMAN,
                6.76))
        self.band_pass_filter_0_0 = filter.fir_filter_ccc(
            int(if_samp_rate/if2_samp_rate),
            firdes.complex_band_pass(
                1,
                if_samp_rate,
                bpf_low[rx_bw],
                bpf_high[rx_bw],
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
        self.audio_source_0_0 = audio.source(audio_samp_rate, "MacBook Pro-mikrofon", True)
        self.audio_source_0 = audio.source(audio_samp_rate, "BlackHole 16ch", True)
        self.audio_sink_0_2 = audio.sink(audio_samp_rate, "WSJT-3", True)
        self.audio_sink_0_1 = audio.sink(audio_samp_rate, "std_spkr", True)
        self.audio_sink_0_0 = audio.sink(audio_samp_rate, "WSJT-3", True)
        self.analog_simple_squelch_cc_0_0 = analog.simple_squelch_cc(sq, .001)
        self.analog_simple_squelch_cc_0 = analog.simple_squelch_cc(sq, .001)
        self.analog_sig_source_x_1_0 = analog.sig_source_f(audio_samp_rate, analog.GR_SIN_WAVE, ssb_tx_bandwidth/2, 1, 0, 0)
        self.analog_sig_source_x_0_0 = analog.sig_source_f(audio_samp_rate, analog.GR_COS_WAVE, ssb_tx_bandwidth/2, 1, 0, 0)
        self.analog_sig_source_x_0 = analog.sig_source_f(50e3, analog.GR_COS_WAVE, cw_midear_beat[side_band_tx], 1, 0, 0)
        self.analog_agc3_xx_0_0 = analog.agc3_cc((1e-1), 3e-6, (.001)*0+.002, .1, 1)
        self.analog_agc3_xx_0_0.set_max_gain(.1)
        self.analog_agc3_xx_0 = analog.agc3_cc((1e-1), 3e-6, (.001)*0+.002, .1, 1)
        self.analog_agc3_xx_0.set_max_gain(.1)
        self.analog_agc2_xx_0 = analog.agc2_ff(1e-1, 1e-2, 0.98, 1.0)
        self.analog_agc2_xx_0.set_max_gain(5)



        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.epy_block_0_0, 'clear_input'), (self.qtgui_edit_box_msg_0, 'val'))
        self.msg_connect((self.epy_block_1, 'onair'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_1, 'onair'), (self.blocks_msgpair_to_var_0, 'inpair'))
        self.msg_connect((self.epy_block_1_0, 'onair'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_1_0, 'onair'), (self.blocks_msgpair_to_var_0_0, 'inpair'))
        self.msg_connect((self.epy_block_2, 'msg_out'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.epy_block_2, 'msg_out'), (self.tx_fq_sync_0, 'msg_in'))
        self.msg_connect((self.msg_formatter, 'msg_out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.msg_formatter_0, 'msg_out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.msg_formatter_0_0, 'msg_out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.msg_formatter_0_0_0, 'msg_out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.msg_formatter_1, 'msg_out'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.qtgui_edit_box_msg_0, 'msg'), (self.epy_block_0_0, 'msg_in'))
        self.msg_connect((self.qtgui_sink_x_0, 'freq'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.qtgui_sink_x_0, 'freq'), (self.epy_block_2, 'msg_in'))
        self.msg_connect((self.rx_distancer, 'hw_fq_out'), (self.blocks_msgpair_to_var_1_0, 'inpair'))
        self.msg_connect((self.rx_distancer, 'filter_fq_out'), (self.blocks_msgpair_to_var_1_0_0, 'inpair'))
        self.msg_connect((self.rx_fq_win, 'valueout'), (self.blocks_msgpair_to_var_1, 'inpair'))
        self.msg_connect((self.rx_fq_win, 'valueout'), (self.rx_distancer, 'freq_in'))
        self.msg_connect((self.rx_fq_win, 'valueout'), (self.tx_fq_sync, 'msg_in'))
        self.msg_connect((self.tx_fq_sync, 'msg_out'), (self.tx_fq_win, 'valuein'))
        self.msg_connect((self.tx_fq_sync_0, 'msg_out'), (self.rx_fq_win, 'valuein'))
        self.msg_connect((self.tx_fq_win, 'valueout'), (self.blocks_message_debug_0, 'print'))
        self.msg_connect((self.tx_fq_win, 'valueout'), (self.blocks_msgpair_to_var_1_1, 'inpair'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0, 'pressed'), (self.msg_formatter_1, 'msg_in'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0_0, 'pressed'), (self.msg_formatter, 'msg_in'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0_0_0, 'pressed'), (self.msg_formatter_0, 'msg_in'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0_0_0_0, 'pressed'), (self.msg_formatter_0_0, 'msg_in'))
        self.msg_connect((self.variable_qtgui_msg_push_button_0_0_0_0_0_0, 'pressed'), (self.msg_formatter_0_0_0, 'msg_in'))
        self.msg_connect((self.zeromq_pull_msg_source_0, 'out'), (self.tx_fq_sync_0, 'msg_in'))
        self.connect((self.analog_agc2_xx_0, 0), (self.blocks_multiply_const_vxx_1_0_0_0_0, 0))
        self.connect((self.analog_agc3_xx_0, 0), (self.rational_resampler_xxx_0, 0))
        self.connect((self.analog_agc3_xx_0_0, 0), (self.rational_resampler_xxx_0_0_0, 0))
        self.connect((self.analog_sig_source_x_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0_0_0, 0))
        self.connect((self.analog_sig_source_x_1_0, 0), (self.blocks_multiply_xx_0_0, 1))
        self.connect((self.analog_simple_squelch_cc_0, 0), (self.analog_agc3_xx_0, 0))
        self.connect((self.analog_simple_squelch_cc_0_0, 0), (self.analog_agc3_xx_0_0, 0))
        self.connect((self.audio_source_0, 0), (self.blocks_multiply_const_vxx_1_0_0_0, 0))
        self.connect((self.audio_source_0_0, 0), (self.analog_agc2_xx_0, 0))
        self.connect((self.band_pass_filter_0, 0), (self.blocks_multiply_const_vxx_1_0_0_1, 0))
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
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_matrix_xx_0, 1))
        self.connect((self.blocks_complex_to_real_0_0_0, 0), (self.blocks_multiply_matrix_xx_0, 0))
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
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.rational_resampler_xxx_1, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_float_to_complex_0_3, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0, 0), (self.audio_sink_0_1, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0, 0), (self.audio_sink_0_2, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0, 0), (self.blocks_selector_2, 1))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_0_0, 0), (self.blocks_selector_2, 2))
        self.connect((self.blocks_multiply_const_vxx_1_0_0_1, 0), (self.epy_block_1_0, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_1_0, 0), (self.audio_sink_0_1, 0))
        self.connect((self.blocks_multiply_const_vxx_1_0_1_0_0, 0), (self.audio_sink_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_4_0, 0), (self.blocks_complex_to_float_0_2, 0))
        self.connect((self.blocks_multiply_const_vxx_4_0_0, 0), (self.blocks_complex_to_float_0_2_0, 0))
        self.connect((self.blocks_multiply_const_vxx_4_0_0_0, 0), (self.qtgui_sink_x_0, 0))
        self.connect((self.blocks_multiply_matrix_xx_0, 1), (self.blocks_multiply_const_vxx_1_0, 0))
        self.connect((self.blocks_multiply_matrix_xx_0, 1), (self.blocks_multiply_const_vxx_1_0_0, 0))
        self.connect((self.blocks_multiply_matrix_xx_0, 0), (self.blocks_multiply_const_vxx_1_0_1_0, 0))
        self.connect((self.blocks_multiply_matrix_xx_0, 0), (self.blocks_multiply_const_vxx_1_0_1_0_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_multiply_xx_0_0, 0), (self.filter_fft_low_pass_filter_0_0, 0))
        self.connect((self.blocks_multiply_xx_0_0_0, 0), (self.filter_fft_low_pass_filter_0_0_0, 0))
        self.connect((self.blocks_nlog10_ff_0, 0), (self.blocks_probe_signal_x_0, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_selector_1, 0))
        self.connect((self.blocks_null_source_0, 0), (self.blocks_selector_1, 5))
        self.connect((self.blocks_null_source_1, 0), (self.blocks_selector_2, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_uchar_to_float_0, 0))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_selector_1, 3))
        self.connect((self.blocks_repeat_0_0, 0), (self.blocks_selector_1, 4))
        self.connect((self.blocks_selector_0, 0), (self.blocks_null_sink_2, 0))
        self.connect((self.blocks_selector_0, 1), (self.rational_resampler_xxx_4_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.qtgui_sink_x_0_0_0, 0))
        self.connect((self.blocks_selector_1, 0), (self.soapy_hackrf_sink_0, 0))
        self.connect((self.blocks_selector_2, 0), (self.band_pass_filter_0, 0))
        self.connect((self.blocks_uchar_to_float_0, 0), (self.root_raised_cosine_filter_0, 0))
        self.connect((self.epy_block_0_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_selector_1, 1))
        self.connect((self.filter_fft_low_pass_filter_0, 0), (self.blocks_selector_1, 2))
        self.connect((self.filter_fft_low_pass_filter_0_0, 0), (self.blocks_float_to_complex_0_0_1, 0))
        self.connect((self.filter_fft_low_pass_filter_0_0_0, 0), (self.blocks_float_to_complex_0_0_1, 1))
        self.connect((self.freq_xlating_fft_filter_ccc_1, 0), (self.pfb_decimator_ccf_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_1_0, 0), (self.blocks_multiply_const_vxx_4_0_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_1_0, 0), (self.pfb_decimator_ccf_0_0_0, 0))
        self.connect((self.mulc_lsb1, 0), (self.blocks_float_to_complex_0_0_0, 0))
        self.connect((self.mulc_lsb_0, 0), (self.blocks_float_to_complex_0_1, 0))
        self.connect((self.mulc_usb1, 0), (self.blocks_float_to_complex_0_1_0_0, 0))
        self.connect((self.mulc_usb_0, 0), (self.blocks_float_to_complex_0_1_0, 0))
        self.connect((self.pfb_decimator_ccf_0_0, 0), (self.blocks_multiply_const_vxx_4_0, 0))
        self.connect((self.pfb_decimator_ccf_0_0_0, 0), (self.blocks_multiply_const_vxx_4_0_0, 0))
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_real_0, 0))
        self.connect((self.rational_resampler_xxx_0_0_0, 0), (self.blocks_complex_to_real_0_0_0, 0))
        self.connect((self.rational_resampler_xxx_1, 0), (self.audio_sink_0_0, 0))
        self.connect((self.rational_resampler_xxx_4_0, 0), (self.filter_fft_low_pass_filter_0, 0))
        self.connect((self.root_raised_cosine_filter_0, 0), (self.root_raised_cosine_filter_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_integrate_xx_1, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.root_raised_cosine_filter_0_0, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.freq_xlating_fft_filter_ccc_1, 0))
        self.connect((self.soapy_hackrf_source_0, 0), (self.freq_xlating_fft_filter_ccc_1_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "FBQ_xcvr")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def setStyleSheetFromFile(self, filename):
        try:
            if not os.path.exists(filename):
                filename = os.path.join(
                    gr.prefix(), "share", "gnuradio", "themes", filename)
            with open(filename) as ss:
                self.setStyleSheet(ss.read())
        except Exception as e:
            print(e, file=sys.stderr)

    def get_ham_bands(self):
        return self.ham_bands

    def set_ham_bands(self, ham_bands):
        self.ham_bands = ham_bands
        self.set_current_allowed_modes(self.ham_bands[self.band_selector][4])
        self.set_current_allowed_tx_bandwidth(self.ham_bands[self.band_selector][3])
        self.set_current_default_fq(self.ham_bands[self.band_selector][2])
        self.set_current_max_fq(self.ham_bands[self.band_selector][1])
        self.set_current_min_fq(self.ham_bands[self.band_selector][0])
        self.set_f0_min(self.ham_bands[self.band_selector][0])

    def get_band_selector(self):
        return self.band_selector

    def set_band_selector(self, band_selector):
        self.band_selector = band_selector
        self._band_selector_callback(self.band_selector)
        self.set_current_allowed_modes(self.ham_bands[self.band_selector][4])
        self.set_current_allowed_tx_bandwidth(self.ham_bands[self.band_selector][3])
        self.set_current_default_fq(self.ham_bands[self.band_selector][2])
        self.set_current_max_fq(self.ham_bands[self.band_selector][1])
        self.set_current_min_fq(self.ham_bands[self.band_selector][0])
        self.set_f0_min(self.ham_bands[self.band_selector][0])

    def get_mode_labels(self):
        return self.mode_labels

    def set_mode_labels(self, mode_labels):
        self.mode_labels = mode_labels
        self.set_mode_default_option(self.mode_labels[(list(set(self.mode_labels) & set(self.current_allowed_modes))[0])])

    def get_current_allowed_modes(self):
        return self.current_allowed_modes

    def set_current_allowed_modes(self, current_allowed_modes):
        self.current_allowed_modes = current_allowed_modes
        Qt.QMetaObject.invokeMethod(self._current_allowed_modes_line_edit, "setText", Qt.Q_ARG("QString", repr(self.current_allowed_modes)))
        self.set_mode_default_option(self.mode_labels[(list(set(self.mode_labels) & set(self.current_allowed_modes))[0])])

    def get_mode_default_option(self):
        return self.mode_default_option

    def set_mode_default_option(self, mode_default_option):
        self.mode_default_option = mode_default_option
        self.set_mode(self.mode_default_option)

    def get_mode_to_sb_rx(self):
        return self.mode_to_sb_rx

    def set_mode_to_sb_rx(self, mode_to_sb_rx):
        self.mode_to_sb_rx = mode_to_sb_rx
        self.set_side_band_rx(self.mode_to_sb_rx[self.mode])

    def get_mode(self):
        return self.mode

    def set_mode(self, mode):
        self.mode = mode
        self._mode_callback(self.mode)
        self.set_mode_display(self.mode)
        self.set_side_band_rx(self.mode_to_sb_rx[self.mode])
        self.set_side_band_tx(self.mode_to_sb_tx[self.mode])
        self.blocks_float_to_char_0.set_scale(1 if self.mode > 0 else 0)
        self.blocks_selector_0.set_output_index((self.ssb_txing or self.ssb_txing_btn) and self.mode > 0)
        self.blocks_selector_2.set_input_index(self.mode_to_audio_input[self.mode])
        self.epy_block_1_0.attack = self.vox_attack[self.mode]
        self.epy_block_1_0.delay = self.vox_delay[self.mode]
        self.epy_block_1_0.threshold = self.vox_threshold[self.mode]

    def get_current_min_fq(self):
        return self.current_min_fq

    def set_current_min_fq(self, current_min_fq):
        self.current_min_fq = current_min_fq
        Qt.QMetaObject.invokeMethod(self._current_min_fq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.current_min_fq)))
        self.set_f0(self.current_min_fq + (self.current_max_fq - self.current_min_fq)/2.0)

    def get_current_max_fq(self):
        return self.current_max_fq

    def set_current_max_fq(self, current_max_fq):
        self.current_max_fq = current_max_fq
        Qt.QMetaObject.invokeMethod(self._current_max_fq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.current_max_fq)))
        self.set_f0(self.current_min_fq + (self.current_max_fq - self.current_min_fq)/2.0)

    def get_current_default_fq(self):
        return self.current_default_fq

    def set_current_default_fq(self, current_default_fq):
        self.current_default_fq = current_default_fq
        Qt.QMetaObject.invokeMethod(self._current_default_fq_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.current_default_fq)))
        self._rx_fq_win_msgdigctl_win.setValue(self.current_default_fq)
        self.set_tx_center_fq(self.current_default_fq)
        self.rx_distancer.desired_fq = self.current_default_fq

    def get_tx_gain(self):
        return self.tx_gain

    def set_tx_gain(self, tx_gain):
        self.tx_gain = tx_gain
        self.set_tc_vga(self.tx_gain)
        self.soapy_hackrf_sink_0.set_gain(0, 'VGA', min(max(self.tx_gain, 0.0), 47.0))

    def get_tx_fq(self):
        return self.tx_fq

    def set_tx_fq(self, tx_fq):
        self.tx_fq = tx_fq
        self.set_tx_fq_q(int(self.tx_fq))
        self.soapy_hackrf_sink_0.set_frequency(0, self.tx_fq+self.tx_mode_offset[self.side_band_tx] + self.fq_calibration)

    def get_tx_center_fq(self):
        return self.tx_center_fq

    def set_tx_center_fq(self, tx_center_fq):
        self.tx_center_fq = tx_center_fq
        self._tx_fq_win_msgdigctl_win.setValue(self.tx_center_fq)

    def get_tx_bw_opts(self):
        return self.tx_bw_opts

    def set_tx_bw_opts(self, tx_bw_opts):
        self.tx_bw_opts = tx_bw_opts
        self.set_ssb_tx_bandwidth(self.tx_bw[self.tx_bw_opts])
        self._tx_bw_opts_callback(self.tx_bw_opts)
        self.set_tx_mode_offset([0, self.tx_bw[self.tx_bw_opts]/2, -self.tx_bw[self.tx_bw_opts]/2, 0, 0, self.tx_bw[self.tx_bw_opts]/2,self.tx_bw[self.tx_bw_opts]/2])
        self.soapy_hackrf_sink_0.set_bandwidth(0, self.tx_bw[self.tx_bw_opts])

    def get_tx_bw(self):
        return self.tx_bw

    def set_tx_bw(self, tx_bw):
        self.tx_bw = tx_bw
        self.set_ssb_tx_bandwidth(self.tx_bw[self.tx_bw_opts])
        self.set_tx_mode_offset([0, self.tx_bw[self.tx_bw_opts]/2, -self.tx_bw[self.tx_bw_opts]/2, 0, 0, self.tx_bw[self.tx_bw_opts]/2,self.tx_bw[self.tx_bw_opts]/2])
        self.soapy_hackrf_sink_0.set_bandwidth(0, self.tx_bw[self.tx_bw_opts])

    def get_ssb_txing(self):
        return self.ssb_txing

    def set_ssb_txing(self, ssb_txing):
        self.ssb_txing = ssb_txing
        self.set_txing(self.cw_txing or self.ssb_txing)
        self.blocks_selector_0.set_output_index((self.ssb_txing or self.ssb_txing_btn) and self.mode > 0)
        self.qtgui_ledindicator_0_0.setState((self.ssb_txing or self.ssb_txing_btn or self.cw_txing))

    def get_side_band_rx(self):
        return self.side_band_rx

    def set_side_band_rx(self, side_band_rx):
        self.side_band_rx = side_band_rx
        self.set_side_band_dislay(self.side_band_rx)
        self.set_variable_qtgui_entry_0(self.side_band_rx)
        self.blocks_multiply_const_vxx_4_0.set_k(self.lsb_chain_gain[self.side_band_rx])
        self.blocks_multiply_const_vxx_4_0_0.set_k(self.usb_chain_gain[self.side_band_rx])
        self.blocks_multiply_matrix_xx_0.set_A(self.af_mix_matrices[self.side_band_rx])
        self.freq_xlating_fft_filter_ccc_1.set_center_freq(self.filter_fq+self.cw_midear_beat[self.side_band_rx])
        self.freq_xlating_fft_filter_ccc_1_0.set_center_freq(self.filter_fq-self.cw_midear_beat[self.side_band_rx])
        self.qtgui_sink_x_0.set_frequency_range(self.fft_corr[self.side_band_rx], self.rx_samp_rate)

    def get_rx_samp_rate(self):
        return self.rx_samp_rate

    def set_rx_samp_rate(self, rx_samp_rate):
        self.rx_samp_rate = rx_samp_rate
        self.set_if0_samp_rate(self.rx_samp_rate)
        self._rx_samp_rate_callback(self.rx_samp_rate)
        self.freq_xlating_fft_filter_ccc_1.set_taps(firdes.low_pass(1,self.rx_samp_rate,self.rx_samp_rate/(2*1),4000))
        self.freq_xlating_fft_filter_ccc_1_0.set_taps(firdes.low_pass(1,self.rx_samp_rate,self.rx_samp_rate/(2*1),4000))
        self.pfb_decimator_ccf_0_0.set_taps(firdes.low_pass(1,self.rx_samp_rate/2, 3900,100))
        self.pfb_decimator_ccf_0_0_0.set_taps(firdes.low_pass(1,self.rx_samp_rate/2, 3900,100))
        self.qtgui_sink_x_0.set_frequency_range(self.fft_corr[self.side_band_rx], self.rx_samp_rate)
        self.rx_distancer.max_distance = self.rx_samp_rate/2.0
        self.soapy_hackrf_source_0.set_sample_rate(0, self.rx_samp_rate)

    def get_rx_hw_fq(self):
        return self.rx_hw_fq

    def set_rx_hw_fq(self, rx_hw_fq):
        self.rx_hw_fq = rx_hw_fq
        self.set_rx_ctr_fq(int(self.rx_hw_fq))
        self.set_wf_fq(self.freq+self.rx_hw_fq)
        self.epy_block_2.offset = self.rx_hw_fq + self.filter_fq
        self.rx_distancer.hw_var = self.rx_hw_fq
        self.soapy_hackrf_source_0.set_frequency(0, self.rx_hw_fq + self.fq_calibration)

    def get_mode_to_sb_tx(self):
        return self.mode_to_sb_tx

    def set_mode_to_sb_tx(self, mode_to_sb_tx):
        self.mode_to_sb_tx = mode_to_sb_tx
        self.set_side_band_tx(self.mode_to_sb_tx[self.mode])

    def get_mic_gain(self):
        return self.mic_gain

    def set_mic_gain(self, mic_gain):
        self.mic_gain = mic_gain
        self.set_mic_inpt_gain_0(self.mic_gain)
        self.blocks_multiply_const_vxx_1_0_0_0_0.set_k(self.mic_gain)

    def get_mgm_input_gain(self):
        return self.mgm_input_gain

    def set_mgm_input_gain(self, mgm_input_gain):
        self.mgm_input_gain = mgm_input_gain
        self.set_mgm_inpt_gain(self.mgm_input_gain)
        self.blocks_multiply_const_vxx_1_0_0_0.set_k(self.mgm_input_gain)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.set_wf_fq(self.freq+self.rx_hw_fq)

    def get_filter_fq(self):
        return self.filter_fq

    def set_filter_fq(self, filter_fq):
        self.filter_fq = filter_fq
        self.set_rx_ctr_fq_0(int(self.filter_fq))
        self.epy_block_2.offset = self.rx_hw_fq + self.filter_fq
        self.freq_xlating_fft_filter_ccc_1.set_center_freq(self.filter_fq+self.cw_midear_beat[self.side_band_rx])
        self.freq_xlating_fft_filter_ccc_1_0.set_center_freq(self.filter_fq-self.cw_midear_beat[self.side_band_rx])
        self.rx_distancer.filter_var = self.filter_fq

    def get_f0(self):
        return self.f0

    def set_f0(self, f0):
        self.f0 = f0
        self.set_rx_center_fq(self.f0-100e3)

    def get_cw_txing(self):
        return self.cw_txing

    def set_cw_txing(self, cw_txing):
        self.cw_txing = cw_txing
        self.set_txing(self.cw_txing or self.ssb_txing)
        self.qtgui_ledindicator_0_0.setState((self.ssb_txing or self.ssb_txing_btn or self.cw_txing))

    def get_wf_gain(self):
        return self.wf_gain

    def set_wf_gain(self, wf_gain):
        self.wf_gain = wf_gain
        self.blocks_multiply_const_vxx_4_0_0_0.set_k(self.wf_gain)

    def get_wf_fq(self):
        return self.wf_fq

    def set_wf_fq(self, wf_fq):
        self.wf_fq = wf_fq

    def get_vox_threshold(self):
        return self.vox_threshold

    def set_vox_threshold(self, vox_threshold):
        self.vox_threshold = vox_threshold
        self.epy_block_1_0.threshold = self.vox_threshold[self.mode]

    def get_vox_sensitivity(self):
        return self.vox_sensitivity

    def set_vox_sensitivity(self, vox_sensitivity):
        self.vox_sensitivity = vox_sensitivity
        self.blocks_multiply_const_vxx_1_0_0_1.set_k(self.vox_sensitivity)

    def get_vox_delay(self):
        return self.vox_delay

    def set_vox_delay(self, vox_delay):
        self.vox_delay = vox_delay
        self.epy_block_1_0.delay = self.vox_delay[self.mode]

    def get_vox_attack(self):
        return self.vox_attack

    def set_vox_attack(self, vox_attack):
        self.vox_attack = vox_attack
        self.epy_block_1_0.attack = self.vox_attack[self.mode]

    def get_vga_gain(self):
        return self.vga_gain

    def set_vga_gain(self, vga_gain):
        self.vga_gain = vga_gain
        self.soapy_hackrf_source_0.set_gain(0, 'VGA', min(max(self.vga_gain, 0.0), 62.0))

    def get_variable_qtgui_entry_0(self):
        return self.variable_qtgui_entry_0

    def set_variable_qtgui_entry_0(self, variable_qtgui_entry_0):
        self.variable_qtgui_entry_0 = variable_qtgui_entry_0
        Qt.QMetaObject.invokeMethod(self._variable_qtgui_entry_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.variable_qtgui_entry_0)))

    def get_variable_function_probe_0(self):
        return self.variable_function_probe_0

    def set_variable_function_probe_0(self, variable_function_probe_0):
        self.variable_function_probe_0 = variable_function_probe_0
        self.qtgui_levelgauge_0.setValue(self.variable_function_probe_0)

    def get_usb_chain_gain(self):
        return self.usb_chain_gain

    def set_usb_chain_gain(self, usb_chain_gain):
        self.usb_chain_gain = usb_chain_gain
        self.blocks_multiply_const_vxx_4_0_0.set_k(self.usb_chain_gain[self.side_band_rx])

    def get_txing(self):
        return self.txing

    def set_txing(self, txing):
        self.txing = txing

    def get_tx_samp_rate(self):
        return self.tx_samp_rate

    def set_tx_samp_rate(self, tx_samp_rate):
        self.tx_samp_rate = tx_samp_rate
        self.blocks_repeat_0_0.set_interpolation(int(self.tx_samp_rate/self.cw_samp_rate))
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.tx_samp_rate, self.ssb_tx_bandwidth, 50, window.WIN_RECTANGULAR, 6.76))
        self.soapy_hackrf_sink_0.set_sample_rate(0, self.tx_samp_rate)

    def get_tx_rprt(self):
        return self.tx_rprt

    def set_tx_rprt(self, tx_rprt):
        self.tx_rprt = tx_rprt
        Qt.QMetaObject.invokeMethod(self._tx_rprt_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_rprt)))
        self.msg_formatter_0.variables = (self.dx_call, self.tx_rprt, self.tx_rprt, self.tx_rprt, self.dx_call)
        self.msg_formatter_0_0.variables = (self.dx_call, self.tx_rprt, self.tx_rprt, self.tx_rprt, self.dx_call)
        self.msg_formatter_0_0_0.variables = (self.dx_call, self.tx_rprt, self.tx_rprt, self.tx_rprt, self.dx_call)

    def get_tx_mode_offset(self):
        return self.tx_mode_offset

    def set_tx_mode_offset(self, tx_mode_offset):
        self.tx_mode_offset = tx_mode_offset
        self.soapy_hackrf_sink_0.set_frequency(0, self.tx_fq+self.tx_mode_offset[self.side_band_tx] + self.fq_calibration)

    def get_tx_fq_win(self):
        return self.tx_fq_win

    def set_tx_fq_win(self, tx_fq_win):
        self.tx_fq_win = tx_fq_win

    def get_tx_fq_q(self):
        return self.tx_fq_q

    def set_tx_fq_q(self, tx_fq_q):
        self.tx_fq_q = tx_fq_q
        Qt.QMetaObject.invokeMethod(self._tx_fq_q_line_edit, "setText", Qt.Q_ARG("QString", str(self.tx_fq_q)))

    def get_tc_vga(self):
        return self.tc_vga

    def set_tc_vga(self, tc_vga):
        self.tc_vga = tc_vga
        Qt.QMetaObject.invokeMethod(self._tc_vga_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.tc_vga)))

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
        self.blocks_selector_0.set_output_index((self.ssb_txing or self.ssb_txing_btn) and self.mode > 0)
        self.qtgui_ledindicator_0_0.setState((self.ssb_txing or self.ssb_txing_btn or self.cw_txing))

    def get_ssb_tx_bandwidth(self):
        return self.ssb_tx_bandwidth

    def set_ssb_tx_bandwidth(self, ssb_tx_bandwidth):
        self.ssb_tx_bandwidth = ssb_tx_bandwidth
        self.analog_sig_source_x_0_0.set_frequency(self.ssb_tx_bandwidth/2)
        self.analog_sig_source_x_1_0.set_frequency(self.ssb_tx_bandwidth/2)
        self.filter_fft_low_pass_filter_0.set_taps(firdes.low_pass(1, self.tx_samp_rate, self.ssb_tx_bandwidth, 50, window.WIN_RECTANGULAR, 6.76))
        self.filter_fft_low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth/2-200, 50, window.WIN_HAMMING, 6.76))
        self.filter_fft_low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth/2-200, 50, window.WIN_HAMMING, 6.76))
        self.qtgui_sink_x_0_0_0.set_frequency_range(0, self.ssb_tx_bandwidth*4)

    def get_sq(self):
        return self.sq

    def set_sq(self, sq):
        self.sq = sq
        self.analog_simple_squelch_cc_0.set_threshold(self.sq)
        self.analog_simple_squelch_cc_0_0.set_threshold(self.sq)

    def get_split_fq(self):
        return self.split_fq

    def set_split_fq(self, split_fq):
        self.split_fq = split_fq
        self._split_fq_callback(self.split_fq)
        self.tx_fq_sync.gate_control = self.split_fq

    def get_spkr_gain(self):
        return self.spkr_gain

    def set_spkr_gain(self, spkr_gain):
        self.spkr_gain = spkr_gain
        self.blocks_multiply_const_vxx_1_0.set_k(self.spkr_gain *self.af_right)
        self.blocks_multiply_const_vxx_1_0_1_0.set_k(self.spkr_gain*(1-self.af_right))

    def get_side_band_tx(self):
        return self.side_band_tx

    def set_side_band_tx(self, side_band_tx):
        self.side_band_tx = side_band_tx
        self.analog_sig_source_x_0.set_frequency(self.cw_midear_beat[self.side_band_tx])
        self.blocks_selector_1.set_input_index(self.side_band_tx)
        self.soapy_hackrf_sink_0.set_frequency(0, self.tx_fq+self.tx_mode_offset[self.side_band_tx] + self.fq_calibration)

    def get_side_band_dislay(self):
        return self.side_band_dislay

    def set_side_band_dislay(self, side_band_dislay):
        self.side_band_dislay = side_band_dislay
        Qt.QMetaObject.invokeMethod(self._side_band_dislay_line_edit, "setText", Qt.Q_ARG("QString", str(self.side_band_dislay)))

    def get_sb_t(self):
        return self.sb_t

    def set_sb_t(self, sb_t):
        self.sb_t = sb_t

    def get_sb_r(self):
        return self.sb_r

    def set_sb_r(self, sb_r):
        self.sb_r = sb_r

    def get_rx_preamp(self):
        return self.rx_preamp

    def set_rx_preamp(self, rx_preamp):
        self.rx_preamp = rx_preamp
        self._rx_preamp_callback(self.rx_preamp)
        self.soapy_hackrf_source_0.set_gain(0, 'AMP', self.rx_preamp)

    def get_rx_fq_win(self):
        return self.rx_fq_win

    def set_rx_fq_win(self, rx_fq_win):
        self.rx_fq_win = rx_fq_win

    def get_rx_fq(self):
        return self.rx_fq

    def set_rx_fq(self, rx_fq):
        self.rx_fq = rx_fq

    def get_rx_ctr_fq_0(self):
        return self.rx_ctr_fq_0

    def set_rx_ctr_fq_0(self, rx_ctr_fq_0):
        self.rx_ctr_fq_0 = rx_ctr_fq_0
        Qt.QMetaObject.invokeMethod(self._rx_ctr_fq_0_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_ctr_fq_0)))

    def get_rx_ctr_fq(self):
        return self.rx_ctr_fq

    def set_rx_ctr_fq(self, rx_ctr_fq):
        self.rx_ctr_fq = rx_ctr_fq
        Qt.QMetaObject.invokeMethod(self._rx_ctr_fq_line_edit, "setText", Qt.Q_ARG("QString", str(self.rx_ctr_fq)))

    def get_rx_center_fq(self):
        return self.rx_center_fq

    def set_rx_center_fq(self, rx_center_fq):
        self.rx_center_fq = rx_center_fq

    def get_rx_bw(self):
        return self.rx_bw

    def set_rx_bw(self, rx_bw):
        self.rx_bw = rx_bw
        self._rx_bw_callback(self.rx_bw)
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))

    def get_qtgui_levelgauge_0(self):
        return self.qtgui_levelgauge_0

    def set_qtgui_levelgauge_0(self, qtgui_levelgauge_0):
        self.qtgui_levelgauge_0 = qtgui_levelgauge_0
        self.qtgui_levelgauge_0.setValue(self.variable_function_probe_0)

    def get_morse_speed(self):
        return self.morse_speed

    def set_morse_speed(self, morse_speed):
        self.morse_speed = morse_speed
        self.blocks_repeat_0.set_interpolation(int(6* self.cw_samp_rate / self.morse_speed))
        self.epy_block_1.delay = 6/self.morse_speed * 25 + 2

    def get_monitor(self):
        return self.monitor

    def set_monitor(self, monitor):
        self.monitor = monitor
        self.blocks_multiply_const_vxx_0.set_k(self.monitor*0.0001*1000)

    def get_mode_to_audio_input(self):
        return self.mode_to_audio_input

    def set_mode_to_audio_input(self, mode_to_audio_input):
        self.mode_to_audio_input = mode_to_audio_input
        self.blocks_selector_2.set_input_index(self.mode_to_audio_input[self.mode])

    def get_mode_options(self):
        return self.mode_options

    def set_mode_options(self, mode_options):
        self.mode_options = mode_options

    def get_mode_labels_values(self):
        return self.mode_labels_values

    def set_mode_labels_values(self, mode_labels_values):
        self.mode_labels_values = mode_labels_values

    def get_mode_labels_keys(self):
        return self.mode_labels_keys

    def set_mode_labels_keys(self, mode_labels_keys):
        self.mode_labels_keys = mode_labels_keys

    def get_mode_display(self):
        return self.mode_display

    def set_mode_display(self, mode_display):
        self.mode_display = mode_display
        Qt.QMetaObject.invokeMethod(self._mode_display_line_edit, "setText", Qt.Q_ARG("QString", str(self.mode_display)))

    def get_mic_inpt_gain_0(self):
        return self.mic_inpt_gain_0

    def set_mic_inpt_gain_0(self, mic_inpt_gain_0):
        self.mic_inpt_gain_0 = mic_inpt_gain_0
        Qt.QMetaObject.invokeMethod(self._mic_inpt_gain_0_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.mic_inpt_gain_0)))

    def get_mgm_output_gain(self):
        return self.mgm_output_gain

    def set_mgm_output_gain(self, mgm_output_gain):
        self.mgm_output_gain = mgm_output_gain
        self.blocks_multiply_const_vxx_1_0_0.set_k(self.mgm_output_gain *self.af_right)
        self.blocks_multiply_const_vxx_1_0_1_0_0.set_k(self.mgm_output_gain*(1-self.af_right))

    def get_mgm_inpt_gain(self):
        return self.mgm_inpt_gain

    def set_mgm_inpt_gain(self, mgm_inpt_gain):
        self.mgm_inpt_gain = mgm_inpt_gain
        Qt.QMetaObject.invokeMethod(self._mgm_inpt_gain_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.mgm_inpt_gain)))

    def get_lsb_chain_gain(self):
        return self.lsb_chain_gain

    def set_lsb_chain_gain(self, lsb_chain_gain):
        self.lsb_chain_gain = lsb_chain_gain
        self.blocks_multiply_const_vxx_4_0.set_k(self.lsb_chain_gain[self.side_band_rx])

    def get_lna_gain(self):
        return self.lna_gain

    def set_lna_gain(self, lna_gain):
        self.lna_gain = lna_gain
        self.soapy_hackrf_source_0.set_gain(0, 'LNA', min(max(self.lna_gain, 0.0), 40.0))

    def get_if_samp_rate(self):
        return self.if_samp_rate

    def set_if_samp_rate(self, if_samp_rate):
        self.if_samp_rate = if_samp_rate
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))

    def get_if2_samp_rate(self):
        return self.if2_samp_rate

    def set_if2_samp_rate(self, if2_samp_rate):
        self.if2_samp_rate = if2_samp_rate

    def get_if0_samp_rate(self):
        return self.if0_samp_rate

    def set_if0_samp_rate(self, if0_samp_rate):
        self.if0_samp_rate = if0_samp_rate

    def get_ham_bands_keys(self):
        return self.ham_bands_keys

    def set_ham_bands_keys(self, ham_bands_keys):
        self.ham_bands_keys = ham_bands_keys

    def get_fq_calibration(self):
        return self.fq_calibration

    def set_fq_calibration(self, fq_calibration):
        self.fq_calibration = fq_calibration
        self.soapy_hackrf_sink_0.set_frequency(0, self.tx_fq+self.tx_mode_offset[self.side_band_tx] + self.fq_calibration)
        self.soapy_hackrf_source_0.set_frequency(0, self.rx_hw_fq + self.fq_calibration)

    def get_fft_corr(self):
        return self.fft_corr

    def set_fft_corr(self, fft_corr):
        self.fft_corr = fft_corr
        self.qtgui_sink_x_0.set_frequency_range(self.fft_corr[self.side_band_rx], self.rx_samp_rate)

    def get_f0_min(self):
        return self.f0_min

    def set_f0_min(self, f0_min):
        self.f0_min = f0_min

    def get_dx_call(self):
        return self.dx_call

    def set_dx_call(self, dx_call):
        self.dx_call = dx_call
        Qt.QMetaObject.invokeMethod(self._dx_call_line_edit, "setText", Qt.Q_ARG("QString", str(self.dx_call)))
        self.msg_formatter.variables = (self.dx_call)
        self.msg_formatter_0.variables = (self.dx_call, self.tx_rprt, self.tx_rprt, self.tx_rprt, self.dx_call)
        self.msg_formatter_0_0.variables = (self.dx_call, self.tx_rprt, self.tx_rprt, self.tx_rprt, self.dx_call)
        self.msg_formatter_0_0_0.variables = (self.dx_call, self.tx_rprt, self.tx_rprt, self.tx_rprt, self.dx_call)

    def get_cw_samp_rate(self):
        return self.cw_samp_rate

    def set_cw_samp_rate(self, cw_samp_rate):
        self.cw_samp_rate = cw_samp_rate
        self.blocks_repeat_0.set_interpolation(int(6* self.cw_samp_rate / self.morse_speed))
        self.blocks_repeat_0_0.set_interpolation(int(self.tx_samp_rate/self.cw_samp_rate))
        self.root_raised_cosine_filter_0.set_taps(firdes.root_raised_cosine(1, self.cw_samp_rate, self.symbol_rate, 0.35, 200))
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(self.cw_level, self.cw_samp_rate, self.symbol_rate, 0.35, 200))

    def get_cw_midear_beat(self):
        return self.cw_midear_beat

    def set_cw_midear_beat(self, cw_midear_beat):
        self.cw_midear_beat = cw_midear_beat
        self.analog_sig_source_x_0.set_frequency(self.cw_midear_beat[self.side_band_tx])
        self.freq_xlating_fft_filter_ccc_1.set_center_freq(self.filter_fq+self.cw_midear_beat[self.side_band_rx])
        self.freq_xlating_fft_filter_ccc_1_0.set_center_freq(self.filter_fq-self.cw_midear_beat[self.side_band_rx])

    def get_cw_level(self):
        return self.cw_level

    def set_cw_level(self, cw_level):
        self.cw_level = cw_level
        self.blocks_multiply_const_vxx_0_0.set_k(self.cw_level)
        self.root_raised_cosine_filter_0_0.set_taps(firdes.root_raised_cosine(self.cw_level, self.cw_samp_rate, self.symbol_rate, 0.35, 200))

    def get_current_allowed_tx_bandwidth(self):
        return self.current_allowed_tx_bandwidth

    def set_current_allowed_tx_bandwidth(self, current_allowed_tx_bandwidth):
        self.current_allowed_tx_bandwidth = current_allowed_tx_bandwidth
        Qt.QMetaObject.invokeMethod(self._current_allowed_tx_bandwidth_line_edit, "setText", Qt.Q_ARG("QString", eng_notation.num_to_str(self.current_allowed_tx_bandwidth)))

    def get_cq_flavor(self):
        return self.cq_flavor

    def set_cq_flavor(self, cq_flavor):
        self.cq_flavor = cq_flavor
        Qt.QMetaObject.invokeMethod(self._cq_flavor_line_edit, "setText", Qt.Q_ARG("QString", str(self.cq_flavor)))
        self.msg_formatter_1.variables = (self.cq_flavor, self.cq_flavor, self.cq_flavor, self.cq_flavor)

    def get_channel_separation(self):
        return self.channel_separation

    def set_channel_separation(self, channel_separation):
        self.channel_separation = channel_separation

    def get_bpf_low(self):
        return self.bpf_low

    def set_bpf_low(self, bpf_low):
        self.bpf_low = bpf_low
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))

    def get_bpf_high(self):
        return self.bpf_high

    def set_bpf_high(self, bpf_high):
        self.bpf_high = bpf_high
        self.band_pass_filter_0_0.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))
        self.band_pass_filter_0_1.set_taps(firdes.complex_band_pass(1, self.if_samp_rate, self.bpf_low[self.rx_bw], self.bpf_high[self.rx_bw], 100, window.WIN_BLACKMAN, 6.76))

    def get_audio_samp_rate(self):
        return self.audio_samp_rate

    def set_audio_samp_rate(self, audio_samp_rate):
        self.audio_samp_rate = audio_samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.audio_samp_rate)
        self.analog_sig_source_x_1_0.set_sampling_freq(self.audio_samp_rate)
        self.band_pass_filter_0.set_taps(firdes.band_pass(1, self.audio_samp_rate, 200, 2700, 100, window.WIN_HAMMING, 6.76))
        self.filter_fft_low_pass_filter_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth/2-200, 50, window.WIN_HAMMING, 6.76))
        self.filter_fft_low_pass_filter_0_0_0.set_taps(firdes.low_pass(1, self.audio_samp_rate, self.ssb_tx_bandwidth/2-200, 50, window.WIN_HAMMING, 6.76))

    def get_af_right(self):
        return self.af_right

    def set_af_right(self, af_right):
        self.af_right = af_right
        self.blocks_multiply_const_vxx_1_0.set_k(self.spkr_gain *self.af_right)
        self.blocks_multiply_const_vxx_1_0_0.set_k(self.mgm_output_gain *self.af_right)
        self.blocks_multiply_const_vxx_1_0_1_0.set_k(self.spkr_gain*(1-self.af_right))
        self.blocks_multiply_const_vxx_1_0_1_0_0.set_k(self.mgm_output_gain*(1-self.af_right))

    def get_af_mix_matrices(self):
        return self.af_mix_matrices

    def set_af_mix_matrices(self, af_mix_matrices):
        self.af_mix_matrices = af_mix_matrices
        self.blocks_multiply_matrix_xx_0.set_A(self.af_mix_matrices[self.side_band_rx])

    def get_RX_power_offset_dB(self):
        return self.RX_power_offset_dB

    def set_RX_power_offset_dB(self, RX_power_offset_dB):
        self.RX_power_offset_dB = RX_power_offset_dB




def main(top_block_cls=FBQ_xcvr, options=None):
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print("Error: failed to enable real-time scheduling.")

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()
    snippets_main_after_init(tb)
    tb.start()
    snippets_main_after_start(tb)
    tb.setStyleSheetFromFile("/Users/bernerus/priv/proj/sdr/grc/FBQ_xcvr.qss")
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
