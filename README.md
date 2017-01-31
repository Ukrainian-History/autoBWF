#autoBWF

A GUI tool for adding de novo BWF internal metadata to freshly-created WAV files. 

It uses system calls to the FADGI BWFMetaEdit command line under the hood, and is meant to be a replacement for the BWFMetaEdit GUI for initial metadata creation. Unlike BWFMetaEdit, autoBWF is highly opinionated and automatically proposes metadata content based on the file name and system metadata using the conventions of the Ukrainian History and Education Center Archives audio collections. It has a relatively self-explanatory JSON configuration file that can be edited to include pre-set data for audio hardware, software, and copyright statements.

autoBWF will not edit or overwrite existing BWF metadata. Please use the FADGI BWFMetaEdit GUI for that purpose.

The bwfmetaedit "--accept-nopadding" flag is used by default, but can be changed in the configuration file.

This code is not currently usable.

Requires Python 3, PyQt 4.8, and the FADGI BWFMetaEdit CLI. It assumes that "bwfmetaedit" executable is in the current PATH.
