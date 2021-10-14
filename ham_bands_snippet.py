self.ham_bands = {
    '50-CW':    (50000000,   50100000,   50090000,    500, ['CW']),
    '50-SSB':   (50100000,   50300000,   50150000,   2700, ['CW', 'SSB']),
    '50-FT8':   (50300000,   50400000,   50313000,   2700, ['FT8']),
    '50-PSK':   (50300000,   50400000,   50305000,   2700, ['PSK']),
    '50-MSK':   (50300000,   50400000,   50350000,   2700, ['MSK']),
    '50-B':     (50400000,   50500000,   50450000,   1000, []),  # Beacons only
    '50-FM':    (50500000,   52000000,   51510000,  12000, ['FM', 'CW', 'SSB']),
    '87-FM':    (87500000,  108000000,   89300000, 200000, []),  # FM broadcast
    '144-SAT':  (144000000, 144025000,  144010000,   2700, []),  # Sat downlink,
    '144-CW':   (144025000, 144100000,  144050000,    500, ['CW']),
    '144-MGM':  (144100000, 144150000,  144116000,    500, ['CW', 'Q65', 'JT65']),
    '144-Q65':  (144100000, 144150000,  144125000,    500, ['Q65']),
    '144-JT65': (144100000, 144150000,  144120000,    500, ['JT65']),
    '144-FT8':  (144150000, 144400000,  144174000,   2700, ['FT8']),
    '144-SSB':  (144150000, 144400000,  144300000,   2700, ['CW', 'SSB', 'FT8', 'JT65', 'Q65']),
    '144-MSK':  (144150000, 144400000,  144360000,   2700, ['MSK']),
    '144-B':    (144400000, 144490000,  144406000,    500, []),  # Beacons
    '144-PB':   (144491000, 144493000,  144492000,    500, ['CW', 'FT8']),  # Personal beacons
    '432-EME':  (432000000, 432025000,  432010000,    500, ['CW']),
    '432-CW':   (432025000, 432100000,  432050000,    500, ['CW','PSK']),
    '432-SSB':  (432100000, 432400000,  432200000,   2700, ['CW', 'SSB']),
    '432-FSK':  (432100000, 432400000,  432370000,   2700, ['CW', 'SSB', 'FSK441']),
    '432-B':    (432400000, 432490000,  432412170,    500, []), # Beacons 70cm / SK6UHF
    '1296-B':  (1296800000, 1296994000,1296811000,    500, []), # Beacons 23cm



}
self.ham_bands_keys = list(self.ham_bands)
self._band_selector_options = self.ham_bands_keys
self._band_selector_labels = self.ham_bands_keys

self._band_selector_combo_box.setMinimumContentsLength(10)
self._band_selector_combo_box.removeItem(0)
for _label in self._band_selector_labels: self._band_selector_combo_box.addItem(_label)
self._band_selector_callback = lambda i: Qt.QMetaObject.invokeMethod(self._band_selector_combo_box, "setCurrentIndex", Qt.Q_ARG("int", self._band_selector_options.index(i)))
self._band_selector_combo_box.currentIndexChanged.connect(
    lambda i: self.set_band_selector(self._band_selector_options[i]))
