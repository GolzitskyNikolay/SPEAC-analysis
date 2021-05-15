import copy

from speac_chapter_7.speac import get_channel

AMOUNT_OFF = 1


def pattern_match(pattern_1, pattern_2, number_wrong_possible):
    pattern_1 = copy.deepcopy(pattern_1)
    pattern_2 = copy.deepcopy(pattern_2)

    # print(pattern_1, pattern_2, number_wrong_possible)
    if pattern_1 == [] and pattern_2 == []:
        # print("1")
        return True

    elif number_wrong_possible == -1 \
            or abs(pattern_1[0] - pattern_2[0]) > AMOUNT_OFF:
        # print("2")
        return False

    elif pattern_1[0] != pattern_2[0]:
        # print("3")
        pattern_1.pop(0)
        pattern_2.pop(0)
        return pattern_match(pattern_1, pattern_2, number_wrong_possible - 1)

    else:
        # print("4")
        pattern_1.pop(0)
        pattern_2.pop(0)
        return pattern_match(pattern_1, pattern_2, number_wrong_possible)


def get_ontimes_and_pitches(events):
    result = []

    while True:
        if len(events) == 0:
            break
        else:
            event = events.pop(0)
            result.append([event[0], event[1]])
    return result


INTERVALS_OFF = 2


def run_pattern_match(pattern, patterns):
    matches = 0

    while True:

        first_n_patterns = patterns[:len(pattern)]

        if len(patterns) < len(pattern):
            return matches

        else:
            if pattern_match(pattern, first_n_patterns, INTERVALS_OFF):
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


def find_matchings(pattern, patterns):
    translator_input = []
    for p in pattern:
        # print(p)
        if DURATION == "yes":
            translator_input.append(p[2])
        else:
            translator_input.append(p[1])

    # print(translator_input)

    translator_res = interval_translator(translator_input)
    # print(translator_res)

    translator_input = []
    for p in patterns:
        if DURATION == "yes":
            translator_input.append(p[2])
        else:
            translator_input.append(p[1])
    translator_res_2 = interval_translator(translator_input)
    # print(translator_res_2)

    result = run_pattern_match(translator_res, translator_res_2)
    # print(result)
    return result


PATTERN_SIZE = 12
def set_pattern_size(number):
    global PATTERN_SIZE
    PATTERN_SIZE = number

THRESHOLD = 2


def find_the_matches(work_1, work_2):
    result = []

    while True:
        if len(work_1) < PATTERN_SIZE:
            break

        else:
            patterns = work_1[:PATTERN_SIZE]
            other_patterns = work_1[PATTERN_SIZE:]
            test = find_matchings(patterns, work_2)

            if test > THRESHOLD:
                translator_input = []
                for p in patterns:
                    translator_input.append(p[1])
                local_result = [test, patterns[0][0], interval_translator(translator_input)]
                result.append(local_result)
                work_1 = other_patterns

            else:
                work_1.pop(0)

    return result


MATCHING_LINE = 1


def simple_matcher(events):
    events.sort()
    channel = get_channel(MATCHING_LINE, events)
    ordered_and_channeled_events = get_ontimes_and_pitches(channel)
    result = find_the_matches(ordered_and_channeled_events, ordered_and_channeled_events)
    return result
