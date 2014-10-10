#!/opt/local/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import h5py
import numpy
import json
import time

def resizeData(outDir,year,month,mset,chunkSizes,partitions):
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
      
      yearMonth = "{}-{:02d}".format(year,month)
      
      # guarantee path exists
      path = outDir+"/"+yearMonth
      if not os.path.exists(path):
         os.makedirs(path);
      path = path + "/" + str(factor)
      if not os.path.exists(path):
         os.makedirs(path);
         
      rowSize = int(round(d.shape[0]/(partitions[p]*1.0)))
      colSize = int(round(d.shape[1]/(partitions[p]*1.0)))
      for row in range(partitions[p]):
         rowStart = row*rowSize
         currentRowSize = rowSize if (rowStart+rowSize) <= d.shape[0] else d.shape[0] - rowStart
         for col in range(partitions[p]):
            seq = row*partitions[p] + col + 1
            colStart = col*colSize
            currentColSize = colSize if (colStart+colSize) <= d.shape[1] else d.shape[1] - colStart
            filename = path+"/partition-"+str(seq)+".xml"
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
   
def main():
   fileName = sys.argv[1]
   outDir = sys.argv[2]
   requested = [];
   for i in range(3,len(sys.argv)):
      requested.append(int(sys.argv[i])-1)
   
   f =  h5py.File(fileName,"r")
   tasmax = f["tasmax"]
   timeb = f["time_bnds"]
   
   months = tasmax.shape[0]
   rows = tasmax.shape[1]
   columns = tasmax.shape[2]
   
   if len(requested)==0:
      requested = range(months)

   startYear = int(1950+timeb[0,0]/365)
   
   print "{} months, lat x lon = {} x {}".format(months,rows,columns)
   
   for m in requested:

      year = startYear+(m+1)/12
      month = (m+1)%12      
      print "{}-{:02d} :".format(year,month)
   
      t1 = time.time()
      mset = tasmax[m,:,:]
      resizeData(outDir,year,month,mset,[5,3,2,2,2],[24,8,4,2,1]);
      t2 = time.time() - t1
      print "Completed in ({}s)".format(t2)
    
   print "Finished."

if __name__ == "__main__":
    main()
