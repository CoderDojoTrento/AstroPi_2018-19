##################################################################################
#   ASTROPI 2019 - MISSION "SPACE LAB" : GRUPPO ASTRORAGA (Italy)                #
##################################################################################
# Abstract: Calcola i parametri reali della ISS a partire dal timestamp delle foto
# da TLE (EPHEM) 
###########################################################################


#==========================================================================

##### Import - Librerie ####
from time import sleep,time
from datetime import datetime,timedelta,timezone
import sys
import re
import os
import ephem
import numpy as np
from matplotlib import pyplot as plt
from math import degrees
from mpl_toolkits.basemap import Basemap
from matplotlib.patches import Circle
import urllib.request, json, requests


#==========================================================================

##### Parametri di configurazione #####
FOLDER_IMMAGINI = "foto800x600" # "enviro-pi" # "file_esempio"
NOME_FILE_LISTA = "astroraga_Foto_.*"   # pattern nome file delle immagini per listato folder
NOME_FILE_ASPETTO = "astroraga_Foto_%Y_%m_%d_%H%M%S.%f.jpg"   # pattern nome file delle immagini per parsing timestamp
NOME_FILE_ASPETTO2 = "astroraga_Foto_%Y_%m_%d_%H%M%S"   # pattern nome file delle immagini per parsing timestamp
FONTE = TLE
#FONTE = API

# Vedi: https://www.celestrak.com/NORAD/elements/ per i dati aggiornati;
# https://api.wheretheiss.at/v1/satellites/25544/tles?format=text&timestamp=1524381828.734232
name = "ISS (ZARYA)";          
line1 = "1 25544U 98067A   19096.14813315  .00001499  00000-0  31543-4 0  9994"
line2 = "2 25544  51.6445 359.3289 0002204 153.5880 353.9123 15.52488458164067"

# ISS = ephem.readtle(name, line1, line2)

#==========================================================================

#### Funzioni #####

##----------ottiene la lista dei files di immagini---------
def prendi_lista_immagini(folder):
    aspetto_file = re.compile(NOME_FILE_LISTA)
    return [fn for fn in os.listdir(folder)
              if aspetto_file.match(fn)]

#=============================================================================

##### Programma principale #####        
lista_imgs = prendi_lista_immagini(FOLDER_IMMAGINI)

## disegna planisfero con demarcatore giorno/notte per il 22.04.2018

# miller projection
map = Basemap(projection='mill', lon_0=0, resolution='l')
# plot coastlines, draw label meridians and parallels.
map.drawcoastlines()
map.drawparallels(np.arange(-90,90,15),labels=[1,0,0,0])
map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,30),labels=[0,0,0,1])
# fill continents 'coral' (with zorder=0), color wet areas 'aqua'
map.drawmapboundary(fill_color='aqua')
map.fillcontinents(color='coral',lake_color='aqua')
map.drawcountries()
# shade the night areas, with alpha transparency so the
# map shows through. Use current time in UTC.
date = datetime.strptime("2019-04-05_17-00", "%Y-%m-%d_%H-%M") #datetime.utcnow()
# CS=map.nightshade(date)


sole = ephem.Sun()

progressivo = 0
Longs = []
Lats = []
for file_immagine in lista_imgs[:699]:

    if ( FONTE == "TLE" ): 
        timestamp_img = datetime.strptime(file_immagine, NOME_FILE_ASPETTO)
        timestamp = datetime.strptime(file_immagine, NOME_FILE_ASPETTO).timestamp()
        ISS = ephem.readtle(name, line1, line2)
        ISS.compute(timestamp_img)
        Longs.append(degrees(ISS.sublong))
        Lats.append(degrees(ISS.sublat))
        # altezza del Sole rispetto all'osservatore sotto la ISS
        osservatore = ephem.Observer()
        osservatore.elevation = 0 # sulla Terra, sotto la ISS
        osservatore.lat = ISS.sublat
        osservatore.long = ISS.sublong
        osservatore.date = timestamp_img
        sole.compute(osservatore)
        angolo_sole = degrees(sole.alt)
        #print("%d,%s,%s,%s,%s,%s,%s" % (progressivo,file_immagine,timestamp,degrees(ISS.sublat), degrees(ISS.sublong), ISS.elevation, angolo_sole))
        ISS_lat = degrees(ISS.sublat)
        ISS_lon = degrees(ISS.sublong)
    
        ## diametro vista oblo':400 Km 
        (x,y)=map(ISS_lon,ISS_lat)
        circle = Circle(xy=(x,y),radius=400000/2, fill=False, color='b' if (angolo_sole<0) else 'r')
    if ( FONTE == "API" ):
        timestamp = datetime.strptime(file_immagine[:32], NOME_FILE_ASPETTO2).replace(tzinfo=timezone.utc).timestamp()
        urlrequest = "https://api.wheretheiss.at/v1/satellites/25544/positions?&timestamps=" + str(timestamp)
        with urllib.request.urlopen(urlrequest) as url:
            data = json.loads(url.read().decode())
       
        for x in data:
            timestamp = x["timestamp"]
            ISS_lat = x["latitude"]
            ISS_lon = x["longitude"]
            visibility = x["visibility"]
            angolo_sole = 0
            print("%d,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % (progressivo,file_immagine,x["timestamp"], x["latitude"], x["longitude"],x["altitude"], x["velocity"],x["visibility"],x["footprint"],x["daynum"],x["solar_lat"], x["solar_lon"],x["units"],x["id"],x["name"]))
      
        ## diametro vista oblo':400 Km 
        (x,y)=map(ISS_lon,ISS_lat)
        circle = Circle(xy=(x,y),radius=400000/2, fill=False, color='b' if (visibility=="eclipsed") else 'r')
        
    if ( (progressivo % 1) == 0 ):
        """plt.gca().annotate(progressivo,(x,y-200000),(x,y-220000), ha="center", va="center",
                size=6,
                arrowprops=dict(arrowstyle='->',
                                patchB=circle,
                                shrinkA=5,
                                shrinkB=5,
                                fc="k", ec="k",
                                connectionstyle="arc3,rad=-0.05",
                                ),
                bbox=dict(boxstyle="square", fc="w"))"""
    plt.gca().add_patch(circle)
    progressivo += 1
    
plt.title('Mappa giorno/notte per %s (UTC)' % date.strftime("%d %b %Y %H:%M:%S"))
plt.show()
