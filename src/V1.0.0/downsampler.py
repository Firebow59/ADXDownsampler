"""
ADX HEADER INFO: https://en.wikipedia.org/wiki/ADX_(file_format)#Technical_description
ADXdownsampler script/GUI and ADXLoopFinder developed by Firebow59 (https://github.com/Firebow59)

ADXDownsampler version: V1.0.0
"""

import struct
import tkinter as tk
import os
import sys
import shutil
import subprocess

from struct import unpack
from tkinter import filedialog, StringVar, IntVar
from os import path
from sys import exit
from shutil import copy
from subprocess import run


master = tk.Tk()
master.withdraw()


currentdir = os.path.join(os.getcwd(), 'bin')
batchconvert = IntVar()
adxdirfile_path = 'bin/resource/txt/adxdir.txt'
selected_adx_file = StringVar()
cleanbinfolder = IntVar()

soxlocation = os.path.join(currentdir, 'resource', 'sox', 'sox.exe')
soxpath = os.path.join(currentdir, 'resource', 'sox')
wavconvert_rootdir = os.path.join(currentdir, 'wav.wav')
looppoints_file = currentdir + '/resource/txt/looppoints.txt'



def getadx():
 global adxfile
 with open(adxdirfile_path, 'r') as adxdirfile:
  global adxdir_txtcontent
  adxdir_txtcontent = adxdirfile.read().strip()
  if adxdir_txtcontent == 'BATCH':
   batchconvert.set(1)
   print('--Batch Mode Enabled--')
   singleadx_nodir = os.path.basename(adxdir_txtcontent)
   selected_adx_file.set(singleadx_nodir)
   batch_convert_runloop()
  else:
   singleadx_nodir = os.path.basename(adxdir_txtcontent)
   adxfile_location = os.path.join(currentdir + '/' + singleadx_nodir)
   selected_adx_file.set(adxfile_location)

  if adxdir_txtcontent == '':
   print("ADX file does not exist, closing script...")
   closeprogram()



readline = IntVar()
readline = 0
batchmode = IntVar()
def batch_convert_runloop():
 global readline
 global batchmode
 readline += 1
 if readline == 1:
  print("") #Space between program title and "Processing file" text
 if batchconvert.get() == 1:
  batchmode.set(1)
  if os.path.isfile(selected_adx_file.get()):
   os.remove(selected_adx_file.get())

  batchfilelist_txt = 'bin/resource/txt/batch_adxfiles-tempfolder.txt'
  with open(batchfilelist_txt, 'r') as filelist:
   lines = filelist.readlines()
   if readline >= len(lines):
    closeprogram()
   else:
    if 0 <= readline < len(lines):
     currentline = lines[readline].strip()
     adx_filename_nodir = os.path.basename(currentline)
     shutil.copy(currentline, currentdir)
     adxfile_rootbinfolder = os.path.join(currentdir + '/' + adx_filename_nodir)
     selected_adx_file.set(adxfile_rootbinfolder)
     print(f"Processing file: {adx_filename_nodir}")

     with open(adxdirfile_path, 'w') as adxdirfile:
      adxdirfile.write(adx_filename_nodir)

     #Clean files to prevent errors
     if os.path.isfile(currentdir + '/downsampled.wav'):
      os.remove(currentdir + '/downsampled.wav')
     if os.path.isfile(wavconvert_rootdir):
      os.remove(wavconvert_rootdir)
     if os.path.isfile(currentdir + '/downsampled.adx'):
      os.remove(currentdir + '/downsampled.adx')
     
     adxcommands()
 else:
  pass
 


print("ADXDownsampler V1.0.0")
def adxcommands():
 samplerate = StringVar()
 audiobitrate = StringVar()
 channeltype = StringVar()

 def findadxloops():
  if batchmode.get() == 1:
   pass
  else:
   print("")
   print('Finding ADX loop points...')
  adxloopfinderprogram = currentdir + '/adxloopfinder.exe'
  #subprocess.run(adxloopfinderprogram, stderr=subprocess.STDOUT, shell=True)
  adxloopfinderprogram_cmd = subprocess.run(adxloopfinderprogram, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


 def get_GUI_values():
  sampleratetxt_path = 'bin/resource/txt/output_samplerate.txt'
  with open(sampleratetxt_path, 'r') as sampleratetxt:
    samplerate.set(sampleratetxt.read().strip())

  audiobitratetxt_path = 'bin/resource/txt/output_audiobitrate.txt'
  with open(audiobitratetxt_path, 'r') as audiobitratetxt:
    audiobitrate.set(audiobitratetxt.read().strip())

  channeltypetxt_path = 'bin/resource/txt/output_channeltype.txt'
  with open(channeltypetxt_path, 'r') as channeltypetxt:
   channeltype.set(channeltypetxt.read().strip())



 def convertadx_to_WAV():
  global vgmstreamlocation
  vgmstreamlocation = os.path.join(currentdir, 'resource', 'vgmstream-win64', 'vgmstream-cli.exe')
  
  if batchmode.get() == 1:
   pass
  else:
   print("Converting ADX to WAV...")

  if os.path.isfile(selected_adx_file.get()):
   pass
  else:
   print("ADX file not found in folder, please try again.")
   sys.exit()
  
  converttoWAV_fixlength = f'{vgmstreamlocation} {selected_adx_file.get()} -f 0.0 -l 1 -o wav.wav'
  converttoWAV_fixlength_cmd = subprocess.run(converttoWAV_fixlength, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True) 
  
  if os.path.isfile(wavconvert_rootdir):
   os.remove(wavconvert_rootdir)
  shutil.move('wav.wav', currentdir)

 def findorigadx_samplerate():
  if batchmode.get() == 1:
   pass
  else:
   print("Finding original ADX's sample rate...")
  
  offsetvalue = 0x08
  end_offsetvalue = 0x0B
  offset_hexvalues = offsetvalue + end_offsetvalue - offsetvalue + 1
  with open(selected_adx_file.get(), 'rb') as singleadx_file:
   singleadx_file.seek(offsetvalue)
   int32_bytes = singleadx_file.read(offset_hexvalues - offsetvalue)
   global origadx_samplerate
   origadx_samplerate = IntVar()
   origadx_samplerate = struct.unpack('>I', int32_bytes)[0]
   
   if int(samplerate.get()) > origadx_samplerate:
    input("Error: Output sample rate cannot be greater than that of the original file, please press any key to exit the program...")
    sys.exit()



 def get_original_looppoints():
  if batchmode.get() == 1:
   pass
  else:
   print("Getting original ADX's loop points...")
  
  global startloopvalue
  global endloopvalue
  global loopexists
  startloopvalue = IntVar()
  endloopvalue = IntVar()

  loopexists = IntVar()
  loopexists.set(1)
  linenumbers = [1, 2]
  with open(looppoints_file, 'r') as looppoints_txtfile:
   lines = looppoints_txtfile.readlines()
   if len(lines) == 0 or len(lines) > max(linenumbers):
    print("No ADX loop points in looppoints.txt, output ADX will NOT be looped.")
    loopexists.set(0)
    converttoadx()
   else:
    startloopvalue = lines[linenumbers[0] - 1].strip()
    endloopvalue = lines[linenumbers[1] - 1].strip()



 def find_and_convert_newlooppoints():
  global downsamplingfactor
  global startloopvalue
  global endloopvalue

  if batchmode.get() == 1:
   pass
  else:
   print("Finding new downsampled loop points...")

  outputsamplerate = float(samplerate.get())
  downsamplingfactor = float(origadx_samplerate) / outputsamplerate

  #Convert loop points to work with new sample rate
  global new_startloopvalue
  global new_endloopvalue
  startloopvalue = float(startloopvalue)
  downsamplingfactor = float(downsamplingfactor)
  new_startloopvalue = startloopvalue / downsamplingfactor

  endloopvalue = float(endloopvalue)
  downsamplingfactor = float(downsamplingfactor)
  new_endloopvalue = endloopvalue / downsamplingfactor



 def converttoadx():
  if batchmode.get() == 1:
   pass
  else:
   print("Downsampling WAV...")
  downsampledADX_file = os.path.join(currentdir, 'downsampled.adx')
  
  downsampleWAV = f'{soxlocation} {wavconvert_rootdir} --rate {samplerate.get()} --channels {channeltype.get()} --compression {audiobitrate.get()} downsampled.wav'
  downsampledWAV_cmd = subprocess.run(downsampleWAV, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  
  downsampledWAV_filepath = os.path.join(currentdir + '/downsampled.adx')
  if os.path.isfile(downsampledWAV_filepath):
   os.remove(downsampledWAV_filepath)
  shutil.move('downsampled.wav', currentdir) #Fix for file appear outside of bin folder


  sourceWAV = os.path.join(currentdir + '/downsampled.wav')
  findtotalsamples_WAV = f'{soxlocation} --info -s {sourceWAV}'
  findtotalsamples_WAV_cmd = subprocess.run(findtotalsamples_WAV, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  #totalWAVsamples = findtotalsamples_WAV_cmd
  #print(f'Total WAV Samples: {totalWAVsamples.stdout.strip()}')

  if os.path.isfile(downsampledADX_file):
   os.remove(downsampledADX_file)


  if batchmode.get() == 1:
   pass
  else:
   print("Converting back to ADX...")
  adxencd_program = os.path.join(currentdir + '/adxencd.exe')
  if loopexists.get() == 0:
   adxencoder=f'{adxencd_program} {sourceWAV} downsampled.adx'
  else:
   adxencoder=f'{adxencd_program} {sourceWAV} -lps{new_startloopvalue} -lpe{new_endloopvalue} downsampled.adx'
  adxencodercmd = subprocess.run(adxencoder, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
  if os.path.isfile('downsampled.adx'):
   shutil.move('downsampled.adx', currentdir) #Fix for file appearing outside of bin folder


  adxfile_noextension = os.path.splitext(selected_adx_file.get())[0]
  outputadxname = os.path.join(currentdir, adxfile_noextension + '-downsampled' + '.adx')
  outputadxname_nodir = os.path.basename(outputadxname)
  downsampledfolder_adxfile = os.path.join(currentdir + '/downsampled_ADX' + '/' + outputadxname_nodir)
  
  def askoverwrite():
   if os.path.isfile(downsampledfolder_adxfile):
    overwrite_existing_downsampled = input("File already exists in downsampled folder, overwrite it? Enter either 'y' or 'n': ")
    if overwrite_existing_downsampled == 'y' or overwrite_existing_downsampled == 'Y':
     os.remove(downsampledfolder_adxfile)
    elif overwrite_existing_downsampled == 'n' or overwrite_existing_downsampled == 'N':
     os.remove(downsampledADX_file)
    else:
     print("Incorrect value entered, please try again...")
     askoverwrite()
     return
  askoverwrite()


  if os.path.isfile(downsampledADX_file):
   os.rename(downsampledADX_file, outputadxname)


  if batchconvert.get() == 1:
   downsampled_dir = os.path.join(currentdir + '/downsampled_ADX')
   if not os.path.exists(downsampled_dir):
    os.mkdir(downsampled_dir)
   batch_convert_runloop()
  else:
   closeprogram()


 global closeprogram
 def closeprogram():
  downsampled_folder = os.path.join(currentdir + '\downsampled_ADX')

  with open('bin/resource/txt/openfolder.txt', 'r') as openfoldertxt:
   lines = openfoldertxt.readlines()
   if len(lines) == 1:
    openfolder = subprocess.run(['explorer', downsampled_folder], shell=True)


  #Remove old files
  downsampledWAV_file = os.path.join(currentdir, 'downsampled.wav')
  if os.path.isfile(downsampledWAV_file):
   os.remove(downsampledWAV_file)
  if os.path.isfile(wavconvert_rootdir):
   os.remove(wavconvert_rootdir)
  if os.path.isfile(selected_adx_file.get()):
   os.remove(selected_adx_file.get())
  if os.path.isfile(wavconvert_rootdir):
   os.remove(wavconvert_rootdir)


  #Reset batch txt files
  batchfilelist_txt = 'bin/resource/txt/batch_adxfiles-tempfolder.txt'
  with open(batchfilelist_txt, "w") as batchfile_tempfolder_txt:
   pass
  with open('bin/resource/txt/batch_adxfiles-origlocation.txt', "w") as batchfile_origfolder_txt:
   pass
  with open('bin/resource/txt/openfolder.txt', "w") as openfolder_txt:
   pass

  #Move files to downsampled_ADX folder
  matching_files = [file for file in os.listdir(currentdir) if file.endswith('.adx') or file.endswith('.ADX')]
  for rootfolder_adxfiles in matching_files:
   rootfolder_adxfile_path = os.path.join(currentdir, rootfolder_adxfiles)
   shutil.move(rootfolder_adxfile_path, downsampled_folder)

  if os.path.isfile(selected_adx_file.get()):
   os.remove(selected_adx_file.get())

  if batchmode.get() == 1:
   with open(adxdirfile_path, 'w') as adxdirfile:
    adxdirfile.seek(0)
    adxdirfile.write('BATCH')
    adxdirfile.truncate()

  cleanbinfolder.set(1)
  clean_loosefiles()
  
  print("")
  if batchmode.get() == 1:
   print("ADX files downsampled!")
  else:
   print("ADX file downsampled!")
  print("")
  print("")
  sys.exit()


 #Run commands
 findadxloops()
 get_GUI_values()
 convertadx_to_WAV()
 findorigadx_samplerate()
 get_original_looppoints()
 find_and_convert_newlooppoints()
 converttoadx()


def clean_loosefiles():
 if cleanbinfolder.get() == 1: #Only run at end of program to avoid it erasing the file before script begins
  filestoremove_ADX = [file for file in os.listdir(currentdir) if file.endswith('.adx') or file.endswith('.ADX')]
  for ADXfile in filestoremove_ADX:
   adxfile_paths = os.path.join(currentdir, ADXfile)
   os.remove(adxfile_paths)
  
  tempadx_folder = os.path.join(currentdir + '/tempadx')
  remove_tempADXfiles = [file for file in os.listdir(tempadx_folder) if file.endswith('.adx') or file.endswith('.ADX')]
  for tempADXfile in remove_tempADXfiles:
   tempadxfile_paths = os.path.join(tempadx_folder, tempADXfile)
   os.remove(tempadxfile_paths)

 filestoremove_WAV = [file for file in os.listdir(currentdir) if file.endswith('.wav') or file.endswith('.WAV')]
 for WAVfile in filestoremove_WAV:
  wavfile_paths = os.path.join(currentdir, WAVfile)
  os.remove(wavfile_paths)

 if os.path.isfile('wav.wav'):
  os.remove('wav.wav')
 if os.path.isfile('downsampled.wav'):
  os.remove('downsampled.wav')
 if os.path.isfile(wavconvert_rootdir):
  os.remove(wavconvert_rootdir)


#Run commands
clean_loosefiles() #Run on boot to clean up any files
getadx()
adxcommands()

master.mainloop()