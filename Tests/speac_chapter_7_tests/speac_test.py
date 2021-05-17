import unittest

from Tests.speac_chapter_7_tests.chopin_33_3 import CHOPIN_33_3
from speac.speac_chapter_7.speac import *


class TestSPEAC(unittest.TestCase):

    def test_all(self):
        self.test_compare()
        self.test_rate_the_intervals()
        self.test_my_round()
        self.test_rate()
        self.test_rate_lists()
        self.test_collect_pitch()
        self.test_collect_pitches()
        self.test_collect_pitch_lists()
        self.test_remove_note()
        self.test_remove_octaves()
        self.test_translate_to_intervals()
        self.test_translate_groups_to_intervals()
        self.test_find_channel_event()
        self.test_remove_zero_durations()
        self.test_collect_simultaneous_events()
        self.test_get_channel()
        self.test_get_all_channels_music()
        self.test_get_shortest()
        self.test_get_shortest_duration()
        self.test_reset_durations()
        self.test_reset_next_durations()
        self.test_get_new_entrance_time()
        self.test_get_next_start_time()
        self.test_get_new_exit_and_entrance_time()
        self.test_remove_all()
        self.test_place_events_in_channel_order()
        self.test_fix_triplets()
        self.test_fix_the_triplets()
        self.test_break_at_each_entrance()
        self.test_collect_beat_lists()
        self.test_create_lists_of_tensions()
        self.test_map_add()
        self.test_lookup_and_figure_metric_tension()
        self.test_map_metric_tensions()
        self.test_get_durations()
        self.test_duration_map()
        self.test_derive_pitches()
        self.test_derive_all_pitches()
        self.test_find_interval_in_chord()
        self.test_derive_intervals()
        self.test_derive_all_intervals()
        self.test_find_root_strenghts_and_roots()
        self.test_find_strongest_root_interval()
        self.test_sort_CADDR()
        self.test_find_upper_lower()
        self.test_derive()
        self.test_scrunch()
        self.test_get_chord_roots()
        self.test_find_motion_weightings()
        self.test_get_root_motion_weightings()
        self.test_compute_duration_tensions()
        self.test_run_the_speac_weightings()


    def test_compare(self):
        beat_ratings_lists = [[0.3], [0.3, 0.65], [0.5], [0.3], [0.92, 0.5], [0.3, 1.2], [0.3], [0.3]]
        result = [0.3, 0.3, 0.5, 0.3, 0.5, 0.3, 0.3, 0.3]
        self.assertEqual(compare(beat_ratings_lists), result)

    def test_rate_the_intervals(self):
        list_of_intervals = [10, 16, 19, 33]
        result = [0.7, 0.2, 0.1, 0.25]
        self.assertEqual(rate_the_intervals(list_of_intervals), result)

        list_of_intervals = [7, 16]
        result = [0.1, 0.2]
        self.assertEqual(rate_the_intervals(list_of_intervals), result)

        list_of_intervals = [5, 13]
        result = [0.55, 1]
        self.assertEqual(rate_the_intervals(list_of_intervals), result)

        list_of_intervals = [10]
        result = [0.7]
        self.assertEqual(rate_the_intervals(list_of_intervals), result)
        self.assertEqual(rate_the_intervals([]), [])

    def test_my_round(self):
        self.assertEqual(1.01, my_round(1.01111))
        self.assertEqual(1.56, my_round(1.56))
        self.assertEqual(1.57, my_round(1.566))

    def test_rate(self):
        self.assertEqual([1.0], rate([[10, 16, 19]]))
        self.assertEqual([2.35, 1.15, 1.0], rate([[2, 6, 11], [10, 16, 21], [10, 16, 19]]))

        lists_of_intervals = [[7, 16]]
        result = [0.3]
        self.assertEqual(result, rate(lists_of_intervals))

        lists_of_intervals = [[4, 21]]
        result = [0.45]
        self.assertEqual(result, rate(lists_of_intervals))

        lists_of_intervals = [[4, 21], [7, 16]]
        result = [0.45, 0.3]
        self.assertEqual(result, rate(lists_of_intervals))

        lists_of_intervals = [[10]]
        result = [0.7]
        self.assertEqual(result, rate(lists_of_intervals))

    def test_rate_lists(self):
        input = [[[10, 16, 19]], [[2, 6, 11], [10, 16, 21], [10, 16, 19]], [[4, 7], [4, 7, 11]],
                 [[4, 7], [5, 9], [5, 9, 18]], [[6, 8, 15], [6, 8, 16]], [[2, 6, 11], [10, 16, 21], [10, 16, 19]],
                 [[4, 7], [4, 7, 11]], [[4, 7], [4, 7]], [[10, 16, 19]], [[10, 16, 20], [10, 16, 20], [10, 16, 19]],
                 [[4, 7, 10], [4, 7, 10, 11]], [[4, 7, 10], [4, 7, 10], [4, 7, 10, 14]], [[16, 22], [16, 23]],
                 [[9, 15, 19], [16, 19, 22, 26], [16, 19, 22]], [[10, 16, 18], [10, 16, 19]], [[2, 6], [10, 16]]]

        result = [[1.0], [2.35, 1.15, 1.0], [0.3, 1.2], [0.3, 0.8, 1.45], [1.15, 1.12], [2.35, 1.15, 1.0], [0.3, 1.2],
                  [0.3, 0.3], [1.0], [1.17, 1.17, 1.0], [1.0, 1.9], [1.0, 1.0, 1.8], [0.9, 1.1], [0.57, 1.8, 1.0],
                  [1.55, 1.0], [1.45, 0.9]]

        self.assertEqual(result, rate_lists(input))

        list1 = [19, 28]
        list2 = [7, 16]
        list3 = [7, 17]
        list4 = [8, 15]
        input = [[list1], [list2, list3], [list4]]
        result = [[0.3], [0.3, 0.65], [0.5]]
        self.assertEqual(result, rate_lists(input))

    def test_collect_pitch(self):
        input = [[6000, 73, 1000, 1, 55], [6000, 64, 1000, 2, 55],
                 [6000, 57, 1000, 3, 55], [6000, 57, 1000, 4, 55]]
        res = [73, 64, 57, 57]
        self.assertEqual(res, collect_pitch(input))

    def test_collect_pitches(self):
        input = [[[6000, 73, 1000, 1, 55], [6000, 64, 1000, 2, 55],
                  [6000, 57, 1000, 3, 55], [6000, 57, 1000, 4, 55]]]
        res = [[73, 64, 57, 57]]
        self.assertEqual(res, collect_pitches(input))

    def test_collect_pitch_lists(self):
        input = [
            [[[6000, 73, 1000, 1, 55], [6000, 64, 1000, 2, 55],
              [6000, 57, 1000, 3, 55], [6000, 57, 1000, 4, 55]]],

            [[[6000, 73, 1000, 1, 55], [6000, 64, 1000, 2, 55],
              [6000, 57, 1000, 3, 55], [6000, 57, 1000, 4, 55]]]]

        res = [[[73, 64, 57, 57]],
               [[73, 64, 57, 57]]]
        self.assertEqual(res, collect_pitch_lists(input))

    def test_remove_note(self):
        note = 60
        notes = [67, 64, 72, 84, 48, 36]
        res = [67, 64]
        self.assertEqual(res, remove_note(note, notes))

    def test_remove_octaves(self):
        notes = [60, 67, 64, 72, 60, 48, 36, 40, 33, 93]
        res = [60, 67, 64, 33]
        remove_octaves_res.clear()
        self.assertEqual(res, remove_octaves(notes))
        remove_octaves_res.clear()

    def test_translate_to_intervals(self):
        input = [[53, 37, 41, 64], [32, 75, 36, 87, 35, 61]]
        res = [[4, 27], [3, 4, 29, 43]]
        self.assertEqual(res, translate_to_intervals(input))

        input = [[73, 69, 64, 45]]
        res = [[19, 28]]
        self.assertEqual(res, translate_to_intervals(input))

    def test_translate_groups_to_intervals(self):
        input = [[[53, 37, 41, 64], [32, 75, 36, 87, 35, 61]], [[73, 69, 64, 45]]]
        res = [[[4, 27], [3, 4, 29, 43]], [[19, 28]]]
        self.assertEqual(res, translate_groups_to_intervals(input))

    def test_find_channel_event(self):
        channel = 3
        events = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [0, 64, 1000, 3, 55], [0, 45, 1000, 4, 55]]
        res = [0, 64, 1000, 3, 55]
        self.assertEqual(res, find_channel_event(channel, events))

    def test_remove_zero_durations(self):
        events = [[1000, 72, 0, 1, 127], [1000, 67, 1, 2, 127]]
        res = [[1000, 67, 1, 2, 127]]
        self.assertEqual(res, remove_zero_durations(events))
        events = [[1000, 72, 0, 1, 127]]
        res = []
        self.assertEqual(res, remove_zero_durations(events))

    def test_collect_simultaneous_events(self):
        events = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]]
        res = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55]]
        self.assertEqual(res, collect_simultaneous_events(events))

    def test_get_channel(self):
        music = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]]
        channel = 2
        res = [[0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]]
        self.assertEqual(res, get_channel(channel, music))

    def test_get_all_channels_music(self):
        music = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]]
        res = [[[0, 73, 1000, 1, 55]], [[0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]],
               [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        self.assertEqual(res, get_all_channels(music))

    def test_get_shortest(self):
        music = [[0, 73, 1000, 1, 55], [0, 69, 1500, 2, 55], [500, 69, 500, 2, 55], [1499, 74, 2000, 3, 55]]
        res = 500
        self.assertEqual(res, get_shortest(music))

    def test_get_shortest_duration(self):
        start_time = 0
        events = [[0, 73, 1000, 1, 55], [0, 69, 500, 2, 55], [0, 69, 250, 2, 55], [1000, 74, 2000, 3, 55]]
        res = 250
        self.assertEqual(res, get_shortest_duration(start_time, events))

    def test_reset_durations(self):
        new_entrance_time = 1700
        simultaneous_events = [[1000, 73, 1800, 1, 55], [1000, 69, 1000, 2, 55]]
        res = [[1000, 73, 700, 1, 55, "*"], [1000, 69, 700, 2, 55, "*"]]
        self.assertEqual(res, reset_durations(new_entrance_time, simultaneous_events))

        new_entrance_time = 500
        simultaneous_events = [[100, 73, 150, 1, 55], [4670, 69, 1290, 2, 55]]
        res = [[100, 73, 150, 1, 55], [4670, 69, -4170, 2, 55, "*"]]
        self.assertEqual(res, reset_durations(new_entrance_time, simultaneous_events))

        new_entrance_time = 2001
        simultaneous_events = [[2000, 57, 1000, 2, 55]]
        res = [[2000, 57, 1, 2, 55, "*"]]
        self.assertEqual(res, reset_durations(new_entrance_time, simultaneous_events))

    def test_reset_next_durations(self):
        new_entrance_time = 1000
        ordered_events = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55]]
        res = [[1000, 73, 0, 1, 55], [1000, 69, 0, 2, 55]]
        self.assertEqual(res, reset_next_durations(new_entrance_time, ordered_events))
        ordered_events = [[0, 73, 1000, 1, 55], [500, 69, 1000, 2, 55]]
        res = [[1000, 73, 0, 1, 55], [1000, 69, 500, 2, 55]]
        self.assertEqual(res, reset_next_durations(new_entrance_time, ordered_events))
        new_entrance_time = -777
        ordered_events = [[7, 73, 1354, 1, 55], [785, 69, -530, 2, 55]]
        res = [[-777, 73, 2138, 1, 55], [-777, 69, 1032, 2, 55]]
        self.assertEqual(res, reset_next_durations(new_entrance_time, ordered_events))

    def test_get_new_entrance_time(self):
        events = [[1500, 73, 1000, 1, 55], [1500, 95, 1000, 1, 55], [1700, 73, 1000, 1, 55]]
        start_time = 1500
        end_time = 3000
        res = 1700
        self.assertEqual(res, get_new_entrance_time(events, start_time, end_time))
        events = [[1500, 73, 1000, 1, 55]]
        start_time = 1500
        end_time = 1600
        res = 1600
        self.assertEqual(res, get_new_entrance_time(events, start_time, end_time))

    def test_get_next_start_time(self):
        events = [[0, 73, 1000, 1, 55], [0, 69, 500, 2, 55], [0, 69, 250, 2, 55], [777, 74, 2000, 3, 55]]
        start_time = 0
        res = 777
        self.assertEqual(res, get_next_start_time(start_time, events))
        events = [[0, 73, 1000, 1, 55]]
        self.assertEqual(None, get_next_start_time(start_time, events))

    def test_get_new_exit_and_entrance_time(self):
        events = [[0, 73, 333, 1, 55], [0, 69, 222, 2, 55], [1500, 45, 1000, 4, 55]]
        start_time = 0
        res = 222
        self.assertEqual(res, get_new_exit_and_entrance_time(events, start_time))

        events = [[0, 73, 333, 1, 55], [0, 69, 444, 2, 55], [1500, 45, 1000, 4, 55]]
        start_time = 0
        res = 333
        self.assertEqual(res, get_new_exit_and_entrance_time(events, start_time))

        events = [[0, 69, 1500, 2, 55]]
        start_time = 0
        res = 1500
        self.assertEqual(res, get_new_exit_and_entrance_time(events, start_time))

    def test_remove_all(self):
        music = [[0, 73, 333, 1, 55], [0, 69, 333, 1, 55], [2000, 73, 333, 1, 55]]
        events = [[0, 73, 333, 1, 55], [0, 69, 333, 1, 55]]
        res = [[2000, 73, 333, 1, 55]]
        self.assertEqual(res, remove_all(events, music))

    def test_place_events_in_channel_order(self):
        events = [[0, 55, 1000, 2, 64], [0, 65, 1000, 2, 64]]
        res = [[0, 55, 1000, 2, 64], [0, 65, 1000, 2, 64]]
        self.assertEqual(res, place_events_in_channel_order(events))

        events = [[0, 73, 1000, 2, 55], [0, 69, 1000, 1, 55], [0, 69, 1000, 4, 55], [0, 69, 1000, 3, 55]]
        res = [[0, 69, 1000, 1, 55], [0, 73, 1000, 2, 55], [0, 69, 1000, 3, 55], [0, 69, 1000, 4, 55]]
        self.assertEqual(res, place_events_in_channel_order(events))

    def test_fix_triplets(self):
        music = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]]
        res = [[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [1000, 69, 1000, 2, 55]]
        self.assertEqual(res, fix_triplets(music))

        music = [[0, 73, 1000, 1, 55], [1001, 69, 500, 2, 55], [1000, 69, 500, 2, 55], [1499, 74, 500, 3, 55]]
        res = [[0, 73, 1001, 1, 55], [1001, 69, 500, 2, 55], [1000, 69, 499, 2, 55], [1499, 74, 500, 3, 55]]
        self.assertEqual(res, fix_triplets(music))

        music = [[2000, 57, 1000, 2, 55], [2001, 64, 1000, 1, 55]]
        res = [[2000, 57, 1000, 2, 55], [2001, 64, 1000, 1, 55]]
        self.assertEqual(res, fix_triplets(music))

    def test_fix_the_triplets(self):
        music = [[0, 45, 1000, 4, 55], [0, 64, 1000, 3, 55],
                 [1000, 57, 1000, 4, 55], [1000, 64, 1000, 3, 55],
                 [2000, 76, 1000, 1, 55],
                 [3000, 57, 1000, 4, 55], [3000, 67, 1000, 4, 55]]
        res = [[2000, 76, 1000, 1, 55], [0, 64, 1000, 3, 55], [1000, 64, 1000, 3, 55],
               [0, 45, 1000, 4, 55], [1000, 57, 1000, 4, 55], [3000, 57, 1000, 4, 55], [3000, 67, 1000, 4, 55]]
        self.assertEqual(res, fix_the_triplets(music))

        music = [[2000, 57, 1000, 2, 55], [2001, 64, 1000, 1, 55]]
        res = [[2001, 64, 1000, 1, 55], [2000, 57, 1000, 2, 55]]
        self.assertEqual(res, fix_the_triplets(music))

    BOOK_EXAMPLE = [[0, 45, 1000, 4, 55], [0, 64, 1000, 3, 55], [0, 69, 1000, 2, 55], [0, 73, 1000, 1, 55],
                    [1000, 57, 1000, 4, 55], [1000, 64, 1000, 3, 55], [1000, 69, 1000, 2, 55], [1000, 73, 500, 1, 55],
                    [1500, 74, 500, 1, 55], [2000, 56, 1000, 4, 55], [2000, 64, 1000, 3, 55], [2000, 71, 1000, 2, 55],
                    [2000, 76, 1000, 1, 55], [3000, 57, 1000, 4, 55], [3000, 64, 1000, 3, 55], [3000, 69, 1000, 2, 55],
                    [3000, 73, 1000, 1, 55], [4000, 54, 1000, 4, 55], [4000, 64, 500, 3, 55], [4500, 62, 500, 3, 55],
                    [4000, 69, 1000, 2, 55], [4000, 69, 1000, 1, 55], [5000, 55, 1000, 4, 55], [5000, 62, 1000, 3, 55],
                    [5000, 67, 500, 2, 55], [5500, 66, 500, 2, 55], [5000, 71, 1000, 1, 55], [6000, 57, 1000, 4, 55],
                    [6000, 57, 1000, 3, 55], [6000, 64, 1000, 2, 55], [6000, 73, 1000, 1, 55], [7000, 50, 1000, 4, 55],
                    [7000, 57, 1000, 3, 55], [7000, 66, 1000, 2, 55], [7000, 74, 1000, 1, 55]]

    def test_break_at_each_entrance(self):
        res = [[[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55], [0, 64, 1000, 3, 55], [0, 45, 1000, 4, 55]],
               [[1000, 73, 500, 1, 55], [1000, 69, 500, 2, 55, "*"], [1000, 64, 500, 3, 55, "*"],
                [1000, 57, 500, 4, 55, "*"]],
               [[1500, 74, 500, 1, 55], [1500, 69, 500, 2, 55], [1500, 64, 500, 3, 55], [1500, 57, 500, 4, 55]],
               [[2000, 76, 1000, 1, 55], [2000, 71, 1000, 2, 55], [2000, 64, 1000, 3, 55], [2000, 56, 1000, 4, 55]],
               [[3000, 73, 1000, 1, 55], [3000, 69, 1000, 2, 55], [3000, 64, 1000, 3, 55], [3000, 57, 1000, 4, 55]],
               [[4000, 69, 500, 1, 55, "*"], [4000, 69, 500, 2, 55, "*"], [4000, 64, 500, 3, 55],
                [4000, 54, 500, 4, 55, "*"]],
               [[4500, 69, 500, 1, 55], [4500, 69, 500, 2, 55], [4500, 62, 500, 3, 55], [4500, 54, 500, 4, 55]],
               [[5000, 71, 500, 1, 55, "*"], [5000, 67, 500, 2, 55], [5000, 62, 500, 3, 55, "*"],
                [5000, 55, 500, 4, 55, "*"]],
               [[5500, 71, 500, 1, 55], [5500, 66, 500, 2, 55], [5500, 62, 500, 3, 55], [5500, 55, 500, 4, 55]],
               [[6000, 73, 1000, 1, 55], [6000, 64, 1000, 2, 55], [6000, 57, 1000, 3, 55], [6000, 57, 1000, 4, 55]],
               [[7000, 74, 1000, 1, 55], [7000, 66, 1000, 2, 55], [7000, 57, 1000, 3, 55], [7000, 50, 1000, 4, 55]]]

        input = self.BOOK_EXAMPLE
        self.assertEqual(res, break_at_each_entrance(input))

        input = [[2000, 57, 1000, 2, 55], [2001, 64, 1000, 1, 55]]
        res = [[[2000, 57, 1, 2, 55, "*"]],
               [[2001, 64, 999, 1, 55, "*"], [2001, 57, 999, 2, 55]],
               [[3000, 64, 1, 1, 55]]]

        self.assertEqual(res, break_at_each_entrance(input))

    def test_collect_beat_lists(self):
        entrance_lists = [[[0, 73, 1000, 1, 55, "*"], [0, 69, 1000, 2, 55, "*"]],
                          [[1000, 69, 500, 1, 55]],
                          [[4000, 69, 500, 2, 55]],
                          [[5000, 71, 500, 1, 55]],
                          [[5500, 73, 1000, 2, 55, "*"]],
                          [[6500, 87, 250, 4, 77]]]

        result = [[[[0, 73, 1000, 1, 55, "*"], [0, 69, 1000, 2, 55, "*"]], [[1000, 69, 500, 1, 55]]],
                  [[[4000, 69, 500, 2, 55]]],
                  [[[5000, 71, 500, 1, 55]]],
                  [[[5500, 73, 1000, 2, 55, "*"]], [[6500, 87, 250, 4, 77]]]]

        self.assertEqual(result, collect_beat_lists(entrance_lists))

    def test_create_lists_of_tensions(self):
        entrance_break = break_at_each_entrance(self.BOOK_EXAMPLE)

        beat_lists = collect_beat_lists(entrance_break)

        group_of_midi_notes = collect_pitch_lists(beat_lists)

        result = [0.3, 0.3, 0.5, 0.3, 0.5, 0.3, 0.3, 0.3]
        self.assertEqual(result, create_lists_of_tensions(group_of_midi_notes))

    def test_map_add(self):
        list1 = [numpy.float32(0.0), numpy.float32(0.3)]
        list2 = [numpy.float32(0.15)]
        list3 = [numpy.float32(0.01), numpy.float32(0.04)]
        list4 = [numpy.float32(0), numpy.float32(0.8)]
        self.assertEqual([numpy.float32(0.16000001)], map_add(list1, list2, list3, list4))

        list1 = [numpy.float32(0.3), numpy.float32(0.3), numpy.float32(0.5), numpy.float32(0.3),
                 numpy.float32(0.5), numpy.float32(0.3), numpy.float32(0.3), numpy.float32(0.3)]

        list2 = [numpy.float32(0.2), numpy.float32(0.05), numpy.float32(0.1), numpy.float32(0.05),
                 numpy.float32(0.2), numpy.float32(0.05), numpy.float32(0.1), numpy.float32(0.05)]

        list3 = [numpy.float32(0.06), numpy.float32(0.06), numpy.float32(0.08), numpy.float32(0.06),
                 numpy.float32(0.08), numpy.float32(0.06), numpy.float32(0.06), numpy.float32(0.06)]

        list4 = [numpy.float32(0), numpy.float32(0), numpy.float32(0.1), numpy.float32(0.1),
                 numpy.float32(0.55), numpy.float32(0.1), numpy.float32(0.8), numpy.float32(0.1)]

        res = [numpy.float32(0.56), numpy.float32(0.41000003), numpy.float32(0.78000003), numpy.float32(0.51000005),
               numpy.float32(1.3299999), numpy.float32(0.51000005), numpy.float32(1.26), numpy.float32(0.51000005)]
        self.assertEqual(res, map_add(list1, list2, list3, list4))

    def test_lookup_and_figure_metric_tension(self):
        self.assertEqual(0.05, lookup_and_figure_metric_tension(9, 7))
        self.assertEqual(0.125, lookup_and_figure_metric_tension(6, 5))
        self.assertEqual(0.15, lookup_and_figure_metric_tension(3, 3))
        self.assertEqual(0.1, lookup_and_figure_metric_tension(2, 2))
        self.assertEqual(0.05, lookup_and_figure_metric_tension(4, 1))

    def test_map_metric_tensions(self):
        start_beat = 4
        total_beats = 8
        meter = 4
        result = [.2, .05, .1, .05, .2, .05, .1, .05]
        self.assertEqual(result, map_metric_tensions(start_beat, total_beats, meter))
        self.assertEqual([0.05, 0.1, 0.15, 0.05, 0.125], map_metric_tensions(1, 5, 6))
        self.assertEqual([0.15], map_metric_tensions(3, 1, 3))

    def test_get_durations(self):
        self.assertEqual([0], get_durations([]))

        ontime = [59000]
        result = [0]
        self.assertEqual(result, get_durations(ontime))

        self.assertEqual([58000, 58000], get_durations([1000, 59000]))

        ontime = [0, 1000, 1500, 2100, 2300, 3000]
        result = [1000, 500, 600, 200, 700, 700]
        self.assertEqual(result, get_durations(ontime))

    def test_duration_map(self):
        input = [[[[59000, 79, 1000, 1, 64, '*'], [59000, 60, 1000, 2, 64], [59000, 64, 1000, 2, 64],
                   [59000, 67, 1000, 2, 64], [59000, 72, 1000, 2, 64]],
                  [[60000, 79, 500, 1, 64], [60000, 55, 500, 2, 64, '*']],
                  [[60500, 80, 500, 1, 64], [60500, 55, 500, 2, 64]]]]
        result = [0]
        self.assertEqual(result, duration_map(input))

        beats = [[[[0, 73, 1000, 1, 55], [0, 69, 1000, 2, 55]]],
                 [[[1000, 73, 500, 1, 55]]],
                 [[[1300, 75, 45, 5, 7]]]]
        result = [1000, 300, 300]
        self.assertEqual(result, duration_map(beats))

        input = collect_beat_lists(break_at_each_entrance(self.BOOK_EXAMPLE))
        result = [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
        self.assertEqual(result, duration_map(input))

    def test_derive_pitches(self):
        pitches = [54, 62, 64, 69]
        result = [[54, 54], [54, 62], [54, 64], [54, 69]]
        self.assertEqual(result, derive_pitches(pitches))

    def test_derive_all_pitches(self):
        pitches = [54, 62, 1]
        result = [54, 54, 54, 62, 54, 1, 62, 62, 62, 1]
        self.assertEqual(result, derive_all_pitches(pitches))

    def test_find_it_in_chord(self):
        interval = 7
        chord = [54, 54, 54, 62, 54, 64, 54, 69, 62, 62, 62, 64, 62, 69, 64, 64, 64, 69]
        result = [69, 62]
        self.assertEqual(result, find_it_in_chord(interval, chord))
        chord2 = [54, 54, 54, 62, 54, 64, 54, 69, 62, 62, 62, 64, 62, 69, 64, 64, 64, 69]
        self.assertEqual([64, 54], find_it_in_chord(10, chord2))

    def test_find_interval_in_chord(self):
        interval = 7
        chord = [54, 54, 54, 62, 54, 64, 54, 69, 62, 62, 62, 64, 62, 69, 64, 64, 64, 69]
        result = [69, 62]
        self.assertEqual(result, find_interval_in_chord(interval, chord))
        self.assertEqual([69], find_interval_in_chord(interval, [69]))
        self.assertEqual([69, 62], find_interval_in_chord(7, [54, 62, 64, 69]))

    def test_derive_intervals(self):
        pitches = [45, 64, 69, 73]
        result = [0, 7, 0, 4]
        self.assertEqual(result, derive_intervals(pitches))
        self.assertEqual([0, 11, 10, 9, 8], derive_intervals([32, 43, 54, 65, 76]))

    def test_derive_all_intervals(self):
        pitches = [45, 64, 69, 73]
        result = [0, 7, 0, 4, 0, 5, 9, 0, 4, 0]
        self.assertEqual(result, derive_all_intervals(pitches))
        self.assertEqual([0, 3, 8, 0, 5, 0], derive_all_intervals([83, 74, 19]))
        self.assertEqual([0], derive_all_intervals([45]))

    def test_find_root_strenghts_and_roots(self):
        self.assertEqual([[0, 0, 11], [7, 0, 1], [4, 0, 3]], find_root_strenghts_and_roots([0, 7, 4]))

    def test_find_strongest_root_interval(self):
        self.assertEqual(1, find_strongest_root_interval([1]))
        self.assertEqual(5, find_strongest_root_interval([0, 3, 4, 6, 2, 5]))
        self.assertEqual(10, find_strongest_root_interval([0, 10]))
        intervals = [0, 7, 4, 0]
        result = 7
        self.assertEqual(result, find_strongest_root_interval(intervals))
        self.assertEqual(9, find_strongest_root_interval([1, 2, 9, 10]))

    def test_sort_CADDR(self):
        lists = [[0, 0, 11], [10, 5, 34], [12, 13, 5]]
        result = [[12, 13, 5], [0, 0, 11], [10, 5, 34]]
        self.assertEqual(result, sort_CADDR(lists))

    def test_find_upper_lower(self):
        self.assertEqual(64, find_upper_lower(5, [45, 64]))
        self.assertEqual(45, find_upper_lower(7, [45, 64]))
        self.assertEqual(45, find_upper_lower(10, [45, 64]))

    def test_derive(self):
        pitches = [55, 64, 84]
        result = [0, 5, 8, 9]
        self.assertEqual(result, derive(pitches))
        self.assertEqual([0], derive([72]))
        self.assertEqual([0, 2, 9, 11], derive([41, 74, 76]))

    def test_scrunch(self):
        self.assertEqual([1, 2, 3, 7, 4, 5, 6], scrunch([[1, 2, 3, 7], [4, 5, 6]]))
        self.assertEqual([1, 5], scrunch([[1, 1, 1], [5, 1]]))

    def test_get_chord_roots(self):
        result = [45, 57, 64, 57, 62, 55, 57, 50]
        self.assertEqual(result, get_chord_roots(self.BOOK_EXAMPLE))

    def test_find_motion_weightings(self):
        roots = [45, 57, 64, 57, 62, 55, 57, 50]
        result = [0, 0.1, 0.1, 0.55, 0.1, 0.8, 0.1]
        self.assertEqual(result, find_motion_weightings(roots))

        roots = [25, 13, 83, 74, 19]
        result = [0, 0.7, 0.25, 0.1]
        self.assertEqual(result, find_motion_weightings(roots))

    def test_get_root_motion_weightings(self):
        result = [0, 0, 0.1, 0.1, 0.55, 0.1, 0.8, 0.1]
        self.assertEqual(result, get_root_motion_weightings(self.BOOK_EXAMPLE))

    def test_compute_duration_tensions(self):
        expected_result = [0.12, 0.14999999, 0.06, 0.08, 0.14, 0.14999999, 0.06, 0.08, 0.12, 0.14999999, 0.12,
                           0.14999999, 0.11, 0.11, 0.12, 0.14, 0.12, 0.14999999, 0.06, 0.099999994, 0.14,
                           0.14999999, 0.06, 0.08, 0.12, 0.14999999, 0.12, 0.14999999, 0.11, 0.14999999, 0.04,
                           0.099999994, 0.02, 0.049999997, 0.07, 0.07, 0.02, 0.12, 0.099999994, 0.04, 0.26, 0.17,
                           0.11, 0.049999997, 0.19999999, 0.04, 0.08, 0.049999997, 0.16, 0.04, 0.16, 0.099999994,
                           0.049999997, 0.19, 0.06, 0.06, 0.12, 0.099999994, 0.06, 0.26999998, 0.19999999, 0.14,
                           0.08, 0.22, 0.04, 0.19, 0.099999994, 0.049999997, 0.16, 0.04, 0.13, 0.12, 0.14999999,
                           0.06, 0.08, 0.14, 0.14999999, 0.06, 0.08, 0.12, 0.14999999, 0.12, 0.14999999, 0.11,
                           0.14999999, 0.12, 0.14, 0.12, 0.14999999, 0.06, 0.08, 0.14, 0.14999999, 0.06, 0.08, 0.12,
                           0.14999999, 0.12, 0.14999999, 0.11, 0.14999999, 0.04, 0.099999994, 0.02]
        for i in range(0, len(expected_result)):
            expected_result[i] = numpy.float32(expected_result[i])

        result = compute_duration_tensions(CHOPIN_33_3)
        self.assertEqual(expected_result, result)

        input = [[59000, 60, 1000, 2, 64], [59000, 64, 1000, 2, 64], [59000, 67, 1000, 2, 64],
                 [59000, 72, 1000, 2, 64], [59000, 79, 1500, 1, 64], [60000, 55, 1000, 2, 64], [60500, 80, 500, 1, 64]]
        self.assertEqual([0.0], compute_duration_tensions(input))

        input = [[1000, 57, 1000, 1, 55]]
        self.assertEqual([0.0], compute_duration_tensions(input))

        result = [numpy.float32(.06), numpy.float32(.06), numpy.float32(.08), numpy.float32(.06), numpy.float32(.08),
                  numpy.float32(.06), numpy.float32(.06), numpy.float32(.06)]
        self.assertEqual(result, compute_duration_tensions(self.BOOK_EXAMPLE))

    def test_run_the_speac_weightings(self):
        phrase = [[59000, 60, 1000, 2, 64], [59000, 64, 1000, 2, 64], [59000, 67, 1000, 2, 64],
                  [59000, 72, 1000, 2, 64], [59000, 79, 1500, 1, 64], [60000, 55, 1000, 2, 64], [60500, 80, 500, 1, 64]]
        start_beat_number = 3
        round_number = 2
        meter = 3
        result = [numpy.float32(0.15)]
        self.assertEqual(result, run_the_speac_weightings(phrase, start_beat_number, round_number, meter))

        result = [numpy.float32(0.56), numpy.float32(0.41000003), numpy.float32(0.78000003), numpy.float32(0.51000005),
                  numpy.float32(1.3299999), numpy.float32(0.51000005), numpy.float32(1.26), numpy.float32(0.51000005)]
        self.assertEqual(result, run_the_speac_weightings(self.BOOK_EXAMPLE, 4, 8, 4))


if __name__ == '__main__':
    unittest.main()
