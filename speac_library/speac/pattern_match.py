import copy

from .speac import get_channel


def pattern_match(pattern_1, pattern_2, number_wrong_possible, speac_settings):
    pattern_1 = copy.deepcopy(pattern_1)
    pattern_2 = copy.deepcopy(pattern_2)

    if pattern_1 == [] and pattern_2 == []:
        return True

    elif number_wrong_possible == -1 \
            or abs(pattern_1[0] - pattern_2[0]) > speac_settings.AMOUNT_OFF:
        return False

    elif pattern_1[0] != pattern_2[0]:
        pattern_1.pop(0)
        pattern_2.pop(0)
        return pattern_match(pattern_1, pattern_2, number_wrong_possible - 1, speac_settings)

    else:
        pattern_1.pop(0)
        pattern_2.pop(0)
        return pattern_match(pattern_1, pattern_2, number_wrong_possible, speac_settings)


def get_ontimes_and_pitches(events):
    result = []

    while True:
        if len(events) == 0:
            break
        else:
            event = events.pop(0)
            result.append([event[0], event[1]])
    return result


def run_pattern_match(pattern, patterns, speac_settings):
    matches = 0

    while True:

        first_n_patterns = patterns[:len(pattern)]

        if len(patterns) < len(pattern):
            return matches

        else:
            if pattern_match(pattern, first_n_patterns, speac_settings.INTERVALS_OFF, speac_settings):
                patterns.pop(0)
                matches += 1

            else:
                patterns.pop(0)


def interval_translator(midi_list):
    result = []

    while True:
        if len(midi_list) == 1:
            break

        else:
            result.append(midi_list[1] - midi_list[0])
            midi_list.pop(0)

    return result


DURATION = "no"


def find_matchings(pattern, patterns, speac_settings):
    translator_input = []
    for p in pattern:
        if DURATION == "yes":
            translator_input.append(p[2])
        else:
            translator_input.append(p[1])

    translator_res = interval_translator(translator_input)

    translator_input = []
    for p in patterns:
        if DURATION == "yes":
            translator_input.append(p[2])
        else:
            translator_input.append(p[1])
    translator_res_2 = interval_translator(translator_input)

    result = run_pattern_match(translator_res, translator_res_2, speac_settings)

    return result


def firstn(number, some_list):
    if len(some_list) < number:
        return firstn(number - 1, some_list)
    else:
        return butlast(some_list, len(some_list) - number)


def butlast(some_list, number=1):
    result = copy.deepcopy(some_list)

    try:
        for i in range(1, number + 1):
            result.pop(len(result) - 1)
        return result
    except IndexError:
        return []


def find_the_matches(work_1, work_2, speac_settings):
    result = []

    while True:
        if len(work_1) < speac_settings.PATTERN_SIZE:
            break

        else:
            patterns = firstn(speac_settings.PATTERN_SIZE, work_1)
            other_patterns = work_1[speac_settings.PATTERN_SIZE:]
            test = find_matchings(patterns, work_2, speac_settings)  # 17 паттерн не совпадает

            if test > speac_settings.THRESHOLD:
                translator_input = []
                for p in patterns:
                    translator_input.append(p[1])
                local_result = [test, patterns[0][0], interval_translator(translator_input)]
                result.append(local_result)
                work_1 = other_patterns

            else:
                work_1.pop(0)

    return result


def sort_by_first_element(some_list):
    return some_list[0]


def simple_matcher(events, speac_settings):
    events.sort(key=sort_by_first_element)
    channel = get_channel(speac_settings.MATCHING_LINE, events)
    ordered_and_channeled_events = get_ontimes_and_pitches(channel)
    result = find_the_matches(ordered_and_channeled_events, ordered_and_channeled_events, speac_settings)
    return result
