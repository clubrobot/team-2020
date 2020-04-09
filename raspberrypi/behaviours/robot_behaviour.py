#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from time import monotonic, sleep
from threading import Thread, Event, current_thread
from logs.log_manager import *
from listeners.end_game_listener import *
from common.components import AccessDenied

class RobotBehavior:
    BLUE_SIDE       = 0
    YELLO_SIDE      = 1
    UNDEFINED_SIDE  = -1

    def __init__(self, manager, *args, timelimit=None, exec_param=Logger.SHOW, log_level=INFO, **kwargs):
        self.manager    = manager
        self.timelimit  = timelimit
        self.outputs    = dict()
        self.stop_event = Event()

        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, exec_param, log_level)

        # Set timelimit
        self.manager.set_timelimit(self.timelimit)

    def perform(self, procedure, args=(), kwargs={}, timelimit=True):
        thread = Thread(args=args, kwargs=kwargs, daemon=True)
        thread_id = id(thread)
        def target(*args, **kwargs):
            try:
                output = procedure(*args, **kwargs)
                self.outputs[thread_id] = output
            except AccessDenied:
                self.outputs[thread_id] = None
            except:
                self.outputs[thread_id] = None
                raise
            finally:
                if thread_id in self.manager.blacklist: self.manager.blacklist.remove(thread_id)
                if thread_id in self.manager.whitelist: self.manager.whitelist.remove(thread_id)

        if not timelimit: self.manager.whitelist.add(thread_id)
        thread._target = target
        thread.start()
        return thread

    def interrupt(self, thread):
        if thread.is_alive():
            thread_id = id(thread)
            self.manager.blacklist.add(thread_id)

    def get(self, thread, timeout=None):
        thread.join(timeout=timeout)
        if thread.is_alive():
            raise TimeoutError('timeout exceeded')
        thread_id = id(thread)
        output = self.outputs[thread_id]
        del self.outputs[thread_id]
        return output

    def start_preparation(self):
        from managers.buttons_manager import ButtonsManager
        ButtonsManager(self).begin()

    def make_decision(self):
        raise RuntimeError("the 'make_decision' method must be overriden")

    def goto_procedure(self, destination):
        raise RuntimeError("the 'goto_procedure' method must be overriden")

    def set_side(self, side):
        raise RuntimeError("the 'set_side' method must be overriden")

    def set_position(self):
        raise RuntimeError("the 'set_position' method must be overriden")

    def run(self):
        raise RuntimeError("the 'run' method must be overriden")

    def positioning(self):
        pass

    def start_procedure(self):
        pass

    def stop_procedure(self):
        pass

    def start(self):
        self.manager.start_time()
        self.stop_event.clear()
        LogManager().reset_time()
        self.logger(INFO, 'Start Behaviour')
        try:
            start = self.perform(self.start_procedure, timelimit=False)
            while (self.timelimit is None or self.manager.get_elapsed_time() < self.timelimit) and not self.stop_event.is_set():
                decision = self.make_decision()
                procedure, args, kwargs, (location, thresholds) = decision
                if procedure is None:
                    self.logger(INFO, 'No decision')
                    sleep(1)
                    continue
                if location is not None:
                    if location[2] is not None:
                        self.logger(INFO, 'Goto: ({0[0]:.0f}, {0[1]:.0f}, {0[2]:.2f})'.format(location))
                    else:
                        self.logger(INFO, 'Goto: ({0[0]:.0f}, {0[1]:.0f})'.format(location))
                    goto = self.perform(self.goto_procedure, args=(location, thresholds))
                    success = self.get(goto)
                else:
                    success = True
                if success:
                    self.logger(INFO, "Perform Action")
                    action = self.perform(procedure, args=args, kwargs=kwargs)
                    self.get(action)
                else:
                    self.logger(WARNING, 'Goto failed')
        except:
            self.manager.whitelist.clear()
            raise
        finally:
            self.stop()
            self.get(start)
            self.manager.whitelist.add(id(current_thread()))

    def stop(self):
        self.logger(INFO, 'Stop match')
        self.perform(self.stop_procedure, timelimit=False)
        self.stop_event.set()


if __name__ == "__main__":
    from math import pi

    from setups.setup_serialtalks import *
    from setups.setup_wheeledbase import *
    from behaviours.action.action import *

    class TakeCup(Action):
        def __init__(self, idx):
            self.idx = idx
            self.actionpoint = (555, 666)# geogebra.get('Point name')
            self.orientation = pi
            self.actionpoint_precision = 10

        def procedure(self, robot):
            print(robot.__class__.__name__)
            print('take : ', self.idx)
            sleep(1)

    class Robot(RobotBehavior):
        def __init__(self, manager, *args, timelimit=None, **kwargs):
                RobotBehavior.__init__(self, manager, *args, timelimit=timelimit, **kwargs)

                take1 = TakeCup(1)
                take2 = TakeCup(2)
                take3 = TakeCup(3)
                take4 = TakeCup(4)
                take5 = TakeCup(5)

                self.automate = [
                    take1,
                    take2,
                    take3,
                    take4,
                    take5
                    ]

                self.automatestep = 0

        def make_decision(self):
            if(self.automatestep < len(self.automate)):
                action = self.automate[self.automatestep]
            else:
                return None, (self,), {}, (None, None)
                self.stop_event.set()

            return action.procedure, (self,), {}, (action.actionpoint + (action.orientation,), (action.actionpoint_precision, None))

        def goto_procedure(self, destination, thresholds=(None, None)):
            self.automatestep += 1
            sleep(1)
            return True

    rb = Robot(manager, timelimit=20)

    rb.start()