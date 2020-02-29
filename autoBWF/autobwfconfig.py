"""
This function is used to generate the default configuration file text.

Yes, it could be stored as data in the package, but that would require a dependency on setuptools, and there's
no need for another package for something this simple.
"""


def default_config():
    default = """\
{
    "accept-nopadding": 1,

    "filenameRegex": ".*_([0-9-]+_[A-Z]{2}\\\d+)_\\\d+_([a-zA-Z]+)_(\\\d+)\\\.wav",

    "originator": "Apocryphal St. U. Archives",

    "iarl": "US, Apocryphal State University Archives and Special Colletions",

    "repocode": "ApoSU",

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

    "isft": [
        "Audacity 2.0.3.0",
        "Audacity x.x.x"
    ],

    "technician": [
        "Doe, John",
        "Doe, Jane"
    ],

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

    "copyright": {
        "list": ["Generic", "CC-BY-SA"],
        "Generic": "Publication and other forms of distribution (including online sharing and streaming) may be restricted. For details, contact the Apocryphal State University Archives.",
        "CC-BY-SA": "This content is copyright by the Apocryphal State University, and is licenced under Creative Commons BY-SA. See https://creativecommons.org/licenses/by-sa/4.0/ for details."
    },

    "source": [
        "Billy Bob Apocryphal papers",
        "Apocryphal University Radio records"
    ],

    "fileuse": {
        "pres": "Preservation Master",
        "presInt": "Preservation Master-Intermediate",
        "prod": "Production Master"
    },

    "owner": [
        "Apocryphal State University",
        "Big Donor"
    ],
    
    "form": [
        "Live sound recordings", 
        "Interviews", 
        "Radio programs", 
        "Oral histories", 
        "Personal recordings", 
        "Field recordings",
        "Poetry readings (Sound recordings)"
    ],
    
    "creator": [
        "",
        "Apocryphal State University",
        "Billy Bob Apocryphal"
    ]
}
"""
    return default
