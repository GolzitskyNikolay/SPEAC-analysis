class SpeacSettings:
    # variables from new_form file
    BEAT = 1000

    def set_beat(self, number):
        self.BEAT = number

    CADENCE_MINIMUM = 9000

    def set_cadence_minimum(self, number):
        self.CADENCE_MINIMUM = number

    INTERVALS_OFF = 2

    def set_intervals_off(self, number):
        self.INTERVALS_OFF = number

    MEASURES = 8

    def set_measures(self, number):
        self.MEASURES = number

    # variables from pattern_match file
    THRESHOLD = 2

    def set_threshold(self, number):
        self.THRESHOLD = number

    PATTERN_SIZE = 12

    def set_pattern_size(self, number):
        self.PATTERN_SIZE = number

    AMOUNT_OFF = 1

    def set_amount_off(self, number):
        self.AMOUNT_OFF = number

    MATCHING_LINE = 1

    def set_matching_line(self, number):
        self.MATCHING_LINE = number
