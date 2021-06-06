import copy

from .pattern_match import pattern_match, simple_matcher
from .speac import remove_all
from .speac_analysis import capture_beats

c1 = [24, 36, 48, 60, 72, 84, 96, 108, 27, 28, 39, 40, 51, 52, 63, 64, 75, 76, 87, 88, 99, 100,
      31, 43, 55, 67, 79, 91, 103]
p1 = [29, 41, 53, 65, 77, 89, 101, 33, 93, 105, 81, 45, 57, 69, 24, 36, 48, 60, 72, 84, 96, 108]
a1 = [31, 43, 55, 67, 79, 91, 103, 35, 47, 59, 71, 83, 95, 107, 26, 38, 50, 62, 74, 86, 98, 29,
      41, 53, 65, 77, 89, 101]
a2 = [35, 47, 59, 71, 83, 95, 107, 26, 38, 50, 62, 74, 86, 98, 29, 41, 53, 65, 77, 89, 101]
c4 = [28, 40, 52, 64, 76, 88, 100, 31, 43, 55, 67, 79, 91, 103, 35, 47, 59, 71, 83, 95, 107]
p2 = [26, 38, 50, 62, 74, 86, 98, 89, 101, 77, 65, 29, 41, 53, 93, 105, 81, 69, 33, 45, 57]
c2 = [33, 45, 57, 69, 81, 93, 105, 24, 36, 48, 60, 72, 84, 96, 108, 28, 40, 52, 64, 76, 88, 100]
s1 = [26, 38, 50, 62, 74, 86, 98, 30, 33, 42, 54, 66, 78, 90, 102, 45, 57, 69, 81, 93, 105]
s3 = [28, 40, 52, 64, 76, 88, 100, 32, 35, 44, 56, 68, 80, 92, 104, 47, 59, 71, 83, 95, 107]
e1 = [33, 45, 57, 69, 81, 93, 105, 25, 37, 49, 61, 73, 85, 97, 28, 40, 52, 64, 76, 88, 100]
e3 = [35, 47, 59, 71, 83, 95, 107, 27, 39, 51, 63, 75, 87, 99, 30, 42, 54, 66, 78, 90, 102]
c3 = [24, 36, 48, 60, 72, 84, 96, 108, 28, 31, 34, 40, 52, 64, 76, 88, 100, 43, 55, 67, 79, 91, 103,
      46, 58, 70, 82, 94, 106]
e2 = [25, 37, 49, 61, 73, 85, 97, 28, 31, 34, 40, 52, 64, 76, 88, 100, 43, 55, 67, 79, 91, 103, 46,
      58, 70, 82, 94, 106]
e4 = [27, 39, 51, 63, 75, 87, 99, 24, 30, 33, 36, 48, 60, 72, 84, 96, 108, 42, 54, 66, 78, 90, 102,
      45, 57, 69, 81, 93, 105]
a3 = [32, 44, 56, 68, 80, 92, 104, 26, 29, 35, 38, 50, 62, 74, 86, 98, 41, 53, 65, 77, 89, 101, 47,
      59, 71, 83, 95, 107]
p3 = [32, 44, 56, 68, 80, 92, 104, 24, 30, 36, 48, 60, 72, 84, 96, 108, 42, 54, 66, 78, 90, 102]
p4 = [25, 37, 49, 61, 73, 85, 97, 29, 32, 41, 53, 65, 77, 89, 101, 44, 56, 68, 80, 92, 104]
s4 = [30, 42, 54, 66, 78, 90, 102, 25, 37, 49, 61, 73, 85, 97, 34, 46, 58, 70, 82, 94, 106]
a4 = [27, 39, 51, 63, 75, 87, 99, 31, 43, 55, 67, 79, 91, 103, 34, 46, 58, 70, 82, 94, 106]
s2 = [34, 46, 58, 70, 82, 94, 106, 26, 38, 50, 62, 74, 86, 98, 29, 41, 53, 65, 77, 89, 101]

ANALYSIS_LEXICON = [c1, p1, a1, a2, c4, p2, c2, s1, s3, e1, e3, c3, e2, e4, a3, p3, p4, s4, a4, s2]
ANALYSIS_LEXICON_NAMES = ["c1", "p1", "a1", "a2", "c4", "p2", "c2", "s1", "s3", "e1",
                          "e3", "c3", "e2", "e4", "a3", "p3", "p4", "s4", "a4", "s2"]


# Возвращает номер бита и соответсвующий ему SPEAC-символ
# (get-function '(0 (79 64 48 48 65 65 50 50)))
# (0 a1)
def get_function(beat_number, chord_notes):
    if len(chord_notes) < 2:
        return [beat_number, "e4"]
    else:
        return [beat_number, compare_them(chord_notes, ANALYSIS_LEXICON)[1]]


# По списоку нот возвращает значение подходящего SPEAC-символа
# (compare-them '(79 64 48 48 65 65 50 50) *analysis-lexicon*)
# ((31 43 55 67 79 91 103 35 47 59 71 83 95 107 26 38 50 62 74 86 98 29 41 53 65
#   77 89 101) a1)
def compare_them(harmonic_notes, harmonic_functions):
    highest = -1
    highest_index = -1
    counts = count_harmonic_notes(harmonic_notes, harmonic_functions)
    for i in range(0, len(counts)):
        if counts[i] > highest:
            highest = counts[i]
            highest_index = i

    return ANALYSIS_LEXICON[highest_index], ANALYSIS_LEXICON_NAMES[highest_index]


# Считает сколько элементов из первого списка содержится в каждом подсписке второго списка
# (count-harmonic-notes '(79 64 48 48 65 65 50 50) *analysis-lexicon*)
# (4 4 5 4 2 4 3 2 1 1 0 4 2 2 4 2 2 0 1 4)
def count_harmonic_notes(harmonic_notes, harmonic_functions):
    count = []
    for speac_symbol_list in harmonic_functions:
        count.append(my_count(harmonic_notes, speac_symbol_list))
    return count


# Считает сколько элементов из первого списка содержится во втором
# (my-count '(79 64 48 48 65 65 50 50) '(38 50 62 74 86 41 53 65 77 89 46 58 70 82 94))
# 4
def my_count(list1, list2):
    count = 0
    for element1 in list1:
        for element2 in list2:
            if element1 == element2:
                count += 1
    return count


def cadences(events, speac_settings):
    events = copy.deepcopy(events)
    captured_beats = capture_beats(events, speac_settings.BEAT)

    pitches = []
    for beat in captured_beats:
        pitches.append(get_pitches(beat))

    functions = []
    for pitch in pitches:
        fun = get_function(pitch[0], pitch[1])
        functions.append(fun)

    best_cadences = return_best_cadences(functions, speac_settings)

    result = []
    for element in best_cadences:
        reversed_element = [element[1], element[0]]
        result.append(reversed_element)

    return result


def next_4(lists):
    if (len(lists) >= 1 and lists[0][1].lower() == "c1") or \
            (len(lists) >= 2 and lists[1][1].lower() == "c1") or \
            (len(lists) >= 3 and lists[2][1].lower() == "c1") or \
            (len(lists) >= 4 and lists[3][1].lower() == "c1"):
        return True
    else:
        return False


def return_best_cadences(function_timing_lists, speac_settings, distance=0, previous=None, minor_flag=0):
    size = len(function_timing_lists)
    function_timing_lists = copy.deepcopy(function_timing_lists)
    result = []

    for i in range(1, size):
        function = function_timing_lists[0]
        next_function = function_timing_lists[1]
        function_timing_lists.pop(0)

        fun_1 = function[1].lower()

        if (minor_flag > 0) and (fun_1 == "c2") and (distance > speac_settings.CADENCE_MINIMUM):
            result.append([function[0], "c1"])
            distance = 0

        elif (minor_flag > 0) and (fun_1 == "c4") and (distance > speac_settings.CADENCE_MINIMUM):
            result.append([function[0], "a1"])
            distance = 0

        elif (previous == "a1") and (fun_1 == "c1") and (distance > speac_settings.CADENCE_MINIMUM):
            result.append(function)
            distance = 0

        elif (distance > speac_settings.CADENCE_MINIMUM) and (fun_1 == "a1") and (next_function[1].lower() != "c1"):
            result.append(function)
            distance = 0

        elif (fun_1 == "c1") and (distance > speac_settings.CADENCE_MINIMUM):
            result.append(function)
            distance = 0

        elif (fun_1 == "a1") and (not next_4(function_timing_lists)) and (distance > speac_settings.CADENCE_MINIMUM):
            result.append(function)
            distance = 0

        else:
            distance += 1000

        previous = fun_1
        minor_flag = set_minor_flag(function, minor_flag)

    return result


def set_minor_flag(list, flag):
    if list[1] == "s3" or list[1] == "a3" or list[1] == "p4":
        return 4
    else:
        if flag > 0:
            return flag - 1
        else:
            return 0


# (get-pitches '((61000 60 1000 4 96) (61000 76 1000 1 96) (61500 69 250 3 96)
#       (61500 72 500 2 96) (61750 70 250 3 96)))
# (61000 (60 76 69 72 70))
def get_pitches(events):
    result = [events[0][0]]
    pitch_result = []

    for event in events:
        pitch_result.append(event[1])

    result.append(pitch_result)
    return result


# (make-composite-rhythm *events*)
# (0 1000 1500 2000 2500 3000)
def make_composite_rhythm(events):
    events_set = set()
    for event in events:
        events_set.add(event[0])
    result = list(events_set)
    result.sort()
    return result


def collect_differential(ontime_map):
    previous = None
    count = 0
    time = ontime_map[0]
    result = []

    while len(ontime_map) >= 0:
        if len(ontime_map) == 0:
            result.append([count, time])

            if len(ontime_map) == 0:
                break

        elif previous is None:
            previous = ontime_map.pop(0)
            count += 1
            time = 0

        elif abs(ontime_map[0] - previous) > 1001:
            result.append([count, time])
            time = ontime_map[0]
            previous = ontime_map[0]
            count = 0

        else:
            previous = ontime_map.pop(0)
            count += 1

    return result


def composite_rhythm(events):
    comp_rhythm = make_composite_rhythm(events)
    return collect_differential(comp_rhythm)


def map_density(beats):
    result = []
    for beat in beats:
        result.append([len(beat), beat[0][0]])
    return result


def collect_by_differences(density_map):
    previous = None
    count = 0
    time = density_map[0][1]
    result = []

    while len(density_map) >= 0:
        if len(density_map) == 0:
            result.append([count, time])

            if len(density_map) == 0:
                break

        elif previous is None:
            previous = density_map.pop(0)
            count += 1

        elif abs(density_map[0][0] - previous[0]) > 2:
            result.append([count, time])
            time = density_map[0][1]
            previous = density_map[0]
            count = 0

        else:
            previous = density_map.pop(0)
            count += 1

    return result


def density(events, speac_settings):
    beats = capture_beats(events, speac_settings.BEAT)
    return collect_by_differences(map_density(beats))


def collect_patterns(list, lists, type, speac_settings):
    result = []

    while True:
        if len(lists) == 0:
            break

        elif pattern_match(list[2], lists[0][2], speac_settings.INTERVALS_OFF, speac_settings):
            local_result = []
            lists[0].pop(0)
            local_result.append(type)
            local_result.append(lists[0][0])
            local_result.append(lists[0][1])
            result.append(local_result)
            lists.pop(0)

        else:
            result.append(lists[0])
            lists.pop(0)

    return result


def almost_the_same_lists(lists, speac_settings):
    types = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k"]
    result = []

    while True:
        if len(lists) == 0:
            break

        elif not isinstance(lists[0][0], int):
            result.append(lists.pop(0))

        else:
            list_0_before = copy.deepcopy(lists[0])
            lists[0].pop(0)

            if len(types) != 0:
                types_0 = types[0]
            else:
                types_0 = []

            result.append([types_0, lists[0][0], lists[0][1]])

            if len(types) != 0:
                first_type = types.pop(0)
            else:
                first_type = []

            lists.pop(0)
            lists = collect_patterns(list_0_before, lists, first_type, speac_settings)
    return result


def evaluate_forms(max, min, forms):
    result = []

    while True:
        if len(forms) == 0:
            break

        elif (len(forms[0]) <= max) and (len(forms[0]) >= min):
            first_form = forms.pop(0)
            result.append(first_form)

        else:
            forms.pop(0)

    return result


def find_letters_used(form):
    while True:
        if len(form) == 0:
            return LETTERS_USED

        elif form[0][0] in ["a", "b", "c", "d", "e", "f", "g"]:
            if form[0][0] not in LETTERS_USED:
                LETTERS_USED.append(form[0][0])

        form.pop(0)


LETTERS = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
           "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]


def name_them(forms, letters):
    result = []

    while True:
        if len(forms) == 0:
            return result
        else:
            if forms[0][0] in LETTERS:
                result.append(forms.pop(0))
            else:
                first_form = forms.pop(0)
                result.append([letters[0], first_form[1]])


def within_range(min, max, lists):
    lists = copy.deepcopy(lists)
    result = []

    while True:
        if len(lists) == 0:
            return result
        else:
            if (lists[0][1] >= min) and (lists[0][1] <= max):
                lists.pop(0)
            else:
                result.append(lists.pop(0))


def return_within_range(original, other, meter, speac_settings):
    amount = meter * speac_settings.BEAT * speac_settings.MEASURES

    while True:
        if len(original) == 0:
            return other
        else:
            first_original = original.pop(0)
            other = within_range(first_original[1] - amount, first_original[1] + amount, other)


def reduce_out_close_calls(pattern_discovery, forms, meter, speac_settings):
    result = []
    forms = copy.deepcopy(forms)
    pattern_discovery = copy.deepcopy(pattern_discovery)

    while True:
        if len(forms) == 0:
            return result
        else:
            first_form = forms.pop(0)
            result.append(return_within_range(pattern_discovery, first_form, meter, speac_settings))


def my_last(some_list):
    try:
        last = [some_list[-1]]
        first_of_last = last[0]
        return first_of_last
    except IndexError:
        return []


def butlast(some_list, number=1):
    result = copy.deepcopy(some_list)

    try:
        for i in range(1, number + 1):
            result.pop(len(result) - 1)
        return result
    except IndexError:
        return []


def combine(forms, meter, speac_settings):
    forms = copy.deepcopy(forms)

    reduce_result = reduce_out_close_calls(my_last(forms), butlast(forms), meter, speac_settings)

    input = []
    for element in forms[-1]:
        input.append(element)

    for element in reduce_result:
        for e in element:
            if e:
                input.append(e)

    used_letters = find_letters_used(my_last(forms))
    used_letters.reverse()

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
                "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    letters = remove_all(used_letters, alphabet)

    result = name_them(input, letters)
    result.sort(key=sort_by_second_element)
    return result


def sort_by_second_element(some_list):
    return some_list[1]


LETTERS_USED = []


def eval_combine_and_integrate_forms(events, meter, speac_settings):
    global LETTERS_USED
    LETTERS_USED = []
    events = copy.deepcopy(events)
    cadences_result = cadences(events, speac_settings)

    density_result = density(events, speac_settings)

    rhythm_result = composite_rhythm(events)

    s_matcher = simple_matcher(events, speac_settings)

    patterns = almost_the_same_lists(s_matcher, speac_settings)

    min = round((events[-1][0] + events[-1][2]) / (meter * 1000 * 8))
    max = round((events[-1][0] + events[-1][2]) / (meter * 1000 * 4))

    forms_result = evaluate_forms(max, min, [cadences_result, density_result, rhythm_result])
    forms_result.append(patterns)
    return combine(forms_result, meter, speac_settings)
