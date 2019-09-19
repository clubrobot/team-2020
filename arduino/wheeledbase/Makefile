# Board properties
BOARD_UUID = wheeledbase
BOARD_TAG  = nano
BOARD_SUB  = atmega328

# Sketch sources
COMMON = ../common
LOCAL_INO_SRCS = wheeledbase.ino
LOCAL_CPP_SRCS = \
	instructions.cpp \
	$(COMMON)/SerialTalks \
	$(COMMON)/CRC16 \
	$(COMMON)/DCMotor \
	$(COMMON)/Codewheel \
	$(COMMON)/PeriodicProcess \
	$(COMMON)/Odometry \
	$(COMMON)/PID \
	$(COMMON)/DifferentialController \
	$(COMMON)/VelocityController \
	$(COMMON)/PositionController \
	$(COMMON)/PurePursuit \
	$(COMMON)/TurnOnTheSpot \
	$(COMMON)/mathutils

# Define
CPPFLAGS += -DPUREPURSUIT_MAX_WAYPOINTS=32
CPPFLAGS += -DSERIALTALKS_MAX_OPCODE=0x30

# Sketch libraries
ARDUINO_LIBS = EEPROM

# Congratulations! You made a pretty Makefile :)
# Now let the grown-ups do the hard work :D
MODULEMK_DIR = ..
include $(MODULEMK_DIR)/Module.mk
