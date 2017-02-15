#!/usr/bin/env python3
import os
import statistics
import sys
import time
from gettext import gettext as _

# Список тестируемых компрессоров и их опций.
# compression_name, compression_options
COMPRESSION = (('gzip', ''),
               ('bzip2', ''),
               ('lzma', ''),
               ('xz', ''),
               ('lzop', ''),
               ('lz4', ''))
# Количество тестов производительности.
TEST_COUNT = 10


class PrintTable:
    cols = (_('Имя'), _('Компр.'), _('Компр. (байт)'), _('Компр. (сек.)'), _('Декомпр. (сек.)'))
    i_len = 0

    @classmethod
    def head(cls, i_len):
        cls.i_len = i_len
        print(_('Исходный размер: {} байт.').format(i_len))
        print('{:<8} {:>16} {:>16} {:>16} {:>16}'.format(*cls.cols))

    @classmethod
    def row(cls, result):
        koef = result[1] / max(cls.i_len, 1)
        print('{:<8} {koef:>16%} {:>16} {:>16.5} {:>16.5}'.format(*result, koef=koef))

    @classmethod
    def status(cls, *args):
        print(' ' * 80, _('Тестирую {}, {} из {}.').format(*args), sep='\r', end='\r', file=sys.stderr)

    # noinspection PyUnusedLocal
    @classmethod
    def foot(cls, results):
        print(_('Меньше лучше.'))


def test_command(command):
    start_time = time.time()
    ret = os.system(command)
    stop_time = time.time()
    if ret:
        raise Exception('Return error #{} ({})'.format(ret, command))
    return stop_time - start_time


def main():
    # Входящий не сжатый файл, на котором проводится тестирование.
    i_file_name = sys.argv[1]

    c_file_name = 'compress_file'
    d_file_name = 'decompress_file'

    # Список с сохраненными результатами.
    # [(c_name, c_len, c_time, d_time), ]
    results = []

    # Получаем размер исходного файла.
    i_len = os.path.getsize(i_file_name)
    results.append(i_len)

    PrintTable.head(i_len)

    # Перебор всех компрессоров из списка.
    for c_name, c_options in COMPRESSION:
        # Формируем команды компрессии и декомпрессии.
        c_command = ('{} {} -c "{}" > "{}"'.format(c_name, c_options, i_file_name, c_file_name))
        d_command = ('{} -d -c "{}" > "{}"'.format(c_name, c_file_name, d_file_name))

        c_times = []
        d_times = []

        # Получаем время.
        for i in range(TEST_COUNT):
            i += 1
            PrintTable.status(c_name, i, TEST_COUNT)

            test_result = test_command(c_command)
            c_times.append(test_result)

            test_result = test_command(d_command)
            d_times.append(test_result)

        # Получаем размер сжатого файла.
        c_len = os.path.getsize(c_file_name)
        # Вычисляем среднее время.
        c_time = statistics.mean(c_times)
        d_time = statistics.mean(d_times)

        result = (c_name, c_len, c_time, d_time)
        results.append(result)

        PrintTable.row(result)

    # Удаляем ненужные файлы
    os.remove(c_file_name)
    os.remove(d_file_name)

    PrintTable.foot(results)


if __name__ == '__main__':
    main()
