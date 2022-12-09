import boto3
import os
import time

if __name__ == "__main__":
    #create s3 and sqs clients
    sqs = boto3.client('sqs')
    s3 = boto3.client('s3')

    #keep track of what is going on for debugging
    logfile = open("log.txt","w")

    #keep running loop and checking for new items on queue
    while True:
        logfile.write("checking for messages...\n")

        #check for items on queue
        response = sqs.receive_message(
                QueueUrl=os.environ["SQS_URL"],
                MaxNumberOfMessages = 1,
                VisibilityTimeout=120,
                WaitTimeSeconds=3
        )

        #if message, process the s3 object
        if "Messages" in response.keys():
            logfile.write("found a file\n")
            s3obj = response["Messages"][0]["Body"]

            #download file locally
            s3.download_file(os.environ["S3_BUCKET"], s3obj, s3obj.split("/")[-1])

            #create command to run fr-hit
            command = "fr-hit -d " + os.environ["REF_GENOME"].split("/")[-1][:-3] + " -a " + s3obj.split("/")[-1] + " -o " + s3obj.split("/")[-1] + ".out -c " + os.environ["PARAM_C"] + " -m " + os.environ["PARAM_M"] + " -T " + os.environ["PARAM_T"]
        
            try:
                logfile.write("Running command: " + command + "\n")
                #execute command
                os.system(command)

                logfile.write("uploading file to s3\n")
                #upload output file to s3
                with open(s3obj.split("/")[-1] + ".out", "rb") as f:
                    s3.upload_fileobj(f, os.environ["S3_OUTPUT"], s3obj + ".out")
                logfile.write("deleting message\n")
                #if successful, delete message from queue
                sqs.delete_message(
                    QueueUrl=os.environ["SQS_URL"],
                    ReceiptHandle=response["Messages"][0]["ReceiptHandle"]
                )
            except Exception as e:
                print(str(e))
                logfile.write("Ran into an issue. Keeping item on queuee: " + str(e) + "\n")
        else:
            #sleep to keep loop running
            time.sleep(5)
    
