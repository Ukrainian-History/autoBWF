autosplice and autolame
===========================

autosplice
------------

Usage::

    autosplice <EDL file>

where `<EDL file>` is a text file that is vaguely reminiscent of an `edit decision list <https://en.wikipedia.org/wiki/Edit_decision_list>`_.

Specifically, the EDL file consists of any number of lines of the form ::

    filename.wav <in-time> <out-time>

which may also optionally contain `fade <in duration> <out duration>` and/or `pad <start padding> <end padding>`. This will append the audio in `filename.wav` from time `<in-time>` to time `<out-time>` (relative to start of the file). All times and durations are in SoX time specification syntax (see the Sox man page for details). The optional `fade` and `pad` parameters add fade in and/or fade out (both values are required: set either to zero if no fade is desired), or padding with silence at beginning and/or end (both values are required: set either to zero if no padding is desired). Padding is added before fade in and after fade out.

The input file must end with a line containing only a filename, and optionally the text `contrast <value>`, but no in or out times. This specifies the name of the output file, as well as any optional SoX "contrast" (a form of audio dynamic range compression).

Example of an EDL input file::

    file1.wav 02:40+54392s 03:03+26995s fade 0 5
    file1.wav 03:31+26995s 04:35+08823s fade 0 20 pad 1.5 2.5
    file2.wav 14:12+26995s 15:02+08823s fade 15 5
    file3.wav 0 5
    output_file.wav

Security note
+++++++++++++++++

``autosplice`` calls ``sox`` using unsanitized strings passed to the Python ``subprocess.call()`` function with the ``shell=True`` argument set. This is a theorectical security risk, as a maliciously-crafted EDL file obtained from an untrusted source could result in a shell injection attack. It is mitigated by the fact that such a malicious file should be easily recognizable by simple visual inspection.

autolame
--------------

Usage::

    autolame [-h] [-o OUTFILE] [--vbr-level VBR_LEVEL] infile [infile ...]

Each `<infile>` will be converted to mp3 and the result will be saved to the same file name with the extension changed to mp3. Multiple <infile>s can be given, or generated using a shell glob (e.g. `*.wav`)

An output file name can be specified using the ``-o`` option, but in that case only one input file is allowed.

The default VBR level is currently 7.