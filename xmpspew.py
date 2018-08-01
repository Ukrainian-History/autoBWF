import sys


def main(arguments):
    from libxmp import XMPFiles
    import argparse

    parser = argparse.ArgumentParser(description='spew XMP XML to stdout')
    parser.add_argument('file', help="file")
    args = parser.parse_args(arguments)

    xmpfile = XMPFiles(file_path=args.file, open_forupdate=True)
    xmp = xmpfile.get_xmp()

    print(xmp)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
