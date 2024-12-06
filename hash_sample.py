#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import hashlib

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MD5 fingerprint from file')
    parser.add_argument('input', nargs='?')
    args = parser.parse_args()
    l = str(hashlib.md5(args.input.encode()).hexdigest())
    print('MD5(' + args.input + '): ' + l)
    