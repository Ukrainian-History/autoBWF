# autoBWF

## A GUI tool for automatically generating and editing BWF metadata

The purpose of autoBWF is to provide an alternative GUI for embedding internal metadata in WAVE audio files using the [Broadcast Wave](https://en.wikipedia.org/wiki/Broadcast_Wave_Format) standard, FADGI [BWFMetaEdit](https://mediaarea.net/BWFMetaEdit), and [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform). 

Unlike the existing BWFMetaEdit GUI, autoBWF is extremely opinionated and will automatically generate metadata content based on file naming conventions and system metadata. In addition, it can copy metadata fields from a template file to avoid having to enter the same information multiple times for several master or derivative files of the same physical instantiantion.


![screenshot of GUI](screenshot.png)


### Requirements

This code requires 
* Python 3
* PyQt 5 
* [Python XMP Toolkit](http://python-xmp-toolkit.readthedocs.io/en/latest/index.html#) ([github](https://github.com/python-xmp-toolkit/python-xmp-toolkit))
  * which in turn requires the [Exempi library](https://libopenraw.freedesktop.org/wiki/Exempi/)
* [BWFMetaEdit](https://mediaarea.net/BWFMetaEdit/Download) CLI. 

It assumes that the "bwfmetaedit" executable is in the current PATH. It has been tested on Linux using bwfmetaedit version 1.3.3. It should also run on Unix-like systems such as MacOS. 

If you want to run on Windows, then you're on your own... Windows users may face challenges getting Exempi installed. If you want to use the BWF and RIFF editing capabilities without XMP, please try using the [2.1 version](https://github.com/Ukrainian-History/autoBWF/releases/tag/v2.1)


### Usage

python autoBWF.py

Alternatively, you can avoid using the "Open" dialog by specifying the target file and (optional) template file on the command line:

python autoBWF.py *target_filename* [-t *template_filename*]

autoBWF will prepopulate the Description, Originator, OriginationDate, OriginationTime, and OriginatorRef GUI elements with reasonable guesses as described below. If *target_filename* already contains BWF metadata, then those values will appear in the GUI in grey italic text. If the user edits those fields, the text color will change to red as a warning that the values will be overwritten in the target file after clicking "Ok". **This cannot be undone!** You have been warned...

The CodingHistory text is generated automatically based on the selections made in the drop-downs to the right of the text box. You can also edit the text manually, but be aware that using the drop-down menus will undo any manual edits that you have made. Similarly, the Copyright text is replaced with the boilerplate corresponding to the dropdown menu selection. The same caveat regarding manual editing holds here as well.

Loading a template file (either using the "Load Template" button or using the optional `-t` command line argument) will prepopulate the contents of the Title, Technician, Source, Copyright, Coding History, and any XMP text fields with the corresponding metadata contained in *template_filename*. These can always be edited before updating the metadata in the target file.

It is strongly recommended that you play around using test files and confirm (using BWFMetaEdit and/or an internal metadata viewer like exiftool) that autoBWF is behaving the way that you expect before working with preservation or production master files.

### Configuration

You can edit the file config.json to customize the values in the dropdown menus and other program behavior to the needs of your use case. In particular, it contains the model, serial number, and software version strings that go into constructing the CodingHistory element, as well as the copyright boilerplate texts. 

The bwfmetaedit "--accept-nopadding" flag is used by default, but that behavior can also be changed in the configuration file.


#### Automatic metadata generation details

 The code assumes that filenames follow the convention of Indiana University Archives of Traditional Music as described in the ["Sound Directions" publication](http://www.dlib.indiana.edu/projects/sounddirections/papersPresent/index.shtml). If the naming convention at your archives is different, then you may be able to make things work by modifying the regex string in config.json, or more substantial customization to the Python code may need to be made. The values of Description, Originator, OriginationDate, OriginationTime, and OriginatorRef are prefilled based on parsing the filename and using file creation date and times obtained from OS metadata together with default values in config.json. If there is a conflict between the OS metadata date and that in the filename, then the program will display a warning and will allow you to choose which one you want to use. If the program cannot parse the filename, then it will display a warning, use the OS file creation date and time to generate OriginationDate, OriginationTime, and OriginatorRef, and will leave Description blank.


#### Known issues

* Does not remove existing XMP metadata fields (i.e. setting a field to "" causes the existing data to remain unchanged)

* For some reason, XMP dc:description shows up as RIFF ISBJ in BWFMetaEdit. This may or may not be a bug...