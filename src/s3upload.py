import sys
import s3copy
from boto.s3.connection import S3Connection

conn = S3Connection(sys.argv[1], sys.argv[2])
bucket = conn.get_bucket(sys.argv[3])
prefix = sys.argv[4]
for i in range(5,len(sys.argv)):
   s3copy.copyToBucket(sys.argv[i],bucket,prefix)

