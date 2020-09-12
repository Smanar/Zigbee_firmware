#!/usr/bin/env python3
# coding: utf-8 -*-

# https://docs.python.org/3.5/library/struct.html#struct.pack
# http://www.zigbee.org/wp-content/uploads/2014/11/docs-09-5264-23-00zi-zigbee-ota-upgrade-cluster-specification.pdf


from struct import pack,unpack

#Open file
#newFile = open("ikea.zigbee", "rb")
#newFile = open("osram.ota", "rb")
#newFile = open("hue.ota", "rb")
newFile = open("NLF-43.ota", "rb")

#Read file
file = newFile.read()

dec = -1
#Search first usable header
for i in range(len(file)-4):
    if hex(unpack('<I',file[0+i:4+i])[0]) == '0xbeef11e':
        dec = i
        print ("\nfind start offset : " + str(i) )
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
    Image_type_desc = 'Manfufacturer Specific'
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

offset = Header_len + dec
print ('\n***** DATA ***** (Start at offset ' + str(offset) + ')\n')
while offset < Image_sizeT + dec - 6:

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
    print ("Tag ID : " + hex(Tag_ID) + ' ' + Tag_desc)
    
    field_len = unpack('<I',file[offset+2:offset+6])[0]
    print ("len field : " + str(field_len) )
    
    if Tag_ID == 0:
        print ("\nFirst data Upgrade image")
        print (file[offset + 6:offset + 106] )
    
    #print ("Data : " + hex(unpack('<I',file[offset+6:offset+field_len+6])[0]) )
    
    print("segment offset " + str(offset) + ">" + str(offset + 6 + field_len))
    print("Remain " + str(Image_sizeT + dec - (offset + 6 + field_len)))
    
    offset += field_len + 6
    
#Check if all data have been read
print ('\n**** END ********')
if Image_sizeT + dec - offset != 0:
    print ('Missing data : ' + str(Image_sizeT + dec - offset))
else:
    print ('All data parsed')

newFile.close()
