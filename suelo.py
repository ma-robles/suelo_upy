import time, ds18x20
from machine import Pin, ADC
import onewire

pines = {}
pines['led'] = 13
pines['tmp'] = 15
pines['adc'] = [ 4, 12, 34 ]
print('iniciando...')

led = Pin( pines['led'], Pin.OUT)
led.off()
adc = []
for a in pines['adc']:
    adc.append( ADC(a, atten = ADC.ATTN_11DB ) )
ow = onewire.OneWire(Pin(pines['tmp']))
ow.reset()             

ds = ds18x20.DS18X20(ow)
roms = ds.scan()
print(roms)
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