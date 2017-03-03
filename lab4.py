#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Creation date: 27.11.2008
# Author: Pavel Ulpi
# Email: passshok@gmail.com
#
# Description:
# Program that controls fan speed depending on processor
# temperature and makes it more quiet then it's default
# behavior on Asus Eee PC 1000 laptops with kernel from
# array.org repository.
#
# License: GPLv3
#

import math, time, sys, signal


def cur_temp():
        """
        Get current temperature
        """
        temp = 0

        f = open("/proc/eee/temperature", "r")
        temp = f.readline()
        f.close()

        return int(temp)


def fan_ctrl(onoff):
        """
        Enable (1) or disable (0) manual control of fan
        """
        f = open("/proc/eee/fan_manual", "w")
        f.write(str(onoff))
        f.close()


def temp2speed(temp):
        """
        Calculates fan speed in percentes according to temperature
        """
        if temp < 55:
                return 0
        elif temp > 65:
                return 100
        else:
                return (temp * 10) - 550

def set_fan_speed(speed):
        """
        Sets new fan speed in percents
        """
        f = open("/proc/eee/fan_speed", "w")
        f.write(str(speed))
        f.close()



fan_ctrl(1)

def sig_hndlr(sig_num, frame):
        fan_ctrl(0)
        sys.exit(0)

signal.signal(signal.SIGHUP, sig_hndlr)

if len(sys.argv) > 1 and sys.argv[1] == "-d":
        # daemon mode
        try:
                while 1:
                        new_temp = temp2speed(cur_temp())
                        set_fan_speed(new_temp)
                        time.sleep(10)
        except (KeyboardInterrupt, SystemExit):
                fan_ctrl(0)
        
else:
        new_temp = temp2speed(cur_temp())
        set_fan_speed(new_temp)
        sys.exit(0)

