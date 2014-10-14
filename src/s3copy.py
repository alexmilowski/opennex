import os,sys,gzip,tempfile
from boto.s3.key import Key

def addFile(fileName,key):
   tempFile = tempfile.NamedTemporaryFile(suffix=".gz", delete=False)
   #print "Compressing to ",tempFile.name
   input = open(fileName, "rb")
   output = gzip.open(tempFile.name,"wb")
   output.writelines(input)
   input.close()
   output.close()
   key.set_metadata("Content-Type", "text/xml" if fileName.endswith(".xml") else "application/octet-stream")
   key.set_metadata("Content-Encoding", "gzip")
   key.set_contents_from_filename(tempFile.name)
   os.unlink(tempFile.name)

def copyToBucket(srcDir,bucket,prefix):
   for root,folders,files in os.walk(srcDir):
      for file in files:
          apath = os.path.join(root,file)
          rpath = os.path.relpath(apath,srcDir)
          k = Key(bucket)
          k.key = prefix+"/"+rpath if len(prefix)>0 else rpath
          #print apath," to ",k.key
          addFile(apath,k)