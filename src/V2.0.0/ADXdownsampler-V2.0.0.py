import struct
import tkinter as tk
import os
import shutil
import subprocess
import argparse

from struct import unpack
from tkinter import StringVar, IntVar
from subprocess import run

"""
ADX HEADER INFO: https://en.wikipedia.org/wiki/ADX_(file_format)#Technical_description
ADXdownsampler script developed by Firebow59 (https://github.com/Firebow59)

ADXDownsampler version: V2.0.0
"""

master = tk.Tk()
master.withdraw()

#Variables
downsamplermode = IntVar()
adxfile = StringVar()
noloop = IntVar()
adxversion = IntVar()
badsamplerate = IntVar()
overwrite = IntVar()
enablemono = IntVar()
copyskipped_int = IntVar()
overwrite_int = IntVar()


#Program/file locations
soxlocation = os.path.join(os.getcwd(), 'resource', 'sox', 'sox.exe')
soxpath = os.path.join(os.getcwd(), 'resource', 'sox')
adxencdlocation = os.path.join(os.getcwd(), 'resource', 'adxencd.exe')
vgmstreamlocation = os.path.join(os.getcwd(), 'resource', 'vgmstream-win64', 'vgmstream-cli.exe')

downsample_tempfolder = os.getcwd() + '/downsample'
outputadx_folder = os.getcwd() + '/downsampledADX'
temp_wavconvert = os.path.join(os.getcwd(), 'downsample', 'wav.wav')
downsampledWAV_file = os.path.join(os.getcwd(), 'downsample', 'downsampled.wav')
downsampledADX_file = os.path.join(os.getcwd(), 'downsample', 'downsampled.adx')


if __name__ == "__main__":
 parser = argparse.ArgumentParser(description='Downsamples ADX files\nExample Command: adxdownsampler -i audio.adx -samplerate 32000 -enablemono')
 parser.add_argument('-i', type=str, help='Input file/directory')
 parser.add_argument('-samplerate', type=int, help='Sample rate of downsampled ADX files.')
 parser.add_argument('-mono', action='store_true', help='Enable mono (1 channel) audio.')
 parser.add_argument('-audiobitrate', type=int, help='Audio bitrate of downsampled ADX files.')
 parser.add_argument('-copyskipped', action='store_true', help='Copies skipped files to out folder.')
 parser.add_argument('-overwrite', action='store_true', help='Auto overwrite files in out folder.')

 args = parser.parse_args()
 samplerate = args.samplerate
 audiobitrate = args.audiobitrate
 copyskipped = args.copyskipped
 overwrite = args.overwrite
 inputfiles = args.i

 if args.mono:
  enablemono.set(1)
 if args.copyskipped:
  copyskipped_int.set(1)
 if args.overwrite:
  overwrite_int.set(1)

 #Change ADXdownsampler mode
 if not os.path.isdir(inputfiles): 
  downsamplermode.set(0)   #0 = single file, 1 = batch downsample
  print("")
 else:
  downsamplermode.set(1)
  print("")
  print("--Batch Mode Enabled--")
   
 #Set up file list
 if downsamplermode.get() == 0:
  adxfile.set(inputfiles)
 
 if downsamplermode.get() == 1:
  file_list = []
  for root, dirs, files in os.walk(inputfiles):
   for file_name in files:
    file_list.append(os.path.join(root, file_name))
   for adx_file_path in file_list:
    pass
   
 #Close script if no file/file does not exist
 elif inputfiles == '' or downsamplermode.get() == 0 and not os.path.isfile(inputfiles):
   print("ADX file does not exist, closing script...")
   os._exit(1)
   
 #Set audio bitrate if none provided by user
 if audiobitrate == None or '':
  audiobitrate = '320'

 

 def print_pre_extraction_info():
  if downsamplermode.get() == 1:
   print("Batch downsample?: Yes")
   number_of_adxfiles = len(file_list)
   print("Number of ADX files:", number_of_adxfiles)
  else:
   print("Batch downsample?: No")
   print("Number of ADX files: 1")
  
  print("Output Sample Rate:", samplerate)
  print(f"Audio Bitrate: {audiobitrate}")
  
  if enablemono.get() == 1:
   print("Enable mono?: Yes")
  else:
   print("Enable mono?: No")
 print_pre_extraction_info()


 def rundownsampler(adx_file_path):
     #Ask to overwrite file if already exists in out folder
     #For overwrite_int - 1 = Overwrite file, 0 = don't overwrite file
     if downsamplermode.get() == 1:
      checkoverwrite_outputfolderadx = outputadx_folder + '/' + os.path.basename(adx_file_path)
     if downsamplermode.get() == 0:
      checkoverwrite_outputfolderadx = outputadx_folder + '/' + os.path.basename(adxfile.get())

     def overwritefile():
      if downsamplermode.get() == 0:
       if args.overwrite:
        overwrite_int.set(1)
       else:
        overwrite_existing_downsampled = input("File already exists in downsampled folder, overwrite it? Enter either 'y' or 'n': ")
        if overwrite_existing_downsampled == 'y' or overwrite_existing_downsampled == 'Y':
         os.remove(checkoverwrite_outputfolderadx)
         overwrite_int.set(1)
        elif overwrite_existing_downsampled == 'n' or overwrite_existing_downsampled == 'N':
         overwrite_int.set(0)
        else:
         print("Incorrect value entered, please try again...")
         overwritefile()
         return
      if downsamplermode.get() == 1:
       if args.overwrite:
        overwrite_int.set(1)
        pass
       else:
        overwrite_existing_downsampled = input("File already exists in downsampled folder, overwrite it? Enter either 'y' or 'n': ")
        if overwrite_existing_downsampled == 'y' or overwrite_existing_downsampled == 'Y':
         os.remove(checkoverwrite_outputfolderadx)
         overwrite_int.set(1)
        elif overwrite_existing_downsampled == 'n' or overwrite_existing_downsampled == 'N':
         overwrite_int.set(0)
        else:
         print("Incorrect value entered, please try again...")
         overwritefile()
        return


     if os.path.exists(checkoverwrite_outputfolderadx):   
      overwritefile()
     else:
      overwrite_int.set(1) #Set this so that even if ADX ISN'T in output folder, it still gets made

     
     if overwrite_int.get() == 0:
      pass
     if overwrite_int.get() == 1:
      if os.path.isfile(temp_wavconvert):
       os.remove(temp_wavconvert)

      if os.path.exists(downsample_tempfolder):
       shutil.rmtree(downsample_tempfolder)
      os.mkdir(downsample_tempfolder)

      if os.path.exists(downsample_tempfolder):
       shutil.rmtree(downsample_tempfolder)
      os.mkdir(downsample_tempfolder)


      #Check for ADX version
      offsetvalue = 0x12
      with open(adx_file_path, 'rb') as singleadx_file:
       singleadx_file.seek(offsetvalue)
       int8_byte = singleadx_file.read(1)
       int8_value = struct.unpack('>B', int8_byte)[0]
       adxversion = int8_value
       if adxversion == 3:
        pass
       if adxversion == 4:
        print(f"{adx_file_path} file is a version 4 file, and currently cannot be downsampled with this program, skipping file...")
        return
       else:
        pass
      
      #Convert file to WAV/extract ADX
      converttoWAV_fixlength = f'{vgmstreamlocation} "{adx_file_path}" -f 0.0 -l 1 -o {temp_wavconvert}'
      converttoWAV_fixlength_cmd = subprocess.run(converttoWAV_fixlength, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True) 


      #Get original ADX sample rate
      originalsamplerate_offsetvalue = 0x08
      end_offsetvalue = 0x0B
      offset_hexvalues = originalsamplerate_offsetvalue + end_offsetvalue - originalsamplerate_offsetvalue + 1
      with open(adx_file_path, 'rb') as getsamplerate_ADXfile:
         getsamplerate_ADXfile.seek(originalsamplerate_offsetvalue)
         int32_bytes = getsamplerate_ADXfile.read(offset_hexvalues - originalsamplerate_offsetvalue)
         origadx_samplerate = IntVar()
         origadx_samplerate = struct.unpack('>I', int32_bytes)[0]
         if int(samplerate) > origadx_samplerate:
          print(f"Error: Output sample rate cannot be greater than that of the original file, skipping {os.path.basename(adx_file_path)}...")
          badsamplerate.set(1)
          if copyskipped_int.get() == 1:
           shutil.copy(adx_file_path, outputadx_folder)


      if badsamplerate.get() == 1:
       pass
      else:
       #Check if ADX has loop points or not
       loopenabled_offsetvalue = 0x17
       with open(adx_file_path, 'rb') as singleadx_file:
         singleadx_file.seek(loopenabled_offsetvalue)
         loopenabled_byte = singleadx_file.read(1)
         adxenableloopvariable = struct.unpack('>B', loopenabled_byte)[0]
  
         if adxenableloopvariable == 0:
          noloop.set(1)
          print(f"No loop detected in {os.path.basename(adx_file_path)}, passing loop calculator...")
         else:
          pass
         
         
      if badsamplerate.get() == 1:
       badsamplerate.set(0) #Reset variable for next file
       pass
      else:
       #Get ADX loop points
       startloop_startoffsetvalue = 0x1C
       startloop_endoffsetvalue = 0x1F
       endloop_startoffsetvalue = 0x24
       endloop_endoffsetvalue = 0x27

       if noloop.get() == 1:
        pass
       else:
        #Get Start Loop value
        offset_hexvalues = startloop_startoffsetvalue + startloop_endoffsetvalue - startloop_startoffsetvalue + 1
        with open(adx_file_path, 'rb') as singleadx_file:
            singleadx_file.seek(startloop_startoffsetvalue)
            int32_bytes = singleadx_file.read(offset_hexvalues - startloop_startoffsetvalue)
            startloopvalue = struct.unpack('>I', int32_bytes)[0]

        #Get End Loop value
        offset_hexvalues = endloop_startoffsetvalue + endloop_endoffsetvalue - endloop_startoffsetvalue + 1
        with open(adx_file_path, 'rb') as singleadx_file:
            singleadx_file.seek(endloop_startoffsetvalue)
            int32_bytes = singleadx_file.read(offset_hexvalues - endloop_startoffsetvalue)
            endloopvalue = struct.unpack('>I', int32_bytes)[0]


       #Convert ADX loop points to output sample rate
       if noloop.get() == 1:
        pass
       else:
        global startloop_newstartvalue
        global endloop_newendvalue
        samplerate_float = float(samplerate)
        downsamplingfactor = float(origadx_samplerate) / samplerate_float
        downsamplingfactor = float(downsamplingfactor)

        originalstartloop_float = float(startloopvalue)
        startloop_newstartvalue = originalstartloop_float / downsamplingfactor
        originalendloop_float = float(endloopvalue)
        endloop_newendvalue = originalendloop_float / downsamplingfactor
     

       #Downsample WAV
       if enablemono.get() == 1:
        channels = 1
       else:
        channels = 2

       if os.path.isfile(downsampledWAV_file):
        os.remove(downsampledWAV_file)
       if os.path.isfile(downsampledADX_file):
        os.remove(downsampledADX_file)

       downsampleWAV = f'{soxlocation} {temp_wavconvert} --rate {samplerate} --channels {channels} --compression {audiobitrate} {downsampledWAV_file}'
       downsampledWAV_cmd = subprocess.run(downsampleWAV, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)


       #Create downsampled ADX
       if not os.path.exists(outputadx_folder):
        os.mkdir(outputadx_folder)

       originaladxfilename = os.path.basename(adx_file_path)
       downsampledADX_outputlocation = os.path.join(outputadx_folder, originaladxfilename)

       if noloop.get() == 1:
        adxencoder=f'{adxencdlocation} {downsampledWAV_file} {downsampledADX_outputlocation}'
       else:
        adxencoder=f'{adxencdlocation} {downsampledWAV_file} -lps{startloop_newstartvalue} -lpe{endloop_newendvalue} {downsampledADX_outputlocation}'
       adxencodercmd = subprocess.run(adxencoder, creationflags=subprocess.CREATE_NO_WINDOW, shell=True, capture_output=True, text=True)
       noloop.set(0) #Reset variable for next file

       #Clean up
       if os.path.isfile(downsampledWAV_file):
        os.remove(downsampledWAV_file)
       if os.path.isfile(temp_wavconvert):
        os.remove(temp_wavconvert)
      
       print("Done!")


 def rundownsampler_modeselect():
  print("----------------------")
  print("")

  cleanupfiles = False  #Check to see if all files have been processed.

  if downsamplermode.get() == 0:
   adx_file_path = adxfile.get()
   print(f"Downsampling file: {os.path.basename(adx_file_path)}")
   rundownsampler(adx_file_path)

  if downsamplermode.get() == 1:
   for root, dirs, files in os.walk(inputfiles):
    for file_name in files:
     adx_file_path = os.path.join(root, file_name)
     print(f"Downsampling file: {os.path.basename(adx_file_path)}")
     rundownsampler(adx_file_path)

  if not cleanupfiles:
   if os.path.exists(downsample_tempfolder):
    shutil.rmtree(downsample_tempfolder)

 rundownsampler_modeselect()