#!/usr/bin/python

import sys
import os
import re
import boto
import h5py
import socket
import time
from boto.s3.connection import S3Connection
from boto.s3.key import Key

# Make sure we can import our local code
sys.path.append(os.path.dirname(__file__))

import opennex_partition as partitioner
import s3copy



aws_key = sys.argv[1]
aws_secret = sys.argv[2]
bucket = sys.argv[3]
prefix = sys.argv[4]

def downloadHDF(bucketName,keyName,fileName):
   f = None
   h5pyAttempt = 0
   h5pySuccess = False
   while h5pyAttempt < 3 and not h5pySuccess:
      h5pyAttempt += 1
      try:
         conn = S3Connection(aws_key, aws_secret)
         data_bucket = conn.get_bucket(bucketName)
         k = data_bucket.get_key(keyName)
      
         attempt = 0
         success = False
         def progress(recieved,size):
            sys.stderr.write(".")
            sys.stderr.flush()
            
         while attempt<3 and not success:
            attempt += 1
            out = open(fileName,"wb")
            try:
               k.get_contents_to_file(out,cb=progress,num_cb=1000)
            except:
               success = False
               out.close()
               continue
            out.flush()
            out.close()
            success = True
            
         conn.close()
      
         sys.stderr.write("\n   resizing data: {0}\n".format(fileName))
         
         f =  h5py.File(fileName,"r")
         h5pySuccess = True
      except:
         sys.stderr.write("Cannot open hdf5 file {0}\n".format(fileName))
         h5pySuccess = False
         
   return f

for line in sys.stdin:


   sys.stderr.write("Processing: "+line+"\n")
   parts = line.split("\t");
   sys.stderr.write("   request: "+parts[-1]+"\n")
   input = parts[-1].split(" ")
   
   requested = []
   for i in range(1,len(input)):
      requested.append(int(input[i])-1)
      
   sys.stderr.write("  s3 input: "+input[0]+"\n")
   m = re.match("s3://([^/]+)/(.+)",input[0])
   

   fileName = input[0][input[0].rfind("/")+1:]
   
   f = downloadHDF(m.group(1),m.group(2),fileName)
   #f = h5py.File(fileName,"r")

   if f is None:
      sys.stderr.write("Aborting!\n")
      exit(1)
      
   tasmax = f["tasmax"]
   timeb = f["time_bnds"]
   
   
   if len(requested)==0:
      months = tasmax.shape[0]
      requested = range(months)

   startYear = int(1950+timeb[0,0]/365)
   
   outDir = "data"
   
   for m in requested:

      year = startYear+m/12
      month = m % 12 + 1    
   
      sys.stderr.write("{0} {1}-{2:02d} :\n".format(m,year,month))
      mset = tasmax[m,:,:]
      t1 = time.time()
      partitioner.partition(outDir,year,month,mset,60)
      t2 = time.time() - t1
      sys.stderr.write("Completed in ({0}s)\n".format(t2))

      summaries = [30,60,120]
      t1 = time.time()
      summary = partitioner.summarize(mset,summaries[0])
      partitioner.writeSummary(outDir,year,month,summaries[0],summary)
      t2 = time.time() - t1
      sys.stderr.write("Completed in {0}s\n".format(t2))
      
      for i in range(1,len(summaries)):
         summary = partitioner.reviseSummary(summary,summaries[i]/summaries[i-1])      
         partitioner.writeSummary(outDir,year,month,summaries[i],summary)
      
   f.close()

   sys.stderr.write("   uploading data...\n")

   conn = S3Connection(aws_key, aws_secret)
   upload_bucket = conn.get_bucket(bucket)
   s3copy.copyToBucket(outDir,upload_bucket,prefix)
   
   sys.stderr.write("DONE!\n")
    
   print line 