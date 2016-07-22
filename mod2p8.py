#!/usr/bin/env python3


import click
import struct
import sys

from collections import namedtuple


ModChannelRow = namedtuple('ModChannelRow', ['period', 'sample', 'effect', 'effect_value'])
ModPatternRow = namedtuple('ModPatternRow', ['channel_rows'])
ModPattern = namedtuple('ModPattern', ['rows'])
ModSong = namedtuple('ModSong', ['patterns'])


def parse_mod_channel_rows(mod_bytes, pattern_index, row_index):

    channel_rows = []

    for channel_index in range(0, 4):
        index = 1084 + (pattern_index * 1024) + (row_index * 16) + (channel_index * 4)
        channel_row_bytes = struct.unpack('BBBB', mod_bytes[index:index + 4])
        sample = (channel_row_bytes[0] & 0xf0) + ((channel_row_bytes[2] & 0xf0) >> 4)
        period = ((channel_row_bytes[0] & 0xf) << 8) + channel_row_bytes[1]
        effect = channel_row_bytes[2] & 0xf
        # TODO: Add parsing for effect 0 and 14.
        effect_value = channel_row_bytes[3]

        channel_rows.append(ModChannelRow(period, sample, effect, effect_value))

    return ModPatternRow(channel_rows)


def parse_pattern_rows(mod_bytes, pattern_index):

    rows = []

    for row_index in range(0, 64):
        rows.append(parse_mod_channel_rows(mod_bytes, pattern_index, row_index))

    return ModPattern(rows)


def parse_patterns(mod_bytes, max_pattern):

    patterns = []

    for pattern_index in range(0, max_pattern):
        patterns.append(parse_pattern_rows(mod_bytes, pattern_index))

    return ModSong(patterns)


def parse_mod(input_mod):

    with open(input_mod, mode='rb') as file:
        mod_bytes = file.read()

    mk_header = struct.unpack('4s', mod_bytes[1080:1084])[0].decode('ascii')

    if mk_header != 'M.K.':
        sys.exit('not a valid mod file')

    mod_title = struct.unpack('20s', mod_bytes[0:20])[0].decode('ascii')
    position_count = struct.unpack('B', mod_bytes[950:951])[0]
    positions = struct.unpack('B' * position_count, mod_bytes[952:952 + position_count])
    max_pattern = max(positions)

    print('title: {}'.format(mod_title))
    print('position count: {}'.format(position_count))
    print('positions: {}'.format(positions))
    print('max pattern: {}'.format(max_pattern))

    return parse_patterns(mod_bytes, max_pattern)


@click.command()
@click.argument('input_mod')
@click.argument('output_p8')
@click.option('--debug', is_flag=True)
def convert(input_mod, output_p8, debug):

    mod = parse_mod(input_mod)

    if debug:
        print('{}'.format(mod))


if __name__ == "__main__":

    convert()
