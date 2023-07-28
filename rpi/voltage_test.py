#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# cython: language_level=3

#Flag Bits
UNDERVOLTED         = '0'
CAPPED              = '1'
THROTTLED           = '2'
SOFT_TEMPLIMIT      = '3'
HAS_UNDERVOLTED     = '16'
HAS_CAPPED          = '17'
HAS_THROTTLED       = '18'
HAS_SOFT_TEMPLIMIT  = '19'

from vcgencmd import Vcgencmd
from colorama import init
from colorama import Fore, Back, Style
import time

init(autoreset=True)

vcgm = Vcgencmd()

def print_log(flag, info):
    if flag:
        print(Fore.RED + Style.BRIGHT + info, end = '  ')
    else:
        print(Fore.GREEN + Style.DIM + info, end = '  ')

while True:

    print('[{}] '.format(time.strftime('%M:%S')), end = '')

    output = vcgm.get_throttled()

    flag = output['breakdown'][UNDERVOLTED]
    print_log(flag, 'UNDERVOLTED')

    flag = output['breakdown'][CAPPED]
    print_log(flag, 'CAPPED')

    flag = output['breakdown'][THROTTLED]
    print_log(flag, 'THROTTLED')

    flag = output['breakdown'][SOFT_TEMPLIMIT]
    print_log(flag, 'SOFT_TEMPLIMIT')

    flag = output['breakdown'][HAS_UNDERVOLTED]
    print_log(flag, 'HAS_UNDERVOLTED')

    flag = output['breakdown'][HAS_CAPPED]
    print_log(flag, 'HAS_CAPPED')

    flag = output['breakdown'][HAS_THROTTLED]
    print_log(flag, 'HAS_THROTTLED')

    flag = output['breakdown'][HAS_SOFT_TEMPLIMIT]
    print_log(flag, 'HAS_SOFT_TEMPLIMIT')
    
    print()
    time.sleep(1)

#EOF
