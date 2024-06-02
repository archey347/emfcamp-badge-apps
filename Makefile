helloworld:
	/root/.local/bin/mpremote a0 cp ./helloworld/* :/apps/helloworld/

introapp:
	/root/.local/bin/mpremote a0 cp ./introapp/* :/apps/introapp/

text-display:
	/root/.local/bin/mpremote a0 cp ./textdisplay/* :/apps/textdisplay/


update-settings:
	/root/.local/bin/mpremote a0 cp ./settings.json :/

shell:
	/root/.local/bin/mpremote a0

.PHONY: helloworld introapp update-settings text-display shell