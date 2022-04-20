import json
import boto3
import cfnresponse
import threading

def copyIndex(sourceBucket, destBucket, apiGatewayUrl):
    s3 = boto3.client('s3')

    index = s3.get_object(Bucket=sourceBucket, Key='collectors/index.template')['Body'].read().decode('utf-8')
    index = index.replace('APGATEWAY', apiGatewayUrl).encode('utf-8')
    s3.put_object(
        Body = index,
        Bucket = destBucket,
        Key = 'index.html',
        ContentType = 'text/html'
    )

def deleteIndex(bucket):
    s3 = boto3.client('s3')
    s3.delete_objects(Bucket=bucket, Delete={'Objects': [{'Key': 'index.html'}]})

def timeout(event, context):
    print('Timing out, sending failure response to CFN')
    cfnresponse.send(event, context, cfnresponse.FAILED, {}, None)

def handler(event, context):
    print(f'Received event: {json.dumps(event)}')
    timer = threading.Timer((context.get_remaining_time_in_millis() / 1000.00) - 0.5, timeout, args=[event, context])
    timer.start()

    status = cfnresponse.SUCCESS
    try:
        sourceBucket = event['ResourceProperties']['SourceBucket']
        destBucket = event['ResourceProperties']['DestBucket']
        apiGatewayUrl = event['ResourceProperties']['APIGatewayURL']
        if event['RequestType'] == 'Delete':
            deleteIndex(destBucket)
        else:
            copyIndex(sourceBucket, destBucket, apiGatewayUrl)
    except Exception as e:
        print(e)
        status = cfnresponse.FAILED
    finally:
        timer.cancel()
        cfnresponse.send(event, context, status, {}, None)
