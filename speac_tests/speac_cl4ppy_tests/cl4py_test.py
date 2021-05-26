import glob
import unittest

import cl4py
import os

import coverage

from speac_library.speac.chopin_33_3 import CHOPIN_33_3
from speac_library.speac.speac_settings import SpeacSettings
from speac_library.speac.top_level import get_the_levels

lisp = cl4py.Lisp()
cl = lisp.function("find-package")("CL")


def load_files():
    path = os.path.join(os.path.dirname(__file__), "lisp_files/*.lisp")
    print(path)

    for file_name in glob.glob(path):
        file_name = file_name.replace("\\", "/")
        lisp.eval(("load", '"' + file_name + '"'))
        print(file_name, " is loaded")


def cl4py_elements_to_python(cl4py_element):
    if isinstance(cl4py_element, cl4py.Symbol):
        return str(cl4py_element.name).lower()

    elif isinstance(cl4py_element, cl4py.Cons):
        result = []
        for element in cl4py_element:
            result.append(cl4py_elements_to_python(element))
        return result

    else:
        return cl4py_element


def set_lisp_variable(variable_name, number):
    lisp.eval(("setq", variable_name, number))
    print("Lisp variable " + variable_name + " = ", number)


class BindingsTest(unittest.TestCase):

    def test_all(self):
        cov = coverage.Coverage()
        cov.start()

        load_files()

        self.test_get_the_levels()

        print("\n")
        cov.stop()
        cov.save()
        cov.report(show_missing=True, include="*/speac/*")

    def test_get_the_levels(self):
        python_input = CHOPIN_33_3
        lisp_input = "chopin-33-3"

        meter = 4
        beat = 1000
        cadence_minimum = 9000
        intervals_off = 2
        measures = 8
        threshold = 2
        pattern_size = 12
        amount_off = 1
        matching_line = 1

        speac_settings = SpeacSettings()
        speac_settings.set_beat(beat)
        speac_settings.set_cadence_minimum(cadence_minimum)
        speac_settings.set_intervals_off(intervals_off)
        speac_settings.set_measures(measures)
        speac_settings.set_threshold(threshold)
        speac_settings.set_pattern_size(pattern_size)
        speac_settings.set_amount_off(amount_off)
        speac_settings.set_matching_line(matching_line)

        set_lisp_variable("*meter*", meter)
        set_lisp_variable("*beat*", beat)
        set_lisp_variable("*cadence_minimum*", cadence_minimum)
        set_lisp_variable("*intervals_off*", intervals_off)
        set_lisp_variable("*measures*", measures)
        set_lisp_variable("*threshold*", threshold)
        set_lisp_variable("*pattern_size*", pattern_size)
        set_lisp_variable("*amount_off*", amount_off)
        set_lisp_variable("*matching_line*", matching_line)

        try:
            lisp_eval = lisp.eval(("get-the-levels", lisp_input))
            lisp_result = cl4py_elements_to_python(lisp_eval)

        except Exception as lisp_exception:
            lisp_result = "Error"
            print("++++++++++++++++++++++++++++++++++++++++++")
            print("Exception in Lisp result:", lisp_exception)
            print("++++++++++++++++++++++++++++++++++++++++++")

        try:
            python_result = get_the_levels(python_input, meter, speac_settings)

        except Exception as python_exception:
            python_result = "Error"
            print("Exception in Python result: ", python_exception)

        print("  Lisp input = ", lisp_input, "\nPython input = ", python_input,
              "\n  Lisp result = ", lisp_result, "\nPython result = ", python_result)

        try:
            self.assertEqual(python_result, lisp_result)
        except AssertionError:
            raise AssertionError("Data aren't equal")


if __name__ == '__main__':
    test = BindingsTest()
    test.test_all()
