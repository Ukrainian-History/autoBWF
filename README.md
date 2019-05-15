The purpose of `autoBWF` is to provide an alternative GUI for embedding internal metadata in WAVE audio files using the [Broadcast Wave](https://en.wikipedia.org/wiki/Broadcast_Wave_Format) standard, FADGI [BWFMetaEdit](https://mediaarea.net/BWFMetaEdit), and [XMP](https://en.wikipedia.org/wiki/Extensible_Metadata_Platform). 

Unlike the existing BWFMetaEdit GUI, autoBWF is extremely opinionated and will automatically generate metadata content based on file naming conventions, system metadata, and pre-configured repository defaults. In addition, it can copy metadata fields from a template file to avoid having to enter the same information multiple times for several master or derivative files of the same physical instantiantion.


![screenshot of GUI](https://github.com/Ukrainian-History/autoBWF/blob/master/screenshot.png)

Also included are two command line programs to simplify the creation of derivative files. `autolame.py` is a wrapper for the `lame` MP3 encoder that automatically transfers Wave BWF, RIFF, and XMP metadata to appropriate ID3v2 and XMP. `autosplice` is a wrapper that generates `sox` commands from an EDL-like text file to splice audio from multiple input files, while also providing means to do basic fade in/out and audio level compression.
### Requirements

This code requires Python 3.6 and PyQt 5, the latter of which will be automatically installed if you use `pip install`.

In addition, it requires non-Python software to be installed in a way that it can be found by `autoBWF`. Most importantly, you will need to install the [BWFMetaEdit](https://mediaarea.net/BWFMetaEdit) CLI (Command Line Interface). Note that simply having the BWFMetaEdit GUI installed is not sufficient. You can select your platform and download it from [here](https://mediaarea.net/BWFMetaEdit/Download), just be sure to click on the "CLI" link. This code has been tested with `bwfmetaedit` version 1.3.3.

In order to run `autolame` and `autosplice`, you will also need to install [lame](http://lame.sourceforge.net/) (for `autolame`) and [SoX](http://sox.sourceforge.net/) v14.4.2 (for `autosplice`). Note that some LINUX package repositories have an earlier version of `SoX` which seems to have problems with time specifications, so you may need to install from source.


### `autoBWF` usage

Simply type `autoBWF` on the command line, and use the GUI "Open" menu item to load your WAVE file.

Alternatively, you can avoid the "Open" dialog by specifying the target file and (optional) template file on the command line:

`autoBWF <target_filename> [-t <template_filename>]`

`autoBWF` will prepopulate the Description, Originator, OriginationDate, OriginationTime, and OriginatorRef GUI elements with reasonable guesses as described below. If *target_filename* already contains BWF metadata, then those values will appear in the GUI in grey italic text. If the user edits those fields, the text color will change to red as a warning that "Save metadata" will cause those the values will be overwritten in the target file. **This cannot be undone!**

The CodingHistory text is generated automatically based on the selections made in the drop-downs to the right of the text box and the values in your configuration file (see below). You can also edit the text manually, but be aware that using the drop-down menus will undo any manual edits that you have made. Similarly, the Copyright text is replaced with the boilerplate corresponding to the dropdown menu selection. The same caveat regarding manual editing holds here as well.

Loading a template file (either using the "Load Template" button or using the optional `-t` command line argument) will prepopulate the contents of the Title, Technician, Source, Copyright, Coding History, and any XMP text fields with the corresponding metadata contained in *template_filename*. These can always be edited before saving the metadata to the target file.

It is strongly recommended that you play around using test files and confirm (using BWFMetaEdit and/or a metadata viewer like exiftool) that autoBWF is behaving the way that you expect before working with master files.

#### Configuration

Program configuration is stored as a JSON file in a directory appropriate to your operating system (e.g. `~/.local/share/autoBWF` on Linux or `/Users/yourname/Library/Application Support/autoBWF` on MacOS). If the file does not exist, then a "starter" `autobwfconfig.json` will be created for you. You should edit this file to customize the values in the dropdown menus and other program behavior to the needs of your repository. In addition, the config file includes the model, serial number, and software version strings that go into constructing the CodingHistory element and copyright boilerplate texts. 

The `--accept-nopadding` flag is sent to `bwfmetaedit` by default, but that behavior can also be changed in the configuration file.


#### Automatic metadata generation details

 The code assumes that filenames follow the convention of Indiana University Archives of Traditional Music as described in the ["Sound Directions" publication](http://www.dlib.indiana.edu/projects/sounddirections/papersPresent/index.shtml). If the naming convention at your archives is different, then you may be able to make things work by modifying the regex string in config.json, or more substantial customization to the Python code may need to be made. The values of Description, Originator, OriginationDate, OriginationTime, and OriginatorRef are prefilled based on parsing the filename and using file creation date and times obtained from OS metadata together with default values in `autobwfconfig.json`. If there is a conflict between the OS metadata date and that in the filename, then the program will display a warning and will allow you to choose which one you want to use. If the program cannot parse the filename, then it will display a warning, use the OS file creation date and time to generate OriginationDate, OriginationTime, and OriginatorRef, and will leave Description blank.


#### Known issues

* Reading of XMP data causes a temp file to be created and deleted in the same directory as the WAVE file. This may cause a change to the modification time for the directory, which could cause a problem for some digital preservation schemes.
* Although `autoBWF` strives to write valid XMP, it is only capable of reading XMP generated by `autoBWF`. It makes significant assumptions about the structure of the XMP, and therefore metadata written by other software may not be correctly parsed. However, metadata created within autoBWF is "roundtripable" in and out of autoBWF.
* Quotation marks in text fields are not escaped and will prevent that text from being saved

### `autolame` usage

`autolame [--vbr-level n] <infile> <outfile>`

The default VBR level is currently 7.

### `autosplice` usage

`autosplice <EDL file>`

where `<EDL file>` is a text file that is vaguely reminiscent of an [edit decision list](https://en.wikipedia.org/wiki/Edit_decision_list).

Specifically, the input file consists of any number of lines of the form

`filename.wav <in-time> <out-time>`
 
 which may also optionally contain `fade <in duration> <out duration>` and/or `pad <start padding> <end padding>`. This will append the audio in `filename.wav` from time `<in-time>` to time `<out-time>` (relative to start of the file). All times and durations are in SoX time specification syntax (see the Sox man page for details). The optional `fade` and `pad` parameters add fade in and/or fade out (both values are required: set either to zero if no fade is desired), or padding with silence at beginning and/or end (both values are required: set either to zero if no padding is desired). Padding is added before fade in and after fade out.
 
 The input file must end with a line containing only a filename, and optionally the text `contrast <value>`, but no in or out times. This specifies the name of the output file, as well as any optional Sox "contrast" (a form of audio dynamic range compression).
 
See `autosplice-example.txt` for an example of an `autosplice` input file. 

## Security note
The code here is a wrapper for a number of external command-line programs (`bwfmetaedit`, `lame`, and `sox`). It calls these programs using unsanitized strings passed to the Python `subprocess.call()` function. This is a theorectical security risk: it is conceivable  that a Wave file obtained from an untrusted outside source could result in injection attacks or other nastiness via maliciously-crafted metadata. 

If you are dealing only with Wave files generated within your repository by trusted users, then your risk is virtually nonexistent. For somebody to do something bad to you, they would need to be "out to get you", have technical knowledge of how this code works, and then go out of their way to embed very specially designed malicious metadata in a Wave file that they deliver to you. However, it is likely that such malicious metadata could be easily spotted using a metadata reader such as `exiftool` or `MediaInfo`. If you see anything that doesn't look like it was written by an archivist or librarian, then you should proceed with extreme caution, preferably by deleting the suspicious-looking metadata.