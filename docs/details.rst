Configuration
===========================


Program configuration is stored as a JSON file in a directory appropriate to your operating system (e.g. `~/.local/share/autoBWF` on Linux or `/Users/yourname/Library/Application Support/autoBWF` on MacOS).

If the file does not exist, then a "starter" ``autobwfconfig.json`` will be created for you. You should edit this file to customize the values in the dropdown menus and other program behavior to the needs of your repository. In addition, the config file includes the model, serial number, and software version strings that go into constructing the CodingHistory element and copyright boilerplate texts.

The structure of the config file
++++++++++++++++++++++++++++++++++++

The ``--accept-nopadding`` flag is sent to ``bwfmetaedit`` by default, but that behavior can also be changed in the configuration file.

**[TODO: explain in detail how the JSON works]**

How does autoBWF generate metadata?
++++++++++++++++++++++++++++++++++++

From filenames
-----------------
The code assumes that filenames follow a convention similar to that used by the Indiana University Archives of Traditional Music as described in the `"Sound Directions" report <http://www.dlib.indiana.edu/projects/sounddirections/papersPresent/index.shtml>`_. If the naming convention at your archives is different, then you may be able to make things work by modifying the regex string in config.json, or more substantial customization to the Python code may need to be made.

**[TODO: explain what regex capture groups are required]**

If the program cannot parse the filename, then it will display a warning, use the OS file creation date and time to generate OriginationDate, OriginationTime, and OriginatorRef, and will leave Description blank.


From operating system metadata
--------------------------------

The values of Description, Originator, OriginationDate, OriginationTime, and OriginatorRef are prefilled based on parsing the filename and using file creation date and times obtained from OS metadata together with default values in ``autobwfconfig.json``. If there is a conflict between the OS metadata date and that in the filename, then the program will display a warning and will allow you to choose which one you want to use.