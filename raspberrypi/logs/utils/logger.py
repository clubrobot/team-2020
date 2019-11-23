#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from collections import namedtuple
from time import time, asctime, sleep

from logs.utils.log_color import Colors

LogCommand = namedtuple('LogCommand', ['command', 'param'])
LogLevel = namedtuple('LogLevel', ['value', 'name', 'color'])
LogMsg = namedtuple(
    'LogMsg', ['time', 'level', 'name', 'args', 'kwargs'])

LogInit = namedtuple(
    'LogInit', ['name', 'exec_param', 'level_disp'])


class Logger:
    SHOW = 0
    WRITE = 1
    BOTH = 2
    # Le programme complet est en train de partir en couille.
    CRITICAL = LogLevel(50, '[CRITICAL]', Colors.RED2)
    # Une opération a foirée.
    ERROR = LogLevel(40, '[ERROR]', Colors.RED)
    # Pour avertir que quelque chose mérite l’attention.
    WARNING = LogLevel(30, '[WARNING]', Colors.YELLOW)
    # Pour informer de la marche du programme.
    INFO = LogLevel(20, '[INFO]', Colors.GREEN)
    # Pour dumper des information quand vous débuggez.
    DEBUG = LogLevel(10, '[DEBUG]', Colors.BLUE)

    # int the logger proxy and send file init parameters to the server
    def __init__(self, parent, name, exec_param, level_disp):
        self.parent = parent
        self.name = name

        self.exec_param = exec_param
        self.level_disp = level_disp
        self.parent.send(LogCommand(self.parent.INIT, LogInit(
            self.name, self.exec_param, self.level_disp)))

    # call write
    def __call__(self, *args, **kwargs):
        self.write(*args, **kwargs)

    # send write command with desired message to the server
    def write(self, *args, **kwargs):
        t = str("[{0:.3g}]".format(time() - self.parent.initial_time))
        if 'level' in kwargs:
            self.parent.send(LogCommand(self.parent.WRITE_LOG,
                                        LogMsg(t, kwargs.pop('level'), self.name, args, kwargs)))
        else:
            self.parent.send(LogCommand(self.parent.WRITE_LOG,
                                        LogMsg(t, self.INFO, self.name, args, kwargs)))
