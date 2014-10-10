#!/opt/local/bin/python
# -*- coding: utf-8 -*-

import sys
import h5py
import numpy
import json
import time

fileName = sys.argv[1]
startYear = int(sys.argv[2])
outputPrefix = "" if len(sys.argv)<4 else sys.argv[3]
outputXML = True if len(sys.argv)<5 else sys.argv[4] != "json"

f =  h5py.File(fileName,"r")
t1 = time.time()
print "Loading dataset array..."
tasmax = f["tasmax"]
t2 = time.time() - t1

print "Finished ({}s)".format(t2)

months = tasmax.shape[0]
rows = tasmax.shape[1]
columns = tasmax.shape[2]


print "{} months, lat x lon = {} x {}".format(months,rows,columns)

def resizeData(m,mset,chunkSizes,partitions):
   factor = 1
   dset = mset;
   for p in range(len(chunkSizes)):
      chunkSize = chunkSizes[p]
      factor = factor*chunkSize
      resolution = factor/120.0
      sizeLat = int(round(dset.shape[0]/(chunkSize*1.0)))
      sizeLon = int(round(dset.shape[1]/(chunkSize*1.0)))
      d = numpy.empty((sizeLat,sizeLon),numpy.float64)
      print "Resizing from ",dset.shape," to ",d.shape
      
      t1 = time.time()
      for i in range(0,d.shape[0]):
         #c1 = time.time()
         for j in range(0,d.shape[1]):
            s = dset[i*chunkSize:i*chunkSize+chunkSize,j*chunkSize:j*chunkSize+chunkSize]
            reduction = reduce(lambda r,x: (r[0]+1,r[1]+x) if x<1.00000002e20 and x>0 else r, s.flat,(0,0))
            d[i,j] = 0 if reduction[0] == 0 else reduction[1] / reduction[0]
            if d[i,j] > 0 and d[i,j] < 100.0:
               print factor,",",i,",",j,": ",s
         #print i," ",(time.time()-c1),"s"
            
      t2 = time.time() - t1
      print " ... # non-zero {} ({}s)".format(len(d.nonzero()[0]),t2)
      
      yearMonth = "{}-{:02d}".format(startYear+(m+1)/12,(m+1)%12)
      rowSize = int(round(d.shape[0]/(partitions[p]*1.0)))
      colSize = int(round(d.shape[1]/(partitions[p]*1.0)))
      for row in range(partitions[p]):
         rowStart = row*rowSize
         currentRowSize = rowSize if (rowStart+rowSize) <= d.shape[0] else d.shape[0] - rowStart
         for col in range(partitions[p]):
            seq = row*partitions[p] + col + 1
            colStart = col*colSize
            currentColSize = colSize if (colStart+colSize) <= d.shape[1] else d.shape[1] - colStart
            filename = outputPrefix+yearMonth+"-"+str(factor)+"-"+str(seq)+".xml"
            print " ... writing {} ...".format(filename)
            xf = open(filename,"w")
            xf.write("<data xmlns='http://milowski.com/opennex/' yearMonth='{}' resolution='{:.5f}' parition='{}' size='{}' rows='{}' cols='{}'>\n".format(yearMonth,resolution,seq,factor,currentRowSize,currentColSize))
            xf.write("<table>\n")
            for i in range(currentRowSize):
               xf.write("<tr>")
               for j in range(currentColSize):
                  v = d[rowStart+i,colStart+j]
                  if  v == 0.0:
                     xf.write("<td/>")
                  else:
                     xf.write("<td>{:5.2f}</td>".format(v))
               xf.write("</tr>\n")
            xf.write("</table>\n")
            xf.write("</data>\n")
            xf.close()
   
            
      t2 = time.time() - t1
      print " ... total elapsed time: {}s".format(t2)
      sys.stdout.flush()
      
      dset = d
   
def resizeDataOld(m,mset,chunkSize,partitions):
   resolution = chunkSize/120.0
   d = numpy.empty((int(round(dset.shape[1]/(chunkSize*1.0))),int(round(dset.shape[2]/(chunkSize*1.0)))),numpy.float32)
   
   t1 = time.time()
   for i in range(0,d.shape[0]):
      #c1 = time.time()
      for j in range(0,d.shape[1]):
         s = mset[i*chunkSize:i*chunkSize+chunkSize,j*chunkSize:j*chunkSize+chunkSize]
         reduction = reduce(lambda r,x: (r[0]+1,r[1]+x) if x<1.00000002e20 else r, s.flat,(0,0))
         d[i,j] = 0 if reduction[0] == 0 else reduction[1] / reduction[0]
      #print i," ",(time.time()-c1),"s"
         
   t2 = time.time() - t1
   print " ... # non-zero {} ({}s)".format(len(d.nonzero()[0]),t2)
   
   yearMonth = "{}-{:02d}".format(startYear+(m+1)/12,(m+1)%12)
   rowSize = int(round(d.shape[0]/(partitions*1.0)))
   colSize = int(round(d.shape[1]/(partitions*1.0)))
   for row in range(partitions):
      rowStart = row*rowSize
      currentRowSize = rowSize if (rowStart+rowSize) <= d.shape[0] else d.shape[0] - rowStart
      for col in range(partitions):
         seq = row*partitions + col + 1
         colStart = col*colSize
         currentColSize = colSize if (colStart+colSize) <= d.shape[1] else d.shape[1] - colStart
         filename = outputPrefix+yearMonth+"-"+str(chunkSize)+"-"+str(seq)+".xml"
         print " ... writing {} ...".format(filename)
         xf = open(filename,"w")
         xf.write("<data xmlns='http://milowski.com/opennex/' yearMonth='{}' resolution='{:.5f}' parition='{}' size='{}' rows='{}' cols='{}'>\n".format(yearMonth,resolution,seq,chunkSize,currentRowSize,currentColSize))
         xf.write("<table>\n")
         for i in range(currentRowSize):
            xf.write("<tr>")
            for j in range(currentColSize):
               v = d[rowStart+i,colStart+j]
               if  v == 0.0:
                  xf.write("<td/>")
               else:
                  xf.write("<td>{:5.2f}</td>".format(v))
            xf.write("</tr>\n")
         xf.write("</table>\n")
         xf.write("</data>\n")
         xf.close()

         
   t2 = time.time() - t1
   print " ... total elapsed time: {}s".format(t2)
   sys.stdout.flush()

for m in range(months):
   mset = tasmax[m,:,:]
   
   print "Month {} :".format(m+1)

   t1 = time.time()
   resizeData(m,mset,[5,3,2,2,2],[24,8,4,2,1]);
   t2 = time.time() - t1
   print "Completed in ({}s)".format(t2)
   #print "Computing 1° resolution ..."
   #resizeData(m,mset,120,1)
   #print "Computing 1/2° resolution ..."
   #resizeData(m,mset,60,2)
   #print "Computing 1/4° resolution ..."
   #resizeData(m,mset,30,4)
   #print "Computing 1/8° resolution ..."
   #resizeData(m,mset,15,8)
   #print "Computing 1/24° resolution ..."
   #resizeData(m,mset,5,24)
 
print "Finished."
