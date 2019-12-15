Auxilliary tools
===========================

autosplice
------------

Usage::

    autosplice <EDL file>

where `<EDL file>` is a text file that is vaguely reminiscent of an `edit
decision list <https://en.wikipedia.org/wiki/Edit_decision_list>`_.

Specifically, the EDL file consists of any number of lines of the form ::

    filename.wav <in-time> <out-time>

which may also optionally contain `fade <in duration> <out duration>` and/or
`pad <start padding> <end padding>`. This will append the audio in
`filename.wav` from time `<in-time>` to time `<out-time>` (relative to start
of the file). All times and durations are in SoX time specification syntax
(see the Sox man page for details). The optional `fade` and `pad` parameters add
fade in and/or fade out (both values are required: set either to zero if no fade
is desired), or padding with silence at beginning and/or end (both values are
required: set either to zero if no padding is desired). Padding is added before
fade in and after fade out.

The input file must end with a line containing only a filename, and optionally
the text `contrast <value>`, but no in or out times. This specifies the name of
the output file, as well as any optional SoX "contrast" (a form of audio dynamic
range compression).

Example of an EDL input file::

    file1.wav 02:40+54392s 03:03+26995s fade 0 5
    file1.wav 03:31+26995s 04:35+08823s fade 0 20 pad 1.5 2.5
    file2.wav 14:12+26995s 15:02+08823s fade 15 5
    file3.wav 0 5
    output_file.wav

Security note
+++++++++++++++++

``autosplice`` calls ``sox`` using unsanitized strings passed to the Python
``subprocess.call()`` function with the ``shell=True`` argument. This is a
theorectical security risk, as a maliciously-crafted EDL file obtained from an
untrusted source could result in a shell injection attack. It is mitigated by the
fact that such a malicious file would be easily detectable by simple visual
inspection.

autolame
--------------

Usage::

    autolame [-h] [-o OUTFILE] [--vbr-level VBR_LEVEL] infile [infile ...]

Each `<infile>` will be converted to mp3 and the result will be saved to the same
file name with the extension changed to mp3. Multiple <infile>s can be given, or
generated using a shell glob (e.g. `*.wav`). Selected embedded metadata values from the BWF
files are migrated to ID3v2 tags in the resulting mp3 files.

An output file name can be specified using the ``-o`` option, but in that case
only one input file is allowed.

The default VBR level is currently 7.

bwf2pbcore
------------------

Usage::

    bwf2pbcore [-h] infile [infile ...]

Embeded Wave metadata in each `<infile>` will be extracted and saved as a PBCore XML sidecar file.
The filename of the generated sidecar file will be the same as that of `<infile>` with
"_pbcore" inserted just before the ".xml" extension (i.e. the input file "foobar.wav" will
result in a sidecar file with the name "foobar_pbcore.xml")

`bwf2pbcore` checks for the presence of a file with the same name as the `<infile>`, but with
"_ohms.xml" as a suffix and extension (i.e. for the input file "foobar.wav", it will look for the
file "foobar_ohms.xml"). If such a file is found, it will assume that it contains XML metadata exported from
the Oral History Metadata Synchronizer, and the contents will be inserted into the PBCore XML
within an instantiation-level `<extensionEmbedded>` element.

bwf2csv
------------------

Usage::

    bwf2csv [-h] infile [infile ...]

Selected elements of embeded Wave metadata in each `<infile>` will be extracted and output to `stdout` in CSV format (one line
per Wave file).