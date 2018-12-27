#!/usr/bin/env python3

__version__='0.0.1'
__author__='zrth1k@gmail.com'

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
    delete_sufix = '/api/offers/{}'

    config = configparser.ConfigParser()
    config.read(ini_file)
    c = config[section]

    global login_url
    global list_url
    global post_url
    global delete_url

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
    delete_url = base_url + delete_sufix

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
    print("JJJJJJJ",meets.json())
    return meet_ids


def test_auth(tr_id):
    log.error("Login successfully. _id:{}".format(tr_id))
    sys.exit()


def clear_meets(s, meet_ids):
    for mid in meet_ids:
        log.warning("removing: {}".format(mid))
        url =  meets_url.format(mid)
        s.delete(url)


def post_new(s):
    print("POST NEW")
    headers = {'Content-Type':'application/json;charset=UTF-8',
                'Accept':'application/json, text/plain, */*'}
    latlng = get_latlng()
    #end_time = datetime.datetime.utcnow().isoformat() + 'Z'
    ## 2 days hard coded for now
    end_time = (datetime.datetime.now() + datetime.timedelta(days=2)).isoformat() + "Z"
    log.warning("Posting new meet: {}@{}".format(latlng, end_time))
    post_data['location'] = latlng
    post_data['validUntil'] = end_time
    log.warning("post_data: " +  str(post_data))
    print("post_url:", post_url)
    import json
    meet = s.post(post_url ,data=json.dumps(post_data), headers=headers)
    log.warning(meet.status_code)
    log.warning(meet.text)


def get_latlng():
    g = geocoder.ip('me') 
    latlng = g.latlng
    print("Found location:", latlng)
    return latlng


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
    
