# -*- coding: utf-8 -*-

"""The cli module parse user entered arguments."""

import argparse


parser = argparse.ArgumentParser(description='Page-loader')

parser.add_argument(
    'target_url',
    help='URL to target page'
    )

parser.add_argument(
    '--output',
    help=(
        "Set directory for saved page"
    ),
    dest='saved_page',
)
