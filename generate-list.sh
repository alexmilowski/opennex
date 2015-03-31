#!/bin/bash

# e.g. s3://nasanex/NEX-DCP30/NEX-quartile/rcp85/mon/atmos/tasmax/r1i1p1/v1.0/CONUS/

BUCKET=$1

aws s3 ls $BUCKET | grep .*nc$ | awk "{ printf \"$BUCKET%s\n\",\$4 }"
