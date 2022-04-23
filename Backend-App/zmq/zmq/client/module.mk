# Change this Variables for your project
# TEMPLATE can be 'app' for application, 'so' for shared library, 'ar' for static library
TARGET = client
TEMPLATE = app

SOURCES += \
./src/main.c

INCLUDEPATH += ./src/

LIBS += -L /usr/local/lib/ -lzmq
#LIBS += -L../../ai-sdk-forMiddleware-NGI/hal/lib/ -lHAL

INSTALL_DIR	:= ../install/
