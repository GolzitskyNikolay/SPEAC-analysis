# Обозначения весов интервала
import copy

import numpy

UNISON = 0
MINOR_SECOND = 1
MAJOR_SECOND = .8
MINOR_THIRD = .225
MAJOR_THIRD = .2
PERFECT_FOURTH = .55
AUGMENTED_FOURTH = .65
PERFECT_FIFTH = .1
MINOR_SIXTH = .275
MAJOR_SIXTH = .25
MINOR_SEVENTH = .7
MAJOR_SEVENTH = .9
PERFECT_OCTAVE = 0

MINOR_NINTH = 1
MAJOR_NINTH = .8
MINOR_TENTH = .225
MAJOR_TENTH = .2
PERFECT_ELEVENTH = .55
AUGMENTED_ELEVENTH = .65
PERFECT_TWELVETH = .1
MINOR_THIRTEENTH = .275
MAJOR_THIRTEENTH = .25
MINOR_FOURTEENTH = .7
MAJOR_FOURTEENTH = .9
PERFECT_FIFTEENTH = 0
MINOR_SIXTEENTH = 1
MAJOR_SIXTEENTH = .8
MINOR_SEVENTEENTH = .225
MAJOR_SEVENTEENTH = .2
PERFECT_EIGHTEENTH = .55
AUGMENTED_EIGHTEENTH = .65
PERFECT_NINETEENTH = .1
MINOR_TWENTIETH = .275
MAJOR_TWENTIETH = .25
MINOR_TWENTYFIRST = .7
MAJOR_TWENTYFIRST = .9
PERFECT_TWENTYSECOND = 0
MINOR_TWENTYTHIRD = 1
MAJOR_TWENTYTHIRD = .8
MINOR_TWENTYFOURTH = .225
MAJOR_TWENTYFOURTH = .2
PERFECT_TWENTYFIFTH = .55
AUGMENTED_TWENTYFIFTH = .65
PERFECT_TWENTYSIXTH = .1
MINOR_TWENTYSEVENTH = .275
MAJOR_TWENTYSEVENTH = .25
MINOR_TWENTYEIGHTH = .7
MAJOR_TWENTYEIGHTH = 0.9
PERFECT_TWENTYNINTH = 0

EXITS_AND_ENTRANCES = []
NEW_ENTRANCE_TIME = 0
SIMULTANEOUS_EVENTS = []
EVENT = []
OCTAVE_SEPARATION = .02
DOWNBEAT = "downbeat"

METRIC_TENSION_TABLE = [[4, [1, 2], [2, 2], [3, 6], [4, 2]],
                        [2, [1, 2], [2, 2]],
                        [3, [1, 2], [2, 2], [3, 2]],
                        [6, [1, 2], [2, 2], [3, 2], [4, 8], [5, 4], [6, 3]],
                        [9, [1, 2], [2, 2], [3, 2], [4, 8], [5, 4], [6, 3], [7, 14], [8, 8], [9, 4]]]

INTERVAL_LIST = [UNISON, MINOR_SECOND, MAJOR_SECOND, MINOR_THIRD, MAJOR_THIRD,
                 PERFECT_FOURTH, AUGMENTED_FOURTH, PERFECT_FIFTH, MINOR_SIXTH,
                 MAJOR_SIXTH, MINOR_SEVENTH, MAJOR_SEVENTH, PERFECT_OCTAVE, MINOR_NINTH,
                 MAJOR_NINTH, MINOR_TENTH, MAJOR_TENTH, PERFECT_ELEVENTH,
                 AUGMENTED_ELEVENTH, PERFECT_TWELVETH, MINOR_THIRTEENTH, MAJOR_THIRTEENTH,
                 MINOR_FOURTEENTH, MAJOR_FOURTEENTH, PERFECT_FIFTEENTH, MINOR_SIXTEENTH,
                 MAJOR_SIXTEENTH, MINOR_SEVENTEENTH, MAJOR_SEVENTEENTH, PERFECT_EIGHTEENTH,
                 AUGMENTED_EIGHTEENTH, PERFECT_NINETEENTH, MINOR_TWENTIETH,
                 MAJOR_TWENTIETH, MINOR_TWENTYFIRST, MAJOR_TWENTYFIRST,
                 PERFECT_TWENTYSECOND, MINOR_TWENTYTHIRD, MAJOR_TWENTYTHIRD,
                 MINOR_TWENTYFOURTH, MAJOR_TWENTYFOURTH, PERFECT_TWENTYFIFTH,
                 AUGMENTED_TWENTYFIFTH, PERFECT_TWENTYSIXTH, MINOR_TWENTYSEVENTH,
                 MAJOR_TWENTYSEVENTH, MINOR_TWENTYEIGHTH, MAJOR_TWENTYEIGHTH,
                 PERFECT_TWENTYNINTH]

ROOT_STRENGHTS_AND_ROOTS = [[7, 0, 1], [5, 5, 2], [4, 0, 3], [8, 8, 4], [3, 0, 5], [9, 9, 6],
                            [2, 2, 7], [10, 0, 8], [1, 1, 9], [11, 0, 10], [0, 0, 11], [6, 6, 12]]


# (run-the-speac-weightings '((0 45 1000 4 55) (0 64 1000 3 55) (0 69 1000 2 55) . . . 4 8 4)
# (0.56 0.41 0.7799999999999999 0.51 1.33 0.51 1.26 0.51)
def run_the_speac_weightings(events, begin_beat, total_beats, meter):
    break_entrance = break_at_each_entrance(events)

    beat_lists_collect = collect_beat_lists(break_entrance)

    pitches = collect_pitch_lists(beat_lists_collect)

    vertical_tensions = create_lists_of_tensions(pitches)

    metric_tensions = map_metric_tensions(begin_beat, total_beats, meter)

    duration_tensions = compute_duration_tensions(events)

    approach_tensions = get_root_motion_weightings(events)

    return map_add(vertical_tensions, metric_tensions, duration_tensions, approach_tensions)


# (CREATE-LISTS-OF-TENSIONS (COLLECT-pitch-lists (collect-beat-lists (BREAK-AT-EACH-ENTRANCE book-example))))
# (0.3 0.3 0.5 0.3 0.5 0.3 0.3 0.3)
def create_lists_of_tensions(groups_of_midi_notes):
    groups_to_intervals = translate_groups_to_intervals(groups_of_midi_notes)
    rates = rate_lists(groups_to_intervals)
    result = compare(rates)
    return result


# (translate-groups-to-intervals '(((73 69 64 45)) ((73 69 64 57)  . . .
# (((19 28)) ((7 16) (7 17)) ((8 15)) . . .
def translate_groups_to_intervals(groups_of_midi_notes):
    result = []
    for beat in groups_of_midi_notes:
        result.append(translate_to_intervals(beat))
    return result


# (translate-to-intervals '((73 69 64 45)))
# ((19 28))
def translate_to_intervals(groups_of_midi_notes):
    result = []
    for list in groups_of_midi_notes:
        list_res = []
        list.sort()
        remove_octaves_res.clear()
        arranged_midi_notes = remove_octaves(list)
        bass_note = arranged_midi_notes[0]
        for note in arranged_midi_notes:
            if note != bass_note:
                list_res.append(note - bass_note)

        result.append(list_res)
    return result


remove_octaves_res = []


# (remove-octaves '(60 67 64 72 60 67 76))
# (60 67 64)
def remove_octaves(notes):
    if len(notes) == 0:
        return notes
    remove_octaves_res.append(notes[0])
    remove_octaves(remove_note(notes[0], notes[0:]))
    return remove_octaves_res


# (remove-note 60 '(67 64 72))
# (67 64)
def remove_note(note, notes):
    result = list(filter(lambda x: x % 12 != note % 12, notes))
    return result


# (collect-pitch-lists '((((0 73 1000 1 55) (0 69 1000 2 55) . . .
# (((73 69 64 45)) ((73 69 64 57) . . .
def collect_pitch_lists(pitch_lists):
    result = []
    for pitch_list in pitch_lists.copy():
        result.append(collect_pitches(pitch_list))
    return result


# (collect-pitches '(((6000 73 1000 1 55) (6000 64 1000 2 55) (6000 57 1000 3 55) (6000 57 1000 4 55))))
# ((73 64 57 57))
def collect_pitches(lists):
    result = []
    for events in lists:
        result.append(collect_pitch(events))
    return result


# (collect-pitch '((6000 73 1000 1 55) (6000 64 1000 2 55) (6000 57 1000 3 55) (6000 57 1000 4 55)))
# (73 64 57 57)
def collect_pitch(events):
    result = []
    for event in events:
        result.append(event[1])
    return result


# Сравнивает рейтинги, чтобы найти более созвучные для каждого бита
# (compare '((0.3) (0.3 0.65) (0.5) (0.3) (0.92 0.5) (0.3 1.2) (0.3) (0.3)))
# (0.3 0.3 0.5 0.3 0.5 0.3 0.3 0.3)
def compare(beat_rating_lists):
    result = []
    for ratings in beat_rating_lists:
        result.append(min(ratings))
    return result


# Назначает веса спискам
# (rate-lists '(((19 28)) ((7 16) (7 17)) ((8 15))  . . .
# ((0.3) (0.3 0.65) (0.5) (0.3) (0.92 0.5) (0.3 1.2) (0.3) (0.3))
def rate_lists(lists_of_intervals):
    result = []
    for list in lists_of_intervals:
        result.append(rate(list))
    return result


# Преобразует аргумент в вес на основе сохранённых значений
# (rate '((7 16) (7 16)))
# (0.3 0.3)
def rate(lists_of_intervals):
    lists_of_intervals = copy.deepcopy(lists_of_intervals)
    result = []

    while True:
        if len(lists_of_intervals) == 0:
            return result
        else:
            first_list = lists_of_intervals.pop(0)
            intervals_rate = rate_the_intervals(first_list)

            list_result = 0.0
            for rate in intervals_rate:
                list_result += rate

            rounded_result = my_round(list_result)
            result.append(rounded_result)


# (my-round 1.566)
#    1.57
def my_round(number):
    return float((round(number * 100)) / 100)


# Вохвращает рейтинг для входного интервала
# (rate-the-intervals '(7 16))
# ((0.1 0.2))
def rate_the_intervals(list_of_intervals):
    list_of_intervals = copy.deepcopy(list_of_intervals)
    result = []

    while True:
        if len(list_of_intervals) == 0:
            return result
        else:
            first_list = list_of_intervals.pop(0)
            result.append(INTERVAL_LIST[first_list])


# (collect-beat-lists '(((0 73 1000 1 55) (0 69 1000 2 55) . . .
# ((((0 73 1000 1 55) (0 69 1000 2 55) . . .
def collect_beat_lists(entrance_lists):
    result = []
    local_result = []
    need_to_add_next = False
    first = True
    for simultaneous_event in entrance_lists:
        if not need_to_add_next and not first:
            result.append(local_result)
            local_result = []

        first = False
        local_result.append(simultaneous_event)
        need_to_add_next = False

        for event in simultaneous_event:
            if len(event) == 6:
                need_to_add_next = True

    result.append(local_result)
    return result


def group_bits(entrance_lists):
    return [entrance_lists]


# (break-at-each-entrance ((0 45 1000 4 55) (0 64 1000 3 55)  . . .
# (((0 73 1000 1 55) (0 69 1000 2 55)  . . .
def break_at_each_entrance(events):
    exits_and_entrances = []
    events = fix_the_triplets(events)
    events.sort()

    while len(events) != 0:
        event = events[0]
        simultaneous_events = place_events_in_channel_order(collect_simultaneous_events(events))

        if exits_and_entrances != []:
            new_entrance_time = get_new_exit_and_entrance_time(events, event[0])
        else:
            new_entrance_time = get_new_entrance_time(events, event[0], event[0] + event[2])

        reset_dur = reset_durations(new_entrance_time, simultaneous_events)
        exits_and_entrances.append(reset_dur)

        reset_next_dur = reset_next_durations(new_entrance_time, copy.deepcopy(simultaneous_events))
        remove_zero_dur = remove_zero_durations(reset_next_dur)
        if remove_zero_dur != []:
            for element in remove_zero_dur:
                events.append(element)
        remove_a = remove_all(simultaneous_events, events)
        events.sort()

    return exits_and_entrances


# (place-events-in-channel-order '((0 73 1000 2 55) (0 69 1000 1 55)))
# ((0 69 1000 1 55) (0 73 1000 2 55))
def place_events_in_channel_order(events):
    ordered_channels = []
    ordered_events = []

    for event in events:
        ordered_channels.append(event[3])
    ordered_channels.sort()

    events_copy = copy.deepcopy(events)

    while len(ordered_events) != len(ordered_channels):
        for channel in ordered_channels:
            for event in events_copy:
                if event[3] == channel:
                    ordered_events.append(event)
                    events_copy.remove(event)
                    break
    return ordered_events


# Выводит нужный элемент бита
# (find-channel-event 2 '((0 73 1000 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55)))
# ((0 69 1000 2 55)
def find_channel_event(channel, events):
    return events[channel - 1]


# (get-channel 1 '((0 45 1000 1 55) (0 64 1000 3 55)))
# ((0 45 1000 1 55))
def get_channel(number, music):
    channel_music = []
    for event in music:
        if event[3] == number:
            channel_music.append(event)
    return channel_music


# (get-all-channels '((0 45 1000 4 55) (0 64 1000 3 55) . . .
# (((0 73 1000 1 55) (1000 73 500 1 55)  . . .
def get_all_channels(music):
    all_channels_music = []
    for i in range(1, 17):
        one_channel_music = get_channel(i, music)
        all_channels_music.append(one_channel_music)
    return all_channels_music


# (remove-zero-durations '((1000 72 0 1 127) (1000 67 0 2 127) (1000 64 0 3 127) (1000 60 0 4 127)))
#  nil
def remove_zero_durations(events):
    return list(filter(lambda event: event[2] != 0, events))


# Собирает в один список ноты, которые играются одновременно в первый момент времени
# (collect-simultaneous-events '((0 73 1000 1 55) (0 69 1000 2 55)  . . .
# ((0 73 1000 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55))
def collect_simultaneous_events(events):
    first_bit_notes = []
    one_time = events[0][0]
    for event in events:
        if event[0] != one_time:
            break
        else:
            first_bit_notes.append(event)
    return first_bit_notes


# (fix-triplets '((0 73 1000 1 55) (1001 73 500 1 55) (1000 74 500 1 55) (999 74 500 55)))
# ((0 73 1001 1 55) (1001 73 500 1 55) (1000 74 500 1 55) (999 74 500 55))
def fix_triplets(events):
    new_events = []
    for i in range(0, len(events)):
        cur_event = events[i]
        # если есть следующая нота
        if i != len(events) - 1:
            next_event = events[i + 1]
            # если следующая нота начинается на 1 раньше или позже
            # (то есть, например, вместо 1000 999 или 1001), то длительность предыдущей ноты
            # изменяется на 1
            if abs(cur_event[0] + cur_event[2] - next_event[0]) == 1:
                cur_event[2] -= (cur_event[0] + cur_event[2] - next_event[0])

        new_events.append(cur_event)
    return new_events


# (fix-the-triplets '((0 45 1000 4 55) (0 64 1000 3 55) (0 69 1000 2 55) (0 73 1000 1 55) (1000 57 1000 4 55) . . .
# ((0 73 1000 1 55) (1000 73 500 1 55)  . . .
def fix_the_triplets(events):
    res = []
    for channel in get_all_channels(events):
        if channel != []:
            triplets_fix = fix_triplets(channel)
            for event in triplets_fix:
                res.append(event)
    return res


# (remove-all '((0 73 333 1 55)) '((0 73 333 1 55) (0 69 444 2 55) (1500 45 1000 4 55)))
# ((0 69 444 2 55) (1500 45 1000 4 55))
def remove_all(simultaneous_events, ordered_events):
    for event in simultaneous_events:
        ordered_events.remove(event)
    return ordered_events


# Вернёт или мин. длительность звучания ноты в ивенте или время начала следующего ивента
# (get-new-exit-and-entrance-time '((0 73 333 1 55) (0 69 444 2 55) (1500 45 1000 4 55)) 0)
# 333
def get_new_exit_and_entrance_time(events, start_time):
    events.sort()
    end_time = get_shortest_duration(start_time, events) + start_time
    new_start_time = get_next_start_time(start_time, events)

    if end_time is None:
        return new_start_time
    elif new_start_time is None:
        return end_time
    elif end_time > new_start_time:
        return new_start_time
    else:
        return end_time


# (get-next-start-time 0 '((0 73 1000 1 55) (0 69 1000 2 55)  . . .
# 1000
def get_next_start_time(start_time, events):
    for event in events:
        if event[0] != start_time:
            return event[0]
    return None


# (get-new-entrance-time '((0 73 1000 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55) (1000 73 500 1 55) . . .
# 1000
def get_new_entrance_time(events, start_time, end_time):
    for event in events:
        if event[0] != start_time:
            return event[0]
    return end_time


# (get-shortest-duration 0 '((0 73 1000 1 55) (0 69 1000 2 55)  . . .
# 1000
def get_shortest_duration(start_time, events):
    start_time_events = []
    for event in events:
        if event[0] != start_time:
            break
        else:
            start_time_events.append(event)
    return get_shortest(start_time_events)


# (get-shortest '((0 73 1000 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55)))
#    1000
def get_shortest(events):
    durations = []
    for event in events:
        durations.append(event[2])
    durations.sort()
    return durations[0]


# (reset-durations 1000 '((0 73 1500 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55)))
# ((0 73 1000 1 55 *) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55))
def reset_durations(new_entrance_time, simultaneous_events):
    edited_events = []
    for event in simultaneous_events:
        new_event = [event[0], event[1]]
        need_to_add_char = False
        if event[0] + event[2] > new_entrance_time:
            new_event.append(new_entrance_time - event[0])
            need_to_add_char = True
        else:
            new_event.append(event[2])
        new_event.append(event[3])
        new_event.append(event[4])
        if need_to_add_char:
            new_event.append("*")
        edited_events.append(new_event)
    return edited_events


# (reset-next-durations 1000 '((0 73 1000 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55)))
# ((1000 73 0 1 55) (1000 69 0 2 55) (1000 64 0 3 55) (1000 45 0 4 55))
def reset_next_durations(new_entrance_time, ordered_events):
    edited_events = []
    for event in ordered_events:
        event[2] = event[2] - (new_entrance_time - event[0])
        event[0] = new_entrance_time
        edited_events.append(event)
    return edited_events


# (map-metric-tensions 4 8 4)
# (0.2 0.05 0.1 0.05 0.2 0.05 0.1 0.05)
def map_metric_tensions(start_beat, total_beats, meter, beat=0, result=[]):
    start_beat_copy = copy.deepcopy(start_beat)
    total_beats = copy.deepcopy(total_beats)

    if beat == 0:
        result.clear()

    if total_beats != beat:

        result.append(lookup_and_figure_metric_tension(meter, start_beat_copy))

        if start_beat_copy == meter:
            new_start_beat = 1
        else:
            new_start_beat = start_beat_copy + 1

        map_metric_tensions(new_start_beat, total_beats, meter, beat + + 1)
    return result


# (lookup-and-figure-metric-tension 9 7)
# 0.05
def lookup_and_figure_metric_tension(meter, beat_number):
    for element in METRIC_TENSION_TABLE:
        if element[0] == meter:
            return float('{:.3}'.format((beat_number * 0.1) / (element[beat_number][1])))


# Добавление карт по различным параметрам анализа
# (map-add '(0.3 0.3 0.5 0.3 0.5 0.3 0.3 0.3)
# '(0.2 0.05 0.1 0.05000000000000001 0.2 0.05 0.1 0.05000000000000001)
# '(0.06 0.06 0.08 0.06 0.08 0.06 0.06 0.06) (0 0 0.1 0.1 0.55 0.1 0.8 0.1))
# (0.56 0.41 0.7799999999999999 0.51 1.33 0.51 1.26 0.51)
def map_add(list_1, list_2, list_3, list_4):
    parameters_result = []
    for i in range(1, len(list_1) + 1):
        if len(list_1) < i or len(list_2) < i or len(list_3) < i or len(list_4) < i:
            break
        cur_res = numpy.float32(list_1[i - 1])
        cur_res += numpy.float32(list_2[i - 1])
        cur_res += numpy.float32(list_3[i - 1])
        cur_res += numpy.float32(list_4[i - 1])
        parameters_result.append(cur_res)
    return parameters_result


# Returns the interval between ontimes
# (get-durations '(0 1000 2000 3000 4000 5000 6000 7000))
#  (1000 1000 1000 1000 1000 1000 1000 1000)
def get_durations(ontimes):
    result = []

    before = None
    for i in range(1, len(ontimes) + 1):
        if before is None:
            before = ontimes[i - 1]
        else:
            result.append(ontimes[i - 1] - before)
            before = ontimes[i - 1]

    if len(ontimes) == 1 or len(ontimes) == 0:
        result.append(0)
    else:
        result.append(result[len(result) - 1])

    return result


# (duration-map '((((0 73 1000 1 55) (0 69 1000 2 55) (0 64 1000 3 55) (0 45 1000 4 55))) (((1000 73 500 1 55) . . .
# (1000 1000 1000 1000 1000 1000 1000 1000)
def duration_map(beats):
    ontimes = []
    for beat in beats:
        ontimes.append(beat[0][0][0])
    return get_durations(ontimes)


# (compute-duration-tensions book-example)
# (0.06 0.06 0.08 0.06 0.08 0.06 0.06 0.06)
def compute_duration_tensions(events):
    each_entrance_break = break_at_each_entrance(events)

    beat_lists_collect = collect_beat_lists(each_entrance_break)

    durations = duration_map(beat_lists_collect)

    pitch_lists_collect = collect_pitch_lists(beat_lists_collect)
    interval_tensions = create_lists_of_tensions(pitch_lists_collect)

    result = []
    i = 0
    # В LISP числа с плавающей точкой 32-разрядные, в Python - нет.
    # Чтобы результаты совпадали приводим к этому формату
    for duration in durations:
        local_res = numpy.float32(0.01) * numpy.float32(
            round(numpy.float32(100) * ((numpy.float32((duration / 4000)) * numpy.float32(0.1)) +
                                        (numpy.float32(interval_tensions[i]) * numpy.float32(0.1)))))
        result.append(local_res)

        i += 1
    return result


# (get-root-motion-weightings book-example)
# (0 0 0.1 0.1 0 0.8 0.8 0.1)
def get_root_motion_weightings(events):
    roots = get_chord_roots(events)
    result = find_motion_weightings(roots)
    result.insert(0, 0)
    return result


# (find-motion-weightings '(45 57 64 57 62 55 57 50))
#  (0 0.1 0.1 0.55 0.1 0.8 0.1)
def find_motion_weightings(roots):
    size = len(roots)
    result = []
    roots_copy = roots.copy()
    for i in range(1, size):
        cur_root = roots_copy[0]

        if len(roots_copy) > 1:
            next_root = roots_copy[1]
            diff = abs(cur_root - next_root)
            result.append(INTERVAL_LIST[diff % 12])
            roots_copy.pop(0)

    return result


# (get-chord-roots book-example)
# (45 57 64 57 62 55 57 50)
def get_chord_roots(events):
    pitch_list = collect_pitch_lists(collect_beat_lists(break_at_each_entrance(events)))
    on_beat_pitch_lists = []

    for i in range(1, len(pitch_list) + 1):
        scrunch_local_res = scrunch(pitch_list[i - 1])
        scrunch_local_res.sort()
        on_beat_pitch_lists.append(scrunch_local_res)

    intervals = []
    for element in on_beat_pitch_lists:
        element_copy = element.copy()
        intervals.append(derive(element_copy))

    roots = []
    for element in intervals:
        element_copy = element.copy()
        roots.append(find_strongest_root_interval(element_copy))

    result = []
    for root in roots:
        interval_in_chord = find_interval_in_chord(root, on_beat_pitch_lists[0])
        interval_in_chord.sort()
        upper_lower_res = find_upper_lower(root, interval_in_chord)
        result.append(upper_lower_res)
        on_beat_pitch_lists.pop(0)

    return result


# (derive (55 64 84)) -> (0 5 8 9)
# (derive (72))       -> (0)
# (derive (41 74 76)) -> (0 2 9 11)
def derive(pitches):
    intervals = derive_all_intervals(pitches)
    return sorted(set(intervals))


# (derive-all-intervals '(45 64 69 73))
#  (0 7 0 4 0 5 9 0 4)
def derive_all_intervals(pitches):
    result = []
    size = len(pitches)

    for i in range(1, size):
        local_result = derive_intervals(pitches)
        for e in local_result:
            result.append(e)
        pitches.pop(0)
    result.append(0)

    return result


# (derive-intervals '(45 64 69 73))
#   (0 7 0 4)
def derive_intervals(pitches):
    result = []
    first_pitch = pitches[0]

    for pitch in pitches:
        diff = pitch - first_pitch
        result.append(diff % 12)
    return result


def scrunch(lists):
    result = []
    for list in lists:
        for element in list:
            if element not in result:
                result.append(element)
    return result


# Returns the root note
# (find-upper-lower 7 '(45 64))
#  45
def find_upper_lower(root, interval):
    test = None
    for element in ROOT_STRENGHTS_AND_ROOTS:
        if root == element[0]:
            test = element
            break
    if test[1] == 0:
        return interval[0]
    else:
        return interval[1]


# (find-strongest-root-interval '(0 7 4 0 0 9 5 0 8))
#   7
def find_strongest_root_interval(intervals):
    intervals_copy = copy.deepcopy(intervals)
    test = find_root_strenghts_and_roots(intervals_copy)
    sorted_test = sort_CADDR(test)
    return sorted_test[0][0]


# ('((2 (a b c))(3 (d e f))(1 (g h i))))
#  >> ((1 (G H I)) (2 (A B C)) (3 (D E F)))
def sort_CADDR(lists):
    lists.sort(key=sort_by_third_element)
    return lists


# Внешняя функция, которая будет сортировать списки по 3 элементу
def sort_by_third_element(some_list):
    return some_list[2]  # Ключом является третий символ в каждом списке, сортируем по нему


# (find-root-strengths-and-roots '(0 7 4 0 0 9 5 0 8))
#   ((0 0 11) (7 0 1) (4 0 3) (0 0 11) (0 0 11) (9 9 6) (5 5 2) (0 0 11) (8 8 4))
def find_root_strenghts_and_roots(pc_intervals):
    result = []
    for interval in pc_intervals:
        for element in ROOT_STRENGHTS_AND_ROOTS:
            if interval == element[0]:
                result.append(element)
                break
    return result


# (find-interval-in-chord 7 '(54 62 64 69))
# (69 62)
def find_interval_in_chord(interval, chord):
    if len(chord) == 1:
        return chord
    else:
        return find_it_in_chord(interval, derive_all_pitches(chord))


# (find-it-in-chord 7 '(54 54 54 62 54 64 54 69 62 62 62 64 62 69 64 64 64 69))
#  (69 62)
def find_it_in_chord(interval, chord):
    size = len(chord)
    for i in range(1, size):
        pitch = chord[0]
        if len(chord) > 1:
            next_pitch = chord[1]
            diff = next_pitch - pitch
            if diff % 12 == interval:
                return [next_pitch, pitch]
        chord.pop(0)
    # В коде на LISP происходит чудо, там (mod -5 11) даст результат 6 (типа 11 - 5)...
    return None


# (derive-all-pitches '(54 62 64 69))
# (54 54 54 62 54 64 54 69 62 62 62 64 62 69 64 64 64 69)
def derive_all_pitches(pitches):
    result = []
    size = len(pitches)
    for i in range(1, size):
        pitch = pitches[0]
        for two_pitches in derive_pitches(pitches):
            for e in two_pitches:
                result.append(e)
        pitches.remove(pitch)

    return result


# (derive-pitches '(54 62 64 69))
#  ((54 54) (54 62) (54 64) (54 69))
def derive_pitches(pitches):
    result = []
    first_pitch = pitches[0]
    for pitch in pitches:
        local_result = [first_pitch, pitch]
        result.append(local_result)
    return result
