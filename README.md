# ADXDownsampler
**A simple, open-source program for automatically downsampling CRI Middleware (v3) ADX files.**

## Features
- Custom sample rates and audio bitrate options
- Option to put audio in mono
- Keeps loop from original file
- Can downsample a single or batch of ADX files
- CMD support (by running ADXdownsampler.exe in a command line)

## CMD commands
If you do wish to use this program as a command line program, here are the options:

    -i:             input file/directory
    -samplerate:    sample rate of output file(s)
    -audiobitrate   bitrate of output file(s)
    -mono:          Forces output file(s) to mono
    -copyskipped:   Copies skipped file(s) to output folder (b/c the output sample rate was greater than the sample rate of the original file)
    -overwrite:     Auto overwrites file(s) in out folder

Example command (batch downsample) - Every ADX file in "C:\ADX" would be downsampled to 32000Hz mono.

    adxdownsampler.exe -i "C:\ADX" -samplerate 32000 -mono 

## Programs included in ADXDownsampler
[SoX](https://sourceforge.net/projects/sox/)

[VGMStream](https://vgmstream.org/)

adxencd.exe from CRI Middleware
