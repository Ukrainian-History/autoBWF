Usage
=======

Simply type ::

    autoBWF

on the command line, and use the GUI "Open" menu item to load your WAVE file.

Alternatively, you can avoid the "Open" dialog by specifying the target file and (optional) template file on the command line::

    autoBWF <target_filename> [-t <template_filename>]

``autoBWF`` will prepopulate the Description, Originator, OriginationDate, OriginationTime, and OriginatorRef GUI elements with reasonable guesses as described below.

If *target_filename* already contains BWF metadata, then those values will appear in the GUI in grey italic text. If the user edits those fields, the text color will change to red as a warning that "Save metadata" will cause those the values will be overwritten in the target file. **This cannot be undone!**

The CodingHistory text is generated automatically based on the selections made in the drop-downs to the right of the text box and the values in the configuration file (see below). You can also edit the text manually, but be aware that using the drop-down menus will undo any manual edits that you have made. Similarly, the Copyright text is replaced with the boilerplate corresponding to the dropdown menu selection. The same caveat regarding manual editing holds here as well.

Loading a template file (either using the "Load Template" button or using the ``-t`` command line argument) will prepopulate the contents of the Title, Technician, Source, Copyright, Coding History, and any XMP text fields with the corresponding metadata contained in *template_filename*. These can always be edited before saving the metadata to the target file. Note that if the target file already has metadata in the same fields as the template, then this could result in the overwriting of data. `This issue <https://github.com/Ukrainian-History/autoBWF/issues/2>`_ will be resolved in a future version.

It is strongly recommended that you work with test files and confirm (using BWFMetaEdit and/or a metadata viewer like ``exiftool``) that ``autoBWF`` is behaving the way that you expect before working with master files.
