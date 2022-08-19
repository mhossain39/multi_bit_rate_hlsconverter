# -*- coding: utf-8 -*-
import os,sys
from mp3hlsfuncs import fixmp3, generate_hls

if len(sys.argv) < 3:
	print ("python fixedmp3tohls.py source destination_folder")
	exit()
source=os.path.abspath(sys.argv[1])
destination = os.path.abspath(sys.argv[2])



fixmp3(source,destination)
generate_hls(source,destination)
