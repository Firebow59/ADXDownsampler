"""
ADX HEADER INFO: https://en.wikipedia.org/wiki/ADX_(file_format)#Technical_description
ADXdownsampler script/GUI developed by Firebow59 (https://github.com/Firebow59)
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
 master.geometry('400x210'), master.title('ADXDownsampler'), master.resizable(False, False)
 optionsframe = LabelFrame(master, text="Options").place(relx=0.010, rely=0.40, relheight=0.57, relwidth=0.980)
 adxfile = StringVar()

 def find_singleadx():
  adxfilelocation = filedialog.askopenfilename(title='Choose an ADX file', filetypes=[("ADX file", ".adx")])
  adxfile.set(adxfilelocation)
  
  if adxfile.get().endswith(".adx") or adxfile.get().endswith(".ADX") and os.path.isfile(adxfile.get()):
   print(f'Found ADX: {adxfile.get()}')
  else:
   print(f"ADX file not found.")


 def batch_downsample():
  adxdirlocation = filedialog.askdirectory(title='Choose a Directory')
  adxfile.set(adxdirlocation)
  if os.path.exists(adxdirlocation):
   pass
  else:
   print("Directory could not be found.")


 def rundownsampler():
  update_samplerate() #Fix for custom sample rates not applying to files

  if forcemono.get() == 1:
   monocmd.set('-mono') 
  else:
   monocmd.set('')
  if copyskipped.get() == 1:
   copyskippedcmd.set('-copyskipped') 
  else:
   copyskippedcmd.set('')
  if autooverwrite.get() == 1:
   autooverwritecmd.set('-overwrite') 
  else:
   autooverwritecmd.set('')
  if samplerate.get() == '': #Fix for if sample rate isn't changed in combobox
   samplerate.set('22050')

  print("--------------------------")
  rundownsampler = f'adxdownsampler.exe -i "{adxfile.get()}" -samplerate {samplerate.get()} {monocmd.get()} -audiobitrate {abitrate.get()} {copyskippedcmd.get()} {autooverwritecmd.get()}'
  rundownsampler_cmd = subprocess.run(rundownsampler, stderr=subprocess.STDOUT, shell=True)



 choosesingleadx_btn = Button(text='Choose single ADX', command=find_singleadx, padx=5, pady=5).place(x=75, y=10)
 choosebatch_btn = Button(text='Batch downsample', command=batch_downsample, padx=5, pady=5).place(x=205, y=10)
 downsample_btn = Button(text='Downsample ADX', command=rundownsampler, padx=73, pady=1).place(x=75, y=47.5)

 forcemono = IntVar()
 monocmd = StringVar()
 usemonocheck = ttk.Checkbutton(text='Force mono', variable=forcemono, onvalue=1, offvalue=0).place(x=293, y=115)
 
 #opendownsampledfolder = IntVar()
 #opendownsampledfoldercheck = ttk.Checkbutton(text='Open folder', variable=opendownsampledfolder, onvalue=1, offvalue=0).place(x=293, y=122)
 #opendownsampledfolder.set(1)

 copyskipped = IntVar()
 copyskippedcmd = StringVar()
 copyskippedcheck = ttk.Checkbutton(text='Copy skipped files to out folder', variable=copyskipped, onvalue=1, offvalue=0).place(x=11, y=150)
 copyskipped.set(1)

 autooverwrite = IntVar()
 autooverwritecmd = StringVar()
 autooverwritecheck = ttk.Checkbutton(text='Auto overwrite files in out folder', variable=autooverwrite, onvalue=1, offvalue=0).place(x=11, y=170)

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
  updater_path = os.getcwd() + '/updater.exe'
  if os.path.isfile(updater_path):
   run_updater = f'{updater_path}'
   run_updater_cmd = subprocess.run(run_updater, stderr=subprocess.STDOUT, shell=True)
   print("")
  else:
   print("Unable to find updater.exe, program will not be able to update.")
   pass
  print("")
 checkforupdate()

 master.mainloop()
gui()


def closeprogram():
 sys.exit()