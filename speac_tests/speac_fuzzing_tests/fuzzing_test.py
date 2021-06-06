import glob
import random
import sys
import unittest

import atheris
import cl4py
import os

import emoji

from speac_library.speac.speac_settings import SpeacSettings
from speac_library.speac.top_level import get_the_levels

lisp = cl4py.Lisp()
cl = lisp.function("find-package")("CL")


def load_files():
    path = os.path.join(os.path.dirname(__file__), "lisp_files/*.lisp")

    for file_name in glob.glob(path):
        file_name = file_name.replace("\\", "/")
        lisp.eval(("load", '"' + file_name + '"'))


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
    if python_input == "" or python_input is None:
        python_input = []

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

    try:
        lisp.eval(("load", '"' + file_name + '"'))
    except RuntimeError:
        pass

    os.remove("./lisp_files/my_variables.lisp")


class BindingsTest(unittest.TestCase):

    def test_get_the_levels(self, events, meter, speac_settings):
        python_input = events
        lisp_input = "LISP-EVENTS"
        create_lisp_input(lisp_input, python_input_to_lisp(python_input))

        beat = speac_settings.BEAT
        cadence_minimum = speac_settings.CADENCE_MINIMUM
        intervals_off = speac_settings.INTERVALS_OFF
        measures = speac_settings.MEASURES
        threshold = speac_settings.THRESHOLD
        pattern_size = speac_settings.PATTERN_SIZE
        amount_off = speac_settings.AMOUNT_OFF
        matching_line = speac_settings.MATCHING_LINE  # differs when 2, fix it later

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

        self.assertEqual(python_result, lisp_result)


def start_testing(data):
    events = []

    for i in range(1, random.randint(1, 100)):  # random events count
        fdp = atheris.FuzzedDataProvider(data)

        # each event has only 5 args, and events values can be only positive
        event = fdp.ConsumeIntListInRange(5, 0, 100000)
        events.append(event)

    meter = atheris.FuzzedDataProvider(data).ConsumeIntInRange(0, 10)
    beat = atheris.FuzzedDataProvider(data).ConsumeIntInRange(500, 4000)
    cadence_minimum = atheris.FuzzedDataProvider(data).ConsumeIntInRange(1000, 20000)
    intervals_off = atheris.FuzzedDataProvider(data).ConsumeIntInRange(0, 10)
    measures = atheris.FuzzedDataProvider(data).ConsumeIntInRange(0, 10)
    threshold = atheris.FuzzedDataProvider(data).ConsumeIntInRange(0, 10)
    pattern_size = atheris.FuzzedDataProvider(data).ConsumeIntInRange(2, 10)
    amount_off = atheris.FuzzedDataProvider(data).ConsumeIntInRange(0, 10)
    matching_line = atheris.FuzzedDataProvider(data).ConsumeIntInRange(0, 10)

    speac_settings = SpeacSettings()
    speac_settings.set_beat(beat)
    speac_settings.set_cadence_minimum(cadence_minimum)
    speac_settings.set_intervals_off(intervals_off)
    speac_settings.set_measures(measures)
    speac_settings.set_threshold(threshold)
    speac_settings.set_pattern_size(pattern_size)
    speac_settings.set_amount_off(amount_off)
    speac_settings.set_matching_line(matching_line)

    test = BindingsTest()

    try:
        test.test_get_the_levels(events, meter, speac_settings)
    except Exception as get_the_levels_exception:

        print("\n")
        for i in range(1, 50):
            print(emoji.emojize(":tired_face:"), end="")
        print("\nERROR!!! Data aren't equal:\nPython and LISP input = ", events)
        variables = ["*METER*", "*BEAT*", "*CADENCE-MINIMUM*", "*INTERVALS-OFF*", "*MEASURES*",
                     "*THRESHOLD*", "*PATTERN-SIZE*", "*AMOUNT-OFF*", "*MATCHING-LINE*"]
        for variable in variables:
            print("Lisp variable " + variable.upper() + " = ", lisp.eval(cl4py.Symbol(variable.upper())))
        for i in range(1, 50):
            print(emoji.emojize(":tired_face:"), end="")
        print("\n")

        raise get_the_levels_exception


if __name__ == '__main__':
    load_files()
    atheris.Setup(sys.argv, start_testing, enable_python_coverage=True, enable_python_opcode_coverage=True)
    atheris.Fuzz()
