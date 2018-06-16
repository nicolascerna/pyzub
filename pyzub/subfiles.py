# Imports =====================================================================
import os
import re

from pyzub.utils import guess_codec
from datetime import timedelta
# =============================================================================


class SRTFile():
    # =========================================================================
    class _SRTSubtitle():

        def __init__(self, index, start_time, end_time, text):

            self.index = index

            self._start_time = start_time
            self._end_time = end_time

            self.text = text

        def __str__(self):

            text = ('Index: {}\n'.format(self.index) +
                    'Start Time: {}:{}:{},{}\n'.format(*self._start_time) +
                    'End Time: {}:{}:{},{}\n'.format(*self._end_time) +
                    'Text: {}'.format(self.text))

            return text

        def __len__(self):

            lenght = len(self.text)

            return lenght

        @property
        def start_time(self):

            h, m, s, ms = self._start_time

            return timedelta(hours=int(h), minutes=int(m), seconds=int(s),
                             milliseconds=int(ms)).total_seconds()

        @start_time.setter
        def start_time(self, dt):

            remainder = dt.total_seconds()
            h = int(remainder // 3600)
            remainder -= h * 3600
            m = int(remainder // 60)
            remainder -= m * 60
            s = int(remainder)
            remainder -= s
            ms = int(remainder * 10**3)

            h = '0' + str(h) if len(str(h)) < 2 else str(h)
            m = '0' + str(m) if len(str(m)) < 2 else str(m)
            s = '0' + str(s) if len(str(s)) < 2 else str(s)
            ms = str(ms)

            while len(ms) < 3:
                ms = '0' + ms

            self._start_time = (h, m, s, ms)

        @property
        def end_time(self):

            h, m, s, us = self._end_time

            return timedelta(hours=int(h), minutes=int(m), seconds=int(s),
                             microseconds=int(us)).total_seconds()

        @end_time.setter
        def end_time(self, dt):

            remainder = dt.total_seconds()
            h = int(remainder // 3600)
            remainder -= h * 3600
            m = int(remainder // 60)
            remainder -= m * 60
            s = int(remainder)
            remainder -= s
            ms = int(remainder * 10**3)

            h = '0' + str(h) if len(str(h)) < 2 else str(h)
            m = '0' + str(m) if len(str(m)) < 2 else str(m)
            s = '0' + str(s) if len(str(s)) < 2 else str(s)
            ms = str(ms)

            while len(ms) < 3:
                ms = '0' + ms

            self._end_time = (h, m, s, ms)

    # =========================================================================
    def __init__(self, filepath, codec=None):

        self.filepath = filepath
        self.codec = codec if codec is not None else guess_codec(filepath)

        self._subtitles = self._load()

    def __str__(self):

        text = ('Absolute Path: {}\n'.format(self.filepath) +
                'Codec: {}\n'.format(self.codec) +
                '#Subtitles: {}'.format(len(self._subtitles)))

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

            srt_sub = SRTFile._SRTSubtitle(index, start_time, end_time, text)
            subtitles.append(srt_sub)

        return subtitles

    def dump(self, filepath):

        with open(filepath, 'w', encoding='utf-8') as f:

            for index, subtitle in enumerate(self._subtitles):

                for key, item in subtitle.__dict__.items():

                    if key == 'index':

                        f.write(item)
                        f.write(os.linesep)

                    if key == '_start_time':
                        f.write(':'.join(item[:-1]) + ',' + item[-1] + ' --> ')

                    elif key == '_end_time':

                        f.write(':'.join(item[:-1]) + ',' + item[-1])
                        f.write(os.linesep)

                    elif key == 'text':
                        f.write(item)

                        if index != len(self._subtitles) - 1:
                            f.write(os.linesep)

                if index != len(self._subtitles) - 1:
                    f.write(os.linesep)
