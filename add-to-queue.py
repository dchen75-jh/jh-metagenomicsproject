import boto3
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            #create s3 and sqs clients
            s3 = boto3.client('s3')

            sqs = boto3.client('sqs')

            #get all objects from s3 bucket
            for obj in s3.list_objects(Bucket=sys.argv[1])["Contents"]:
                
                #add the s3 object URL to the queue
                response = sqs.send_message(
                        QueueUrl=sys.argv[2],
                        DelaySeconds=0,
                        MessageBody=(str(obj["Key"]))
                        )
        except Exception as e:
            print("Ran into an error adding items to queue: " + str(e))


