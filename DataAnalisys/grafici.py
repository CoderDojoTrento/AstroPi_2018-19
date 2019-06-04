###########################################################################
# legge i dati dal file csv e crea un grafico con le variabili specificate
###########################################################################

import pandas as pd
import math
import matplotlib.pyplot as plt

datafile = 'sintesi.CSV'

reader = pd.read_csv(datafile)
write_header = True

ax = plt.gca()

reader.plot(kind='line',x='ID',y='F_vero', label='F da modello', color='red', ax=ax)
reader.plot(kind='line',x='ID',y='F_corretto', label='F calcolato', color='green', ax=ax)

plt.show()

#plt.savefig('output.png')
