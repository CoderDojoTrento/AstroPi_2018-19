import pandas as pd
import math
import matplotlib.pyplot as plt

def convert_decimal(coordinate):
  if coordinate.startswith('-'):
    multiplier = -1
    components = coordinate[1:].split(':')
  else:
    multiplier = 1
    components = coordinate.split(':')
  degrees = int(components[0])
  minutes = int(components[1])
  seconds = float(components[2])
  decimal_coordinate = float("{0:.5f}".format(multiplier * (degrees + (minutes / 60) + (seconds / 3600))))
  return decimal_coordinate


#================================================
# Importa il file CSV con i dati della ISS
#================================================
datafile = 'astroraga_data01.csv'


# Legge una riga alla volta 
reader = pd.read_csv(datafile, chunksize=1)
write_header = True  # Needed to get header for first chunk

i = 0
for chunk in reader:
    #================================================
    # Converte le coordinate in formato decimale
    #================================================
    chunk['lat_dec'] = convert_decimal(chunk.latitudine.item())
    chunk['lon_dec'] = convert_decimal(chunk.longitudine.item())

    #==========================================================================
    # calcola parametri del campo magnetico in base ai valori del magnetometro
    #==========================================================================	

    x=chunk.mag_x.item()
    y=chunk.mag_y.item()
    z=chunk.mag_z.item()
	
    chunk['H'] = math.sqrt(x*x+y*y)
    chunk['F'] = math.sqrt(x*x+y*y+z*z)
    chunk['D'] = math.degrees(math.atan(y/x))
    chunk['I'] = math.degrees(math.atan(z/chunk.H.item()))
    #==========================================================================		
    # ricalcola parametri con fattore di correzione su z = 24
    #==========================================================================	    
    fattore_correttivo = 24
    chunk['z_corretto'] = z-fattore_correttivo
    chunk['F_corretto'] = math.sqrt(x*x+y*y+(z-fattore_correttivo)*(z-fattore_correttivo))
    chunk['I_corretto'] = math.degrees(math.atan((z-fattore_correttivo)/chunk['H'].item()))	

    #aggiunge ID di riga
    i = i + 1
    chunk['ID'] = i

    # Save the file to a csv, appending each new chunk you process. mode='a' means append.
    chunk.to_csv('final.csv', mode='a', header=write_header, index=False)
    write_header = False  # Update so later chunks don't write header


