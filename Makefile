all: tabbed

tabbed: tabbed.ui
	pyuic5 tabbed.ui -o tabbed.py
