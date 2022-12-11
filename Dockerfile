FROM ubuntu:18.04
ARG REF_GENOME

##################
## FR-HIT ##
##################

MAINTAINER Daniel Chen <dchen75@jh.edu>
LABEL Description="This image is used to run fragment recruitment software called FR-HIT with supplemental code for implementation of a queue." Version="1.0.0"

RUN apt-get -y update && apt-get install -y python3 python3-pip git libpcap-dev unzip curl wget gzip

RUN git init
RUN git remote add origin https://github.com/Beifang/fr-hit.git
RUN git pull origin master
RUN make
RUN mv fr-hit /usr/local/bin
#RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
#RUN unzip awscliv2.zip
#RUN ./aws/install
RUN git clone https://github.com/dchen75-jh/jh-metagenomicsproject
RUN wget $REF_GENOME
RUN for f in *.gz ; do gzip -d "$f" > ./"{f$.*}" ; done
RUN pip3 install boto3
ENTRYPOINT ["python3", "./jh-metagenomicsproject/process-queue.py"]
