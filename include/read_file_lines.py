#!/usr/bin/env python3


def read_file_lines(filename: str):
    f = open(filename)
    lines = f.readlines()
    f.close()
    return lines

