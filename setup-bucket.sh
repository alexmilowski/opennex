#!/bin/bash

aws s3 mb s3://$1/
aws s3 cp bootstrap-python.sh s3://$1/
aws s3 cp bootstrap-swap.sh s3://$1/
aws s3 cp src/opennex_tasmax_resizer.py s3://$1/
aws s3 cp src/s3copy.py s3://$1/
aws s3 cp src/resize.py s3://$1/
aws s3 cp src/opennex_partition.py s3://$1/
aws s3 cp src/partition.py s3://$1/
