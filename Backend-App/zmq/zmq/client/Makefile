include module.mk

#####################################################################################
# Do not change below part unless you have understood this script very well			#
#####################################################################################

CROSS_TOOL_PREFIX	:= 

OPTIMIZE	:= -O1
WARNINGS	:= -Wall -W
DEFS		+= -DLINUX -DDEBUG_CONSOLE -DDEBUG_VMF_TRACE
EXTRA_CFLAGS	:= -pipe

MODULE_TOP_DIR	:= ./
SRC_TOP_DIR	:= $(MODULE_TOP_DIR)src/
BIN_TOP_DIR	:= $(MODULE_TOP_DIR)bin/
LIB_TOP_DIR	:= $(MODULE_TOP_DIR)lib/
OBJ_TOP_DIR	:= $(MODULE_TOP_DIR)obj/
SRC_DIRS	:= $(sort $(dir $(SOURCES)))
OBJ_DIRS	:= $(subst $(SRC_TOP_DIR),$(OBJ_TOP_DIR),$(SRC_DIRS))
INC_DIRS	:= $(foreach d, $(SRC_DIRS) $(INCLUDEPATH), -I$d)

#FUNC# set the variable `SOURCE_x' according to the input SUFFIX
define set_src_x
SOURCE_$1 := $(filter %.$1,$(SOURCES))

endef

#FUNC# set the variable `OBJECT_x' according to the input SUFFIX
define set_obj_x
OBJECT_$1 := $(patsubst $(SRC_TOP_DIR)%.$1,$(OBJ_TOP_DIR)%.o,$(SOURCE_$1))

endef

SUFFIX	:= c cpp
$(eval $(foreach i,$(SUFFIX),$(call set_src_x,$i)))
$(eval $(foreach i,$(SUFFIX),$(call set_obj_x,$i)))
OBJECTS := $(foreach i,$(SUFFIX),$(OBJECT_$i))

GCC		:= $(CROSS_TOOL_PREFIX)gcc
LD		:= $(CROSS_TOOL_PREFIX)gcc
AR		:= $(CROSS_TOOL_PREFIX)ar
MKDIR	:= mkdir -p
RM		:= rm -f
COPY	:= cp -f -p

CFLAGS	:= $(EXTRA_CFLAGS) $(WARNINGS) $(OPTIMIZE) $(DEFS)
LDFLAGS	:= -Wl,-O1
LIBS	+= -lrt -lpthread
TARGET_TYPE	:= $(strip $(TEMPLATE))

ifeq ($(filter $(TARGET_TYPE),so ar app),)
$(error Unexpected TEMPLATE `$(TEMPLATE)')
endif

ifeq ($(TARGET_TYPE),app)
TARGET	:= $(BIN_TOP_DIR)$(TARGET)
else
ifeq ($(TARGET_TYPE),ar)
TARGET	:= $(LIB_TOP_DIR)lib$(TARGET).a
else	# for so
CFLAGS  += -fPIC
TARGET	:= lib$(TARGET).so
LDFLAGS += -shared -Wl,-soname,$(TARGET)
LIBS	+= -lc
TARGET	:= $(LIB_TOP_DIR)$(TARGET)
endif
endif

all:  $(TARGET)


ifeq ($(SOURCES),)
	@echo "The content of SOURCES is empty!!!"
else

ifeq ($(TARGET_TYPE),app)
$(TARGET): $(BIN_TOP_DIR) $(OBJ_DIRS) $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@
else
ifeq ($(TARGET_TYPE),ar)
$(TARGET): $(LIB_TOP_DIR) $(OBJ_DIRS) $(OBJECTS)
	-$(RM) $@
	$(AR) rcvs $@ $(OBJECTS)
else	# for so
$(TARGET): $(LIB_TOP_DIR) $(OBJ_DIRS) $(OBJECTS)
	$(LD) $(LDFLAGS) $(OBJECTS) $(LIBS) -o $@
endif
endif

endif



$(BIN_TOP_DIR) $(OBJ_DIRS) $(LIB_TOP_DIR):
	-$(MKDIR) $@

define cmd_o
$(OBJECT_$1): $(OBJ_TOP_DIR)%.o: $(SRC_TOP_DIR)%.$1
	$(GCC) -Wp,-MT,$$@ -Wp,-MMD,$$@.d -c $(CFLAGS) $(INC_DIRS) $$< -o $$@

endef
$(eval $(foreach i,$(SUFFIX),$(call cmd_o,$i)))

-include $(patsubst %.o,%.o.d,$(OBJECTS))

clean:
	-$(RM) $(OBJECTS) $(patsubst %.o,%.o.d,$(OBJECTS))

INSTALL_INC_DIR	:= $(INSTALL_DIR)include/

ifeq ($(TARGET_TYPE),app)
INSTALL_TARGET_DIR	:= $(INSTALL_DIR)bin/
else
INSTALL_TARGET_DIR	:= $(INSTALL_DIR)lib/
endif

install: $(INSTALL_TARGET_DIR) $(INSTALL_INC_DIR)
ifeq ($(INSTALL_DIR),)
	echo '------------------ Failed!!! INSTALL_DIR is empty! ------------------'
else
	$(COPY) $(TARGET) $(INSTALL_TARGET_DIR)
	
ifneq ($(wildcard *.h),)
	$(COPY) ./*.h $(INSTALL_INC_DIR)
endif
endif

DEPLOY_DIR	:= /home/zero/nfs/rootfs/

ifeq ($(TARGET_TYPE),app)
DEPLOY_TARGET_DIR	:= $(DEPLOY_DIR)opt/
else
DEPLOY_TARGET_DIR	:= $(DEPLOY_DIR)usr/local/lib/
endif

deploy: $(DEPLOY_TARGET_DIR)
	$(COPY) $(TARGET) $(DEPLOY_TARGET_DIR)
	-@./DeployOtherFile.sh

$(INSTALL_TARGET_DIR) $(INSTALL_INC_DIR) $(DEPLOY_TARGET_DIR):
	-$(MKDIR) $@

integration:
	make all && make install

.PHONY: all clean install deploy integration
