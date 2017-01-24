all: main

main: main.ui
	pyuic5 main.ui -o main.py
