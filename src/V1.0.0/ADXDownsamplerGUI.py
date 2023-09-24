"""
ADX HEADER INFO: https://en.wikipedia.org/wiki/ADX_(file_format)#Technical_description
ADXdownsampler script/GUI and ADXLoopFinder developed by Firebow59 (https://github.com/Firebow59)
"""

import tkinter as tk
import os
import sys
import subprocess
import shutil

from tkinter import filedialog, StringVar, IntVar, LabelFrame, Label, ttk, Button, messagebox
from os import path
from sys import exit
from subprocess import run
from shutil import copy


def gui():
 master = tk.Tk()
 master.geometry('400x160'), master.title('ADXDownsampler'), master.resizable(False, False)
 optionsframe = LabelFrame(master, text="Options").place(relx=0.010, rely=0.52, relheight=0.45, relwidth=0.980)

 currentdir = os.path.join(os.getcwd(), 'bin')
 adxdirfile_path = 'bin/resource/txt/adxdir.txt'
 singleadx_filepath = StringVar()

 def find_singleadx():
  adxfilelocation = filedialog.askopenfilename(title='Choose an ADX file', filetypes=[("ADX file", ".adx")])
  if not os.path.exists(adxfilelocation) or adxfilelocation == '':
   tk.messagebox.showerror(title="Directory Error", message="Invalid directory selected, please select a different directory or try again.")
  
  global adxfile
  adxfile = os.path.basename(adxfilelocation)
  global adxfile_noextension
  adxfile_noextension = os.path.splitext(adxfile)[0]
  if os.path.isfile(adxfile):
   pass
  else:
   if not adxfilelocation == '':
    shutil.copy(adxfilelocation, currentdir)


  with open(adxdirfile_path, 'r+') as adxdirfile:
    adxdirfile.seek(0)
    adxdirfile.write(adxfile)
    adxdirfile.truncate()
    if not adxdirfile == '':
     if adxfile == '':
      pass
     else:
      print(f'Found ADX: {adxfile}')
      singleadx_filepath.set(adxfile)



 def batch_downsample():
  #Make batch txt files blank if text is in them
  batchfilelist_txt_tempfolder = currentdir + '/resource/txt/batch_adxfiles-tempfolder.txt'
  batchfilelist_txt_origlocation = currentdir + '/resource/txt/batch_adxfiles-origlocation.txt'
  with open(batchfilelist_txt_tempfolder, "w") as batchfile_tempfolder_txt:
   pass
  with open(batchfilelist_txt_origlocation, "w") as batchfile_origfolder_txt:
   pass
  
  adxdirlocation = filedialog.askdirectory(title='Choose a Directory')
  adxbatchdir = adxdirlocation

  for root, dirs, files in os.walk(adxbatchdir):
   for file_batchadx in files:

    if file_batchadx.endswith(".adx") or file_batchadx.endswith(".ADX"):
     tempadx_path = os.path.join(currentdir + '/tempadx')
     batchadx_filelist = os.path.join(root, file_batchadx)
     if os.path.exists(tempadx_path):
      pass
     else:
      os.mkdir(tempadx_path)
  

     #Write to batch_adxfiles-origfolder.txt
     batch_adxfiles_txt = batchfilelist_txt_origlocation
     with open(batch_adxfiles_txt, 'a') as batchtxt:
      batchtxt.seek(0)
      batchtxt.write(batchadx_filelist + '\n')
      batchtxt.truncate()
      shutil.copy2(batchadx_filelist, tempadx_path)


  #Write to batch_adxfiles.txt + copy files to temp folder
  filelist_tempadx = os.listdir(tempadx_path)
  matching_files = [file for file in os.listdir(tempadx_path) if file.endswith('.adx') or file.endswith('.ADX')]
  for tempfolder_adxfile in matching_files:
    tempadx_files_filepath = os.path.join(tempadx_path, tempfolder_adxfile)

    batch_adxfiles_tempfolder_txt = batchfilelist_txt_tempfolder
    with open(batch_adxfiles_tempfolder_txt, 'a') as batchtxt_tempfolder:
     batchtxt_tempfolder.seek(0)
     batchtxt_tempfolder.write(tempadx_files_filepath + '\n')
     batchtxt_tempfolder.truncate()

  #Check for downsampler.exe's batch mode
  with open(adxdirfile_path, 'r+') as adxdirfile:
    adxdirfile.seek(0)
    adxdirfile.write('BATCH')
    adxdirfile.truncate()


 def rundownsampler():
  update_samplerate() #Fix for custom sample rates not applying to files

  if samplerate.get() == '': #Fix for if sample rate isn't changed in combobox
   samplerate.set('22050')

  if opendownsampledfolder.get() == 1:
   openfoldertxt_path = 'bin/resource/txt/openfolder.txt'
   with open(openfoldertxt_path, 'w') as openfoldertxt:
    openfoldertxt.write('OPENFOLDER')

  sampleratetxt_path = 'bin/resource/txt/output_samplerate.txt'
  with open(sampleratetxt_path, 'w') as sampleratetxt:
   sampleratetxt.write(samplerate.get())

  audiobitratetxt_path = 'bin/resource/txt/output_audiobitrate.txt'
  with open(audiobitratetxt_path, 'w') as audiobitratetxt:
   audiobitratetxt.write(abitrate.get())

  channeltypetxt_path = 'bin/resource/txt/output_channeltype.txt'
  with open(channeltypetxt_path, 'w') as channeltypetxt:
   if forcemono.get() == 1:
    channeltypetxt.write('1')
   if forcemono.get() == 0:
    channeltypetxt.write('2')

  print("--------------------------")
  run_downsampler_program = os.path.join(currentdir, 'downsampler.exe')
  rundownsampler = subprocess.run(run_downsampler_program, stderr=subprocess.STDOUT, shell=True)



 choosesingleadx_btn = Button(text='Choose single ADX', command=find_singleadx, padx=5, pady=5).place(x=75, y=10)
 choosebatch_btn = Button(text='Batch downsample', command=batch_downsample, padx=5, pady=5).place(x=205, y=10)
 downsample_btn = Button(text='Downsample ADX', command=rundownsampler, padx=73, pady=1).place(x=75, y=47.5)

 forcemono = IntVar()
 monocmd = StringVar()
 usemonocheck = ttk.Checkbutton(text='Force mono', variable=forcemono, onvalue=1, offvalue=0).place(x=293, y=102)
 
 opendownsampledfolder = IntVar()
 opendownsampledfoldercheck = ttk.Checkbutton(text='Open folder', variable=opendownsampledfolder, onvalue=1, offvalue=0).place(x=293, y=122)
 opendownsampledfolder.set(1)

 abitrate = StringVar()
 audiobitrate_label = Label(text="Audio Bitrate:", font=("Arial Bold", 8)).place(x=178, y=100)
 audiobitrateentry = ttk.Entry(textvariable=abitrate, width=15)
 audiobitrateentry.insert(0, "320")
 audiobitrateentry.place(x=180, y=120)

 samplerate_label = Label(text="Output Sample Rate (in Hz):", font=("Arial Bold", 8)).place(x=9, y=100)
 OPTIONS_samplerate = ["11025", "22050", "32000", "41000"]
 samplerate = StringVar()
 comboboxsamplerate = StringVar()
 sampleratebox = ttk.Combobox(master, value=OPTIONS_samplerate, textvariable=comboboxsamplerate)
 sampleratebox.place(x=12, y=120)
 sampleratebox.current(1)

 def update_samplerate(event=None):
  selected_sampleratevalue = comboboxsamplerate.get()
  if selected_sampleratevalue == "11025":
   comboboxsamplerate.set(OPTIONS_samplerate[0])
   samplerate.set("11025")
   sampleratebox.selection_clear()
  elif selected_sampleratevalue == "22050":
   comboboxsamplerate.set(OPTIONS_samplerate[1])
   samplerate.set("22050")
   sampleratebox.selection_clear()
  elif selected_sampleratevalue == "32000":
   comboboxsamplerate.set(OPTIONS_samplerate[2])
   samplerate.set("32000")
   sampleratebox.selection_clear()
  elif selected_sampleratevalue == "41000":
   comboboxsamplerate.set(OPTIONS_samplerate[3])
   samplerate.set("41000")
   sampleratebox.selection_clear()
  else:
   custom_value = int(selected_sampleratevalue)
   if custom_value >= 0:
    samplerate.set(custom_value)
   else:
    samplerate.set("")
  master.after(100, update_samplerate)
 sampleratebox.bind("<FocusOut>", update_samplerate)
 sampleratebox.bind("<<ComboboxSelected>>", update_samplerate)


 #Check for update
 def checkforupdate():
  print("Checking for update...")
  updater_path = currentdir + '/updater.exe'
  if os.path.isfile(updater_path):
   run_updater = f'{updater_path}'
   run_updater_cmd = subprocess.run(run_updater, stderr=subprocess.STDOUT, shell=True)
   print("")
  else:
   print("Unable to find updater.exe, program will not be able to update.")
   pass
 checkforupdate()

 master.mainloop()
gui()


def closeprogram():
 sys.exit()