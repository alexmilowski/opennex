#!/bin/bash

s3cmd put bootstrap-python.sh s3://$1/
s3cmd put bootstrap-swap.sh s3://$1/
s3cmd put src/opennex_tasmax_resizer.py s3://$1/
s3cmd put src/s3copy.py s3://$1/
s3cmd put src/resize.py s3://$1/
