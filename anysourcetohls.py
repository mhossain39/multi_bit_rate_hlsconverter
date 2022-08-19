# -*- coding: utf-8 -*-
import subprocess, os, sys
profiles=[]
if len(sys.argv) < 3:
	print "python anysourcetohls.py source destination_folder"
	exit()
source=sys.argv[1]
destination = sys.argv[2]

###### Configureable Section ###########
#profiles.append("256x144,100k,32k")	#Put a # at the beginning of this line to disable this profile
profiles.append("426x240,50k,64k")	#Put a # at the beginning of this line to disable this profile
profiles.append("640x360,100k,96k")	#Put a # at the beginning of this line to disable this profile
profiles.append("842x480,500k,128k")	#Put a # at the beginning of this line to disable this profile
profiles.append("1280x720,1200k,128k")	#Put a # at the beginning of this line to disable this profile
#profiles.append("1920x1080,5000k,192k") #Put a # at the beginning of this line to disable this profile
live=0					#set to 1 for Live
video_codec="h264"			#Change Video Codec


segment_target_duration=4       
max_bitrate_ratio=1.07          
rate_monitor_buffer_ratio=1.5
master_playlist="""#EXTM3U
#EXT-X-VERSION:3
"""
cmdlist=["ffmpeg", "-hide_banner", "-y", "-i", source]
try:  
    os.mkdir(destination)
except OSError:  
    pass

for profile in profiles:
	p= profile.split(",")

	hw=p[0].split("x")
	width=hw[0]
	height=hw[1]
	bitrate=p[1]
	bitratei=p[1].replace("k","")

	audiorate=p[2]
	maxrate=str(int(bitratei)+int(int(bitratei)*max_bitrate_ratio))+"k"
  	bufsize=str(int(bitratei)+int(int(bitratei)*rate_monitor_buffer_ratio))+"k"
  	bandwidth=int(bitratei)*1000
	name=str(height)+"p"
	if live:
		tmplist=["-vf", "scale=w="+str(width)+":h="+str(height)+":force_original_aspect_ratio=decrease", "-c:a", "aac", "-ar", "48000", "-c:v", video_codec, "-profile:v", "high", "-crf", "20", "-sc_threshold", "0", "-g", "48", "-keyint_min", "48", "-hls_time", "4",   "-b:v", bitrate, "-maxrate", maxrate, "-bufsize", bufsize, "-b:a", audiorate, "-hls_segment_filename", destination+"/"+name+"_%03d.ts", destination+"/"+name+".m3u8"]
	else:
		tmplist=["-vf", "scale=w="+str(width)+":h="+str(height)+":force_original_aspect_ratio=decrease", "-c:a", "aac", "-ar", "48000", "-c:v", video_codec, "-profile:v", "high", "-crf", "20", "-sc_threshold", "0", "-g", "48", "-keyint_min", "48", "-hls_time", "4",   "-b:v", bitrate, "-maxrate", maxrate, "-bufsize", bufsize, "-b:a", audiorate, "-hls_playlist_type", "vod","-hls_segment_filename", destination+"/"+name+"_%03d.ts", destination+"/"+name+".m3u8"]
	master_playlist+="#EXT-X-STREAM-INF:BANDWIDTH="+str(bandwidth)+",RESOLUTION="+p[0]+"\n"+name+".m3u8\n"
	cmdlist+=tmplist
cmdlist+=["-loglevel", "quiet"]

if live:
	f = open(destination+"/playlist.m3u8", "w")
	f.write(master_playlist)
	f.close() 

print "Started...."
subprocess.call(cmdlist)

if not live:
	f = open(destination+"/playlist.m3u8", "w")
	f.write(master_playlist)
	f.close() 
print "Done"

