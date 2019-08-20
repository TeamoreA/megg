SHELL = /usr/bin/env /bin/bash

## Start service
start:
	@echo ''
	${INFO} "starting service $(service) ...."
	@docker start $(service) > /dev/null
	@echo .....
	${SUCCESS} "service $(service) started ..."
	@echo ''

## Display service status
status:
	@echo ''
	@if [ "$(STATUS)" = "true" ]; then printf $(GREEN); echo "===>$(RUNNING) "; printf $(NC); else printf $(GREEN); echo "===> $(STOPPED) "; printf $(NC); fi
	@echo ''

## Stop service
stop:
	@echo ''
	${INFO} "Stopping megg ....."
	@docker stop megg> /dev/null
	@echo .....
	${SUCCESS} "$(service) stopped "
	@echo ''

## Restart service
restart:
	@echo ''
	${INFO} "Restarting $(service) .."
	@docker restart $(service) > /dev/null
	@echo .....
	${SUCCESS} "$(service) restarted"
	@echo ''

## Attach to container and execute commands
attach:
	@echo ''
	${INFO} "Attaching to service $(service) ..."
	@echo ''
	@docker exec -i -t $(service) bash

## Build service and launch
build:
	@echo ''
	${INFO} "Builing service ..."
	@docker build -t megg . 
	${SUCCESS} "Service successfully build"
	${INFO} "starting application ..."
	@docker run -d --name megg -p 8000:8000 -v $(shell pwd)/src:/src megg 
	${SUCCESS} "Application started successfully"

## View service logs
log:
	@echo ''
	${INFO} "Viewing $(service) logs"
	@docker logs -f $(service)

## Update application dependencies
update:
	@echo ''
	${INFO} "Updating $(service) dependencies..."
	${INFO} "Copying depencies file ..."
	@docker cp cpanfile $(service):/cpanfile
	@docker exec -t $(service) bash -c "cd / && cpanm --installdeps ."
	${SUCCESS} "Dependencies updated successfully."

## Remove service
clean:
	@echo ''
	${INFO} "Removing service ..."
	@docker rm -f megg >> /dev/null
	${SUCCESS} "Service $(service) successfully removed"


RUNNING = ...Service $(service) is running ...
STOPPED = "... Service $(service) is not running ..."
STATUS := $$(docker inspect -f '{{.State.Running}}' $(service))
GREEN  := $(shell tput -Txterm setaf 2)
YELLOW := $(shell tput -Txterm setaf 3)
RED := $(shell tput -Txterm setaf 1)
RESET  := $(shell tput -Txterm sgr0)
NC := "\e[0m"
TARGET_MAX_CHAR_NUM=10
INFO := @bash -c 'printf $(YELLOW); echo "===> $$1"; printf $(NC)' SOME_VALUE
SUCCESS := @bash -c 'printf $(GREEN); echo "===> $$1"; printf $(NC)' SOME_VALUE
ERROR := @bash -c 'printf $(RED); echo "====> $$1"; printf $(NC)' SOME_VALUE