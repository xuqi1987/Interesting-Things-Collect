# Change this Variables for your project
# Each component has a modules.mk in which define the submodulse of this component

include modules.mk

#####################################################################################
# Do not change below part unless you have understood this script very well			#
#####################################################################################

MAKE	:= make

first: all

all clean install deploy integration:
	@for d in $(SUBPROJECT_BUILD_DIRS); do \
	  if $(MAKE) -C $$d $@; then \
	    echo '------------------ '$$d' Success! ------------------'; \
	  else \
	    exit 1; \
	  fi; \
	done; \
	echo '------------------ ALL SUBPROJECT Success! ------------------'

.PHONY: all clean install deploy integration
