#!/bin/bash

# e.g. s3://nasanex/NEX-DCP30/NEX-quartile/rcp85/mon/atmos/tasmax/r1i1p1/v1.0/CONUS/

s3cmd ls $1 | grep .*nc$ | awk "{ print \$4 }"
