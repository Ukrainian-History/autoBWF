from libxmp import XMPFiles, consts

xmpfile = XMPFiles( file_path="blahblah_1999-01_CA66_010101_pres_20161229.wav", open_forupdate=True )
xmp = xmpfile.get_xmp()

print(xmp)
