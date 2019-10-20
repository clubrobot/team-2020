# Board properties
BOARD_UUID = VL53L0X
BOARD_TAG  = nano
BOARD_SUB  = atmega328

# Sketch sources
COMMON = ../common
LOCAL_INO_SRCS = main.ino
LOCAL_CPP_SRCS = \
	$(COMMON)/SerialTalks.cpp \
	$(COMMON)/CRC16.cpp \
	$(COMMON)/VL53L0X.cpp

# Define
CPPFLAGS += -DPUREPURSUIT_MAX_WAYPOINTS=32
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30

# Sketch libraries
ARDUINO_LIBS = EEPROM Wire

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk
