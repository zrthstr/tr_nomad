# TR-Nomad
* posts your current location to TR
* current location is defined as in `python geocoder.ip('me')`
* default TTL is 36h

## About

```
% ./trn.py version

    ox0x0o0  o0xoo
  o0xox0 o0o o0ox0o0
 oo00 xx0x0o 0oo 0oox
 o0o o 0xox0  xoxx0xo
  0xo xoox0o0o o 0o0       TRN - TR-Nomad - 0.0.1 
    0oo\0o\  /o/0o         Copyright (C) 2018 - zrth1k@gmail.com
        \  \/ /
         |   /             This program may be freely redistributed under
         | D|              the terms of the GNU General Public License.
  ______/____\______

```

## Config
```
cp trmeet.ini_example trmeet.ini
vim trmeet.ini
```

## Usage
```
% ./trn.py --help                                                                                                     :(
usage: trn.py [-h] [--verbose] {version,auth,list,post,clear,update}

positional arguments:
  version      # print version
  auth         # test auth
  list         # list all meets
  post         # post new meet with current location valid for 36h
  clear        # delete all old meets
  update       # delete old meets and post new

optional arguments:
  -h, --help            show this help message and exit
  --verbose, -v
```

