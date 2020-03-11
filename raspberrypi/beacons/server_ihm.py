#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess

import Adafruit_SSD1306   # This is the driver chip for the Adafruit PiOLED

from PIL import Image, ImageDraw, ImageFont
from time import sleep
import RPi.GPIO as GPIO

from common.parallel import Thread
from threading import Event

class JetsonSwitch():
    def __init__(self, pin, attached_func):
        self.pin = pin
        self.attached_func = attached_func

        GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme

        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, GPIO.LOW)
        sleep(0.2)
        GPIO.setup(self.pin, GPIO.IN)

        Thread(target=self.target, daemon=True).start()

    def target(self):
        while True:
            value = GPIO.input(self.pin)
            if value == GPIO.HIGH:
                sleep(0.05)
                GPIO.setup(self.pin, GPIO.OUT)
                sleep(0.05)
                GPIO.output(self.pin, GPIO.LOW)
                sleep(0.05)
                GPIO.setup(self.pin, GPIO.IN)
                self.attached_func()
            sleep(0.05)

_BORNIBUS_ID = 1
_R128_ID = 2

_INTER_1_PIN = 26
_INTER_2_PIN = 19
_INTER_3_PIN = 13
_INTER_4_PIN = 6


class ServerIHM():
    def __init__(self):

        self.screen  = Adafruit_SSD1306.SSD1306_128_32(rst=None, i2c_bus=1, gpio=1)

        self.green_switch   = JetsonSwitch(_INTER_1_PIN, self.on_green_switch)
        self.yellow_switch  = JetsonSwitch(_INTER_2_PIN, self.on_yellow_switch)
        self.blue_switch    = JetsonSwitch(_INTER_3_PIN, self.on_blue_switch)
        self.red_switch     = JetsonSwitch(_INTER_4_PIN, self.on_red_switch)

        self.green_event    = Event()
        self.yellow_event   = Event()
        self.blue_event     = Event()
        self.red_event      = Event()

        # Init Screen
        self.screen.begin()

        # Clear display.
        self.screen.clear()
        self.screen.display()

        # Create blank image for drawing.
        self.image = Image.new('1', (self.screen.width, self.screen.height))

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(self.image)

        self.padding = -2
        self.top = self.padding
        self.bottom = self.screen.height - self.padding

        self.x = 0

        # Load default font.
        self.font = ImageFont.load_default()

        self._clear_picture()

    def on_green_switch(self):
        self.green_event.set()

    def on_yellow_switch(self):
        self.yellow_event.set()

    def on_blue_switch(self):
        self.blue_event.set()

    def on_red_switch(self):
        self.red_event.set()

    def _clear_picture(self):
        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.screen.width, self.screen.height), outline=0, fill=0)

    def _get_network_interface_state(self,interface):
        return subprocess.check_output('cat /sys/class/net/%s/operstate' % interface, shell=True).decode('ascii')[:-1]

    def _get_ip_address(self, interface):
        if self._get_network_interface_state(interface) == 'down':
            return None
        cmd = "ifconfig %s | grep -Eo 'inet (addr:)?([0-9]*\.){3}[0-9]*' | grep -Eo '([0-9]*\.){3}[0-9]*' | grep -v '127.0.0.1'" % interface
        return subprocess.check_output(cmd, shell=True).decode('ascii')[:-1]

    def _get_cpu_usage(self):
        # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True)
        return CPU

    def _get_gpu_usage(self):
        GPU = 0.0
        with open("/sys/devices/gpu.0/load", encoding="utf-8") as gpu_file:
            GPU = gpu_file.readline()
            GPU = int(GPU)/10
        return GPU

    def show_init_message(self, clients):
        if self.green_event.is_set():
            self._clear_picture()
            self.green_event.clear()
            self.draw.text((self.x, self.top), "Green",  font=self.font, fill=255)

        if self.yellow_event.is_set():
            self._clear_picture()
            self.yellow_event.clear()
            self.draw.text((self.x, self.top), "Yellow",  font=self.font, fill=255)

        if self.blue_event.is_set():
            self._clear_picture()
            self.blue_event.clear()
            self.draw.text((self.x, self.top), "Blue",  font=self.font, fill=255)

        if self.red_event.is_set():
            self._clear_picture()
            self.red_event.clear()
            self.draw.text((self.x, self.top), "Red",  font=self.font, fill=255)

        # self.draw.text((self.x, self.top), "wlan0: " + str(self._get_ip_address('wlan0')),  font=self.font, fill=255)

        # if _BORNIBUS_ID in list(clients):
        #     self.draw.text((self.x, self.top + 8), "Bornibus : Ok !",  font=self.font, fill=255)
        # else:
        #     self.draw.text((self.x, self.top + 8), "Bornibus : None",  font=self.font, fill=255)
        # if _R128_ID in list(clients):
        #     self.draw.text((self.x, self.top + 16), "128 Ok !",  font=self.font, fill=255)
        # else:
        #     self.draw.text((self.x, self.top + 16), "128 : None",  font=self.font, fill=255)

        # self.draw.text((self.x, self.top + 24), "Press to start ...",  font=self.font, fill=255)
        try :
            self.screen.image(self.image)
            self.screen.display()
        except IOError:
            print('screen error')