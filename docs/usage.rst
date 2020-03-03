Usage
=======

Opening target file and editing metadata
+++++++++++++++++++++++++++++++++++++++++

Simply type ::

    autoBWF

on the command line, and use the GUI "Open" menu item to load your WAVE file.

Alternatively, you can avoid the "Open" dialog by specifying the target file on the command line::

    autoBWF <target_filename>

autoBWF will prepopulate the Description, Originator, OriginationDate, OriginationTime, and OriginatorRef
GUI elements with reasonable guesses as described below.

If *<target_filename>* already contains embedded metadata, then those values will appear in the GUI as grey italic text.
If the user edits those fields, the text color will change to red as a warning that the original values
will be overwritten in the target file if saved. **Once saved, this cannot be undone!** You can use the drop-down menu
to the right of or below each text element to switch between the original and edited versions prior to saving.

The CodingHistory text is generated automatically based on the selections made in the drop-downs to the right of the
text box and the values in the :ref:`configuration <configuration>` file. Similarly, the Copyright text is replaced
with the boilerplate corresponding to the dropdown menu selection.

.. note::
    You can edit the Copyright and Coding History texts manually prior to saving, but be aware that
    using the drop-down menus will destroy any manual edits that you have made.


Template files
+++++++++++++++++++

autoBWF supports the transfer of metadata embedded in one file (the "template" file) to the target file.
This can be done either by clicking on the "Load Template" button, or by using the optional ``-t`` command line
argument::

    autoBWF <target_filename> -t <template_filename>

This will prepopulate the contents of the Title, Technician, Source, Copyright, Coding History, Archival Location,
and all XMP data fields with the corresponding metadata contained in *template_filename*. These can always be edited
before saving the metadata to the target file. If the target file has existing metadata that conflicts with
the template, then the template value text will be shown in yellow italics. The drop-down menus next to each field
can be used to switch between the existing, template, and edited texts.

Saving metadata
+++++++++++++++++++++++++++++++

When you have entered or modified the data and reviewed it for accuracy, you can save those values to the target file
by clicking on "Save metadata" in the top menu bar. Again, once you click "Save metadata", all changed metadata fields
will be overwritten without any possibility of recovery.

.. note::
    It is strongly recommended that you work with test files and confirm (using BWFMetaEdit and/or a metadata viewer
    like exiftool) that autoBWF is behaving the way that you expect before working with master files.

Exporting metadata and generating access files
++++++++++++++++++++++++++++++++++++++++++++++++++++

You can use the "Export metadata" button to save the currently displayed metadata to a
`PBCore <https://pbcore.org>`_ XML sidecar file. Clicking the button will bring up a window where you can specify
the folder and file name of the PBCore file, and where you can optionally embed existing XML from other software (such
as OHMS) within a PBCore `instantiationExtension <https://pbcore.org/elements/instantiationextension>`_ element. In
addition, it is possible to automatically run `lame` to generate an MP3 access file from the target BWF. Only VBR
encoding is currently supported.

.. note::
    The metadata exported to PBCore correspond to the texts visible in the autoBWF GUI at the time that the "Export
    metadata" button was clicked. Note that if you have edited metadata fields but have not saved the metadata
    to the BWF, then the exported PBCore will **not** match the internal metadata in the BWF.

How does autoBWF generate metadata?
++++++++++++++++++++++++++++++++++++++++

From filenames
-----------------
autoBWF was designed assuming that filenames follow a convention similar to that used by the Indiana University
Archives of Traditional Music as described in the `"Sound Directions" report
<http://www.dlib.indiana.edu/projects/sounddirections/papersPresent/index.shtml>`_. It uses a `regular expression
("regex") <https://www.regular-expressions.info/>`_ to parse the filename and extract components (called
`"capture groups" <https://www.regular-expressions.info/brackets.html>`_) for use in generating the
Description and OriginationDate BWF fields. This regex is specified in the configuration JSON file,
see :ref:`program_behavior`.

Specifically, autoBWF expects that the regex has capture groups for the following three pieces of data:

- an item-level identifier of the physical instantiation corresponding to this digital object in arbitrary format
- a file use indicator
- the date of file creation in hyphenless ISO 8601 format

These data must occur in that order within the filename. The file use indicator is translated into natural language
using the "fileuse" element in the JSON configuration file, see :ref:`program_behavior`.

If autoBWF cannot parse the filename, then it will display a warning, use the OS file creation date and
time to generate OriginationDate, OriginationTime, and OriginatorRef, and will leave Description blank.

If the naming convention at your archives is different enough from the above that it cannot be accomodated by
modification of the regex, then that will require modifications to the Python codebase. If the modifications can be
made without significant rewriting, then you may be able to convince the maintainer of the project into making
changes to accomodate your needs. Please create an "issue" `on GitHub <https://github.com/Ukrainian-History/
autoBWF/issues>`_ that describes your needs (click on the green "New issue" button), and let's talk about it! (Please
note that anything you write in a GitHub issue is visible to the entire Internet, so don't include anything
that you don't want to reveal publicly.) If you want to make substantial local modifications, feel free to fork
the project.


From operating system metadata
--------------------------------

The values of OriginationTime and OriginatorRef are generated by combining
the file creation dates and times obtained from OS metadata together with
default values in ``autobwfconfig.json``. If there is a conflict between the OS metadata date and that in
the filename, then the program will display a warning and will allow you to choose which one you want to use.