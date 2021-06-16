from .new_form import eval_combine_and_integrate_forms
from .speac_analysis import *
from .speac import *
from .speac_settings import SpeacSettings


# (do-speac-on-phrases '(((0 55 1000 2 64) (0 65 1000 2 64). . .
#     ((("preparation" "extension" "extension" "extension" "preparation" . . .
def do_speac_on_phrases(phrases, meter, note_to_speac=[]):
    result = []
    phrases_copy = copy.deepcopy(phrases)

    for i in range(1, len(phrases_copy) + 1):
        phrase = phrases_copy[i - 1]
        start_beat_number = get_the_start_beat_number(phrase, meter)
        round_number = round(get_length(phrase) / 1000)
        weights = run_the_speac_weightings(phrase, start_beat_number, round_number, meter)
        if note_to_speac:
            note_to_speac[i - 1] = collect_beat_lists(break_at_each_entrance(note_to_speac[i - 1]))

        avg = my_round(sum(weights) / len(weights))

        speac_res = run_speac(weights, avg)

        if note_to_speac:
            for k in range(1, len(speac_res) + 1):
                note_to_speac[i - 1][k - 1].append(speac_res[k - 1])

        local_res = [speac_res, avg]
        result.append(local_res)

    return result


# (get-length '((0 55 1000 2 64) (0 65 1000 2 64) (1000 71 1500 2 64)))
# 2500
def get_length(events):
    last_event = events[-1]
    return last_event[0] + last_event[2] - events[0][0]


# (get-the-start-beat-numbe '((21000 55 1000 2 64) . . . 3))
#   1
def get_the_start_beat_number(events, meter):
    onbeat = round(events[0][0] / 1000)
    return onbeat % meter + 1


# Returns all those events whose ontime is before time
# (get-events-to 1500 '((0 5 23 23 23) (0 12 12 12 12) (500 12 12 12 12) (1600 12 12 12 12)))
# ((0 5 23 23 23) (0 12 12 12 12) (500 12 12 12 12))
def get_events_to(time, events):
    result = []
    for event in events:
        if event[0] < time:
            result.append(event)
    return result


def get_events_from(time, events):
    result = []

    while True:
        if len(events) == 0:
            return result
        elif events[0][0] >= time:
            result.append(events.pop(0))
        else:
            events.pop(0)


def break_into_phrases(events, timings):
    timings = copy.deepcopy(timings)
    events_copy = copy.deepcopy(events)
    result = []

    while True:
        if len(timings) == 0:
            result.append(events_copy)
            return result
        else:
            first_timing = timings.pop(0)
            result.append(get_events_to(first_timing, events_copy))
            events_copy = get_events_from(first_timing, events_copy)


def group_speac_lists(speac_lists, grouped_form):
    speac_lists = copy.deepcopy(speac_lists)
    grouped_form = copy.deepcopy(grouped_form)
    result = []

    while True:
        if len(grouped_form) == 0:
            return result
        else:
            first_grouped_form = grouped_form.pop(0)
            first_n_speac = speac_lists[:len(first_grouped_form)]
            result.append(first_n_speac)
            speac_lists = speac_lists[len(first_grouped_form):]


def group_form(form):
    result = []

    while True:
        if len(form) == 0:
            return result
        else:
            test = group_them(form)
            result.append(test)
            form = form[len(test):]


def group_them(form):
    form = copy.deepcopy(form)
    element = form[0][0]
    result = []

    while True:
        if len(form) == 0:
            return result
        else:
            if element == form[0][0]:
                result.append(form.pop(0))
            else:
                return result


def get_speac_middleground(speac_lists, grouped_form, note_to_speac=[]):
    grouped_speac_lists = group_speac_lists(speac_lists, grouped_form)

    if note_to_speac:
        new_note_to_speac = group_speac_lists(note_to_speac, grouped_form)
        note_to_speac.clear()
        note_to_speac.append(new_note_to_speac)

    result = []
    for i in range(1, len(grouped_speac_lists) + 1):
        phrase = grouped_speac_lists[i - 1]
        test = []
        for e in phrase:
            test.append(e[-1])

        sum = 0
        for element in test:
            sum += element

        test_average = my_round(sum / len(test))
        speac_result = run_speac(test, test_average)
        if note_to_speac:
            for k in range(1, len(speac_result) + 1):
                note_to_speac[0][i - 1][k - 1].append(speac_result)

        result.append([speac_result, test_average])

    return result


def get_speac_background(speac_middleground, note_to_speac=[]):
    test = []


    for element in speac_middleground:
        test.append(element[-1])
    avg = my_round(sum(test) / len(test))
    speac_res = run_speac(test, avg)

    if note_to_speac:
        for i in range(1, len(speac_res) + 1):
            note_to_speac[i - 1].append(speac_res[i - 1])

    result = [speac_res, avg]
    return result


def run_the_program(events, meter, speac_settings, get_not_to_speac=False):
    events = copy.deepcopy(events)

    form = eval_combine_and_integrate_forms(events, meter, speac_settings)

    new_form = []
    for element in form:
        if element not in new_form:
            new_form.append(element)
    form = new_form

    second_elements = []
    for i in range(1, len(form)):
        second_elements.append(form[i][1])

    phrased_events = break_into_phrases(events, second_elements)

    if get_not_to_speac:
        note_to_speac = break_into_phrases(copy.deepcopy(events), second_elements)
    else:
        note_to_speac = []

    speac_phrase_lists = do_speac_on_phrases(phrased_events, meter, note_to_speac)

    speac_middleground = get_speac_middleground(speac_phrase_lists, group_form(form), note_to_speac)

    if get_not_to_speac:
        note_to_speac = note_to_speac[0]

    speac_background = get_speac_background(speac_middleground, note_to_speac)

    ursatz = get_speac_background([speac_background], note_to_speac)
    if get_not_to_speac:
        note_to_speac = [note_to_speac, ursatz[0][0]]

    if get_not_to_speac:
        return note_to_speac
    else:
        return [ursatz, speac_background, speac_middleground, speac_phrase_lists, form]


def number_the_elements(levels):
    level_numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    result = []
    for level in levels:
        mini_res = []

        for phrase in level:
            local_res = []

            for element in phrase:
                local_res.append(element + level_numbers[0])
            mini_res.append(local_res)

        result.append(mini_res)
        level_numbers.pop(0)
    return result


def derive_speac_symbol(speac_name):
    speac_name = speac_name.lower()

    if speac_name == "consequent":
        return "c"
    elif speac_name == "antecedent":
        return "a"
    elif speac_name == "statement":
        return "s"
    elif speac_name == "extension":
        return "e"
    elif speac_name == "preparation":
        return "p"
    else:
        return None


def wrap_first_two(lists):
    return [[lists[0]], [lists[1]], lists[2], lists[3]]


def create_the_window_levels(levels_from_the_program):
    levels = wrap_first_two(levels_from_the_program[:5])
    result = []

    for phrase in levels:
        mini_res = []

        for element in phrase:
            local_res = []

            for speac in element[0]:
                local_res.append(derive_speac_symbol(speac))

            mini_res.append(local_res)

        result.append(mini_res)
    return result


def get_the_levels(events, meter, speac_settings=SpeacSettings(), note_to_speac=False):
    output = run_the_program(events, meter, speac_settings, note_to_speac)

    if note_to_speac:
        return output
    else:
        return number_the_elements(create_the_window_levels(output))


def get_note_and_speac(events, meter, speac_settings=SpeacSettings()):
    result = get_the_levels(events, meter, speac_settings, True)

    notes_and_speac = []

    for e in range(1, len(result[0]) + 1):
        element = result[0][e - 1]
        middleground_index = 0

        for i in range(1, len(element)):
            background = element[-1]

            if i < len(element):
                phrases = element[i - 1]
                middlegrounds = phrases[-1]

                for j in range(1, len(phrases) + 1):
                    phrase = phrases[j - 1]

                    if isinstance(phrase[-1], str):
                        foreground = phrase[-1]
                    else:
                        foreground = None  

                    if isinstance(phrase[0], str):
                        middleground_index += 1

                    else:
                        for l in range(1, len(phrase)):
                            events = phrase[l - 1]

                            for p in range(1, len(events) + 1):
                                event = events[p - 1]
                                new_event = event[:5]
                                new_event.append(foreground)
                                new_event.append(middlegrounds[middleground_index])
                                new_event.append(background)
                                notes_and_speac.append(new_event)

    return notes_and_speac
