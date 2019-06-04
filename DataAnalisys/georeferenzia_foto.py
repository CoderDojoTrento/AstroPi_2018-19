###########################################################################
# legge i dati dal file csv e inserisce le coordinate nei dati EXIF
# struttura del file csv:
# name,lat_g,lat_m,lat_s,lat_d,lon_g,lon_m,lon_s,lon_d
# Foto_2019_04_05_161628.099668.jpg,29,21,20,N,49,40,58,W
# Foto_2019_04_05_161643.429154.jpg,30,2,7,N,48,56,48,W
# Foto_2019_04_05_161658.600762.jpg,30,42,36,N,48,11,59,W
###########################################################################

import tempfile
import os
import sys
import re
from fractions import Fraction

log_file = "log.csv"

csv = open(log_file, 'r')
count = 0
images = []
for line in csv.readlines():
        count += 1
        if count == 1:
            continue
        image, lat_g, lat_m, lat_s, lat_d, lon_g, lon_m, lon_s, lon_d = line.split(',')
        os.system('exiv2 -M"set Exif.GPSInfo.GPSLatitude {deglat}/1 {minslat}/1 {secfraclat}/1"'
                  ' -M"set Exif.GPSInfo.GPSLatitudeRef {reflat}" {image}'.format(deglat=lat_g, minslat=lat_m, secfraclat=int(lat_s),reflat=lat_d, image="astroraga_"+image))

        os.system('exiv2 -M"set Exif.GPSInfo.GPSLongitude {deglon}/1 {minslon}/1 {secfraclon}/1"'
                  ' -M"set Exif.GPSInfo.GPSLongitudeRef {reflon}" {image}'.format(deglon=lon_g, minslon=lon_m, secfraclon=int(lon_s),reflon=lon_d, image="astroraga_"+image))
        print('exiv2 -M"set Exif.GPSInfo.GPSLatitude {deglat}/1 {minslat}/1 {secfraclat}/1"'
             ' -M"set Exif.GPSInfo.GPSLatitudeRef {reflat}" {image}'.format(deglat=lat_g, minslat=lat_m, secfraclat=lat_s,reflat=lat_d, image="astroraga_"+image))
