import unittest

from speac_library.speac.speac_analysis import *

BOOK_EXAMPLE = [[0, 45, 1000, 4, 55], [0, 64, 1000, 3, 55], [0, 69, 1000, 2, 55], [0, 73, 1000, 1, 55],
                [1000, 57, 1000, 4, 55], [1000, 64, 1000, 3, 55], [1000, 69, 1000, 2, 55], [1000, 73, 500, 1, 55],
                [1500, 74, 500, 1, 55], [2000, 56, 1000, 4, 55], [2000, 64, 1000, 3, 55], [2000, 71, 1000, 2, 55],
                [2000, 76, 1000, 1, 55], [3000, 57, 1000, 4, 55], [3000, 64, 1000, 3, 55], [3000, 69, 1000, 2, 55],
                [3000, 73, 1000, 1, 55], [4000, 54, 1000, 4, 55], [4000, 64, 500, 3, 55], [4500, 62, 500, 3, 55],
                [4000, 69, 1000, 2, 55], [4000, 69, 1000, 1, 55], [5000, 55, 1000, 4, 55], [5000, 62, 1000, 3, 55],
                [5000, 67, 500, 2, 55], [5500, 66, 500, 2, 55], [5000, 71, 1000, 1, 55], [6000, 57, 1000, 4, 55],
                [6000, 57, 1000, 3, 55], [6000, 64, 1000, 2, 55], [6000, 73, 1000, 1, 55], [7000, 50, 1000, 4, 55],
                [7000, 57, 1000, 3, 55], [7000, 66, 1000, 2, 55], [7000, 74, 1000, 1, 55]]


class SPEAC_analysis_test(unittest.TestCase):
    def test_all(self):
        self.test_almost()
        self.test_develop_speac()
        self.test_run_speac()
        self.test_collect_beat()
        self.test_collect_beats()
        self.test_break_event()
        self.test_break_events_into_beats()
        self.test_capture_beats()


    def test_almost(self):
        self.assertEqual(False, almost(1.17, 1.37, 0.2))
        self.assertEqual(True, almost(1.1700001, 1.37, 0.2))
        self.assertEqual(False, almost(1.77, 1.97, 0.2))
        self.assertEqual(True, almost(1.26, 1.33, 0.2))
        self.assertEqual(False, almost(1.26, 1.5, 0.2))

    def test_develop_speac(self):
        weights = [0.56, 0.41, 0.78, 0.51, 1.33, 0.51, 1.26, 0.91]
        average = 0.73
        largest = 1.33
        smallest = 0.41
        result = ["preparation", "extension", "statement", "extension",
                  "antecedent", "consequent", "antecedent", "statement"]
        self.assertEqual(result, develop_speac(weights, average, largest, smallest))

    def test_run_speac(self):
        weights = [1.17, 1.25, 1.06, 0.65, 1.9100001, 1.3, 0.96000004, 0.48000002, 1.97, 1.1999999, 1.77,
                   1.3, 1.76, 1.95, 0.64, 1.225, 0.120000005, 1.25, 1.37, 1.1700001, 1.17, 2.07, 1.55,
                   0.84000003, 2.9099998]
        result = ["preparation", "extension", "extension", "statement", "extension", "extension",
                  "extension", "extension", "extension", "extension", "extension", "extension",
                  "preparation", "extension", "statement", "extension", "extension", "preparation",
                  "extension", "extension", "extension", "statement", "extension", "extension",
                  "antecedent"]
        self.assertEqual(result, run_speac(weights, 1.32))

        weights = [1.17, 1.25, 1.06, 0.98, 1.36, 1.3, 0.96000004, 0.48000002, 1.97, 1.1999999, 1.77, 1.3,
                   1.76, 1.95, 0.64, 1.225, 0.67]
        result = ["preparation", "extension", "extension", "extension", "preparation", "extension",
                  "statement", "extension", "antecedent", "statement", "extension", "extension",
                  "preparation", "extension", "statement", "extension", "extension"]
        self.assertEqual(result, run_speac(weights, 1.24))

        weights = [1.41, 1.29, 1.66, 1.55, 0.7, 2.6399999, 0.46, 0.61, 1.27, 1.55, 1.06, 3.47, 2.8, 1.27, 0.93,
                   2.22, 1.39, 2.4399998, 1.0, 0.67499995, 1.56, 1.24, 1.1500001]
        result = ["preparation", "extension", "preparation", "extension", "statement", "extension",
                  "preparation", "extension", "statement", "extension", "extension", "antecedent",
                  "statement", "extension", "extension", "extension", "extension", "extension",
                  "extension", "extension", "extension", "preparation", "extension"]
        self.assertEqual(result, run_speac(weights, 1.49))

        weights = [0.56, 0.41, 0.78, 0.51, 1.33, 0.51, 1.26, 0.91]
        average = 0.73
        result = ["preparation", "extension", "statement", "extension",
                  "antecedent", "consequent", "antecedent", "statement"]
        self.assertEqual(result, run_speac(weights, average))

    def test_collect_beat(self):
        self.assertEqual([[4100, 45, 1000, 4, 55], [5000, 45, 1000, 4, 55]],
                         collect_beat(6000, [[4100, 45, 1000, 4, 55], [5000, 45, 1000, 4, 55]]))
        input = [[5000, 55, 1000, 4, 55], [6000, 55, 1000, 4, 55], [7000, 55, 1000, 4, 55], [8000, 55, 1000, 4, 55]]
        result = [[5000, 55, 1000, 4, 55], [6000, 55, 1000, 4, 55]]
        self.assertEqual(result, collect_beat(7000, input))

    def test_collect_beats(self):
        input = [[0, 45, 1000, 4, 55],
                 [2100, 45, 1000, 4, 55], [3000, 45, 1000, 4, 55],
                 [4100, 45, 1000, 4, 55], [5000, 45, 1000, 4, 55]]

        beat = 2000

        expected = [[[0, 45, 1000, 4, 55]], [[2100, 45, 1000, 4, 55], [3000, 45, 1000, 4, 55]],
                    [[4100, 45, 1000, 4, 55], [5000, 45, 1000, 4, 55]]]
        result = collect_beats(input, beat)
        self.assertEqual(expected, result)

        input = [[0, 45, 1000, 4, 55],
                 [2005, 45, 1000, 4, 55], [2099, 45, 1000, 4, 55], [2100, 45, 1000, 3, 55],
                 [4100, 45, 1000, 4, 55]]

        expected = [[[0, 45, 1000, 4, 55]],
                    [[2005, 45, 1000, 4, 55], [2099, 45, 1000, 4, 55]],
                    [[2100, 45, 1000, 3, 55]],
                    [[4100, 45, 1000, 4, 55]]]
        self.assertEqual(expected, collect_beats(input, 100))

    def test_break_event(self):
        event = [7000, 57, 1000, 3, 55]
        result = [[7000, 57, 300, 3, 55], [7300, 57, 300, 3, 55],
                  [7600, 57, 300, 3, 55], [7900, 57, 100, 3, 55]]
        self.assertEqual(result, break_event(300, event))
        self.assertEqual([[7000, 57, 1000, 3, 55]], break_event(1000, [7000, 57, 1000, 3, 55]))
        self.assertEqual([[7000, 57, 999, 3, 55], [7999, 57, 1, 3, 55]], break_event(999, [7000, 57, 1000, 3, 55]))

    def test_break_events_into_beats(self):
        events = [[7000, 57, 1000, 3, 55], [8000, 57, 600, 3, 55]]
        result = [[7000, 57, 500, 3, 55], [7500, 57, 500, 3, 55],
                  [8000, 57, 500, 3, 55], [8500, 57, 100, 3, 55]]
        self.assertEqual(result, break_events_into_beats(500, events))

    def test_capture_beats(self):
        result = [[[0, 45, 777, 4, 55], [0, 64, 777, 3, 55], [0, 69, 777, 2, 55], [0, 73, 777, 1, 55]],
                  [[777, 45, 223, 4, 55], [777, 64, 223, 3, 55], [777, 69, 223, 2, 55], [777, 73, 223, 1, 55],
                   [1000, 57, 777, 4, 55], [1000, 64, 777, 3, 55], [1000, 69, 777, 2, 55], [1000, 73, 500, 1, 55],
                   [1500, 74, 500, 1, 55]],
                  [[1777, 57, 223, 4, 55], [1777, 64, 223, 3, 55], [1777, 69, 223, 2, 55], [2000, 56, 777, 4, 55],
                   [2000, 64, 777, 3, 55], [2000, 71, 777, 2, 55], [2000, 76, 777, 1, 55]],
                  [[2777, 56, 223, 4, 55], [2777, 64, 223, 3, 55], [2777, 71, 223, 2, 55], [2777, 76, 223, 1, 55],
                   [3000, 57, 777, 4, 55], [3000, 64, 777, 3, 55], [3000, 69, 777, 2, 55], [3000, 73, 777, 1, 55]],
                  [[3777, 57, 223, 4, 55], [3777, 64, 223, 3, 55], [3777, 69, 223, 2, 55], [3777, 73, 223, 1, 55]],
                  [[4000, 54, 777, 4, 55], [4000, 64, 500, 3, 55], [4000, 69, 777, 2, 55], [4000, 69, 777, 1, 55],
                   [4500, 62, 500, 3, 55]],
                  [[4777, 54, 223, 4, 55], [4777, 69, 223, 2, 55], [4777, 69, 223, 1, 55], [5000, 55, 777, 4, 55],
                   [5000, 62, 777, 3, 55], [5000, 67, 500, 2, 55], [5000, 71, 777, 1, 55]],
                  [[5500, 66, 500, 2, 55], [5777, 55, 223, 4, 55], [5777, 62, 223, 3, 55], [5777, 71, 223, 1, 55],
                   [6000, 57, 777, 4, 55], [6000, 57, 777, 3, 55], [6000, 64, 777, 2, 55], [6000, 73, 777, 1, 55]],
                  [[6777, 57, 223, 4, 55], [6777, 57, 223, 3, 55], [6777, 64, 223, 2, 55], [6777, 73, 223, 1, 55]],
                  [[7000, 50, 777, 4, 55], [7000, 57, 777, 3, 55], [7000, 66, 777, 2, 55], [7000, 74, 777, 1, 55]],
                  [[7777, 50, 223, 4, 55], [7777, 57, 223, 3, 55], [7777, 66, 223, 2, 55], [7777, 74, 223, 1, 55]]]

        self.assertEqual(result, capture_beats(BOOK_EXAMPLE, 777))