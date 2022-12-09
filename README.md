jh-metagenomicsproject
===========
This repository contains code used for my metagenomics final project. The repository contains a few scripts that utilize a few technologies such as docker and AWS S3 and AWS SQS to parallelize the fragment recruitment algorithm tool called FR-HIT (Qin J, et al. Nature 2010, 464:59). The scripts and DOCKERFILE automatically run with the instructions provided to pull files from S3 via a queue to speed up the efficient processing of FR-HIT. By utilizing containers, you can process reads magnitudes quicker by launching more containers to assist with the processing.

Current version: 0.1

Install
--------

A few services are required to run the docker container. User must have access to read and modify rights to the following services:

		AWS S3 bucket (inputs)
		AWS S3 bucket (outputs)
		AWS SQS queue URL

Docker must be installed. To build the container, REF_GENOME (URL for reference genome to recruit to) must be provided for the container to download:

        git clone https://github.com/dchen75-jh/jh-metagenomicsproject
        cd jh-metagenomicsproject
        docker build --build-arg REF_GENOME=https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/017/821/535/GCF_017821535.1_ASM1782153v1/GCF_017821535.1_ASM1782153v1_genomic.fna.gz -t fr-hit .

To run the container, a few parameters must be passed to the container:

		SQS_URL - AWS SQS URL
		AWS_DEFAULT_REGION - default region for AWS services
		AWS_ACCESS_KEY_ID - AWS access key for commandline access
		AWS_SECRET_ACCESS_KEY - AWS secret access key for commandline access
		S3_BUCKET - S3 bucket name for input files (must have access)
		S3_OUTPUT - S3 bucket name for output files (must have access)
		REF_GENOME - reference genome URL
		PARAM_C - value for -c for fr-hit (refer to https://github.com/Beifang/fr-hit)
		PARAM_M - value for -m for fr-hit (refer to https://github.com/Beifang/fr-hit)
		PARAM_T - value for -t for fr-hit (refer to https://github.com/Beifang/fr-hit)
		
Once the necessary values have beeen obtained, to run the container:

		docker run -e SQS_URL='https://sqs.us-east-1.amazonaws.com/700804413907/fr-hit' -e AWS_DEFAULT_REGION='us-east-1' -e AWS_ACCESS_KEY_ID='###' -e AWS_SECRET_ACCESS_KEY='###' -e S3_BUCKET='jh-metagenomics' -e 'S3_OUTPUT=jh-metagenomics-out' -e REF_GENOME='https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/017/821/535/GCF_017821535.1_ASM1782153v1/GCF_017821535.1_ASM1782153v1_genomic.fna.gz' -e PARAM_C='80' -e PARAM_M='30' -e PARAM_T='1' -d -t fr-hit

This will start the container and begin processing items from the queue. 

A script is included to add items to the queue. This script will identify all of the read files in the S3 bucket and add them to the queue for processing:
		
		python3 add-to-queue.py jh-metagenomics https://sqs.us-east-1.amazonaws.com/700804413907/fr-hit

Recruited reads will be uploaded into the S3_OUTPUT bucket