import copy

# (get-the-speac ((0 60 1000 4 127) (0 67 1000 2 127) (0 64 1000 3 127)))
# consequent
import numpy


# Запускает SPEAC, используя при этом вес и среднее значение
# (run-speac '(0.56 0.41 0.78 0.51 1.33 0.51 1.26 0.51) 0.73)
# ("preparation" "extension" "statement" "extension" "antecedent" "consequent" "antecedent" "consequent")
def run_speac(weights, average):
    return develop_speac(weights, average, max(weights), min(weights))


# (develop-speac '(0.56 0.41 0.78 0.51 1.33 0.51 1.26 0.51) 0.73 1.33 0.41)
# ("preparation" "extension" "statement" "extension" "antecedent" "consequent" "antecedent" "consequent")
def develop_speac(weights, average, largest, smallest):
    weights_copy = copy.deepcopy(weights)
    result = []
    previous_assignment = None

    for i in range(1, len(weights_copy) + 1):
        weight = weights_copy[i - 1]
        previous_weight = None
        if i > 1:
            previous_weight = weights_copy[i - 2]

        next_weight = None
        if i + 1 <= len(weights_copy):
            next_weight = weights_copy[i]

        if almost(weight, previous_weight, 0.2):
            result.append("extension")
            previous_assignment = "extension"

        elif almost(weight, next_weight, 0.2):
            if previous_assignment == "preparation":
                result.append("extension")
                previous_assignment = "extension"
            else:
                result.append("preparation")
                previous_assignment = "preparation"

        elif almost(weight, average, 0.2):
            if previous_assignment == "statement":
                result.append("extension")
            else:
                result.append("statement")
            previous_assignment = "statement"

        elif almost(weight, largest, 0.2):
            if previous_assignment == "antecedent":
                result.append("extension")
                previous_assignment = "extension"
            else:
                result.append("antecedent")
                previous_assignment = "antecedent"

        elif previous_assignment == "antecedent" and almost(weight, smallest, 0.2):
            if previous_assignment == "consequent":
                result.append("extension")
            else:
                result.append("consequent")
            previous_assignment = "consequent"

        else:
            if previous_assignment == "statement":
                result.append("extension")
            else:
                result.append("statement")
            previous_assignment = "statement"

    return result


# (almost 1.26 1.33 0.2)
# t
def almost(first, second, allowance):
    if first is None or second is None:
        return False
    elif abs(numpy.float32(first) - numpy.float32(second)) < allowance:
        return True
    else:
        return False


# (collect-beats '((0 45 1000 4 55) (2100 64 1000 3 55) (3000 69 1000 2 55) (4100 73 1000 1 55) (5000 57 1000 4 55))
# 2000)
# (((0 45 1000 4 55)) ((2100 64 1000 3 55) (3000 69 1000 2 55)) ((4100 73 1000 1 55) (5000 57 1000 4 55)))
def collect_beats(clarified_music, beat):
    collected_beat = collect_beat(beat, clarified_music)
    accumulated_beat = beat
    result = [collected_beat]

    while True:
        accumulated_beat += beat
        collected_beat = collect_beat(accumulated_beat, clarified_music)

        if collected_beat:
            result.append(collected_beat)

        if len(clarified_music) == 0:
            return result


# (collect-beat 6000 '((5000 55 1000 4 55) (5200 62 1000 3 55) (6000 62 1000 3 55) (7000 62 1000 3 55)))
# ((5000 55 1000 4 55) (5200 62 1000 3 55))
def collect_beat(beat, clarified_music):
    result = []
    size = len(clarified_music)
    for i in range(1, size + 1):
        event = clarified_music[0]
        if event[0] < beat:
            result.append(event)
            clarified_music.pop(0)
    return result


# (break-event 300 '(7000 57 1000 3 55))
# ((7000 57 300 3 55) (7300 57 300 3 55) (7600 57 300 3 55) (7900 57 100 3 55))
def break_event(beat, event):
    ontime = event[0]
    duration = event[2]
    result = []

    while duration != 0:
        local_result = [ontime, event[1]]

        if duration > beat:
            local_result.append(beat)
            duration -= beat
        else:
            local_result.append(duration)
            duration -= duration

        local_result.append(event[3])
        local_result.append(event[4])
        result.append(local_result)

        ontime += beat
    return result


# (break-events-into-beats 500 '((7000 57 1000 3 55) (8000 57 600 3 55)))
# ((7000 57 500 3 55) (7500 57 500 3 55) (8000 57 500 3 55) (8500 57 100 3 55))
def break_events_into_beats(beat, music):
    accumulated_beat = beat

    result = []
    for event in music:
        if event[0] < accumulated_beat:
            for element in break_event(beat, event):
                result.append(element)
        else:
            for element in break_event(beat, event):
                result.append(element)
        accumulated_beat += beat
    return result


def sort_by_first_element(some_list):
    return some_list[0]


def capture_beats(music, beat):
    break_res = break_events_into_beats(beat, music)
    break_res.sort(key=sort_by_first_element)
    return collect_beats(break_res, beat)
