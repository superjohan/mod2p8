#!/usr/bin/env python3


import click


@click.command()
@click.argument('input_mod')
@click.argument('output_p8')
def convert(input_mod, output_p8):

    print("hello there")


if __name__ == "__main__":

    convert()
