opennex
=======

Bootstrap actions:


1/5 m1.medium = 8 parallel
1/5 m1.large = 28 parallel

## Setup your bucket

You'll need to store the code and bootstrapping into S3.  Create a bucket (e.g., mybucket) and then run:

    setup-bucket.sh mybucket


## Making EMR Inputs

Generate a list of files

    generate-list.sh s3://nasanex/NEX-DCP30/NEX-quartile/rcp85/mon/atmos/tasmax/r1i1p1/v1.0/CONUS/ > files.txt

Find a subset of files to process (e.g. quartile75) and run the list through the generate-input.py program.  This will group months into pairs so that each map task does not take too long.  The program takes a prefix (e.g., 'quartile75') as an argument that it will use for the files generated.

    grep quartile75 files.txt | python generate-input.py quartile75

Store the files into S3 group into pairs using your bucket name (e.g., 'mybucket') and a prefix (e.g., 'quartile75').  This will create a set of groups of files to process that can be associated with each EMR (Hadoop) step.

    make-input-bucket.sh mybucket quartile75-input quartile75-*.txt

## Partitioning the Data using EMR

You'll need to start an EMR cluster.  I find that 1 master and 5 Core nodes of size m1.large seems to work reasonable well without costing too much.With this configuration, you'll get 28 parallel tasks and each step (120 months) takes about 1.5 hours.

There are two bootstrap actions needed:

   * bootstrap-python.sh - configures python to process HDF5
   * bootstrap-swap.sh - adds a bit of swap space to make sure we don't run out of memory

Each of these scripts were stored into your bucket when you set it up.  You'll just need to tell EMR to use them as bootstrap actions (e.g., s3://mybucket/bootstrap-python.sh and s3://mybucket/bootstrap-swap.sh).

Because HDF5 libraries need to be built, bootstrapping takes longer than normal.  Be patient!

You can also configure Hadoop to fail after one attempt just in case something goes wrong:

    Configure Hadoop	s3://elasticmapreduce/bootstrap-actions/configure-hadoop	-m, mapred.map.max.attempts=1

## Run a Partition Job

There is a script for running the jobs and you'll need:

   * the Job Flow ID of your cluster
   * Your AWS key and secret
   * the S3 bucket (e.g., mybucket)
   * your input stored into S3 (e.g., quartile75-input-1)
   * a name for your output (e.g., quartile75-output)
   * a name partitioned data (e.g., quartile75)
   * a step name (e.g., "#1")

The script is invoked as:

    run-partition.sh <job-flow-id> <aws-key> <aws-secret> mybucket quartile75-input-1 quartile75-output quartile75 "#1"

Note: the brackets are not necessary and just represent the arguments you must supply but I've omitted here.

## Web Server AMI ##

An AMI is available so you can run the Web server application directly:

[https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-fcc04494](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#LaunchInstanceWizard:ami=ami-fcc04494)

This web application is available at:

[http://data.pantabular.org/opennex/](http://data.pantabular.org/opennex/)
   



