#!/opt/local/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import h5py
import numpy
import time
import math

def sequenceNumber(lat,lon,latSize,lonSize):
   nlat = 90-lat;
   nlon = lon if lon>=0 else 360+lon
   rows = int(math.floor(nlat/latSize))
   cols = int(math.floor(nlon/lonSize))
   #print rows,cols
   seq = rows*int(math.floor(360/lonSize)) + cols + 1
   return seq

region = [50.0,-126.0,24.0,-66.0]
gridSize = 1/120.0
# original data region but we shift it from center to the edge of 1/120 degree cells
# dataRegion = [49.9375,-125.02083333,24.0625,-66.47916667]
# Note: sequence numbers calculated in 1/120ths
dataRegion = [(49*120+113)*gridSize, (-(125*120 + 3))*gridSize]
dataRegion = dataRegion + [dataRegion[0] - 3105*gridSize,dataRegion[1] + 7025*gridSize]

dataRegionSeq = [ 
   sequenceNumber(dataRegion[0]         ,dataRegion[1]         ,gridSize,gridSize),
   sequenceNumber(dataRegion[0]         ,dataRegion[3]-gridSize,gridSize,gridSize),
   sequenceNumber(dataRegion[2]+gridSize,dataRegion[1]         ,gridSize,gridSize),
   sequenceNumber(dataRegion[2]+gridSize,dataRegion[3]-gridSize,gridSize,gridSize)
]
seqRow = int(360/gridSize)

rowAdjust = dataRegionSeq[0] / seqRow


def partition(outDir,year,month,mset,partitionSize):

   resolution = partitionSize/120.0
   
   latDim = int(math.fabs(math.ceil(region[0] - region[2])))
   lonDim = int(math.fabs(math.ceil(region[1] - region[3])))
   latCount = int(math.ceil(latDim / resolution))
   lonCount = int(math.ceil(lonDim / resolution))
   
   sys.stderr.write("Partitioning by {0} into {1} x {2} to resolution {3} ...\n".format(partitionSize,latCount,lonCount,resolution))
   
   d = numpy.empty((latCount,lonCount),numpy.float64)
   partition = numpy.empty((partitionSize,partitionSize),numpy.float64)
   
   yearMonth = "{0}-{1:02d}".format(year,month)
   # guarantee path exists
   path = outDir+"/"+yearMonth
   if not os.path.exists(path):
      os.makedirs(path)
   path = path + "/" + str(partitionSize)
   if not os.path.exists(path):
      os.makedirs(path)
      
   for i in range(0,d.shape[0]):
      sys.stderr.write("  {0}".format(i));
      for j in range(0,d.shape[1]):

         lat = region[0] - resolution*i
         lon = region[1] + resolution*j
         seq = sequenceNumber(lat,lon,resolution,resolution)
         pseq = sequenceNumber(lat,lon,gridSize,gridSize)
         
         #print lat,lon,seq,pseq
         
         for row in range(0,partition.shape[0]):
            for col in range(0,partition.shape[1]):
               #plat = region[0] - resolution*row
               #plon = region[1] + resolution*col
               #seq = sequenceNumber(plat,plon,gridSize,gridSize)
               cellSeq = pseq + row*seqRow + col

               # note: we use interger division so the fractions are dropped
               adjSeq = cellSeq - (cellSeq / seqRow - rowAdjust)*seqRow
               lonx = adjSeq - dataRegionSeq[0]
               laty = cellSeq / seqRow - rowAdjust
               #print cellSeq,laty,lonx,mset[laty,lonx]
               #print cellSeq,laty,lonx
               # either the sequence number is outside of the possible range or it is inside the range but not within the region's column subset
               #print cellSeq,dataRegionSeq,adjSeq
               try:
                  partition[row][col] = mset[laty,lonx] if cellSeq >= dataRegionSeq[0] and cellSeq <= dataRegionSeq[3] and adjSeq >= dataRegionSeq[0] and adjSeq <= dataRegionSeq[1] else 0.0
                  if partition[row][col]>=1.00000002e20:
                     partition[row][col] = 0
               except:
                  print i,j,row,col,laty,lonx
                  print d.shape
                  print partition.shape
                  print cellSeq,adjSeq,seqRow,rowAdjust,dataRegionSeq
                  exit(1)
               
         #reduction = reduce(lambda r,x: (r[0]+1,r[1]+x) if x<1.00000002e20 and x>0 else r, partition.flat,(0,0))
         #print "",reduction,0 if reduction[0] == 0 else reduction[1] / reduction[0]
         
         filename = path+"/"+str(seq)+".xml"
         #sys.stderr.write(" ... writing {0} ...\n".format(filename))
         xf = open(filename,"w")
         xf.write("<data xmlns='http://milowski.com/opennex/' yearMonth='{0}' resolution='{1:.5f}' sequence='{2}' size='{3}' rows='{4}' cols='{5}'>\n".format(yearMonth,resolution,seq,partitionSize,partition.shape[0],partition.shape[1]))
         xf.write("<table>\n")
         for row in reversed(range(0,partition.shape[0])):
            xf.write("<tr>")
            for col in range(0,partition.shape[1]):
               if  partition[row,col] == 0.0:
                  xf.write("<td/>")
               else:
                  xf.write("<td>{0:5.2f}</td>".format(partition[row,col]))
            xf.write("</tr>\n")
         xf.write("</table>\n")
         xf.write("</data>\n")
         xf.close()
         
   sys.stderr.write("\n")
   

#TODO: partition and summarize run the same algorithm and it should be refactored
def summarize(mset,partitionSize):

   resolution = partitionSize/120.0
   
   latDim = int(math.fabs(math.ceil(region[0] - region[2])))
   lonDim = int(math.fabs(math.ceil(region[1] - region[3])))
   latCount = int(math.ceil(latDim / resolution))
   lonCount = int(math.ceil(lonDim / resolution))
   
   sys.stderr.write("Summarizing by {0} for {1} x {2} ...\n".format(partitionSize,latCount,lonCount,resolution))
   
   d = numpy.empty((latCount,lonCount),numpy.float64)
   partition = numpy.empty((partitionSize,partitionSize),numpy.float64)
   
   for i in range(0,d.shape[0]):
      sys.stderr.write("  {0}".format(i));
      for j in range(0,d.shape[1]):

         lat = region[0] - resolution*i
         lon = region[1] + resolution*j
         seq = sequenceNumber(lat,lon,resolution,resolution)
         pseq = sequenceNumber(lat,lon,gridSize,gridSize)
         
         #print lat,lon,seq,pseq
         
         for row in range(0,partition.shape[0]):
            for col in range(0,partition.shape[1]):
               cellSeq = pseq + row*seqRow + col

               # note: we use interger division so the fractions are dropped
               adjSeq = cellSeq - (cellSeq / seqRow - rowAdjust)*seqRow
               lonx = adjSeq - dataRegionSeq[0]
               laty = cellSeq / seqRow - rowAdjust
               try:
                  partition[row][col] = mset[laty,lonx] if cellSeq >= dataRegionSeq[0] and cellSeq <= dataRegionSeq[3] and adjSeq >= dataRegionSeq[0] and adjSeq <= dataRegionSeq[1] else 0.0
                  if partition[row][col]>=1.00000002e20:
                     partition[row][col] = 0
               except:
                  print i,j,row,col,laty,lonx
                  print d.shape
                  print partition.shape
                  print cellSeq,adjSeq,seqRow,rowAdjust,dataRegionSeq
                  exit(1)
               
         reduction = reduce(lambda r,x: (r[0]+1,r[1]+x) if x<1.00000002e20 and x>0 else r, partition.flat,(0,0))
         d[i,j] = 0 if reduction[0] == 0 else reduction[1] / reduction[0]
   sys.stderr.write("\n")
   return d
   
def writeSummary(outDir,year,month,partitionSize,summary):
   resolution = partitionSize/120.0
   yearMonth = "{0}-{1:02d}".format(year,month)
   # guarantee path exists
   path = outDir+"/"+yearMonth
   if not os.path.exists(path):
      os.makedirs(path)
      
   filename = path+"/" + str(partitionSize)+".xml"
   sys.stderr.write(" ... writing {0} ...\n".format(filename))
   xf = open(filename,"w")
   xf.write("<data xmlns='http://milowski.com/opennex/' yearMonth='{0}' resolution='{1:.5f}' size='{2}' rows='{3}' cols='{4}'>\n".format(yearMonth,resolution,partitionSize,summary.shape[0],summary.shape[1]))
   xf.write("<table>\n")
   for row in reversed(range(0,summary.shape[0])):
      xf.write("<tr>")
      for col in range(0,summary.shape[1]):
         if  summary[row,col] == 0.0:
            xf.write("<td/>")
         else:
            xf.write("<td>{0:5.2f}</td>".format(summary[row,col]))
      xf.write("</tr>\n")
   xf.write("</table>\n")
   xf.write("</data>\n")
   xf.close()
   
def reviseSummary(dset,partitionSize):
   sizeLat = int(round(dset.shape[0]/(partitionSize*1.0)))
   sizeLon = int(round(dset.shape[1]/(partitionSize*1.0)))
   d = numpy.empty((sizeLat,sizeLon),numpy.float64)
   for i in range(0,d.shape[0]):
      for j in range(0,d.shape[1]):
         s = dset[i*partitionSize:i*partitionSize+partitionSize,j*partitionSize:j*partitionSize+partitionSize]
         reduction = reduce(lambda r,x: (r[0]+1,r[1]+x) if x>0 else r, s.flat,(0,0))
         d[i,j] = 0 if reduction[0] == 0 else reduction[1] / reduction[0]
   return d

   
def main():
   fileName = sys.argv[1]
   outDir = sys.argv[2]
   size = int(sys.argv[3])
   summaries = map(lambda x: int(x),sys.argv[4].split(","))
   requested = []
   for i in range(5,len(sys.argv)):
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
   
   sys.stderr.write("{0} months, lat x lon = {1} x {2}\n".format(months,rows,columns))
   
   startTime = time.time()
   
   for m in requested:

      year = startYear+m/12
      month = m % 12 + 1    
      sys.stderr.write("{0}-{1:02d} :\n".format(year,month))
   
      t1 = time.time()
      mset = tasmax[m,:,:]
      partition(outDir,year,month,mset,size)
      t2 = time.time() - t1
      sys.stderr.write("Completed in {0}s\n".format(t2))
      
      t1 = time.time()
      summary = summarize(mset,summaries[0])
      writeSummary(outDir,year,month,summaries[0],summary)
      t2 = time.time() - t1
      sys.stderr.write("Completed in {0}s\n".format(t2))
      
      for i in range(1,len(summaries)):
         summary = reviseSummary(summary,summaries[i]/summaries[i-1])      
         writeSummary(outDir,year,month,summaries[i],summary)
      
   endTime = time.time() - startTime
   sys.stderr.write("Finished in {0}s\n".format(endTime))

if __name__ == "__main__":
    main()
