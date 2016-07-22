#!/usr/bin/env python3


import click
import struct
import sys


def parse_mod(input_mod):

    with open(input_mod, mode='rb') as file:
        mod_bytes = file.read()

    mk_header = struct.unpack('4s', mod_bytes[1080:1084])[0].decode('ascii')

    if mk_header != 'M.K.':
        sys.exit('not a valid mod file')


@click.command()
@click.argument('input_mod')
@click.argument('output_p8')
def convert(input_mod, output_p8):

    parse_mod(input_mod)

if __name__ == "__main__":

    convert()
