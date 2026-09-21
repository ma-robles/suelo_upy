import time, ds18x20
from machine import Pin, ADC, I2C, RTC, SDCard, reset
import onewire
import ds3231
import os
from info import *

pines = {}
pines['led'] = 13
pines['tmp'] = 15
pines['adc'] = [ 4, ]
print('iniciando... ID= ', ID )

led = Pin( pines['led'], Pin.OUT)
led.off()
adc = []

print('Inicializando canales analógicos')
for a in pines['adc']:
    adc.append( ADC(a, atten = ADC.ATTN_11DB ) )

print('Inicializando sensor de temperatura')
ow = onewire.OneWire(Pin(pines['tmp']))
ow.reset()             
ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print(roms)

print('Inicializando I2C')
i2c = I2C(0, scl=Pin(22, Pin.OPEN_DRAIN, Pin.PULL_UP),
              sda=Pin(21, Pin.OPEN_DRAIN, Pin.PULL_UP), freq=100000)
print('i2c:', i2c.scan() )

# remove week day from date (index 3)
def rm_wday(date):
    return date[:3]+date[4:7]

# date tuple to str
def dt2str(date):
    date = rm_wday(date)
    return '{}/{:02d}/{:02d} {:02d}:{:02d}:{:02d}'.format(*date)

rtc = RTC()
# rtc (year, month, day, weekday, hours, minutes, seconds, subseconds)
time_rtc = rtc.datetime()

# ds3231 YY, MM, DD, wday, hh, mm, ss, 0
time_ds3231 = ds3231.get_time(i2c)
#time_ds3231 = time_ds3231[0:3] + time_ds3231[4:] + tuple([0])
print(
      'rtc:', time_rtc, )
print(
      'ds3231:', time_ds3231,)

print( time_rtc > time_ds3231,
      )

# comparing dates
if (rm_wday(time_rtc) > rm_wday(time_ds3231) ):
    print('Updating DS3231')
    ds3231.set_time(i2c, )
else:
    print('Updating RTC')
    rtc.datetime( time_ds3231 )

print('RTC', rtc.datetime() )
print('DS3231', ds3231.get_time(i2c) )

print('Inicializando tarjeta de memoria')
try:
    sdcrd = SDCard( slot =2, freq =1000000)
except:
    reset()
path_SD = '/sd'

print( 'ID,ADC0,Temperatura')
time.sleep(3)

time_msample = (time_sample * 60 *1000) - 750
while (True):
    ds.convert_temp()
    time.sleep_ms(750)
    led.on()
    now = rtc.datetime()
    date = dt2str( now ) + ','
    data = []
    for a in adc:
        data.append(a.read_u16())
        
    for rom in roms:
        data.append(ds.read_temp(rom))
    msg = ID + date
    msg += ','.join(map(str,data) ) 

    print( msg )
    filename = path_SD + '/data_{}_{}{:02d}{:02d}.csv'.format( ID, *now)
    print('guardando en', filename)
    try:
        os.mount(sdcrd , path_SD )
    except Exception as  e:
        print('Fallo al montar SD')
        print(e)
    try:
        with open( filename, 'a') as file:
            file.write(msg +'\n')
    except:
        print('fallo al guardar datos')

    try:
        os.umount( path_SD ) 
        print('datos almacenados correctamente')
    except:
        print('fallo al desmontar SD')
        
    led.off()
    time.sleep_ms(time_msample)
