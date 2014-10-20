#!/bin/bash

BUCKET=$1
PREFIX=$2
shift
shift

COUNT=`expr $# - 1`

for i in `seq 0 $COUNT`
do
   index=`expr $i / 2 + 1`
   s3cmd put $1 s3://$BUCKET/$PREFIX-$index/$1
   shift
done
