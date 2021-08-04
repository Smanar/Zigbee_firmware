# Zigbee_firmware

Python tool in command line to retreive information for a Zigbee Firmware. It give somes informations on firmware file.   
```
J:\test>python read.py ikea.zigbee
```

Result:   

```
File name : ikea.zigbee
File size : 174150 Bytes
find start offset : 392

**** HEADER ***
Upgrade File identifier : 0xbeef11e
Header version : 0x100
Header lenght : 56
Header field control : 0
Manufacturer code : 0x117c
Image type : 0x2202 Manfufacturer Specific
File version : 0x12217572 > App release:114 App Build:117 Stack release:33 Stack Build:18
zigbee stack version: 0x2
Header string: b'EBL tradfri_light_1000ml\x00\x00\x00\x00\x00\x00\x00\x00'
Total image size: 173246
No special headers

***** DATA ***** (Start at offset 448)

Segment 1
-------------
Tag ID : 0x0 Upgrade Image
len field : 173184 bytes
segment offset 448>173637 (173190 bytes)
Image percentage 100.0%

*** IMAGE COMPLETE ***

Segment 2
-------------
Tag ID : 0xdd64 Reserved
*** Recalculating lenght, value in TAG too big = 3927358301
segment offset 173638>174149 (512 bytes)

**** END ********
Unused data : 0
```   

