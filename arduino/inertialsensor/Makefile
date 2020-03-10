BOARD_UUID = mainv
BOARD_TAG  = nano
BOARD_SUB  = atmega328

# Sketch sources
COMMON = ../common
LOCAL_INO_SRCS = main.ino
LOCAL_CPP_SRCS = \
	instructions.cpp \
	$(COMMON)/SerialTalks.cpp \
	$(COMMON)/CRC16.cpp \
	$(COMMON)/Clock.cpp \
	$(COMMON)/Wire.cpp \

LOCAL_C_SRCS = \
	$(COMMON)/twi.c \
	

# Sketch libraries
ARDUINO_LIBS = EEPROM

MONITOR_PORT=/dev/ttyS0


# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk