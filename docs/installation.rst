Installation
================

Prerequisites
++++++++++++++

Python 3
------------

This code requires Python 3.6 or later. If you are running on Linux or Mac OS,
then it is almost certainly already installed. If you are running on Widows,
you can install Python using instructions on any number of web
sites (such as `this one
<https://www.digitalocean.com/community/tutorials/how-to-install-
python-3-and-set-up-a-local-programming-environment-on-windows-10>`_).

You may wish to configure a `virtual environment
<https://docs.python-guide.org/dev/virtualenvs/>`_ within which to install and
run ``autoBWF``.

bwfmetaedit
----------------------------
If needed, download and run the installer for the `BWFMetaEdit
<https://mediaarea.net/BWFMetaEdit>`_ CLI (Command Line Interface) appropriate
to your operating system from `mediaarea.net <https://mediaarea
.net/BWFMetaEdit/Download>`_. Note that having the BWFMetaEdit GUI
installed is not sufficient.

``autoBWF`` has been tested with ``bwfmetaedit`` v1.3.3 and v1.3.8. Note that
earlier versions of ``bwfmetaedit`` have a bug that introduces spurious characters
at the end of the ``CodingHistory`` element. This bug has been confirmed to exist
in v1.3.1.1, and it may affect other versions prior to v1.3.3.

Optional software
----------------------

In order to run ``autolame`` and ``autosplice``, you will also need to install
`lame <http://lame.sourceforge.net/>`_ (for ``autolame``) and `SoX <http://sox
.sourceforge.net/>`_ v14.4.2 (for ``autosplice``).

Note that some LINUX package repositories (e.g. Ubuntu 16.04) have an earlier
version of ``SoX`` that seems to have problems with time specifications, so you
may need to install from source. If you are doing so on Ubuntu, you may need to
run ``sudo ldconfig`` after installation if you get a ``sox: error while loading
shared libraries: libsox.so.3: cannot open shared object file: No such file or
directory`` error.

Installing autoBWF
+++++++++++++++++++++++++

The latest release of ``autoBWF`` is available on PyPI and can be installed using ::

    pip3 install autoBWF

The "bleeding edge" version is in the master branch `on github <https://github
.com/Ukrainian-History/autoBWF>`_, and can be installed by cloning the repository
and installing the local code with ``pip3``, or by running ::

    pip3 install git+git://github.com/Ukrainian-History/autoBWF.git#egg=autoBWF

The master branch *should* contain functional code — development work that is likely
to result in a broken state is done on feature branches.
