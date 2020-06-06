# -*- coding: utf-8 -*-

"""The cli module parse user entered arguments."""

import argparse


parser = argparse.ArgumentParser(description='Page-loader')

parser.add_argument(
    'target_url',
    help='URL to target page'
    )

parser.add_argument(
    '-o',
    '--output',
    help=(
        "Set directory for saved page"
    ),
    metavar='OUTPUT',
    dest='destination',
    default='',
)

parser.add_argument(
    '-l',
    '--log',
    help=(
        "Set level of logging information: 'none', 'warning', 'debug'"
    ),
    metavar='LOG_LEVEL',
    dest='log_level',
    choices=['none', 'warning', 'debug'],
    default='none',
)
