import sys
import math

def sequenceNumber(lat,lon,latSize,lonSize):
   nlat = 90-lat;
   nlon = lon if lon>=0 else 360+lon
   rows = int(math.floor(nlat/latSize))
   cols = int(math.floor(nlon/lonSize))
   #print rows,cols
   seq = rows*int(math.floor(360/lonSize)) + cols + 1
   return seq

region = [50.0,-124.0,24.0,-66.0]
gridSize = 1/120.0

# original data region but we shift it from center to the edge of 1/120 degree cells
# dataRegion = [49.9375,-125.02083333,24.0625,-66.47916667]
# Note: sequence numbers calculated in 1/120ths
dataRegion = [(49*120+113)*gridSize, (-(125*120 + 3))*gridSize]
dataRegion = dataRegion + [dataRegion[0] - 3105*gridSize,dataRegion[1] + 7025*gridSize]

resolution = int(sys.argv[1])/120.0
dataRegionSeq = [ 
   sequenceNumber(dataRegion[0]         ,dataRegion[1]         ,resolution,resolution),
   sequenceNumber(dataRegion[0]         ,dataRegion[3]-gridSize,resolution,resolution),
   sequenceNumber(dataRegion[2]+gridSize,dataRegion[1]         ,resolution,resolution),
   sequenceNumber(dataRegion[2]+gridSize,dataRegion[3]-gridSize,resolution,resolution)
]
regionSeq = [ 
   sequenceNumber(region[0]         ,region[1]         ,resolution,resolution),
   sequenceNumber(region[0]         ,region[3]-gridSize,resolution,resolution),
   sequenceNumber(region[2]+gridSize,region[1]         ,resolution,resolution),
   sequenceNumber(region[2]+gridSize,region[3]-gridSize,resolution,resolution)
]

print region
print regionSeq
print dataRegion
print dataRegionSeq