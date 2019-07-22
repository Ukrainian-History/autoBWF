.. _configuration:

Configuration
===============

Program configuration is stored as a `JSON <https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects
/JSON>`_ file named ``autobwfconfig.json`` in a directory appropriate to your operating system. If the file does not
exist, then a "starter" file will be created for you. You can find the location of your configuration file by
running::

    autoBWF --config

This file should be edited using the text editing program of your choice in order to reflect your repository's usage.
In particular, you can customize the values in all of the dropdown menus, set the boilerplate copyright
texts, and save the models and serial numbers of your hardware for constructing the BWF CodingHistory element.


Originator and repository information
----------------------------------------

- Set the pre-filled value for the BWF Originator element::

    "originator": "Apocryphal St. U. Archives"


- Set the value of the RIFF IARL element::

    "iarl": "US, Apocryphal State University Archives and Special Colletions"

- Set the repository code used to construct the BWF OriginatorRef element::

    "repocode": "ApoSU"

.. _program_behavior:

Program behavior
-----------------

- Control whether ``bwfmetaedit`` is sent the ``--accept-nopadding`` flag (no if 0, yes otherwise)::

    "accept-nopadding": 1

- Specify the filename format (see below for full usage details)::

    "filenameRegex": ".*_([0-9-]+_[A-Z]{2}\\\d+)_\\\d+_([a-zA-Z]+)_(\\\d+)\\\.wav"

- Control how the file use portion of the file name is translated into a file use statement in the BWF Description::

    "fileuse": {
        "pres": "Preservation Master",
        "presInt": "Preservation Master-Intermediate",
        "prod": "Production Master"
    }

Combo box elements
---------------------

The prefilled values of the autoBWF combo box GUI elements (ISFT, ITCH, ISRC, Copyright owner) are controlled by list
value associated with the appropriate key::

    "isft": [
        "Audacity 2.0.3.0",
        "Audacity 2.3.2"
    ],
    "technician": [
        "Doe, John",
        "Doe, Jane"
    ],
    "source": [
        "Billy Bob Apocryphal papers",
        "Apocryphal University Radio records"
    ],
    "owner": [
        "Apocryphal State University",
        "Big Donor"
    ]

If you want a combo box to be empty be default but still have a set of preconfigured choices in the dropdown, then
make the first element of the list an empty string::

        "technician": [
             "",
             "Doe, John",
             "Doe, Jane"
         ]


Copyright boilerplate
----------------------

The copyright dropdown menu and associated texts are controled by the ``copyright`` key::

    "copyright": {
        "list": ["Generic", "CC-BY-SA"],
        "Generic": "Publication and other forms of distribution (including online sharing and streaming) may be restricted. For details, contact the Apocryphal State University Archives.",
        "CC-BY-SA": "This content is copyright by the Apocryphal State University, and is licenced under Creative Commons BY-SA. See https://creativecommons.org/licenses/by-sa/4.0/ for details."
    }

Within it is the ``list`` key, the corresponding value of which is a list of user-friendly names for the various
copyright choices in the form that they should appear in the dropdown menu. That should be followed by key-value pairs
corresponding to each of those user-friendly names and the corresponding boilerplate text that should be filled in
the text field. For example, we can add a "public domain" menu choice as follows::

    "copyright": {
        "list": ["Generic", "CC-BY-SA", "Public domain"],
        "Generic": "Publication and other forms of distribution (including online sharing and streaming) may be restricted. For details, contact the Apocryphal State University Archives.",
        "CC-BY-SA": "This content is copyright by the Apocryphal State University, and is licenced under Creative Commons BY-SA. See https://creativecommons.org/licenses/by-sa/4.0/ for details.",
        "Public domain": "This content has been placed into the public domain."
    }

CodingHistory constructor menus
--------------------------------

autoBWF constructs the CodingHistory text based on user selections in the dropdown menus to the right of the text
box. The contents of those menus is controlled by the following JSON elements::

    "deck": {
        "list": ["Studer", "Realistic"],
        "Studer": "Studer A810 SN:11223344",
        "Realistic": "Realistic 909A SN:1234321"
    },

    "adc": {
        "list": ["Lynx"],
        "Lynx": "Lynx Aurora 16 SN:897969"
    },

    "software": {
        "list": ["Audacity - Mac", "Audacity - Linux"],
        "Audacity - Mac": "Audacity 2.0.3.0 (Mac)",
        "Audacity - Linux": "Audacity x.x.x. (Linux Ubuntu)"
    },


    "media": [
        "1/4 inch open reel",
        "cassette"
    ],

    "speed": [
        "",
        "7.5 ips",
        "3.25 ips"
    ],

    "eq": [
        "",
        "Dolby B",
        "Dolby C"
    ],

    "type": [
        "",
        "CrO2",
        "Metal"
    ],

Some of these elements have a "list" key similar to the copyright dropdown menu configuration ("deck", "adc",
"software"), while for the remainder the text in the dropdown menu is the same as the text inserted into the
CodingHistory (similar to the combo box configuration).
