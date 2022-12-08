import boto3
import sys
import os

if __name__ == "__main__":
    if "S3_URL" in os.environ:
        try:
            s3 = boto3.client('s3')

            sqs = boto3.client('sqs')

            for obj in s3.list_objects(Bucket=os.environ["S3_URL"])["Contents"]:
                print(obj["Key"])
                response = sqs.send_message(
                        QueueUrl=os.environ["SQS_URL"],
                        DelaySeconds=0,
                        MessageBody=(str(obj["Key"]))
                        )
                print(response["MessageId"])
        except Exception as e:
            print("Ran into an error processing file: " + str(e))


