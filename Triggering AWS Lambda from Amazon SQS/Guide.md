# Triggering AWS Lambda from Amazon SQS

## Introduction

In this hands-on AWS lab, you will learn how to trigger a Lambda function using SQS. This Lambda function will process messages from the SQS queue and insert the message data as records into a DynamoDB table.

## Solution

Log in to the AWS Management Console using the credentials provided on the lab instructions page. Make sure you're using the us-east-1 (N. Virginia) region.

### Create the Lambda Function

1. Open Lambda services.
2. Click the Create function button.
3. On the Create function page, select Author from scratch.
4. Under Basic Information, set the following parameters for each field:
    1. Function name: Enter "SQSDynamoDB".
    2. Runtime: Select Python 3.8 from the dropdown menu.
    3. Execution role: Select Use an existing role.
    4. Existing role: Select lambda-execution-role from the dropdown menu,
5. Click the Create function button.



### Create the SQS Trigger

1. Click the + Add trigger button.
2. Under Trigger configuration, enter "sqs" in the search bar.
3. From the search results, select Simple Queue Service.
4. Under SQS queue, click the search bar and select Messages.
5. Click Add.



### Copy the Source Code into the Lambda Function

1. Under the + Add trigger button, click the Code tab.

2. On the left side, double-click on lambda_function.py.

    - ```python
        from datetime import datetime
        import json
        import os
        import boto3
        
        dynamodb = boto3.resource('dynamodb')
        
        def lambda_handler(event, context):
            # Count items in the Lambda event
            no_messages = str(len(event['Records']))
            print("Found " +no_messages +" messages to process.")
        
            for message in event['Records']:
        
                print(message)
        
                # Write message to DynamoDB
                table = dynamodb.Table('Message')
        
                response = table.put_item(
                    Item={
                        'MessageId': message['messageId'],
                        'Body': message['body'],
                        'Timestamp': datetime.now().isoformat()
                    }
                )
                print("Wrote message to DynamoDB:", json.dumps(response))
        ```

3. Delete the contents of the function.

4. In a new browser tab or window, open up this link to the source code for lambda_function.py.

5. Copy the code.

6. Return to the AWS console and paste the code into the lambda_function.py code box.

7. Click the Deploy button.



### Log In to the EC2 Instance and Test the Script

1. In the search bar on top of the console, enter "sqs".

2. From the search results, select Simple Queue Service.

3. Click `Messages`.

4. Click the Monitoring tab to monitor our SQS messages.

5. In the search bar on top, enter "ec2".

6. From the search results, select EC2 and open it in a new browser tab or window.

7. Under Resources, click Instances (running).

8. In the existing instance available, click the checkbox next to its name.

9. Click the Connect button at the top.

10. Click Connect at the bottom to open a shell and access the command line.

11. In the shell, become the cloud_user role:

    - ```
        su - cloud_user
        ```

12. View a list of files available to you:

    - ```
        ls
        ```

13. View the contents of the send_message.py file:

    - ```
        cat send_message.py
        ```

14. Start sending messages to our DynamoDB table from our Messages SQS queue with an interval of 0.1 seconds:

    - ```
        ./send_message.py -q Messages -i 0.1
        ```

15. After a few seconds, hit Control + C to stop the command from continuing to run.


```python
#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
import argparse
import logging
import sys
from time import sleep
import boto3
from faker import Faker


parser = argparse.ArgumentParser()
parser.add_argument("--queue-name", "-q", required=True,
                    help="SQS queue name")
parser.add_argument("--interval", "-i", required=True,
                    help="timer interval", type=float)
parser.add_argument("--message", "-m", help="message to send")
parser.add_argument("--log", "-l", default="INFO",
                    help="logging level")
args = parser.parse_args()

if args.log:
    logging.basicConfig(
        format='[%(levelname)s] %(message)s', level=args.log)

else:
    parser.print_help(sys.stderr)

sqs = boto3.client('sqs')

response = sqs.get_queue_url(QueueName=args.queue_name)

queue_url = response['QueueUrl']

logging.info(queue_url)

while True:
    message = args.message
    if not args.message:
        fake = Faker()
        message = fake.text()

    logging.info('Sending message: ' + message)

    response = sqs.send_message(
        QueueUrl=queue_url, MessageBody=message)

    logging.info('MessageId: ' + response['MessageId'])
    sleep(args.interval)
```

```
[INFO] https://queue.amazonaws.com/331079837625/Messages
[INFO] Sending message: My for film discuss heart interview area ever. Option half thank day million people.
Safe somebody exist role memory turn million none. Reach follow adult police eight evening.
[INFO] MessageId: d6b057c9-0e29-4256-b89b-07c25f023d9f
[INFO] Sending message: Hundred far economy return road every. Manager real pattern community cut provide. Have strategy charge after.
Above movie dream necessary produce. Subject project size crime. Collection stage exist.
[INFO] MessageId: 1a503e26-a2a4-4cbf-b1f8-37316d9b7da1
[INFO] Sending message: Material daughter professional our course court. Edge possible environment reality through everyone fact. Authority involve might 
out wonder piece. Series indeed exist order pass office.
[INFO] MessageId: 93a8da1b-44fd-4b86-ac5a-1f25a7a2414a
[INFO] Sending message: Member their suggest middle away southern without lead. Order sometimes business walk out material trial report. Member up without
 decade themselves station look.
[INFO] MessageId: d48df228-d52c-4609-ae8f-2b3b34f95226
[INFO] Sending message: Culture gas last speech three no network. Thank several fish information need your.
[INFO] MessageId: 6c453ce3-0b9a-4ab0-93d5-168f5b48379d
```

### Confirm Messages Were Inserted into the DynamoDB Table

1. Return to the browser tab or window with the AWS console.
2. In the search bar on top, enter "dynamodb".
3. From the search results, select DynamoDB.
4. In the left-hand navigation menu, select Tables.
5. Select the Message table.
6. In the top-right corner of the page, click Explore table items and review the list of items that were inserted from our script, sent to SQS, triggered Lambda, and inserted into the DynamoDB database.