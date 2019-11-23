#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from multiprocessing import Process, Pipe, Lock
from collections import namedtuple
from time import time, asctime, sleep

from common.singleton import singleton
from logs.utils.log_color import Colors, colorise
from logs.utils.logger import *


PipeType = namedtuple('PipeType', ['parent_conn', 'child_conn'])


@singleton
class LogManager(Process):
    # command
    INIT = 0
    WRITE_LOG = 1

    # execution parameter
    SHOW = 0
    WRITE = 1
    BOTH = 2

    def __init__(self):
        Process.__init__(self)
        # terminate with the main process
        self.daemon = True

        self.lock = Lock()

        # communication pipe
        self.pipe = PipeType(*Pipe())

        # initial log time
        self.initial_time = time()

        # dict that contain all loggers proxy context
        self.loggersContext = dict()

        # file to store all logs
        self.commonLogFile = None
        self.commonLogFileName = None

    # resetting log init time
    def reset_time(self):
        self.initial_time = time()

    # process
    def run(self):
        # infinite loop
        while True:
            # get the message
            msg = self.recv()

            # called at logger creation
            if(msg.command == self.INIT):
                # if logger doesn't exist
                if not msg.param.name in self.loggersContext:
                    # create it and store the context
                    self.loggersContext[msg.param.name] = dict()
                    self.commonLogFileName = '{}-{}-{}.log'.format(
                        *asctime().split(" ")[1:4])
                    self.loggersContext[msg.param.name]["filename"] = msg.param.name + \
                        '-' + self.commonLogFileName
                    self.loggersContext[msg.param.name]["exec_param"] = msg.param.exec_param
                    self.loggersContext[msg.param.name]["level_disp"] = msg.param.level_disp.value

                    # if write parameter is set, create file
                    if msg.param.exec_param > 0:
                        self.loggersContext[msg.param.name]["file"] = open(
                            self.loggersContext[msg.param.name]["filename"], "a", newline='\n', encoding="utf-8")
                        self.commonLogFile = open(
                            self.commonLogFileName, "a", newline='\n', encoding="utf-8")

                    else:
                        self.loggersContext[msg.param.name]["file"] = None

            # called at each logger write cmd
            elif(msg.command == self.WRITE_LOG):
                # if logger exist
                if msg.param.name in self.loggersContext:
                    # if disaly is set
                    if self.loggersContext[msg.param.name]["exec_param"] % 2 == 0:
                        # check the desired diplaylog severity
                        if msg.param.level.value <= self.loggersContext[msg.param.name]["level_disp"]:
                            # show the message
                            print(self.formatTime(msg.param.time),
                                  self.formatName(msg.param.name),
                                  self.formatLevel(msg.param.level),
                                  ':',
                                  *msg.param.args)
                            for key, content in msg.param.kwargs.items():
                                print("  •", key, ":")
                                print("      ", content)

                    # get specific logger file
                    file = self.loggersContext[msg.param.name]["file"]
                    # if write on file is set
                    if self.loggersContext[msg.param.name]["exec_param"] > 0 and file is not None:
                        # write specific logs
                        file.write(msg.param.time)
                        file.write('('+msg.param.name+')')
                        file.write(msg.param.level.name)
                        file.write(" : ")
                        for arg in msg.param.args:
                            file.write(" {}".format(str(arg)))
                        for key, content in msg.param.kwargs.items():
                            file.write("\n{} : ".format(
                                str(key)), "\t", str(content))
                        file.write("\n")
                        file.flush()

                        # write common logs
                        self.commonLogFile.write(msg.param.time)
                        self.commonLogFile.write('('+msg.param.name+')')
                        self.commonLogFile.write(msg.param.level.name)
                        self.commonLogFile.write(" : ")
                        for arg in msg.param.args:
                            self.commonLogFile.write(" {}".format(str(arg)))
                        for key, content in msg.param.kwargs.items():
                            self.commonLogFile.write("\n{} : ".format(
                                str(key)), "\t", str(content))
                        self.commonLogFile.write("\n")
                        self.commonLogFile.flush()

    # format time with colorisation
    def formatTime(self, time):
        return colorise(time, car_attr=Colors.BOLD)

    # format level with colorisation
    def formatLevel(self, level):
        return colorise(level.name, color=level.color)

    # format name with colorisation
    def formatName(self, name):
        name = '('+name+')'
        return colorise(name, color=Colors.GREY, car_attr=Colors.BOLD)

    # receive pipe message
    def recv(self):
        return self.pipe.parent_conn.recv()

    # send pipe message
    def send(self, obj):
        self.lock.acquire()
        self.pipe.child_conn.send(obj)
        self.lock.release()

    # close pipe
    def close(self):
        self.pipe.child_conn.close()

    # get logger proxy
    def getlogger(self, name, exec_param=SHOW, level_disp=Logger.DEBUG):
        return Logger(self, name, exec_param, level_disp)
