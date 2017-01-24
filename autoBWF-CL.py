#!/usr/local/bin/python3

import argparse
import re
import os.path
from datetime import date
from datetime import datetime
import subprocess

history_strings = {"Tandberg": "Tandberg 12-42; 2201485; {0} ips; open reel tape", 
				"Focusrite Scarlett": "Focusrite; Scarlett 2i2; S363312221352"}

deck_sn = {"Tandberg": "2201485"}

fileuse = {"pres": "Preservation Master", "presInt": "Preservation Master-Intermediate",
			"prod": "Production Master", "access": "Access Copy"}

#  bwfmetaedit --specialchars --History="A=ANALOGUE,M=stereo,T=The dulcet tones of Mike Andrec\nA=PCM,F=96000,W=24,M=stereo,T=MacBook Pro\n" ukrheca_2014-99-99_RL1_010101_pres_20141020.wav

def generate_internal(file, options):
	if not os.path.exists(file):
		return(file + " does not exist")

	m = re.compile("ukrheca_([0-9-]+)_RL(\d+)_\d+_([a-zA-Z]+)_(\d+).wav").match(file)

	if not m: return(file + " does not follow UkrHEC filenaming convention")

	matches = m.groups()
	acc = matches[0]
	reel = matches[1]
	use = matches[2]
	datestring = matches[3]

	datestring_iso = datestring[0:4] + "-" + datestring[4:6] + "-" + datestring[6:]

	deck = options["deck"]
	ips = options["ips"]
	adconv = options["ADconv"]
	override_date = options["override_date"]

	acc = acc.replace("-", ".")

	try:
		use = fileuse[use]
	except KeyError:
		return(file + " does not follow UkrHEC filenaming convention: invalid file use " + use)

	date_time = datetime.fromtimestamp(os.path.getctime(file)).replace(microsecond=0).isoformat()
	[date, time] = date_time.split("T")

	if date != datestring_iso:
		if override_date is None:
			return(file + " timestamp " + date + " does not match date in filename: use --override-date option")
		else:
			datestring_iso = override_date
			datestring = datestring.replace("-", "")

	filecont = "File content: Accession " + acc + " Reel " + reel + ". File use: " + use + ". Original filename: " + file
	originator = "UkrHEC Archives"
	originator_reference = "UkrHECArch " + deck_sn[deck] + " " + time.replace(":", "")
	origination_date = datestring_iso
	origination_time = time
	history = "A=ANALOGUE,M=stereo,T=" + history_strings[deck].format(ips) + "\nA=PCM,F=96000,W=24,M=stereo,T=" + history_strings[adconv]

	print(filecont)
	print(originator)
	print(originator_reference)
	print(origination_date)
	print(origination_time)
	print(history)

	proceed = input("Write internal metadata to file? (Y/n) ")

	if proceed is "" or proceed is "Y": 
		common_args = "bwfmetaedit --reject-overwrite --specialchars "
		if options["padding"]: common_args = common_args + "--accept-nopadding "
		sysout = subprocess.call(common_args + "--MD5-embed " + file, shell=True)
		sysout = subprocess.call(common_args + '--Description="' + filecont + '" ' + file, shell=True)
		sysout = subprocess.call(common_args + '--Originator="' + originator + '" ' + file, shell=True)
		sysout = subprocess.call(common_args + '--OriginatorReference="' + originator_reference + '" ' + file, shell=True)
		sysout = subprocess.call(common_args + '--OriginationDate="' + origination_date + '" ' + file, shell=True)
		sysout = subprocess.call(common_args + '--OriginationTime="' + origination_time + '" ' + file, shell=True)
		sysout = subprocess.call(common_args + '--Timereference=0 ' + file, shell=True)
		sysout = subprocess.call(common_args + '--History="' + history + '" ' + file, shell=True)
		#print(sysout)
		# bwfmetaedit --specialchars --History=history filename

	return(None)


def main():
	parser = argparse.ArgumentParser(description='Create internal and external metadata for WAV file(s).')
	parser.add_argument('filename', nargs='+', help='WAV file to be processed')
	parser.add_argument('-q', '--quiet', action="store_true", help="silence helpful messages")
	parser.add_argument('--deck', help="short name of tape deck", default="Tandberg")
	parser.add_argument('--ADconv', help="short name of A/D converter", default="Focusrite Scarlett")
	parser.add_argument('--comp', help="short name of recording computer", default="Linuxbox")
	parser.add_argument('--ips', choices=["30", "15", "7.5", "3.75", "1.875"], help="tape speed", required=True)
	parser.add_argument("--override-date", help="override the date in the file system timestamp")
	parser.add_argument("--padding", action="store_true", help="ignore padding errors")
	
	args = parser.parse_args()

	p = re.compile("^([0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])$")
	if args.override_date is not None and not p.match(args.override_date):
		print(args.override_date + " is not a valid ISO date")
		return(None)

	options = {"quiet": args.quiet, "deck": args.deck, "ADconv": args.ADconv, "comp": args.comp, 
				 "ips": args.ips, "override_date": args.override_date, "padding": args.padding}

	# check to make sure hardware names are valid

	for filename in args.filename:
		warn = generate_internal(filename, options)
		if warn: print(warn)

main()

