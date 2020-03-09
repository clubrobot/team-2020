#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from time import monotonic, sleep
from threading import Thread, Event, current_thread
from logs.log_manager import *
from listeners.end_game_listener import *

class AccessDenied(Exception): pass

class RobotBehavior:
    BLUE_SIDE       = 0
    YELLO_SIDE      = 1
    UNDEFINED_SIDE  = -1

    def __init__(self, manager, *args, timelimit=None, exec_param=Logger.SHOW, log_level=INFO, **kwargs):
        self.manager    = manager
        self.timelimit  = timelimit
        self.whitelist  = set()
        self.blacklist  = set()
        self.outputs    = dict()
        self.stop_event = Event()

        # Keep old manager method
        self.manager_send = self.manager.send

        # Override manager send method
        self.manager.send = self.send

        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, exec_param, log_level)

    def perform(self, procedure, args=(), kwargs={}, timelimit=True):
        thread = Thread(args=args, kwargs=kwargs, daemon=True)
        thread_id = id(thread)
        def target(*args, **kwargs):
            try:
                print(*args)
                output = procedure(*args, **kwargs)
                self.outputs[thread_id] = output
            except AccessDenied:
                self.outputs[thread_id] = None
            except:
                self.outputs[thread_id] = None
                raise
            finally:
                if thread_id in self.blacklist: self.blacklist.remove(thread_id)
                if thread_id in self.whitelist: self.whitelist.remove(thread_id)

        if not timelimit: self.whitelist.add(thread_id)
        thread._target = target
        thread.start()
        return thread

    def interrupt(self, thread):
        if thread.is_alive():
            thread_id = id(thread)
            self.blacklist.add(thread_id)

    def get(self, thread, timeout=None):
        thread.join(timeout=timeout)
        if thread.is_alive():
            raise TimeoutError('timeout exceeded')
        thread_id = id(thread)
        output = self.outputs[thread_id]
        del self.outputs[thread_id]
        return output

    def send(self, *args, **kwargs):
        thread_id = id(current_thread())
        denyaccess = thread_id in self.blacklist
        if not thread_id in self.whitelist:
            if self.timelimit is not None:
                denyaccess |= (self.get_elapsed_time() > self.timelimit)
            denyaccess |= self.stop_event.is_set()
        if denyaccess:
            raise AccessDenied(thread_id)
        else:
            return self.manager_send(self, *args, **kwargs)

    def start_preparation(self):
        from robots.buttons_manager import ButtonsManager
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
        self.starttime = monotonic()
        self.stop_event.clear()
        self.logger(INFO, 'Start Behaviour')
        try:
            start = self.perform(self.start_procedure, timelimit=False)
            while (self.timelimit is None or self.get_elapsed_time() < self.timelimit) and not self.stop_event.is_set():
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

                    print((location, thresholds))
                    goto = self.perform(self.goto_procedure, args=(location, thresholds))
                    success = self.get(goto)
                else:
                    success = True
                if success:
                    action = self.perform(procedure, args=args, kwargs=kwargs)
                    self.get(action)
                else:
                    self.logger(INFO, 'Goto failed')
        except:
            self.whitelist.clear()
            raise
        finally:
            self.stop()
            self.get(start)
            self.whitelist.add(id(current_thread()))

    def stop(self):
        self.logger(INFO, 'Stop match')
        self.perform(self.stop_procedure, timelimit=False)
        self.stop_event.set()

    def get_elapsed_time(self):
        if hasattr(self, 'starttime'):
            return monotonic() - self.starttime
        else:
            return 0


if __name__ == "__main__":
    from math import pi

    from setups.setup_serialtalks import *
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

            return True

    rb = Robot(manager, timelimit=20)

    rb.start()