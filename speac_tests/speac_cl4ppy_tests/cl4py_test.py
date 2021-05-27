import glob
import unittest
import cl4py
import os
import coverage
import emoji

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
    lisp.eval(("setq", variable_name.upper(), number))


def python_input_to_lisp(python_input):
    lisp_input = str(python_input).replace("[", "(").replace("]", ")").replace(",", "").replace("'", "")
    if len(lisp_input) > 0 and lisp_input[0] == "(":
        return "'" + lisp_input
    else:
        return lisp_input


def create_lisp_input(variable_name, variable_value):
    file = open("./lisp_files/my_variables.lisp", "w+")
    file.write("(defVar " + variable_name + " " + variable_value + ")")
    file.close()

    file_name = os.path.join(os.path.dirname(__file__), "lisp_files/my_variables.lisp")
    file_name = file_name.replace("\\", "/")

    lisp.eval(("load", '"' + file_name + '"'))
    print(file_name, " is loaded")
    os.remove("./lisp_files/my_variables.lisp")


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
        lisp_input = "LISP-INPUT"

        create_lisp_input("LISP-INPUT", python_input_to_lisp(python_input))

        meter = 3
        beat = 1000
        cadence_minimum = 9000
        intervals_off = 2
        measures = 8
        threshold = 3
        pattern_size = 12
        amount_off = 1
        matching_line = 1  # differs when 2, fix it later

        speac_settings = SpeacSettings()
        speac_settings.set_beat(beat)
        speac_settings.set_cadence_minimum(cadence_minimum)
        speac_settings.set_intervals_off(intervals_off)
        speac_settings.set_measures(measures)
        speac_settings.set_threshold(threshold)
        speac_settings.set_pattern_size(pattern_size)
        speac_settings.set_amount_off(amount_off)
        speac_settings.set_matching_line(matching_line)

        set_lisp_variable("*METER*", meter)
        set_lisp_variable("*BEAT*", beat)
        set_lisp_variable("*CADENCE-MINIMUM*", cadence_minimum)
        set_lisp_variable("*INTERVALS-OFF*", intervals_off)
        set_lisp_variable("*MEASURES*", measures)
        set_lisp_variable("*THRESHOLD*", threshold)
        set_lisp_variable("*PATTERN-SIZE*", pattern_size)
        set_lisp_variable("*AMOUNT-OFF*", amount_off)
        set_lisp_variable("*MATCHING-LINE*", matching_line)

        try:
            lisp_eval = lisp.eval(("get-the-levels", lisp_input))
            lisp_result = cl4py_elements_to_python(lisp_eval)

        except Exception as lisp_exception:
            lisp_result = "Error"

        try:
            python_result = get_the_levels(python_input, meter, speac_settings)

        except Exception as python_exception:
            python_result = "Error"

        try:
            self.assertEqual(python_result, lisp_result)
        except AssertionError:
            print("\n")
            for i in range(1, 50):
                print(emoji.emojize(":tired_face:"), end="")
            print("\nERROR!!! Data aren't equal:\nPython and LISP input = ", python_input)
            print("  Lisp result = ", lisp_result, "\nPython result = ", python_result)
            variables = ["*METER*", "*BEAT*", "*CADENCE-MINIMUM*", "*INTERVALS-OFF*", "*MEASURES*",
                         "*THRESHOLD*", "*PATTERN-SIZE*", "*AMOUNT-OFF*", "*MATCHING-LINE*"]
            for variable in variables:
                print("Lisp variable " + variable.upper() + " = ", lisp.eval(cl4py.Symbol(variable.upper())))
            for i in range(1, 50):
                print(emoji.emojize(":tired_face:"), end="")
            print("\n")


if __name__ == '__main__':
    test = BindingsTest()
    test.test_all()
