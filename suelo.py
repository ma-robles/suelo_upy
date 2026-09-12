import time, ds18x20
from machine import Pin, ADC, I2C, RTC
import onewire
import ds3231

pines = {}
pines['led'] = 13
pines['tmp'] = 15
pines['adc'] = [ 4, ]
print('iniciando...')

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
rtc = RTC()
print(rtc.datetime())

print ('Leyendo reloj:' )
ans = ds3231.get_time(i2c)
print(ans)

print( 'ADC0,Temperatura')
time.sleep(3)

while (True):
    ds.convert_temp()
    time.sleep_ms(750)
    led.on()
    data = []
    for a in adc:
        data.append(a.read_u16())
        
    for rom in roms:
        data.append(ds.read_temp(rom))
    print(','.join(map(str,data) ) )
        
    led.off()
