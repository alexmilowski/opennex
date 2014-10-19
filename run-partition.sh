#!/bin/bash
JOBFLOW=$1
AWS_KEY=$2
AWS_SECRET=$3
BUCKET=$4
INPUT=$5
TSTAMP=`date "+%Y-%m-%dT%H:%M:%S"`
OUTPUT="$6-$TSTAMP"
PREFIX=$7
NAME=$8
CLI=~/workspace/elastic-mapreduce-ruby/elastic-mapreduce
$CLI --jobflow $JOBFLOW --stream --mapper "partition.py $AWS_KEY $AWS_SECRET $BUCKET $PREFIX" --reducer NONE --input "s3://$BUCKET/$INPUT/" --output "s3://$BUCKET/$OUTPUT/" --jobconf mapred.reduce.tasks=0 --jobconf mapred.task.timeout=1200000 --arg "-files" --arg "s3://$BUCKET/partition.py,s3://$BUCKET/s3copy.py,s3://$BUCKET/opennex_partition.py" --args "-inputformat,org.apache.hadoop.mapred.lib.NLineInputFormat" --step-name "Partition: $NAME"
