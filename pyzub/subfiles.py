# Imports =====================================================================
import os
import re

from pyzub.utils import guess_codec
from pyzub.subexceptions import InvalidTimeString
from datetime import timedelta
from tqdm import tqdm
# =============================================================================


class SRTFile():
    # =========================================================================
    class SRTSubtitle():

        def __init__(self, index, start_time, end_time, text):

            self.index = index

            self._start_time = start_time
            self._end_time = end_time

            self.text = text

        def __str__(self):

            text = ('Index: {}\n'.format(self.index) +
                    'Start Time: {}\n'.format(self.start_time) +
                    'End Time: {}\n'.format(self.end_time) +
                    'Text: {}'.format(self.text))

            return text

        def __len__(self):

            lenght = len(self.text)

            return lenght

        @property
        def start_time(self):

            remainder = self._start_time.total_seconds()

            h = int(remainder // 3600)
            remainder -= h * 3600
            m = int(remainder // 60)
            remainder -= m * 60
            s = int(remainder)
            remainder -= s
            ms = round(remainder * 10**3)

            h = '0' + str(h) if len(str(h)) < 2 else str(h)
            m = '0' + str(m) if len(str(m)) < 2 else str(m)
            s = '0' + str(s) if len(str(s)) < 2 else str(s)
            ms = str(ms)

            while len(ms) < 3:
                ms = '0' + ms

            return ','.join((':'.join((h, m, s)), ms))

        @start_time.setter
        def start_time(self, tm):

            if isinstance(tm, timedelta):
                self._start_time = tm

            elif isinstance(tm, str):

                regex_str = r'(\d+):(\d{2}):(\d{2}),(\d{3})'
                regex = re.compile(regex_str)
                match = regex.match(tm)

                if match is not None:

                    match_groups = match.groups()
                    tm = timedelta(hours=int(match_groups[0]),
                                   minutes=int(match_groups[1]),
                                   seconds=int(match_groups[2]),
                                   milliseconds=int(match_groups[3]))
                    self._start_time = tm

                else:
                    raise InvalidTimeString
            else:
                raise TypeError

        @property
        def end_time(self):

            remainder = self._end_time.total_seconds()

            h = int(remainder // 3600)
            remainder -= h * 3600
            m = int(remainder // 60)
            remainder -= m * 60
            s = int(remainder)
            remainder -= s
            ms = round(remainder * 10**3)

            h = '0' + str(h) if len(str(h)) < 2 else str(h)
            m = '0' + str(m) if len(str(m)) < 2 else str(m)
            s = '0' + str(s) if len(str(s)) < 2 else str(s)
            ms = str(ms)

            while len(ms) < 3:
                ms = '0' + ms

            return ','.join((':'.join((h, m, s)), ms))

        @end_time.setter
        def end_time(self, tm):

            if isinstance(tm, timedelta):
                self._end_time = tm

            elif isinstance(tm, str):

                regex_str = r'(\d+):(\d{2}):(\d{2}),(\d{3})'
                regex = re.compile(regex_str)
                match = regex.match(tm)

                if match is not None:

                    match_groups = match.groups()
                    tm = timedelta(hours=int(match_groups[0]),
                                   minutes=int(match_groups[1]),
                                   seconds=int(match_groups[2]),
                                   milliseconds=int(match_groups[3]))
                    self._end_time = tm

                else:
                    raise InvalidTimeString

            else:
                raise TypeError

    # =========================================================================
    def __init__(self, filepath, codec=None):

        self.filepath = filepath
        self.codec = codec if codec is not None else guess_codec(filepath)

        self._subtitles = self._load()

    def __str__(self):

        text = ('Relative Path: {}\n'.format(self.filepath) +
                'Codec: {}\n'.format(self.codec) +
                'No. of Subtitles: {}'.format(len(self._subtitles)))

        return text

    def __len__(self):

        lenght = len(self._subtitles)

        return lenght

    def __iter__(self):

        for subtitle in self._subtitles:
            yield subtitle

    def get_subtitle(self, index):

        if index < 1 or index > len(self._subtitles):
                raise IndexError('Subtitle index out of range.')

        return self._subtitles[index - 1]

    def slide(self, hours=0.0, minutes=0.0, seconds=0.0, milliseconds=0.0,
              microseconds=0.0, progress_bar=False):

        dt = timedelta(hours=hours,
                       minutes=minutes,
                       seconds=seconds,
                       milliseconds=milliseconds,
                       microseconds=microseconds)

        for subtitle in tqdm(self, disable=not(progress_bar)):

            aux = subtitle._start_time.total_seconds()
            subtitle.start_time = timedelta(seconds=aux) + dt
            aux = subtitle._end_time.total_seconds()
            subtitle.end_time = timedelta(seconds=aux) + dt

    def _load(self):

        try:
            with open(self.filepath, 'r', encoding=self.codec) as f:
                lines = f.read()

        except UnicodeDecodeError:
                print("Error: Text encoding not recognized.")

        regex_str1 = (r'(\d+)' + '\s' + '(\d+):(\d{2}):(\d{2}),(\d{3})' +
                      '\W+' + '(\d+):(\d{2}):(\d{2}),(\d{3})' + '\s' +
                      '(.*?)' + '\s{2}')
        regex_str2 = (r'(\d+)' + '\s' + '(\d+):(\d{2}):(\d{2}),(\d{3})' +
                      '\W+' + '(\d+):(\d{2}):(\d{2}),(\d{3})' + '\s' +
                      '(.*)' + '\s?')

        regex = re.compile(regex_str1 + '|' + regex_str2, re.DOTALL)

        regex_list = regex.findall(lines)

        regex_list_new = []

        for match_group in regex_list:

            aux = [i for i in match_group if i != '']
            regex_list_new.append(aux)

        subtitles = []

        for match_group in regex_list_new:

            index = match_group[0]
            start_time = tuple(match_group[1:5])
            end_time = tuple(match_group[5:9])
            text = match_group[9]

            start_time = timedelta(hours=int(start_time[0]),
                                   minutes=int(start_time[1]),
                                   seconds=int(start_time[2]),
                                   milliseconds=int(start_time[3]))

            end_time = timedelta(hours=int(end_time[0]),
                                 minutes=int(end_time[1]),
                                 seconds=int(end_time[2]),
                                 milliseconds=int(end_time[3]))

            srt_sub = SRTFile.SRTSubtitle(index, start_time, end_time, text)
            subtitles.append(srt_sub)

        return subtitles

    def dump(self, filepath):

        with open(filepath, 'w', encoding='utf-8') as f:

            for index, subtitle in enumerate(self):

                f.write(subtitle.index)
                f.write(os.linesep)

                f.write(subtitle.start_time + ' --> ' + subtitle.end_time)
                f.write(os.linesep)

                f.write(subtitle.text)
                f.write(os.linesep)

                if index != len(self) - 1:
                    f.write(os.linesep)
