from machine import SDCard
import os

sdcrd = SDCard( slot =2, freq =1000000)
path_SD = '/sd'
os.mount(sdcrd , path_SD )