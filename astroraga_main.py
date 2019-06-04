############################################################################
#                PROGRAMMA  ASTROPI GRUPPO ASTRORAGA                       #
############################################################################
#
# Membri Gruppo ASTRORAGA:
# - Nicola Bortolotti
# - Gael Bouche
# - Thomas Pedretti
# - Andrea Pedrotti
#
#=========================================
# !!!!!!!IMPORTANT NOTE!!!!!!!!!!!!!!
#
# Pease, update TLE DATA. Thanks!
#=========================================
#
#
# Can astronauts orient themselves in space with the compass?
# Can we measure the Earth's magnetic field at 400 km in height?
# Are there variations in magnetic field with the latitude and longitudine?
# We will analyze the values ​​of the magnetometer and at the same time we will collect
# data from the gyroscope and the images of the Earth's surface to see if the ISS has
# rotated with respect to the North during the orbit.
# After every cycle (about 15 sec.) we display the north direction on the senseHat
#
# @ CoderDojo Trento 2019
###########################################################################

from sense_hat import SenseHat
from time import sleep
from datetime import datetime
from datetime import timedelta
import csv
import ephem
import os
from picamera import PiCamera


#********************************************************
# TLE della ISS----Aggiornare per favore
# Latest ISS TLE---Please update TLE
name = "ISS (ZARYA)"
line1 = "1 25544U 98067A   19035.70914902  .00002470  00000-0  45950-4 0  9990"
line2 = "2 25544  51.6436 300.0564 0005072 352.8246  93.8019 15.53235656154673"
#********************************************************
iss = ephem.readtle(name, line1, line2)

sense = SenseHat()

camera = PiCamera()
camera.resolution = (2592,1944)

dir_path = os.path.dirname(os.path.realpath(__file__))

# definisce i colori per l'animazione
# color definition
i=(255,255,255)
o=(0,0,0)

# frecce per animazione bussola su matrice LED
# arrows for compass animation on LED Matrix
freccia1 = [
    o,o,o,i,i,o,o,o,
    o,o,i,i,i,i,o,o,
    o,i,i,i,i,i,i,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    ]
freccia2 = [
    o,o,o,i,i,i,i,i,
    o,o,o,o,o,i,i,i,
    o,o,o,o,i,i,i,i,
    o,o,o,i,i,i,o,i,
    o,o,i,i,i,o,o,i,
    o,i,i,i,o,o,o,o,
    i,i,i,o,o,o,o,o,
    i,i,o,o,o,o,o,o,
    ]
freccia3 = [
    o,o,o,o,o,o,o,o,
    o,o,o,o,o,i,o,o,
    o,o,o,o,o,i,i,o,
    i,i,i,i,i,i,i,i,
    i,i,i,i,i,i,i,i,
    o,o,o,o,o,i,i,o,
    o,o,o,o,o,i,o,o,
    o,o,o,o,o,o,o,o,
    ]
freccia4 = [
    i,i,o,o,o,o,o,o,
    i,i,i,o,o,o,o,o,
    o,i,i,i,o,o,o,o,
    o,o,i,i,i,o,o,i,
    o,o,o,i,i,i,o,i,
    o,o,o,o,i,i,i,i,
    o,o,o,o,o,i,i,i,
    o,o,o,i,i,i,i,i,
    ]
freccia5 = [
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,o,o,i,i,o,o,o,
    o,i,i,i,i,i,i,o,
    o,o,i,i,i,i,o,o,
    o,o,o,i,i,o,o,o,
    ]
freccia6 = [
    o,o,o,o,o,o,i,i,
    o,o,o,o,o,i,i,i,
    o,o,o,o,i,i,i,o,
    i,o,o,i,i,i,o,o,
    i,o,i,i,i,o,o,o,
    i,i,i,i,o,o,o,o,
    i,i,i,o,o,o,o,o,
    i,i,i,i,i,o,o,o,
    ]
freccia7 = [
    o,o,o,o,o,o,o,o,
    o,o,i,o,o,o,o,o,
    o,i,i,o,o,o,o,o,
    i,i,i,i,i,i,i,i,
    i,i,i,i,i,i,i,i,
    o,i,i,o,o,o,o,o,
    o,o,i,o,o,o,o,o,
    o,o,o,o,o,o,o,o,
    ]
freccia8 = [
    i,i,i,i,i,o,o,o,
    i,i,i,o,o,o,o,o,
    i,i,i,i,o,o,o,o,
    i,o,i,i,i,o,o,o,
    i,o,o,i,i,i,o,o,
    o,o,o,o,i,i,i,o,
    o,o,o,o,o,i,i,i,
    o,o,o,o,o,o,i,i,
    ]

# scrive la riga di intestazione del file dati CSV
# Creating data file and writing the first row

with open(dir_path+"/data01.csv", mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(['data_ora','latitudine','longitudine','mag_x','mag_y','mag_z','nord','accel_x','accel_y','accel_z','accel_pitch','accel_roll','accel_yaw','gyro_x','gyro_y','gyro_z','gyro_pitch','gyro_roll','gyro_yaw','pitch','roll','yaw','temperatura','temperatura2','pressione','umidita'])
csv_file.close()

# inizio dell'esperimento
# start of experiment

inizio = datetime.now()
print(str(inizio)+ " - INIZIO Esperimento")
sense.show_message("3 2 1 GO!")

# ciclo di 178 minuti: legge sensori, scrittura file e animazione
# loop 178 minutes: sensors reading, data file writing, LED animation

while (datetime.now() < inizio + timedelta(minutes=178)):

  try:
      # ---------- Lettura sensori ---------------
      # ---------- Sensors reading ---------------

      #legge i sensori della IMU velocemente per 60 volte per avere un valore accurato
      #read IMU's sensors 60 times with high frequency to get accurate values
      nletture = 0
      while nletture < 60:
        mag = sense.get_compass_raw()
        nord = sense.get_compass()
        accelraw = sense.get_accelerometer_raw()
        accel = sense.get_accelerometer()
        gyroraw = sense.get_gyroscope_raw()
        gyro = sense.get_gyroscope()
        ori = sense.get_orientation()
        nletture = nletture + 1

      # lettura sensori
      # sensors'values reading
      mag_x = mag['x']
      mag_y = mag['y']
      mag_z = mag['z']

      accel_x = accelraw['x']
      accel_y = accelraw['y']
      accel_z = accelraw['z']
      accel_pitch = accel['pitch']
      accel_roll = accel['roll']
      accel_yaw = accel['yaw']

      gyro_x = gyroraw['x']
      gyro_y = gyroraw['y']
      gyro_z = gyroraw['z']
      gyro_pitch = gyro['pitch']
      gyro_roll = gyro['roll']
      gyro_yaw = gyro['yaw']

      pitch = ori['pitch']
      roll = ori['roll']
      yaw = ori['yaw']

      temperatura = sense.get_temperature()
      temperatura2 = sense.get_temperature_from_humidity()
      pressione = sense.get_pressure()
      umidita = sense.get_humidity()

      print(str(datetime.now()) + " - lettura sensori")

  except:
    print(str(datetime.now()) + " - Eccezione lettura sensori")

  # ---------- Calcola la posizione della ISS               ---------------
  # ---------- Take picture                     ---------------
  # calcoliamo la posizione in questo momento
  try:
    iss.compute()
    print(str(datetime.now()) + " - calcolo posizione ISS")
  except:
    print(str(datetime.now()) + " - Errore calcolo posizione ISS")

  ora = str(datetime.now()).replace(' ', '_')

  # ---------- Scatta fotografia      -------------------------
  # ---------- Taking picture         -------------------------
  try:
      camera.start_preview()
      sleep(2)
      camera.stop_preview()
      camera.capture(dir_path+"/Foto_%s.jpg" % ora)
      print(str(datetime.now()) + " - foto")

  except:

      print(str(datetime.now()) + " - Eccezione scatto foto")

  # ---------- Scrive dati nel file                ---------------
  # ---------- Appending sensors value to datafile ---------------
  try:
      with open(dir_path+"/data01.csv", mode='a') as csv_file:
          writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
          writer.writerow([ora,iss.sublat,iss.sublong,mag_x,mag_y,mag_z,nord,accel_x,accel_y,accel_z,accel_pitch,accel_roll,accel_yaw,gyro_x,gyro_y,gyro_z,gyro_pitch,gyro_roll,gyro_yaw,pitch,roll,yaw,temperatura,temperatura2,pressione,umidita])
      csv_file.close()
      print(str(datetime.now()) + " - scrittura file")
  except:
    print(str(datetime.now()) + " - Eccezione scrittura file")

  # ---------- Animazione matrice LED             ---------------
  # ---------- LED Matrix Animation               ---------------

  try:
      # rotazione dell'ago della bussola
      # compass arrow rotation
      print(str(datetime.now()) + " - Animazione")

      a=1

      while a<3:
        sense.set_pixels(freccia1)
        sleep(0.1)
        sense.set_pixels(freccia2)
        sleep(0.1)
        sense.set_pixels(freccia3)
        sleep(0.1)
        sense.set_pixels(freccia4)
        sleep(0.1)
        sense.set_pixels(freccia5)
        sleep(0.1)
        sense.set_pixels(freccia6)
        sleep(0.1)
        sense.set_pixels(freccia7)
        sleep(0.1)
        sense.set_pixels(freccia8)
        sleep(0.1)
        a=a+1

      # posiziona la freccia in base al Nord
      # reading nord value and set compass

      if (nord >= 340 or nord <= 22 ):
             sense.set_pixels(freccia1)
      elif (nord <= 67):
             sense.set_pixels(freccia2)
      elif (nord <= 112):
             sense.set_pixels(freccia3)
      elif (nord <= 157):
             sense.set_pixels(freccia4)
      elif (nord <= 202):
             sense.set_pixels(freccia5)
      elif (nord <= 247):
             sense.set_pixels(freccia6)
      elif (nord <= 292):
             sense.set_pixels(freccia7)
      elif (nord <= 339):
             sense.set_pixels(freccia8)

  except:
    print(str(datetime.now()) + " - Eccezione animazione")

  # aspetta 3 secondi -> totale 15s(7IMU+3FOTO+2ANIM+3SLEEP)
  # sleep 3 seconds -> total 15s(7IMU+3PHOTO+2ANIM+3SLEEP)

  sleep(3)

print(str(datetime.now()) + " - FINE Esperimento")
sense.show_message("bye bye - Astroraga (Codedojo Trento)", scroll_speed=0.05)
