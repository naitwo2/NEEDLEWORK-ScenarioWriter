build:
	docker build . -t needlework-scenariowriter 

container-test: pre
	docker run -v $(PWD)/config/sample_cfg.txt:/scenario.txt \
	-e DISABLE_POLICY_OUTPUT=n \
	needlework-scenariowriter:latest
	docker run -v $(PWD)/config/sample_cfg.txt:/scenario.txt \
	-e DISABLE_POLICY_OUTPUT=y \
	needlework-scenariowriter:latest
	docker run -v $(PWD)/config/sample_cfg.txt:/scenario.txt \
	needlework-scenariowriter:latest

container-interactive: pre
	docker run -v $(PWD)/config/sample_cfg.txt:/scenario.txt \
	-e DISABLE_POLICY_OUTPUT=n \
	-ti \
	needlework-scenariowriter:latest /bin/sh

pre:
	$(eval PWD := $(shell pwd))


