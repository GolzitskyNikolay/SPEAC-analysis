import unittest

from Tests.speac_chapter_7_tests.chopin_67_4 import CHOPIN_67_4
from Tests.speac_chapter_7_tests.chopin_63_2 import CHOPIN_63_2
from Tests.speac_chapter_7_tests.chopin_33_3 import CHOPIN_33_3
from speac_chapter_7.pattern_match import set_pattern_size
from speac_chapter_7.top_level import *

BOOK_EXAMPLE = [[0, 45, 1000, 4, 55], [0, 64, 1000, 3, 55], [0, 69, 1000, 2, 55], [0, 73, 1000, 1, 55],
                [1000, 57, 1000, 4, 55], [1000, 64, 1000, 3, 55], [1000, 69, 1000, 2, 55], [1000, 73, 500, 1, 55],
                [1500, 74, 500, 1, 55], [2000, 56, 1000, 4, 55], [2000, 64, 1000, 3, 55], [2000, 71, 1000, 2, 55],
                [2000, 76, 1000, 1, 55], [3000, 57, 1000, 4, 55], [3000, 64, 1000, 3, 55], [3000, 69, 1000, 2, 55],
                [3000, 73, 1000, 1, 55], [4000, 54, 1000, 4, 55], [4000, 64, 500, 3, 55], [4500, 62, 500, 3, 55],
                [4000, 69, 1000, 2, 55], [4000, 69, 1000, 1, 55], [5000, 55, 1000, 4, 55], [5000, 62, 1000, 3, 55],
                [5000, 67, 500, 2, 55], [5500, 66, 500, 2, 55], [5000, 71, 1000, 1, 55], [6000, 57, 1000, 4, 55],
                [6000, 57, 1000, 3, 55], [6000, 64, 1000, 2, 55], [6000, 73, 1000, 1, 55], [7000, 50, 1000, 4, 55],
                [7000, 57, 1000, 3, 55], [7000, 66, 1000, 2, 55], [7000, 74, 1000, 1, 55]]


class TopLevelTest(unittest.TestCase):

    def test_all(self):

        self.test_get_the_start_beat_number()
        self.test_get_length()
        self.test_do_speac_on_phrases()
        self.test_get_events_to()
        self.test_get_events_from()
        self.test_group_them()
        self.test_group_form()
        self.test_group_speac_lists()
        self.test_get_speac_middleground()
        self.test_get_speac_background()
        self.test_run_the_program()
        self.test_number_the_elements()
        self.test_create_the_window_levels()
        self.test_get_the_levels()

    def test_get_the_start_beat_number(self):
        events = [[21000, 55, 1000, 2, 64]]
        meter = 3
        self.assertEqual(1, get_the_start_beat_number(events, meter))

    def test_get_length(self):
        self.assertEqual(8000, get_length(BOOK_EXAMPLE))
        phrases = [[0, 55, 1000, 2, 64], [0, 65, 1000, 2, 64]]
        self.assertEqual(1000, get_length(phrases))

    def test_do_speac_on_phrases(self):
        set_pattern_size(12)
        form = eval_combine_and_integrate_forms(CHOPIN_33_3, 3)
        second_elements = []
        for i in range(1, len(form)):
            second_elements.append(form[i][1])
        phrased_events = break_into_phrases(CHOPIN_33_3, second_elements)

        result = [[["preparation", "extension", "extension", "extension", "preparation", "extension",
                    "statement", "extension", "extension", "extension", "antecedent", "preparation",
                    "extension", "statement", "antecedent", "statement"],
                   1.22],
                  [["preparation", "extension", "extension", "statement", "extension", "extension",
                    "extension", "extension", "extension", "extension", "extension", "extension",
                    "preparation", "extension", "statement", "extension", "extension", "preparation",
                    "extension", "extension", "extension", "statement", "extension", "extension",
                    "antecedent"],
                   1.32],
                  [["statement", "extension", "extension", "antecedent", "consequent", "statement",
                    "extension"],
                   1.15],
                  [["preparation", "extension", "preparation", "extension", "statement", "extension",
                    "preparation", "extension", "statement", "extension", "extension", "antecedent",
                    "statement", "extension", "extension", "extension", "extension", "extension",
                    "extension", "extension", "extension", "preparation", "extension"],
                   1.49],
                  [["preparation", "extension", "extension", "extension", "preparation", "extension",
                    "statement", "extension", "extension", "extension", "antecedent", "preparation",
                    "extension", "extension", "extension", "statement"],
                   1.22],
                  [["preparation", "extension", "extension", "extension", "preparation", "extension",
                    "statement", "extension", "antecedent", "statement", "extension", "extension",
                    "preparation", "extension", "statement", "extension", "extension"],
                   1.24]]

        self.assertEqual(result, do_speac_on_phrases(phrased_events, 3))

    def test_get_events_to(self):
        events = [[0, 1, 2, 3, 4], [0, 22, 33, 44, 55],
                  [500, 1, 2, 3, 4], [600, 1, 2, 3, 4]]
        time = 500
        result = [[0, 1, 2, 3, 4], [0, 22, 33, 44, 55]]
        self.assertEqual(result, get_events_to(time, events))

    def test_get_events_from(self):
        timings = 1000
        events = [[0, 23, 500, 1, 55], [0, 28, 500, 1, 55],
                  [1000, 45, 1000, 2, 56], [2500, 23, 500, 2, 34]]
        self.assertEqual([[1000, 45, 1000, 2, 56], [2500, 23, 500, 2, 34]], get_events_from(timings, events))

    def test_group_them(self):
        form = [["a", 10000], ["a", 21000], ["a", 33000]]
        result = [['a', 10000], ['a', 21000], ['a', 33000]]
        self.assertEqual(result, group_them(form))
        form = [["a", 10000], ["b", 21000], ["a", 33000]]
        result = [['a', 10000]]
        self.assertEqual(result, group_them(form))

    def test_group_form(self):
        form = [["a", 10000], ["a", 21000], ["b", 33000]]
        result = [[['a', 10000], ['a', 21000]], [['b', 33000]]]
        self.assertEqual(result, group_form(form))

    def test_group_speac_lists(self):
        set_pattern_size(2)
        form = eval_combine_and_integrate_forms(CHOPIN_33_3, 3)

        second_elements = []
        for i in range(1, len(form)):
            second_elements.append(form[i][1])

        phrased_events = break_into_phrases(CHOPIN_33_3, second_elements)
        speac_phrase_lists = do_speac_on_phrases(phrased_events, 3)
        grouped_form = group_form(form)
        result = [[[['preparation', 'extension'], 1.26]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 0.4],
                   [['statement'], 0.06],
                   [['statement', 'antecedent'], 1.13]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 0.75], [['preparation', 'extension'], 1.14]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 1.13],
                   [['statement'], 0.06],
                   [['statement', 'antecedent'], 0.9]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 0.68]],
                  [[['preparation', 'extension'], 1.26]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 0.77],
                   [['statement'], 0.06],
                   [['statement', 'antecedent'], 1.13]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 0.75], [['preparation', 'extension'], 1.26]],
                  [[['statement'], 0.16]],
                  [[['statement', 'antecedent'], 1.13], [['statement'], 0.06]],
                  [[['statement', 'antecedent'], 0.73]],
                  [[['statement', 'antecedent'], 0.58]],
                  [[['preparation', 'extension'], 0.17]],
                  [[['statement', 'antecedent'], 0.74], [['preparation', 'extension'], 0.72]],
                  [[['statement', 'antecedent'], 0.68]],
                  [[['antecedent', 'consequent'], 0.84],
                   [['statement', 'antecedent'], 1.78],
                   [['antecedent', 'consequent'], 1.33],
                   [['statement'], 0.15]],
                  [[['statement'], 1.7], [['statement'], 0.27], [['statement'], 0.37]],
                  [[['statement'], 0.32]],
                  [[['statement'], 1.37],
                   [['statement'], 0.27],
                   [['preparation', 'extension'], 1.61]],
                  [[['statement'], 0.32],
                   [['antecedent', 'consequent'], 1.2],
                   [['statement'], 0.38],
                   [['statement', 'extension'], 1.41],
                   [['statement'], 0.38],
                   [['preparation', 'extension'], 2.83],
                   [['preparation', 'extension'], 1.03],
                   [['statement', 'antecedent'], 1.0]],
                  [[['statement'], 0.4]],
                  [[['statement', 'antecedent'], 1.15]],
                  [[['antecedent', 'consequent'], 0.67]],
                  [[['statement', 'antecedent'], 0.85]],
                  [[['statement'], 0.44]],
                  [[['statement', 'antecedent'], 0.87], [['statement', 'antecedent'], 1.06]],
                  [[['statement'], 1.2], [['statement'], 0.38]],
                  [[['statement'], 0.43], [['statement'], 1.28]],
                  [[['statement'], 1.2],
                   [['statement'], 0.38],
                   [['statement', 'antecedent'], 1.03],
                   [['statement'], 1.2],
                   [['statement'], 1.15]],
                  [[['statement'], 1.2], [['statement'], 1.04]],
                  [[['statement'], 1.2]],
                  [[['statement'], 1.15]],
                  [[['preparation', 'extension'], 1.22]],
                  [[['statement'], 1.2], [['statement'], 0.38]],
                  [[['statement'], 0.43], [['statement'], 1.28]],
                  [[['statement'], 1.2],
                   [['statement'], 0.38],
                   [['statement', 'antecedent'], 1.24],
                   [['statement'], 1.2],
                   [['statement'], 1.15]],
                  [[['statement'], 1.2], [['statement'], 1.04]],
                  [[['statement'], 1.2]],
                  [[['statement', 'antecedent', 'statement'], 0.76]]]

        self.assertEqual(result, group_speac_lists(speac_phrase_lists, grouped_form))

    def test_get_speac_middleground(self):
        set_pattern_size(2)
        form = eval_combine_and_integrate_forms(CHOPIN_33_3, 3)

        second_elements = []
        for i in range(1, len(form)):
            second_elements.append(form[i][1])

        phrased_events = break_into_phrases(CHOPIN_33_3, second_elements)
        speac_phrase_lists = do_speac_on_phrases(phrased_events, 3)
        grouped_form = group_form(form)

        result = [[['statement'], 1.26],
                  [['statement'], 0.16],
                  [['statement', 'extension', 'antecedent'], 0.53],
                  [['statement'], 0.16],
                  [['statement', 'extension'], 0.94],
                  [['statement'], 0.16],
                  [['antecedent', 'consequent', 'statement'], 0.7],
                  [['statement'], 0.16],
                  [['statement'], 0.68],
                  [['statement'], 1.26],
                  [['statement'], 0.16],
                  [['statement', 'extension', 'antecedent'], 0.65],
                  [['statement'], 0.16],
                  [['statement', 'antecedent'], 1.0],
                  [['statement'], 0.16],
                  [['antecedent', 'consequent'], 0.6],
                  [['statement'], 0.73],
                  [['statement'], 0.58],
                  [['statement'], 0.17],
                  [['preparation', 'extension'], 0.73],
                  [['statement'], 0.68],
                  [['statement', 'antecedent', 'statement', 'extension'], 1.03],
                  [['antecedent', 'preparation', 'extension'], 0.78],
                  [['statement'], 0.32],
                  [['statement', 'extension', 'antecedent'], 1.08],
                  [['statement',
                    'extension',
                    'extension',
                    'extension',
                    'extension',
                    'antecedent',
                    'preparation',
                    'extension'],
                   1.07],
                  [['statement'], 0.4],
                  [['statement'], 1.15],
                  [['statement'], 0.67],
                  [['statement'], 0.85],
                  [['statement'], 0.44],
                  [['preparation', 'extension'], 0.97],
                  [['antecedent', 'consequent'], 0.79],
                  [['statement', 'antecedent'], 0.86],
                  [['antecedent', 'consequent', 'preparation', 'extension', 'extension'], 0.99],
                  [['preparation', 'extension'], 1.12],
                  [['statement'], 1.2],
                  [['statement'], 1.15],
                  [['statement'], 1.22],
                  [['antecedent', 'consequent'], 0.79],
                  [['statement', 'antecedent'], 0.86],
                  [['statement', 'extension', 'preparation', 'extension', 'extension'], 1.03],
                  [['preparation', 'extension'], 1.12],
                  [['statement'], 1.2],
                  [['statement'], 0.76]]

        self.assertEqual(result, get_speac_middleground(speac_phrase_lists, grouped_form))

        set_pattern_size(12)
        form = eval_combine_and_integrate_forms(CHOPIN_33_3, 3)

        second_elements = []
        for i in range(1, len(form)):
            second_elements.append(form[i][1])

        phrased_events = break_into_phrases(CHOPIN_33_3, second_elements)
        speac_phrase_lists = do_speac_on_phrases(phrased_events, 3)
        grouped_form = group_form(form)

        result = [[["preparation", "extension"], 1.27], [["statement", "extension"], 1.32],
                  [["preparation", "extension"], 1.23]]

        self.assertEqual(result, get_speac_middleground(speac_phrase_lists, grouped_form))

    def test_get_speac_background(self):
        input = [[["preparation", "extension"], 1.27], [["statement", "extension"], 1.32],
                 [["preparation", "extension"], 1.23]]
        result = [["preparation", "extension", "extension"], 1.27]
        self.assertEqual(result, get_speac_background(input))

        input = [[["preparation", "extension", "extension", "extension", "extension",
                   "extension", "antecedent", "preparation", "extension", "extension",
                   "extension", "statement"],
                  1.24]]
        result = [["statement"], 1.24]
        self.assertEqual(result, get_speac_background(input))

    def test_run_the_program(self):
        result = [[["statement"], 1.27], [["preparation", "extension", "extension"], 1.27],
                  [[["preparation", "extension"], 1.27], [["statement", "extension"], 1.32],
                   [["preparation", "extension"], 1.23]],
                  [[["preparation", "extension", "extension", "extension", "preparation", "extension",
                     "statement", "extension", "extension", "extension", "antecedent", "preparation",
                     "extension", "statement", "antecedent", "statement"],
                    1.22],
                   [["preparation", "extension", "extension", "statement", "extension", "extension",
                     "extension", "extension", "extension", "extension", "extension", "extension",
                     "preparation", "extension", "statement", "extension", "extension", "preparation",
                     "extension", "extension", "extension", "statement", "extension", "extension",
                     "antecedent"],
                    1.32],
                   [["statement", "extension", "extension", "antecedent", "consequent", "statement",
                     "extension"],
                    1.15],
                   [["preparation", "extension", "preparation", "extension", "statement", "extension",
                     "preparation", "extension", "statement", "extension", "extension", "antecedent",
                     "statement", "extension", "extension", "extension", "extension", "extension",
                     "extension", "extension", "extension", "preparation", "extension"],
                    1.49],
                   [["preparation", "extension", "extension", "extension", "preparation", "extension",
                     "statement", "extension", "extension", "extension", "antecedent", "preparation",
                     "extension", "extension", "extension", "statement"],
                    1.22],
                   [["preparation", "extension", "extension", "extension", "preparation", "extension",
                     "statement", "extension", "antecedent", "statement", "extension", "extension",
                     "preparation", "extension", "statement", "extension", "extension"],
                    1.24]],
                  [["a", 0, [2, -2, -2, -1, 1, 1, 1, 1, 1, -2, -2]],
                   ["a", 24000, [2, -2, -2, -1, 1, 1, 1, 1, 1, -2, -2]],
                   ["b", 56000], ["b", 67000], ["a", 96000, [2, -2, -2, -1, 1, 1, 1, 1, 1, -2, -2]],
                   ["a", 120000, [2, -2, -2, -1, 1, 1, 1, 1, 1, -2, -2]]]]

        set_pattern_size(12)
        self.assertEqual(result, run_the_program(CHOPIN_33_3, 3))

    def test_number_the_elements(self):
        levels = [[["c"]], [["a", "c"], ["e", "c"]], [["p", "a"], ["a", "a"], ["e", "e"]],
                  [["p", "p"], ["s", "p"], ["p", "a"], ["a", "a"], ["s", "e"], ["e", "e"]]]
        result = [[['c1']],
                  [['a2', 'c2'], ['e2', 'c2']],
                  [['p3', 'a3'], ['a3', 'a3'], ['e3', 'e3']],
                  [['p4', 'p4'],
                   ['s4', 'p4'],
                   ['p4', 'a4'],
                   ['a4', 'a4'],
                   ['s4', 'e4'],
                   ['e4', 'e4']]]
        self.assertEqual(result, number_the_elements(levels))

    def test_create_the_window_levels(self):
        input = run_the_program(CHOPIN_33_3, 3)
        result = [[["s"]], [["p", "e", "e"]], [["p", "e"], ["s", "e"], ["p", "e"]],
                  [["p", "e", "e", "e", "p", "e", "s", "e", "e", "e", "a", "p", "e", "s", "a", "s"],
                   ["p", "e", "e", "s", "e", "e", "e", "e", "e", "e", "e", "e", "p", "e", "s", "e", "e", "p", "e", "e",
                    "e", "s", "e", "e", "a"], ["s", "e", "e", "a", "c", "s", "e"],
                   ["p", "e", "p", "e", "s", "e", "p", "e", "s", "e", "e", "a", "s", "e", "e", "e", "e", "e", "e", "e",
                    "e", "p", "e"],
                   ["p", "e", "e", "e", "p", "e", "s", "e", "e", "e", "a", "p", "e", "e", "e", "s"],
                   ["p", "e", "e", "e", "p", "e", "s", "e", "a", "s", "e", "e", "p", "e", "s", "e", "e"]]]

        self.assertEqual(result, create_the_window_levels(input))

    def test_get_the_levels(self):
        result = [[["s1"]], [["p2", "e2", "e2"]], [["p3", "e3"], ["s3", "e3"], ["p3", "e3"]],
                  [["p4", "e4", "e4", "e4", "p4", "e4", "s4", "e4", "e4", "e4", "a4", "p4", "e4", "s4", "a4", "s4"],
                   ["p4", "e4", "e4", "s4", "e4", "e4", "e4", "e4", "e4", "e4", "e4", "e4", "p4", "e4", "s4", "e4",
                    "e4", "p4", "e4", "e4", "e4", "s4", "e4", "e4", "a4"],
                   ["s4", "e4", "e4", "a4", "c4", "s4", "e4"],
                   ["p4", "e4", "p4", "e4", "s4", "e4", "p4", "e4", "s4", "e4", "e4", "a4", "s4", "e4", "e4", "e4",
                    "e4",
                    "e4", "e4", "e4", "e4", "p4", "e4"],
                   ["p4", "e4", "e4", "e4", "p4", "e4", "s4", "e4", "e4", "e4", "a4", "p4", "e4", "e4", "e4", "s4"],
                   ["p4", "e4", "e4", "e4", "p4", "e4", "s4", "e4", "a4", "s4", "e4", "e4", "p4", "e4", "s4", "e4",
                    "e4"]]]

        self.assertEqual(result, get_the_levels(CHOPIN_33_3, 3))

        result = [[["s1"]], [
            ["s2", "a2", "p2", "e2", "a2", "p2", "e2", "a2", "p2", "e2", "a2", "p2", "e2", "e2", "a2", "p2", "e2", "a2",
             "p2", "e2"]],
                  [["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"],
                   ["s3"],
                   ["a3", "c3", "p3", "e3", "a3", "s3", "p3", "e3", "e3"], ["s3"], ["s3"], ["s3"], ["s3"], ["s3"],
                   ["s3"]],
                  [["s4", "e4", "e4", "e4", "e4", "e4", "e4", "e4", "p4", "e4", "p4", "e4", "p4", "e4", "e4", "s4",
                    "e4", "e4", "e4", "e4", "e4", "p4", "e4", "s4", "e4", "p4", "e4", "s4", "e4", "e4", "e4", "e4",
                    "e4",
                    "e4", "p4", "e4", "s4", "e4", "p4", "e4", "e4", "e4", "p4", "e4", "s4", "e4", "e4", "e4"],
                   ["s4", "e4", "e4", "p4", "e4", "a4", "s4", "e4"], ["s4", "p4", "e4", "a4", "c4", "p4", "e4", "s4"],
                   ["s4", "e4", "e4", "a4", "p4", "e4"],
                   ["s4", "p4", "e4", "s4", "e4", "a4", "s4", "e4"], ["s4", "p4", "e4", "a4", "c4", "s4", "e4"],
                   ["p4", "e4", "p4", "e4", "p4", "e4", "p4", "e4", "a4", "s4"],
                   ["s4", "e4", "e4", "p4", "e4", "a4", "s4", "e4"],
                   ["s4", "p4", "e4", "a4", "c4", "p4", "e4", "s4"], ["s4", "e4", "e4", "a4", "p4", "e4"],
                   ["s4", "p4", "e4", "s4", "e4", "a4", "s4", "e4"],
                   ["s4", "p4", "e4", "a4", "c4", "s4", "e4"],
                   ["p4", "e4", "p4", "e4", "p4", "e4", "p4", "e4", "a4", "s4", "e4", "e4", "e4", "e4", "e4", "p4",
                    "e4", "s4", "e4", "e4", "p4", "e4", "s4", "e4", "e4", "e4", "e4", "e4", "e4", "e4", "e4", "e4",
                    "e4", "a4"],
                   ["s4", "e4", "e4", "a4", "s4", "e4", "p4", "e4", "s4"],
                   ["p4", "e4", "s4", "e4", "e4", "a4", "p4", "e4", "p4", "e4", "e4"],
                   ["s4", "e4", "e4", "p4", "e4", "a4", "s4", "e4", "p4", "e4"],
                   ["p4", "e4", "s4", "e4", "e4", "e4", "a4", "s4", "e4", "e4"],
                   ["s4", "e4", "e4", "e4", "e4", "e4", "a4", "s4", "e4"],
                   ["p4", "e4", "s4", "p4", "e4", "s4", "e4", "e4", "a4", "p4", "e4", "s4"],
                   ["s4", "e4", "e4", "e4", "e4", "e4", "e4", "a4", "s4", "e4"],
                   ["p4", "e4", "p4", "e4", "p4", "e4", "p4", "e4", "e4", "s4", "e4"],
                   ["s4", "p4", "e4", "s4", "e4", "p4", "e4", "s4", "e4", "e4", "e4", "e4", "e4", "e4", "p4", "e4",
                    "s4", "e4", "p4", "e4", "e4", "e4", "p4", "e4", "s4", "e4", "e4", "e4", "p4", "e4"],
                   ["s4", "e4", "e4", "p4", "e4", "a4", "s4", "e4"], ["s4", "p4", "e4", "a4", "c4", "p4", "e4", "s4"],
                   ["s4", "e4", "e4", "a4", "p4", "e4"],
                   ["s4", "p4", "e4", "s4", "e4", "a4", "s4", "e4"], ["s4", "p4", "e4", "a4", "c4", "s4", "e4"],
                   ["p4", "e4", "p4", "e4", "p4", "e4", "p4", "e4", "a4", "s4"]]]

        self.assertEqual(result, get_the_levels(CHOPIN_67_4, 3))

        result = [[["s1"]], [["p2", "e2", "e2"]], [["p3", "e3"], ["s3", "p3", "e3", "s3"], ["p3", "e3"]],
                  [["p4", "e4", "e4", "e4", "s4", "e4", "e4", "e4", "p4", "e4", "p4", "e4", "e4", "s4", "e4", "e4",
                    "a4"],
                   ["p4", "e4", "e4", "e4", "s4", "e4", "e4", "p4", "e4", "s4", "e4", "p4", "e4", "p4", "e4", "e4",
                    "p4", "e4", "s4", "e4", "e4", "e4", "e4", "e4", "p4",
                    "e4", "s4", "e4", "a4"],
                   ["s4", "e4", "a4", "s4", "e4", "e4", "e4", "e4", "e4", "p4", "e4", "s4"],
                   ["p4", "e4", "s4", "e4", "e4", "p4", "e4", "s4", "e4", "a4"],
                   ["s4", "e4", "e4", "e4", "p4", "e4", "a4", "c4", "p4", "e4", "e4", "e4"],
                   ["p4", "e4", "e4", "s4", "p4", "e4", "p4", "e4", "a4", "p4", "e4", "e4", "s4", "e4", "a4", "s4",
                    "p4", "e4", "e4", "s4", "e4", "e4", "p4", "e4"],
                   ["s4", "e4", "e4", "e4", "e4", "a4", "c4", "s4", "p4", "e4", "p4", "e4", "e4", "s4", "e4", "e4",
                    "e4"],
                   ["p4", "e4", "e4", "e4", "s4", "e4", "e4", "p4", "e4", "a4", "s4", "p4", "e4", "p4", "e4", "e4",
                    "p4", "e4", "a4", "s4", "e4"]]]

        self.assertEqual(result, get_the_levels(CHOPIN_63_2, 3))
