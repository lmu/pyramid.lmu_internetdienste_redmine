# -*- coding: utf-8 -*-

import argparse

import ipdb


def main(**settings):
    parser = argparse.ArgumentParser()

    parser.add_argument('command')

    ipdb.set_trace()
    args = parser.parse_args()

    return (parser, args)
