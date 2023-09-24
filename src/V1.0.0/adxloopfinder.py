import struct
import tkinter as tk
import os
import time
import sys

from struct import unpack
from tkinter import filedialog, StringVar, IntVar
from os import path
from time import sleep
from sys import exit

master = tk.Tk()
master.withdraw()

singleadx_filepath = StringVar()
offsetvalue = IntVar()
start_offsetvalue = IntVar()
end_offsetvalue = IntVar()
offset_hexvalues = StringVar()
printvalue = StringVar()
noloop = IntVar()
looptypeint = IntVar()
startlooppointvalue = StringVar()
endlooppointvalue = StringVar()
looptxtfile = 'bin/resource/txt/looppoints.txt'
currentdir = os.path.join(os.getcwd(), 'bin')

print("ADXLoopFinder by Firebow59")
print("---------------------------")

def findsingleadx():
 print("Searching for adxdir.txt...")
 adxdirfile_path = 'bin/resource/txt/adxdir.txt'
 if os.path.isfile(adxdirfile_path):
  print("adxdir.txt found!")
  print("")
  with open(adxdirfile_path, 'r') as file:
   txtcontents = file.read()
   if txtcontents == '':
    input('No ADX file set in adxdir.txt, unable to continue. Press enter to close the program.')
    return
   else:
    print(f'Found ADX: {txtcontents}')
    singleadx_filepath.set(os.path.join(currentdir + '/' + txtcontents))
    print(singleadx_filepath.get())
 else:
  adxfile = input("adxdir.txt couldn't be found, please input the directory of ADX file (with \(ADX NAME HERE) at the end): ")

def openlooppoints_txt():
 with open(looptxtfile, 'w') as startloopfile:
  pass

def findadxversion_andifloopexists():
 #Check for ADX version
 offsetvalue = 0x12
 with open(singleadx_filepath.get(), 'rb') as singleadx_file:
  singleadx_file.seek(offsetvalue)
  int8_byte = singleadx_file.read(1)
  int8_value = struct.unpack('>B', int8_byte)[0]
 
  global adxversion
  adxversion = int8_value
  printvalue = 'ADX version:'
 if adxversion == 3:
   print(printvalue, int8_value)
 if adxversion == 4:
   print("ADX file is a version 4 file, and currently cannot be downsampled with this program.")
   input("Please press enter to close the program...")
   sys.exit()

 #Check for if loop is enabled
 offsetvalue = 0x16
 with open(singleadx_filepath.get(), 'rb') as singleadx_file:
  singleadx_file.seek(offsetvalue)
  int16_byte = singleadx_file.read(2)
  global int16_value
  int16_value = struct.unpack('>H', int16_byte)[0]
  
 if int16_value == 0:
  noloop.set(1)
  print("")
  print("No loop detected in ADX file, passing loop commands...")
  with open(looptxtfile, 'w') as looptxt:
   pass
  with open(looptxtfile, 'a') as looptxt:
   looptxt.seek(0)
   looptxt.write("0 \n")
   print("0", file=looptxt)
  closeprogram()
 
 if int16_value == 1:
  printvalue = 'Loop:'
  print(printvalue, int16_value)


def setvariables_startlooppoints():
 global offsetvalue, start_offsetvalue, end_offsetvalue, printvalue
 offsetvalue = 0x1C
 start_offsetvalue = 0x1C
 end_offsetvalue = 0x1F
 printvalue = 'Start Loop Value:'

def setvariables_endlooppoints():
 global offsetvalue, start_offsetvalue, end_offsetvalue, printvalue
 offsetvalue = 0x24
 start_offsetvalue = 0x24
 end_offsetvalue = 0x27
 printvalue = 'End Loop Value:'



def findlooppoints_int32():
 if noloop.get() == 1:
  return
 else:
  offset_hexvalues = offsetvalue + end_offsetvalue - start_offsetvalue + 1
  with open(singleadx_filepath.get(), 'rb') as singleadx_file:
   singleadx_file.seek(offsetvalue)
   int32_bytes = singleadx_file.read(offset_hexvalues - offsetvalue)
   global int32_value
   int32_value = struct.unpack('>I', int32_bytes)[0]
   

   global startlooppointvalue
   startlooppointvalue = int32_value

   global endlooppointvalue
   endlooppointvalue = int32_value
   print(printvalue, int32_value)



def writestartlooppoint_tofile():
 if os.path.isfile(looptxtfile):
  with open(looptxtfile, 'r+') as loop_txtfile:
   loop_txtfile.write("")
   with open(looptxtfile, 'r+') as loop_txtfile:
    loop_txtfile.seek(0)
    if noloop.get() == 1:
     print("", file=loop_txtfile)
     loop_txtfile.truncate()
    else:
     print(str(startlooppointvalue), file=loop_txtfile)
     loop_txtfile.truncate()


def writeendlooppoint_tofile():
 if noloop.get() == 1:
  pass
 else:
  with open(looptxtfile, 'a') as loop_txtfile:
   if noloop.get() == 1:
    print("", file=loop_txtfile)
    loop_txtfile.truncate()
   else:
    print(str(endlooppointvalue), file=loop_txtfile)
    loop_txtfile.truncate()


def closeprogram():
 if os.path.isfile('bin/looppoints.txt'):
  os.remove('bin/looppoints.txt') #Remove txt that gets created but not written to in root folder
 time.sleep(1)
 sys.exit()


#Run commands
print("")
findsingleadx()
print("Finding ADX info...")
findadxversion_andifloopexists()

openlooppoints_txt()
setvariables_startlooppoints()
findlooppoints_int32()
writestartlooppoint_tofile()

setvariables_endlooppoints()
findlooppoints_int32()
writeendlooppoint_tofile()

if noloop.get() == 1:
 closeprogram()
 pass
else:
 print("")
 print("Writing loop points to file...")
 print("Done!")
 closeprogram()


master.mainloop()