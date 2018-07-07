all: main tabbed

main: main.ui
	pyuic5 main.ui -o main.py

tabbed: tabbed.ui
	pyuic5 tabbed.ui -o tabbed.py