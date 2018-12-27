#!/usr/bin/env python3

__version__='0.0.1'
__author__='zrth1k@gmail.com'

import sys
import requests
import argparse
import logging
import configparser

def logger():
    log = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def parse_commandline():
    actions=['version', 'auth', 'list', 'post', 'clear']
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('action', default='list', choices=actions, help='....')
    return parser


def parse_config():
    section = 'default'
    ini_file = 'trmeet.ini'

    base_url = 'https://www.trustroots.org'
    
    post_sufix = '/api/offers'
    auth_sufix = '/api/auth/signin'
    list_sufix = '/api/offers-by/{}?types=meet'

    config = configparser.ConfigParser()
    config.read(ini_file)
    c = config[section]

    global login_url
    global list_url
    global post_url

    global login_data
    global post_data

    login_data = {'username':c['username'],
                  'password':c['password']}

    post_data = {"type":"meet",
                 "description":c["description"],
                 "location":None,
                 "validUntil":None}

    login_url = base_url + auth_sufix
    list_url = base_url + list_sufix
    post_url = base_url + post_sufix

    return c


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


def init():
    s = requests.Session()
    login = s.post(login_url, data=login_data)
    if login.status_code == 200:
        log.info("Login successfull")
    else:
        log.error("login failed with http.status_code: " + login.status_code)
        sys.exit()

    tr_id = login.json()['_id']
    return tr_id, s


def list_meets(s, tr_id):
    list_url = 'https://www.trustroots.org/api/offers-by/{}?types=meet'.format(tr_id)
    meets = s.get(list_url)
    print(meets.text)
    print(meets.status_code)


def test_auth(tr_id):
    log.error("Login successfully. _id:{}".format(tr_id))
    sys.exit()


def clear_meets(s, tr_id):
    pass

def post_new(s):
    

def main():
    global log
    parser = parse_commandline()
    args = parser.parse_args()
    log = logger()
    print(args)
    log.error(args)
    config = parse_config()


    if args.action == 'version':
        version()
        return

    tr_id, session = init()

    if args.action == 'auth':
        test_auth(tr_id)

    elif args.action == 'list':
        list_meets(session, tr_id)

    elif args.action == 'clear':
        clear_meets(session)

    elif args.action == 'post':
        post_new(session)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    
