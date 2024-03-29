#!/usr/bin/env python3
# coding: utf-8 -*-

# https://docs.python.org/3.5/library/struct.html#struct.pack
# http://www.zigbee.org/wp-content/uploads/2014/11/docs-09-5264-23-00zi-zigbee-ota-upgrade-cluster-specification.pdf

import sys
from struct import pack,unpack

if (len (sys.argv) > 1):
    f = sys.argv[1]
else:
    #f = "ikea.zigbee"
    #f = "osram.ota"
    #f = "hue.ota"
    #f = "NLF-43.ota"
    #f = "NLC-11.fw"
    #f = "philipsmultiplesegment.zigbee"
    #f = "badikea.ota"
    #f = "MainRemote_00244203.ota"
    #f = "Double-Remote_00084203.ota"
    f = "DimwoNeutral_002E4203.ota"
    #f= "NLC-11.fw"
    #f= "Shutter_00224203.ota"

#Read file
newFile = open(f, "rb")
file = newFile.read()
TotalFileSize = len(file)

print ("File name : " + f)
print ("File size : " + str(TotalFileSize) + " Bytes" )

dec = -1
Search = 0
#Search first usable header
for i in range(len(file)-4):
    if hex(unpack('<I',file[0+i:4+i])[0]) == '0xbeef11e':
        Search += 1
        if Search == 1:
            dec = i
            print ("find start offset : " + str(i) )
            break
        
if dec == -1:
    print ('Bad file format')
    import sys
    sys.exit()

#affichage
print ('\n**** HEADER ***')
print ("Upgrade File identifier : " + hex(unpack('<I',file[0+dec:4+dec])[0]) )
print ("Header version : " + hex(unpack('<H',file[4+dec:6+dec])[0]) )

Header_len = unpack('<H',file[6+dec:8+dec])[0]
print ("Header lenght : " + str(Header_len) )

fc = unpack('<H',file[8+dec:10+dec])[0]
print ("Header field control : " + str(fc) )

print ("Manufacturer code : " + hex(unpack('<H',file[(10+dec):(12+dec)])[0]) )

Image_type = unpack('<H',file[12+dec:14+dec])[0]
if Image_type < 65472:
    Image_type_desc = 'Manufacturer Specific'
elif Image_type == 65472:
    Image_type_desc = 'Client security credential'
elif Image_type == 65473:
    Image_type_desc = 'Client configuration'
elif Image_type == 65474:
    Image_type_desc = 'Server log'
else:
    Image_type_desc = 'Reserved'
print ("Image type : " + hex(Image_type) + ' ' + Image_type_desc )

print ("File version : " + hex(unpack('<I',file[14+dec:18+dec])[0]) + ' > App release:' + str(unpack('<B',file[14+dec:15+dec])[0]) + \
      ' App Build:' + str(unpack('<B',file[15+dec:16+dec])[0]) + ' Stack release:' + str(unpack('<B',file[16+dec:17+dec])[0]) + ' Stack Build:' + str(unpack('<B',file[17+dec:18+dec])[0]))
print ("zigbee stack version: " + hex(unpack('<H',file[18+dec:20+dec])[0]) )
print ("Header string: " + str(unpack('<32s',file[20+dec:52+dec])[0]) )

Image_sizeT = unpack('<I',file[52+dec:56+dec])[0]
print ("Total image size: " + str(Image_sizeT) )

if Header_len > 56:
    #TODO : to finish, and need to use Header field control instead of header lenght
    print ("Security credential Version: " + hex(unpack('<B',file[56+dec:57+dec])[0]) )
    print ("Upgrade file destination: " + str(unpack('<8s',file[57+dec:65+dec])[0]) )
    print ("Minimum Hardware : " + hex(unpack('<H',file[65+dec:67+dec])[0]) )
    print ("Maximum Hardware: " + hex(unpack('<H',file[67+dec:69+dec])[0]) )
else:
    print ("No special headers")

#for i in range(80):
#    print (str(i) + ' > ' + hex(unpack('<H',file[i+dec:i+dec+2])[0]) )

StartingOffsetImage = Header_len + dec

offset = StartingOffsetImage
DataGet = Header_len
Segment = 1

print ('\n***** DATA ***** (Start at offset ' + str(offset) + ')\n')
while offset < TotalFileSize :

    Tag_ID = unpack('<H',file[offset:offset+2])[0]
    Tag_desc = ''
    if Tag_ID == 0:
        Tag_desc = 'Upgrade Image'
    elif Tag_ID == 1:
        Tag_desc = 'ECDSA signature'
    elif Tag_ID == 2:
        Tag_desc = 'ECDSA Signing certificate'
    elif Tag_ID == 3:
        Tag_desc = 'Image integrety code'
    elif Tag_ID < 0xefff :
        Tag_desc = 'Reserved'
    else:
        Tag_desc = 'Reserved'

    print ("Segment " + str(Segment) )
    print ("-------------")
    Segment += 1
    print ("Tag ID : " + hex(Tag_ID) + ' ' + Tag_desc)
    
    field_len = unpack('<I',file[offset+2:offset+6])[0]
    
    if (offset + field_len) >= (Image_sizeT + StartingOffsetImage):
        print ("*** Recalculating lenght, value in TAG too big = " + str(field_len) )
        field_len = TotalFileSize - offset - 6
    else:
        print ("len field : " + str(field_len) + " bytes" )
    
    DataGet += field_len + 6
    
    OffsetS = offset
    OffsetE = offset + 6 + field_len  - 1
    
    #if Tag_ID == 0:
    #    print ("\nFirst data Upgrade image")
    #    print (file[offset + 6:offset + 106] )
    
    #print ("Data : " + hex(unpack('<I',file[offset+6:offset+field_len+6])[0]) )
    
    print("segment offset " + str(OffsetS) + ">" + str(OffsetE) + ' (' + str(OffsetE - OffsetS +1) + ' bytes)')
    if DataGet <= Image_sizeT :
        print("Image percentage " + str( (DataGet * 100)/Image_sizeT ) + '%')
        if DataGet == Image_sizeT:
            print("\n*** IMAGE COMPLETE ***\n")
    
    offset = OffsetE + 1
    
#Check if all data have been read
print ('\n**** END ********')
print ('Unused data : ' + str(TotalFileSize - offset ))

newFile.close()
