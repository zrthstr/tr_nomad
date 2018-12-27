#!/usr/bin/env python3

__version__='0.0.1'
__author__='zrth1k@gmail.com'

import argparse
import logging

def logger():
    log = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('action', choices=['version', 'auth', 'list', 'post', 'clear'])
    return parser


def version():
    banner="""
    oxoxoo    ooxoo
  ooxoxo oo  oxoxooo
 oooo xxoxoo ooo ooox
 oxo o oxoxo  xoxxoxo
  oxo xooxoooo o ooo
    ooo\oo\  /o/o
        \  \/ /
         |   /
         | D|
         |  |
  ______/____\____ {} {}""".format(__version__, __author__)
    print(banner)


def main():
    parser = parse_commandline()
    args = parser.parse_args()
    log = logger()
    print(args) 
    log.error(args)

    if args.action == 'version':
        version()


if __name__ == "__main__":
    main()
    
