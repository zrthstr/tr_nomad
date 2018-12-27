#!/usr/bin/env python3

__version__ = '0.0.1'
__author__ = 'zrth1k@gmail.com'

import json
import sys
import geocoder
import requests
import argparse
import logging
import datetime
import configparser


def logger():
    log = logging.getLogger()
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    log.addHandler(handler)
    return log


def parse_commandline():
    actions=['version', 'auth', 'list', 'post', 'clear', 'update']
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', '-v', action='count')
    parser.add_argument('action', default='list', choices=actions, help='....')
    return parser


def parse_config():
    global login_url
    global list_url
    global post_url
    global delete_url
    global clear_url

    global headers
    global login_data
    global post_data
    global hoursonline

    section = 'default'
    ini_file = 'trmeet.ini'

    base_url = 'https://www.trustroots.org'
    
    post_sufix = '/api/offers'
    auth_sufix = '/api/auth/signin'
    list_sufix = '/api/offers-by/{}?types=meet'
    clear_sufix = '/api/offers/{}'

    config = configparser.ConfigParser()
    config.read(ini_file)
    c = config[section]

    headers = {'Content-Type':'application/json;charset=UTF-8',
                'Accept':'application/json, text/plain, */*'}

    login_data = {'username':c['username'],
                  'password':c['password']}

    post_data = {"type":"meet",
                 "description":c["description"],
                 "location":None,
                 "validUntil":None}

    hoursonline = int(c['hoursonline'])

    login_url = base_url + auth_sufix
    list_url = base_url + list_sufix
    post_url = base_url + post_sufix
    clear_url = base_url + clear_sufix


def version():
    banner = ('\n'
              '    ox0x0o0  o0xoo\n'
              '  o0xox0 o0o o0ox0o0\n'
              ' oo00 xx0x0o 0oo 0oox\n'
              ' o0o o 0xox0  xoxx0xo\n'
              '  0xo xoox0o0o o 0o0       TRN - TR-Nomad - {} \n'
              '    0oo\\0o\  /o/0o         Copyright (C) 2018 - {}\n'
              '        \  \/ /\n'
              '         |   /             This program may be freely redistributed under\n'
              '         | D|              the terms of the GNU General Public License.\n'
              '  ______/____\____').format(__version__, __author__)
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
    meets_all = meets.json()
    print(meets.status_code)
    if meets.status_code == 200:
        meet_ids = [m['_id'] for m in meets_all ]
        print( meet_ids)
        return  meet_ids
    else:
        return []
    #print("mmmmm",meets_all)
    #print("JJJJJJJ",meets.json())
    #print("Found:", meet_ids)
    #return meet_ids


def test_auth(tr_id):
    log.error("Login successfully. _id:{}".format(tr_id))
    sys.exit()


def clear_meets(s, tr_id):
    meet_ids = list_meets(s, tr_id)
    for mid in meet_ids:
        log.warning("removing: {}".format(mid))
        s.delete(clear_url.format(mid))


def post_new(s):
    #print("POST NEW")
    latlng = get_latlng()
    end_time = (datetime.datetime.now() + datetime.timedelta(hours=hoursonline)).isoformat() + "Z"
    log.warning("Posting new meet: {}@{}".format(latlng, end_time))
    post_data['location'] = latlng
    post_data['validUntil'] = end_time
    #log.warning("post_data: " +  str(post_data))
    meet = s.post(post_url ,data=json.dumps(post_data), headers=headers)
    #log.warning(meet.status_code)
    #log.warning(meet.text)


def get_latlng():
    g = geocoder.ip('me') 
    latlng = g.latlng
    return latlng


def main():
    global log
    parser = parse_commandline()
    args = parser.parse_args()
    log = logger()
    #log.error(args)
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
        clear_meets(session, tr_id)

    elif args.action == 'post':
        post_new(session)
    
    elif args.action == 'update':
        clear_meets(session, tr_id)
        post_new(session)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
    
